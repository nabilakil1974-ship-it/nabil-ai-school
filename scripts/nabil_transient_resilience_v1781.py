from __future__ import annotations
import hashlib,json,os,re,time
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone
from pathlib import Path
from typing import Any,Callable,Iterable,Sequence

EXIT_PAUSED_TRANSIENT=75
EXIT_PROVIDER_UNAVAILABLE=78
EXIT_NEEDS_ATTENTION=79
CHECKPOINT_SCHEMA="nabil-v1781-paid-unit-v2"
STATE_SCHEMA="nabil-v1781-state-v2"
STATUS_PAUSED_TRANSIENT="PAUSED_TRANSIENT"
STATUS_PROVIDER_UNAVAILABLE="PAUSED_PROVIDER_UNAVAILABLE"
STATUS_NEEDS_ATTENTION="NEEDS_ATTENTION"
STATUS_BLOCKED="BLOCKED"

@dataclass(frozen=True)
class ProviderErrorInfo:
    kind:str
    status_code:int|None
    retry_after_seconds:int|None
    message:str

class ProviderTransientError(RuntimeError):
    def __init__(self,message,*,retry_after_seconds=None,status_code=None):
        super().__init__(message);self.retry_after_seconds=retry_after_seconds;self.status_code=status_code
class ProviderDailyQuotaError(ProviderTransientError): pass
class ProviderUnavailableError(RuntimeError): pass
class NeedsAttentionError(RuntimeError): pass
class CheckpointWriteError(RuntimeError): pass
class ScientificGateBlocked(RuntimeError): pass

def _txt(v):
    try:return str(v or "")
    except Exception:return repr(v)

def _code(v):
    for a in ("status_code","code"):
        try:
            x=getattr(v,a,None);x=x() if callable(x) else x
            if x is not None:
                m=re.search(r"\b([1-5]\d\d)\b",str(x))
                if m:return int(m.group(1))
        except Exception:pass
    m=re.search(r"(?:HTTP\s*|status(?:_code)?\s*[=:]?\s*|\b)(400|401|402|403|404|408|409|425|429|500|502|503|504)\b",_txt(v),re.I)
    return int(m.group(1)) if m else None

def _duration(text):
    low=str(text or "").casefold()
    cands=re.findall(r"\b(?:\d+\s*h)?(?:\d+\s*m)?(?:\d+(?:\.\d+)?\s*s)\b",low)
    for raw in cands:
        hm=re.search(r"(\d+)\s*h",raw);mm=re.search(r"(\d+)\s*m",raw);sm=re.search(r"(\d+(?:\.\d+)?)\s*s",raw)
        n=(int(hm.group(1))*3600 if hm else 0)+(int(mm.group(1))*60 if mm else 0)+(int(float(sm.group(1))) if sm else 0)
        if n:return n
    return None

def _retry(v):
    for owner in (v,getattr(v,"response",None)):
        try:
            h=getattr(owner,"headers",None);raw=h.get("Retry-After") if h else None
            if raw:return max(1,int(float(raw)))
        except Exception:pass
    text=_txt(v)
    m=re.search(r"retry(?:ing)?\s+(?:in|after)\s+([0-9]+(?:\.[0-9]+)?)\s*s",text,re.I)
    if m:
        return max(1,int(float(m.group(1))))
    m=re.search(r"\bwait_seconds\s*[=:]\s*([0-9]+(?:\.[0-9]+)?)",text,re.I)
    if m:
        return max(1,int(float(m.group(1))))
    return _duration(text)

def classify_provider_error(v):
    t=_txt(v);low=t.casefold();c=_code(v);r=_retry(v)
    if any(x in low for x in ("per day","daily quota","requests per day","quota per day","daily limit","day quota","reset tomorrow","per_day")):
        return ProviderErrorInfo("daily_quota",c,r,t)
    if c==401 or any(x in low for x in ("invalid api key","api key not valid","unauthenticated","authentication failed","missing api key")):
        return ProviderErrorInfo("auth_billing",c,r,t)
    if c==402 and any(x in low for x in ("payment required","insufficient credits","credit balance","billing","credits exhausted")):
        return ProviderErrorInfo("auth_billing",c,r,t)
    if c==400 or any(x in low for x in ("content policy","safety policy","blocked by safety","content refusal","invalid argument","bad request","invalid schema","schema validation","malformed prompt")):
        return ProviderErrorInfo("needs_attention",c,r,t)
    if c in {408,409,425,429,500,502,503,504} or any(x in low for x in ("timeout","timed out","deadline exceeded","temporarily unavailable","high demand","overloaded","rate limit","too many requests","service unavailable","all_providers_cooling_down","all providers cooling down","cooling_down","cooling down")):
        return ProviderErrorInfo("transient",c,r,t)
    if c in {402,403,404}:return ProviderErrorInfo("needs_attention",c,r,t)
    return ProviderErrorInfo("unknown",c,r,t)

