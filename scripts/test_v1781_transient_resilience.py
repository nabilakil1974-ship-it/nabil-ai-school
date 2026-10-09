from __future__ import annotations
import tempfile
from pathlib import Path
from nabil_transient_resilience_v1781 import *

def P(n,m,f): return ProviderSpec(n,m,f)

def main():
    passed=[]
    def ok(name): passed.append(name); print("PASS",name)

    q=classify_provider_error(RuntimeError("429 daily quota exceeded; retry in 5m12s"))
    assert q.kind=="daily_quota" and q.retry_after_seconds==312; ok("daily_quota_parse_5m12s")
    assert classify_provider_error(RuntimeError("401 invalid API key")).kind=="auth_billing"; ok("401_quarantine")
    assert classify_provider_error(RuntimeError("402 payment required credits exhausted")).kind=="auth_billing"; ok("402_quarantine")
    assert classify_provider_error(RuntimeError("400 invalid schema")).kind=="needs_attention"; ok("400_needs_attention")

    sleeps=[];c={"n":0}
    def retry(u):
        c["n"]+=1
        if c["n"]==1: raise RuntimeError("503 service unavailable retry after 37s")
        return {"ok":1}
    with tempfile.TemporaryDirectory() as td:
        r=Path(td)
        run_units_with_checkpoint(units=[1],unit_id=lambda u:"U",source_hash=lambda u:stable_sha256("s"),prompt_version="p",operation="op",lesson_id="L",checkpoint_root=r/"cp",state_root=r/"st",providers_for_unit=lambda u:[P("g","m",retry)],authorised_providers_for_unit=lambda u:{"g"},verify=lambda u,x:x["ok"]==1,persist=lambda u,x:("x",stable_sha256(x)),attempts_per_provider=2,sleep=lambda s:sleeps.append(s))
        assert sleeps==[37];ok("retry_after_honoured")

    calls={("g",i):0 for i in range(1,9)};calls.update({("b",i):0 for i in range(1,9)});first={5:True}
    def g(u):
        calls[("g",u)]+=1
        if u==5 and first[5]: first[5]=False; raise RuntimeError("503 high demand")
        if u==6: raise RuntimeError("503 high demand")
        return {"a":u*2}
    def b(u): calls[("b",u)]+=1; return {"a":u*2}
    with tempfile.TemporaryDirectory() as td:
        r=Path(td)
        kw=dict(units=range(1,9),unit_id=lambda u:f"E{u}",source_hash=lambda u:stable_sha256({"s":u}),prompt_version="p1",operation="exercise_solution",lesson_id="L",checkpoint_root=r/"cp",state_root=r/"st",providers_for_unit=lambda u:[P("g","gm",g),P("b","bm",b)],verify=lambda u,x:x["a"]==u*2,persist=lambda u,x:(f"m:{u}",stable_sha256(x)),attempts_per_provider=1,sleep=lambda s:None)
        try: run_units_with_checkpoint(authorised_providers_for_unit=lambda u:{"g"} if u==5 else {"g","b"},**kw); raise AssertionError()
        except ProviderTransientError: pass
        run_units_with_checkpoint(authorised_providers_for_unit=lambda u:{"g","b"},**kw)
        assert all(calls[("g",i)]==1 for i in range(1,5))
        cp=load_verified_unit(r/"cp",lesson_id="L",unit_id="E6",operation="exercise_solution",source_hash=stable_sha256({"s":6}),prompt_version="p1")
        assert cp["provider"]=="b" and cp["model"]=="bm";ok("503_resume_no_repeat_and_provider_recorded")

    qc={"g":0,"b":0}
    def qg(u): qc["g"]+=1; raise RuntimeError("429 daily quota exceeded retry in 5m12s")
    def qb(u): qc["b"]+=1; raise RuntimeError("429 daily quota exceeded retry in 10m0s")
    with tempfile.TemporaryDirectory() as td:
        r=Path(td)
        try: run_units_with_checkpoint(units=[1],unit_id=lambda u:"U",source_hash=lambda u:stable_sha256("s"),prompt_version="p",operation="op",lesson_id="L",checkpoint_root=r/"cp",state_root=r/"st",providers_for_unit=lambda u:[P("g","m",qg),P("b","m",qb)],authorised_providers_for_unit=lambda u:{"g","b"},verify=lambda u,x:True,persist=lambda u,x:("x","y"),attempts_per_provider=3,sleep=lambda s:None);raise AssertionError()
        except ProviderDailyQuotaError: pass
        st=load_state(r/"st","L");assert qc=={"g":1,"b":1} and st["status"]==STATUS_PAUSED_TRANSIENT and st["retry_after_seconds"]==312 and st["next_retry_at"];ok("daily_quota_failover_pause")

    def pay(u): raise RuntimeError("402 payment required credits exhausted")
    with tempfile.TemporaryDirectory() as td:
        r=Path(td)
        try: run_units_with_checkpoint(units=[1],unit_id=lambda u:"U",source_hash=lambda u:stable_sha256("s"),prompt_version="p",operation="op",lesson_id="L",checkpoint_root=r/"cp",state_root=r/"st",providers_for_unit=lambda u:[P("a","m",pay),P("b","m",pay)],authorised_providers_for_unit=lambda u:{"a","b"},verify=lambda u,x:True,persist=lambda u,x:("x","y"),sleep=lambda s:None);raise AssertionError()
        except ProviderUnavailableError: pass
        assert load_state(r/"st","L")["status"]==STATUS_PROVIDER_UNAVAILABLE;ok("all_402_provider_unavailable")

    def bad(u): raise RuntimeError("400 content policy refusal")
    with tempfile.TemporaryDirectory() as td:
        r=Path(td)
        try: run_units_with_checkpoint(units=[1],unit_id=lambda u:"U",source_hash=lambda u:stable_sha256("s"),prompt_version="p",operation="op",lesson_id="L",checkpoint_root=r/"cp",state_root=r/"st",providers_for_unit=lambda u:[P("g","m",bad)],authorised_providers_for_unit=lambda u:{"g"},verify=lambda u,x:True,persist=lambda u,x:("x","y"),sleep=lambda s:None);raise AssertionError()
        except NeedsAttentionError: pass
        assert load_state(r/"st","L")["status"]==STATUS_NEEDS_ATTENTION;ok("content_refusal_needs_attention")

    cc={"n":0}
    def f(u): cc["n"]+=1;return {"ok":1}
    with tempfile.TemporaryDirectory() as td:
        r=Path(td);base=dict(units=[1],unit_id=lambda u:"U",operation="op",lesson_id="L",checkpoint_root=r/"cp",state_root=r/"st",providers_for_unit=lambda u:[P("g","m",f)],authorised_providers_for_unit=lambda u:{"g"},verify=lambda u,x:x["ok"]==1,persist=lambda u,x:("x",stable_sha256(x)),sleep=lambda s:None)
        run_units_with_checkpoint(source_hash=lambda u:stable_sha256("A"),prompt_version="p1",**base)
        run_units_with_checkpoint(source_hash=lambda u:stable_sha256("B"),prompt_version="p1",**base)
        run_units_with_checkpoint(source_hash=lambda u:stable_sha256("B"),prompt_version="p2",**base)
        assert cc["n"]==3;ok("checkpoint_identity_strict")

    with tempfile.TemporaryDirectory() as td:
        r=Path(td);st=scientific_gate_result(r,lesson_id="L",passed=False,reason="SOURCE_EVIDENCE_MISSING")
        assert st["status"]==STATUS_BLOCKED and st["blocked"];ok("scientific_gate_only_blocked")

    print(f"V17.81_RESILIENCE_MATRIX_PASS tests={len(passed)}")

if __name__=="__main__":main()