def stable_sha256(v):
    raw=v if isinstance(v,bytes) else (v.encode() if isinstance(v,str) else json.dumps(v,sort_keys=True,separators=(",",":")).encode())
    return hashlib.sha256(raw).hexdigest()

def _safe(v):return re.sub(r"[^A-Za-z0-9._-]+","-",str(v or "").strip()).strip("-") or "unit"
def checkpoint_path(root,lesson_id,operation,unit_id):return Path(root)/_safe(lesson_id)/_safe(operation)/(f"{_safe(unit_id)}.json")
def checkpoint_key(source_hash,prompt_version,operation,unit_id):return stable_sha256({"source_hash":source_hash,"prompt_version":prompt_version,"operation":operation,"unit_id":unit_id})

def atomic_json_write_verified(path,payload):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+".tmp")
    try:
        tmp.write_text(json.dumps(payload,sort_keys=True,indent=2)+"\n",encoding="utf-8");os.replace(tmp,path)
        reread=json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:raise CheckpointWriteError(f"CHECKPOINT_WRITE_OR_READBACK_FAILED:{e}") from e
    if stable_sha256(reread)!=stable_sha256(payload):raise CheckpointWriteError("CHECKPOINT_READBACK_MISMATCH")
    return reread

def save_verified_unit(root,*,lesson_id,unit_id,operation,source_hash,prompt_version,provider,model,artifact_ref="",artifact_hash="",extra=None):
    p={"schema_version":CHECKPOINT_SCHEMA,"lesson_id":lesson_id,"unit_id":unit_id,"operation":operation,"source_hash":source_hash,"prompt_version":prompt_version,"provider":provider,"model":model,"artifact_ref":artifact_ref,"artifact_hash":artifact_hash,"verification":"PASS","checkpoint_key":checkpoint_key(source_hash,prompt_version,operation,unit_id)}
    if extra:p["extra"]=extra
    return atomic_json_write_verified(checkpoint_path(root,lesson_id,operation,unit_id),p)

def load_verified_unit(root,*,lesson_id,unit_id,operation,source_hash,prompt_version):
    try:d=json.loads(checkpoint_path(root,lesson_id,operation,unit_id).read_text())
    except Exception:return None
    expected=checkpoint_key(source_hash,prompt_version,operation,unit_id)
    return d if d.get("schema_version")==CHECKPOINT_SCHEMA and d.get("checkpoint_key")==expected and d.get("verification")=="PASS" and d.get("source_hash")==source_hash and d.get("prompt_version")==prompt_version else None

def _state_path(root,lid):return Path(root)/_safe(lid)/"STATE.json"
def load_state(root,lid):
    try:return json.loads(_state_path(root,lid).read_text())
    except Exception:return {}

def save_state(root,*,lesson_id,status,reason="",unit_id="",retry_seconds=None,max_pause_cycles=12):
    old=load_state(root,lesson_id);cycles=int(old.get("pause_resume_cycles") or 0)
    if status in {STATUS_PAUSED_TRANSIENT,STATUS_PROVIDER_UNAVAILABLE}:
        cycles+=1
        if cycles>max_pause_cycles:status=STATUS_NEEDS_ATTENTION;reason=f"PAUSE_RESUME_CYCLE_CAP_EXCEEDED:{cycles}:{reason}";retry_seconds=None
    now=datetime.now(timezone.utc)
    p={"schema_version":STATE_SCHEMA,"lesson_id":lesson_id,"status":status,"reason":reason,"unit_id":unit_id,"pause_resume_cycles":cycles,"blocked":status==STATUS_BLOCKED,"updated_at":now.replace(microsecond=0).isoformat(),"retry_after_seconds":int(retry_seconds) if retry_seconds else None,"next_retry_at":(now+timedelta(seconds=retry_seconds)).replace(microsecond=0).isoformat() if retry_seconds else None}
    return atomic_json_write_verified(_state_path(root,lesson_id),p)

@dataclass
class ProviderSpec:
    name:str
    model:str
    call:Callable[[Any],Any]

def call_with_authorised_failover(unit,*,providers:Sequence[ProviderSpec],authorised_providers:set[str],attempts_per_provider=3,sleep:Callable[[float],None]=time.sleep):
    eligible=[p for p in providers if p.name in authorised_providers]
    if not eligible:raise ProviderUnavailableError("NO_AUTHORISED_PROVIDER_FOR_UNIT")
    quotas=[];auth=[];att=[];trans=[]
    for p in eligible:
        for attempt in range(1,attempts_per_provider+1):
            try:return p.call(unit),p.name,p.model
            except Exception as e:
                i=classify_provider_error(e)
                if i.kind=="daily_quota":quotas.append(i.retry_after_seconds or 21600);break
                if i.kind=="auth_billing":auth.append(p.name);break
                if i.kind in {"needs_attention","unknown"}:att.append(f"{p.name}:{i.message}");break
                if attempt>=attempts_per_provider:trans.append(p.name);break
                sleep(min(i.retry_after_seconds or (5*(2**(attempt-1))),120))
    if att:raise NeedsAttentionError(";".join(att))
    if auth and len(auth)==len(eligible):raise ProviderUnavailableError("ALL_AUTHORISED_PROVIDERS_QUARANTINED")
    if quotas:raise ProviderDailyQuotaError("ALL_USABLE_PROVIDERS_DAILY_QUOTA",retry_after_seconds=min(quotas),status_code=429)
    if trans:raise ProviderTransientError("ALL_USABLE_PROVIDERS_TRANSIENTLY_DOWN",retry_after_seconds=60,status_code=503)
    raise ProviderUnavailableError("NO_PROVIDER_REMAINED_USABLE")

def run_units_with_checkpoint(*,units:Iterable[Any],unit_id,source_hash,prompt_version,operation,lesson_id,checkpoint_root,state_root,providers_for_unit,authorised_providers_for_unit,verify,persist,attempts_per_provider=3,sleep=time.sleep,max_pause_cycles=12):
    out=[]
    for u in units:
        uid=unit_id(u);sh=source_hash(u)
        cp=load_verified_unit(checkpoint_root,lesson_id=lesson_id,unit_id=uid,operation=operation,source_hash=sh,prompt_version=prompt_version)
        if cp is not None:out.append({"unit_id":uid,"status":"CHECKPOINT","provider":cp.get("provider"),"model":cp.get("model")});continue
        try:
            result,provider,model=call_with_authorised_failover(u,providers=providers_for_unit(u),authorised_providers=authorised_providers_for_unit(u),attempts_per_provider=attempts_per_provider,sleep=sleep)
        except ProviderDailyQuotaError as e:
            e.state=save_state(state_root,lesson_id=lesson_id,status=STATUS_PAUSED_TRANSIENT,reason=str(e),unit_id=uid,retry_seconds=e.retry_after_seconds or 21600,max_pause_cycles=max_pause_cycles);raise
        except ProviderTransientError as e:
            e.state=save_state(state_root,lesson_id=lesson_id,status=STATUS_PAUSED_TRANSIENT,reason=str(e),unit_id=uid,retry_seconds=e.retry_after_seconds or 60,max_pause_cycles=max_pause_cycles);raise
        except ProviderUnavailableError as e:
            e.state=save_state(state_root,lesson_id=lesson_id,status=STATUS_PROVIDER_UNAVAILABLE,reason=str(e),unit_id=uid,max_pause_cycles=max_pause_cycles);raise
        except NeedsAttentionError as e:
            e.state=save_state(state_root,lesson_id=lesson_id,status=STATUS_NEEDS_ATTENTION,reason=str(e),unit_id=uid,max_pause_cycles=max_pause_cycles);raise
        if not verify(u,result):
            save_state(state_root,lesson_id=lesson_id,status=STATUS_NEEDS_ATTENTION,reason=f"UNIT_VERIFICATION_FAILED:{uid}",unit_id=uid);raise NeedsAttentionError(f"UNIT_VERIFICATION_FAILED:{uid}")
        ref,ah=persist(u,result)
        cp=save_verified_unit(checkpoint_root,lesson_id=lesson_id,unit_id=uid,operation=operation,source_hash=sh,prompt_version=prompt_version,provider=provider,model=model,artifact_ref=ref,artifact_hash=ah,extra={"actual_provider":provider,"actual_model":model,"operation":operation})
        out.append({"unit_id":uid,"status":"GENERATED","provider":provider,"model":model,"checkpoint_key":cp["checkpoint_key"]})
    save_state(state_root,lesson_id=lesson_id,status="COMPLETE")
    return out

def scientific_gate_result(state_root,*,lesson_id,passed,reason=""):
    return save_state(state_root,lesson_id=lesson_id,status=("SCIENTIFIC_GATE_PASS" if passed else STATUS_BLOCKED),reason=reason or ("" if passed else "SCIENTIFIC_GATE_FAILED"))
