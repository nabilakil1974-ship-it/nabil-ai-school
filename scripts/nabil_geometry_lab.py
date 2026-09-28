#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic, evidence-gated geometry proof renderer for NABIL AI.

The LLM may propose a layout, but every mathematical relation visualized as a
proof mark must be explicitly backed by a verified evidence quote before this
renderer is called.  The renderer never infers equality, parallelism,
perpendicularity, midpoint, congruence or symmetry from how a sketch looks.
"""
from __future__ import annotations

import html
import json
import math
import re
from typing import Any, Dict, Iterable, List, Tuple


GEOMETRY_MARK_TYPES = {
    "equal_segments",
    "equal_angles",
    "perpendicular",
    "parallel",
    "midpoint",
    "symmetry_axis",
}


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", str(value or "geo"))


def _point_map(spec: Dict[str, Any]) -> Dict[str, Tuple[float, float]]:
    out: Dict[str, Tuple[float, float]] = {}
    for item in spec.get("points") or []:
        label = str((item or {}).get("label") or "").strip()
        if not label:
            continue
        x = float(item.get("x"))
        y = float(item.get("y"))
        # Normalized authoring coordinates -> deterministic SVG board.
        out[label] = (52 + x * 5.3, 38 + y * 3.25)
    return out


def validate_geometry_proof_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    if str(spec.get("kind") or "").upper() != "GEOMETRY_PROOF":
        return spec

    points = spec.get("points")
    segments = spec.get("segments")
    marks = spec.get("marks")
    proof_steps = spec.get("proof_steps")
    if not isinstance(points, list) or not 2 <= len(points) <= 12:
        raise RuntimeError("LAB_GEOMETRY_POINTS_INVALID")
    labels: List[str] = []
    for p in points:
        if not isinstance(p, dict):
            raise RuntimeError("LAB_GEOMETRY_POINT_INVALID")
        label = str(p.get("label") or "").strip()
        if not label or label in labels:
            raise RuntimeError("LAB_GEOMETRY_POINT_LABEL_INVALID")
        labels.append(label)
        try:
            x = float(p.get("x")); y = float(p.get("y"))
        except Exception as exc:
            raise RuntimeError("LAB_GEOMETRY_POINT_LAYOUT_INVALID") from exc
        if not (0 <= x <= 100 and 0 <= y <= 100):
            raise RuntimeError("LAB_GEOMETRY_POINT_LAYOUT_OUT_OF_RANGE")

    if not isinstance(segments, list) or not 1 <= len(segments) <= 20:
        raise RuntimeError("LAB_GEOMETRY_SEGMENTS_INVALID")
    seg_ids: List[str] = []
    for seg in segments:
        if not isinstance(seg, dict):
            raise RuntimeError("LAB_GEOMETRY_SEGMENT_INVALID")
        sid = str(seg.get("id") or "").strip()
        a = str(seg.get("a") or "").strip()
        b = str(seg.get("b") or "").strip()
        if not sid or sid in seg_ids or a not in labels or b not in labels or a == b:
            raise RuntimeError("LAB_GEOMETRY_SEGMENT_ENDPOINT_INVALID")
        seg_ids.append(sid)

    if not isinstance(marks, list):
        raise RuntimeError("LAB_GEOMETRY_MARKS_INVALID")
    mark_ids: List[str] = []
    for mark in marks:
        if not isinstance(mark, dict):
            raise RuntimeError("LAB_GEOMETRY_MARK_INVALID")
        mid = str(mark.get("id") or "").strip()
        mtype = str(mark.get("type") or "").strip().lower()
        quote = str(mark.get("evidence_quote") or "").strip()
        if not mid or mid in mark_ids or mtype not in GEOMETRY_MARK_TYPES or not quote:
            raise RuntimeError("LAB_GEOMETRY_MARK_METADATA_INVALID")
        mark_ids.append(mid)
        targets = mark.get("targets") or []
        if mtype in {"equal_segments", "parallel", "midpoint"}:
            if not isinstance(targets, list) or len(targets) < 1 or any(str(x) not in seg_ids for x in targets):
                raise RuntimeError(f"LAB_GEOMETRY_MARK_TARGET_INVALID:{mid}")
        elif mtype in {"equal_angles", "perpendicular"}:
            angles = mark.get("angles") or []
            if not isinstance(angles, list) or len(angles) < 1:
                raise RuntimeError(f"LAB_GEOMETRY_ANGLE_MARK_INVALID:{mid}")
            for angle in angles:
                if not isinstance(angle, dict):
                    raise RuntimeError(f"LAB_GEOMETRY_ANGLE_MARK_INVALID:{mid}")
                if any(str(angle.get(k) or "") not in labels for k in ("a", "vertex", "b")):
                    raise RuntimeError(f"LAB_GEOMETRY_ANGLE_POINT_INVALID:{mid}")
        elif mtype == "symmetry_axis":
            axis = str(mark.get("axis_segment") or "").strip()
            if axis not in seg_ids:
                raise RuntimeError(f"LAB_GEOMETRY_SYMMETRY_AXIS_INVALID:{mid}")
            pairs = mark.get("point_pairs") or []
            for pair in pairs:
                if not isinstance(pair, list) or len(pair) != 2 or any(str(x) not in labels for x in pair):
                    raise RuntimeError(f"LAB_GEOMETRY_SYMMETRY_PAIR_INVALID:{mid}")

    if not isinstance(proof_steps, list) or not 1 <= len(proof_steps) <= 12:
        raise RuntimeError("LAB_GEOMETRY_PROOF_STEPS_INVALID")
    for i, step in enumerate(proof_steps):
        if not isinstance(step, dict):
            raise RuntimeError(f"LAB_GEOMETRY_PROOF_STEP_INVALID:{i}")
        if not str(step.get("title") or "").strip() or not str(step.get("text") or "").strip():
            raise RuntimeError(f"LAB_GEOMETRY_PROOF_STEP_TEXT_INVALID:{i}")
        if not str(step.get("evidence_quote") or "").strip():
            raise RuntimeError(f"LAB_GEOMETRY_PROOF_STEP_EVIDENCE_MISSING:{i}")
        reveal = step.get("reveal_marks") or []
        if not isinstance(reveal, list) or any(str(x) not in mark_ids for x in reveal):
            raise RuntimeError(f"LAB_GEOMETRY_PROOF_STEP_MARK_INVALID:{i}")
        targets = step.get("target_ids") or []
        allowed_targets = (
            set(mark_ids)
            | {f"point:{label}" for label in labels}
            | {f"segment:{sid}" for sid in seg_ids}
        )
        if (
            not isinstance(targets, list)
            or not targets
            or any(str(x) not in allowed_targets for x in targets)
        ):
            raise RuntimeError(f"LAB_GEOMETRY_PROOF_STEP_TARGET_INVALID:{i}")
    interaction = spec.get("interaction")
    if interaction is not None:
        if not isinstance(interaction, dict):
            raise RuntimeError("LAB_GEOMETRY_INTERACTION_INVALID")
        draggable = interaction.get("draggable_points") or []
        if not isinstance(draggable, list) or any(str(x) not in labels for x in draggable):
            raise RuntimeError("LAB_GEOMETRY_DRAG_POINT_INVALID")
        if draggable and not str(interaction.get("evidence_quote") or "").strip():
            raise RuntimeError("LAB_GEOMETRY_DRAG_EVIDENCE_MISSING")
        constraints = interaction.get("constraints") or {}
        if not isinstance(constraints, dict):
            raise RuntimeError("LAB_GEOMETRY_DRAG_CONSTRAINT_INVALID")
        for label in draggable:
            c = constraints.get(str(label)) or {"type": "free"}
            ctype = str(c.get("type") or "")
            if not isinstance(c, dict) or ctype not in {"free","horizontal","vertical","segment","circle"}:
                raise RuntimeError(f"LAB_GEOMETRY_DRAG_CONSTRAINT_INVALID:{label}")
            if ctype == "segment" and str(c.get("segment_id") or "") not in seg_ids:
                raise RuntimeError(f"LAB_GEOMETRY_DRAG_SEGMENT_INVALID:{label}")
            if ctype == "circle":
                if str(c.get("center") or "") not in labels:
                    raise RuntimeError(f"LAB_GEOMETRY_DRAG_CIRCLE_CENTER_INVALID:{label}")
                try:
                    if float(c.get("radius")) <= 0:
                        raise ValueError()
                except Exception as exc:
                    raise RuntimeError(f"LAB_GEOMETRY_DRAG_CIRCLE_RADIUS_INVALID:{label}") from exc
    return spec


def _seg_map(spec: Dict[str, Any], pts: Dict[str, Tuple[float, float]]) -> Dict[str, Tuple[Tuple[float,float],Tuple[float,float]]]:
    out = {}
    for seg in spec.get("segments") or []:
        out[str(seg["id"])] = (pts[str(seg["a"])], pts[str(seg["b"])])
    return out


def _tick_paths(a: Tuple[float,float], b: Tuple[float,float], count: int = 1) -> str:
    ax, ay = a; bx, by = b
    dx, dy = bx-ax, by-ay
    L = math.hypot(dx,dy) or 1.0
    nx, ny = -dy/L, dx/L
    tx, ty = dx/L, dy/L
    mx, my = (ax+bx)/2, (ay+by)/2
    pieces=[]
    for k in range(count):
        off=(k-(count-1)/2)*8
        cx,cy=mx+tx*off,my+ty*off
        pieces.append(f"M{cx-nx*7:.1f},{cy-ny*7:.1f} L{cx+nx*7:.1f},{cy+ny*7:.1f}")
    return " ".join(pieces)


def _parallel_path(a: Tuple[float,float], b: Tuple[float,float], count: int = 1) -> str:
    ax, ay = a; bx, by = b
    dx,dy=bx-ax,by-ay
    L=math.hypot(dx,dy) or 1.0
    tx,ty=dx/L,dy/L
    nx,ny=-ty,tx
    mx,my=(ax+bx)/2,(ay+by)/2
    pieces=[]
    for k in range(count):
        off=(k-(count-1)/2)*14
        cx,cy=mx+tx*off,my+ty*off
        p1=(cx-tx*8+nx*6,cy-ty*8+ny*6)
        p2=(cx,cy)
        p3=(cx-tx*8-nx*6,cy-ty*8-ny*6)
        pieces.append(f"M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}")
    return " ".join(pieces)


def _angle_arc(a, v, b, r=30.0) -> str:
    def ang(p):
        return math.atan2(p[1]-v[1],p[0]-v[0])
    a1,a2=ang(a),ang(b)
    d=a2-a1
    while d>math.pi: d-=2*math.pi
    while d<-math.pi: d+=2*math.pi
    p1=(v[0]+r*math.cos(a1),v[1]+r*math.sin(a1))
    p2=(v[0]+r*math.cos(a1+d),v[1]+r*math.sin(a1+d))
    sweep=1 if d>0 else 0
    return f"M{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 0 {sweep} {p2[0]:.1f},{p2[1]:.1f}"


def _right_square(a, v, b, size=16.0) -> str:
    def unit(p):
        dx,dy=p[0]-v[0],p[1]-v[1]
        L=math.hypot(dx,dy) or 1.0
        return dx/L,dy/L
    u=unit(a); w=unit(b)
    p1=(v[0]+u[0]*size,v[1]+u[1]*size)
    p2=(p1[0]+w[0]*size,p1[1]+w[1]*size)
    p3=(v[0]+w[0]*size,v[1]+w[1]*size)
    return f"M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}"


def render_geometry_proof_lab(spec: Dict[str, Any], lang: str, lab_id: str) -> Tuple[str, bool]:
    validate_geometry_proof_spec(spec)
    safe=_safe_id(lab_id)
    pts=_point_map(spec); segs=_seg_map(spec,pts)
    labels={
        "ar":{"prev":"◀ السابق","next":"التالي ▶","speak":"🔊 اشرح هذه الخطوة","all":"▶ اشرح من البداية","stop":"■ أوقف الشرح","reset":"↺ أعد البرهان","proof":"👨‍🏫 شرح نبيل","idle":"يمكنك متابعة البرهان خطوة خطوة."},
        "fr":{"prev":"◀ Précédent","next":"Suivant ▶","speak":"🔊 Expliquer cette étape","all":"▶ Expliquer depuis le début","stop":"■ Arrêter","reset":"↺ Réinitialiser","proof":"👨‍🏫 Explication de NABIL","idle":"Suivez la démonstration étape par étape."},
        "en":{"prev":"◀ Previous","next":"Next ▶","speak":"🔊 Explain this step","all":"▶ Explain from the beginning","stop":"■ Stop","reset":"↺ Reset proof","proof":"👨‍🏫 NABIL explanation","idle":"Follow the proof step by step."},
    }.get(lang)
    segment_svg=[]
    for seg in spec.get("segments") or []:
        sid=str(seg["id"]); a,b=segs[sid]
        segment_svg.append(
            f'<line id="{safe}_seg_{_safe_id(sid)}" x1="{a[0]:.1f}" y1="{a[1]:.1f}" '
            f'x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="geo-seg"/>'
        )
    point_svg=[]
    for label,(x,y) in pts.items():
        point_svg.append(
            f'<g id="{safe}_pt_{_safe_id(label)}"><circle cx="{x:.1f}" cy="{y:.1f}" r="5" class="geo-point"/>'
            f'<text x="{x+9:.1f}" y="{y-8:.1f}" class="geo-label">{html.escape(label)}</text></g>'
        )
    marks_svg=[]
    mark_targets={}
    for idx,mark in enumerate(spec.get("marks") or [],1):
        mid=str(mark["id"]); mtype=str(mark["type"]).lower()
        count=max(1,min(3,int(mark.get("style_index") or idx)))
        paths=[]
        anchor=(320.0,210.0)
        if mtype in {"equal_segments","midpoint"}:
            for sid in mark.get("targets") or []:
                a,b=segs[str(sid)]; paths.append(_tick_paths(a,b,count))
                anchor=((a[0]+b[0])/2,(a[1]+b[1])/2)
        elif mtype=="parallel":
            for sid in mark.get("targets") or []:
                a,b=segs[str(sid)]; paths.append(_parallel_path(a,b,min(2,count)))
                anchor=((a[0]+b[0])/2,(a[1]+b[1])/2)
        elif mtype=="equal_angles":
            for angle in mark.get("angles") or []:
                a=pts[str(angle["a"])]; v=pts[str(angle["vertex"])]; b=pts[str(angle["b"])]
                paths.append(_angle_arc(a,v,b,24+6*min(2,count)))
                anchor=v
        elif mtype=="perpendicular":
            for angle in mark.get("angles") or []:
                a=pts[str(angle["a"])]; v=pts[str(angle["vertex"])]; b=pts[str(angle["b"])]
                paths.append(_right_square(a,v,b))
                anchor=v
        elif mtype=="symmetry_axis":
            a,b=segs[str(mark["axis_segment"])]
            paths.append(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}")
            anchor=((a[0]+b[0])/2,(a[1]+b[1])/2)
        mark_targets[mid]=anchor
        cls="geo-mark geo-symmetry" if mtype=="symmetry_axis" else "geo-mark"
        marks_svg.append(f'<path id="{safe}_mark_{_safe_id(mid)}" d="{" ".join(paths)}" class="{cls}" data-mark-type="{html.escape(mtype)}"/>')

    steps=spec.get("proof_steps") or []
    step_payload=[]
    for step in steps:
        targets=step.get("target_ids") or []
        if not targets and step.get("reveal_marks"):
            targets=list(step["reveal_marks"])
        step_payload.append({
            "title":str(step.get("title") or ""),
            "text":str(step.get("text") or ""),
            "formula":str(step.get("formula") or ""),
            "reveal":list(step.get("reveal_marks") or []),
            "targets":targets,
        })
    mark_xy={k:[round(v[0],1),round(v[1],1)] for k,v in mark_targets.items()}
    point_xy={f"point:{k}":[round(v[0],1),round(v[1],1)] for k,v in pts.items()}
    seg_xy={f"segment:{sid}":[round((a[0]+b[0])/2,1),round((a[1]+b[1])/2,1)] for sid,(a,b) in segs.items()}
    target_xy={**mark_xy,**point_xy,**seg_xy}
    return f"""
<section class="interactive-lab nabil-geometry-proof" id="lab_{safe}"
 data-lab-kind="GEOMETRY_PROOF" data-teacher-pointer="sentence-synced"
 data-proof-marks="evidence-gated" data-demo-ms="{max(8000,len(steps)*2800)}"
 style="margin-top:16px;background:#071827;color:#f8fafc;border:1px solid #24506f;border-radius:14px;padding:14px;">
 <style>
 #lab_{safe} .geo-board{{position:relative;background:#020912;border:1px solid #1c4569;border-radius:14px;overflow:hidden}}
 #lab_{safe} svg{{width:100%;height:auto;display:block}}
 #lab_{safe} .geo-seg{{stroke:#d7e9f6;stroke-width:3}}
 #lab_{safe} .geo-point{{fill:#ffd76b;stroke:#fff;stroke-width:2}}
 #lab_{safe} .geo-label{{fill:#ffd76b;font:bold 14px system-ui}}
 #lab_{safe} .geo-mark{{fill:none;stroke:#55e6a4;stroke-width:3.3;stroke-linecap:round;stroke-linejoin:round;opacity:0;transition:opacity .25s}}
 #lab_{safe} .geo-mark.on{{opacity:1}}
 #lab_{safe} .geo-symmetry{{stroke:#c891ff;stroke-width:10;stroke-dasharray:10 8;animation:{safe}_pulse 1.1s ease-in-out infinite}}
 #lab_{safe} .geo-focus{{filter:drop-shadow(0 0 7px #2de1ff);stroke:#2de1ff!important}}
 #lab_{safe} .proof-panel{{background:#061725;border:1px solid #254a68;border-radius:12px;padding:10px;margin-top:10px}}
 #lab_{safe} .proof-panel h4{{margin:0 0 6px;color:#ffd76b}}
 #lab_{safe} .proof-formula{{direction:ltr;text-align:center;font-family:"Cambria Math",serif;font-size:18px;background:#03111d;border:1px dashed #315d79;border-radius:9px;padding:8px;margin-top:7px}}
 #lab_{safe} .geo-controls{{display:flex;gap:7px;flex-wrap:wrap;margin-top:9px}}
 #lab_{safe} .geo-controls button{{min-height:44px;border:1px solid #426d8b;background:#153955;color:#fff;padding:8px 11px;border-radius:9px;font-weight:800}}
 #lab_{safe} .geo-timeline{{display:flex;gap:5px;flex-wrap:wrap;margin-top:8px}}
 #lab_{safe} .geo-dot{{width:32px;height:32px;min-height:32px;border-radius:50%;padding:0;background:#071725;color:#9fb5c9;border:1px solid #31506b}}
 #lab_{safe} .geo-dot.on{{background:#0b5d70;border-color:#2de1ff;color:#fff}}
 #lab_{safe} .geo-dot.done{{background:#0d4c3c;border-color:#55e6a4;color:#fff}}
 @keyframes {safe}_pulse{{0%,100%{{opacity:.22}}50%{{opacity:.72}}}}
 @media(max-width:430px){{#lab_{safe}{{padding:7px}}#lab_{safe} .geo-controls{{display:grid;grid-template-columns:1fr 1fr}}}}
 </style>
 <h3 style="margin-top:0;color:#2de1ff">{html.escape(str(spec.get("title") or "Geometry Proof"))}</h3>
 <p>{html.escape(str(spec.get("instructions") or ""))}</p>
 <div class="geo-board">
  <svg viewBox="0 0 640 420" role="img" aria-label="{html.escape(str(spec.get("title") or "Geometry proof"))}">
   <defs><pattern id="{safe}_grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#0a2135"/></pattern>
   <marker id="{safe}_arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#2de1ff"/></marker></defs>
   <rect width="640" height="420" fill="#020912"/><rect width="640" height="420" fill="url(#{safe}_grid)"/>
   {"".join(segment_svg)}{"".join(marks_svg)}{"".join(point_svg)}
   <line id="{safe}_teacherArrow" x1="600" y1="46" x2="500" y2="95" stroke="#2de1ff" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#{safe}_arrow)"/>
  </svg>
 </div>
 <div class="proof-panel"><div style="display:flex;justify-content:space-between;gap:8px"><strong>{html.escape(labels["proof"])}</strong><span id="{safe}_count"></span></div>
  <h4 id="{safe}_title"></h4><div id="{safe}_text"></div><div class="proof-formula" id="{safe}_formula"></div>
 </div>
 <div class="geo-controls">
  <button id="{safe}_prev">{html.escape(labels["prev"])}</button><button id="{safe}_next">{html.escape(labels["next"])}</button>
  <button id="{safe}_speak">{html.escape(labels["speak"])}</button><button id="{safe}_all">{html.escape(labels["all"])}</button>
  <button id="{safe}_stop">{html.escape(labels["stop"])}</button><button id="{safe}_reset">{html.escape(labels["reset"])}</button>
 </div>
 <div class="geo-timeline" id="{safe}_timeline"></div>
 <div style="margin-top:8px;font-size:12px;color:#b9d7ea">{html.escape(str(spec.get("observation") or labels["idle"]))}</div>
 <script>
 (()=>{{
  const q=id=>document.getElementById(id);
  const steps={json.dumps(step_payload,ensure_ascii=False)};
  const xy={json.dumps(target_xy,ensure_ascii=False)};
  const authoredPoints={json.dumps({k:[float(v[0]),float(v[1])] for k,v in pts.items()},ensure_ascii=False)};
  const segmentDefs={json.dumps([{"id":str(s["id"]),"a":str(s["a"]),"b":str(s["b"])} for s in (spec.get("segments") or [])],ensure_ascii=False)};
  const interaction={json.dumps(spec.get("interaction") or {},ensure_ascii=False)};
  let step=0,token=0,dragLabel=null,dragPid=null;
  function clearFocus(){{
    q('lab_{safe}').querySelectorAll('.geo-mark').forEach(x=>x.classList.remove('on'));
    q('lab_{safe}').querySelectorAll('.geo-focus').forEach(x=>x.classList.remove('geo-focus'));
  }}
  function targetPoint(key){{
    const p=xy[key];if(!p)return [500,95];return p;
  }}
  function arrowTo(key){{
    const p=targetPoint(key),arrow=q('{safe}_teacherArrow');arrow.setAttribute('x2',p[0]);arrow.setAttribute('y2',p[1]);
    let el=null;
    if(key.startsWith('segment:'))el=q('{safe}_seg_'+key.slice(8).replace(/[^a-zA-Z0-9_]/g,'_'));
    else if(key.startsWith('point:'))el=q('{safe}_pt_'+key.slice(6).replace(/[^a-zA-Z0-9_]/g,'_'));
    else el=q('{safe}_mark_'+String(key).replace(/[^a-zA-Z0-9_]/g,'_'));
    el?.classList.add('geo-focus');
  }}
  function renderStep(){{
    const s=steps[step];clearFocus();
    const established=[];
     for(let j=0;j<=step;j++) (steps[j].reveal||[]).forEach(id=>{{if(!established.includes(id))established.push(id)}});
     established.forEach(id=>q('{safe}_mark_'+String(id).replace(/[^a-zA-Z0-9_]/g,'_'))?.classList.add('on'));
    arrowTo((s.targets&&s.targets[0])||s.reveal[0]||'');
    q('{safe}_title').textContent=s.title;q('{safe}_text').textContent=s.text;q('{safe}_formula').textContent=s.formula||'';
    q('{safe}_formula').style.display=s.formula?'block':'none';q('{safe}_count').textContent=(step+1)+' / '+steps.length;
    [...q('{safe}_timeline').children].forEach((b,i)=>b.className='geo-dot '+(i<step?'done':i===step?'on':''));
  }}

  function svgLocal(e){{
    const svg=q('{safe}_teacherArrow')?.ownerSVGElement;
    const p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;
    return p.matrixTransform(svg.getScreenCTM().inverse());
  }}
  function pointGroup(label){{return q('{safe}_pt_'+String(label).replace(/[^a-zA-Z0-9_]/g,'_'))}}
  function pointXY(label){{
    const c=pointGroup(label)?.querySelector('circle');
    return c?[Number(c.getAttribute('cx')),Number(c.getAttribute('cy'))]:(authoredPoints[label]||[0,0]);
  }}
  function setPointXY(label,x,y){{
    const grp=pointGroup(label);if(!grp)return;
    x=Math.max(18,Math.min(622,x));y=Math.max(18,Math.min(402,y));
    const c=grp.querySelector('circle'),t=grp.querySelector('text');
    c?.setAttribute('cx',x);c?.setAttribute('cy',y);
    t?.setAttribute('x',x+9);t?.setAttribute('y',y-8);
    xy['point:'+label]=[x,y];
  }}
  function projectConstraint(label,p){{
    const c=(interaction.constraints||{{}})[label]||{{type:'free'}};
    const original=authoredPoints[label]||[p.x,p.y];
    if(c.type==='horizontal') return [p.x,original[1]];
    if(c.type==='vertical') return [original[0],p.y];
    if(c.type==='segment'){{
      const s=segmentDefs.find(x=>x.id===String(c.segment_id));if(!s)return original;
      const A=pointXY(s.a),B=pointXY(s.b),vx=B[0]-A[0],vy=B[1]-A[1],d=vx*vx+vy*vy||1;
      const tt=Math.max(0,Math.min(1,((p.x-A[0])*vx+(p.y-A[1])*vy)/d));
      return [A[0]+tt*vx,A[1]+tt*vy];
    }}
    if(c.type==='circle'){{
      const C=pointXY(String(c.center)),r=Number(c.radius)||0,dx=p.x-C[0],dy=p.y-C[1],L=Math.hypot(dx,dy)||1;
      return [C[0]+dx/L*r,C[1]+dy/L*r];
    }}
    return [p.x,p.y];
  }}
  function refreshDynamicGeometry(){{
    segmentDefs.forEach(s=>{{
      const A=pointXY(s.a),B=pointXY(s.b),el=q('{safe}_seg_'+String(s.id).replace(/[^a-zA-Z0-9_]/g,'_'));
      if(el){{el.setAttribute('x1',A[0]);el.setAttribute('y1',A[1]);el.setAttribute('x2',B[0]);el.setAttribute('y2',B[1]);}}
      xy['segment:'+s.id]=[(A[0]+B[0])/2,(A[1]+B[1])/2];
    }});
  }}
  function installReferenceDrag(){{
    const allowed=new Set(Array.isArray(interaction.draggable_points)?interaction.draggable_points.map(String):[]);
    allowed.forEach(label=>{{
      const c=pointGroup(label)?.querySelector('circle');if(!c)return;
      c.style.cursor='grab';c.style.touchAction='none';
      c.addEventListener('pointerdown',e=>{{token++;dragLabel=label;dragPid=e.pointerId;c.setPointerCapture?.(dragPid);c.style.cursor='grabbing';e.preventDefault()}});
      c.addEventListener('pointermove',e=>{{
        if(dragLabel!==label||e.pointerId!==dragPid)return;
        const p=svgLocal(e),qv=projectConstraint(label,p);setPointXY(label,qv[0],qv[1]);refreshDynamicGeometry();renderStep();e.preventDefault();
      }});
      const end=e=>{{if(dragLabel===label&&e.pointerId===dragPid){{dragLabel=null;dragPid=null;c.style.cursor='grab'}}}};
      c.addEventListener('pointerup',end);c.addEventListener('pointercancel',end);
    }});
  }}

  function buildTimeline(){{q('{safe}_timeline').innerHTML='';steps.forEach((_,i)=>{{const b=document.createElement('button');b.className='geo-dot';b.textContent=i+1;b.onclick=()=>{{token++;step=i;renderStep()}};q('{safe}_timeline').appendChild(b)}})}}
  async function speakOne(i,done){{
    step=i;renderStep();const s=steps[i];const my=token;
    const sentences=(s.text+' '+(s.formula||'')).split(/(?<=[.!?؟])\s+/).filter(Boolean);
    let k=0;
    const next=async()=>{{
      if(my!==token)return;
      if(k>=sentences.length){{done?.();return}}
      const key=(s.targets&&s.targets[Math.min(k,s.targets.length-1)])||(s.reveal&&s.reveal[0])||'';
      arrowTo(key);
      const txt=sentences[k++];
      try{{await Promise.resolve(window.NABILLessonE2E?.speak?.(txt,{json.dumps(lang)}));}}catch(_e){{}}
      if(my!==token)return;
      setTimeout(next,180);
    }};
    next();
  }}
  function playAll(){{
     token++;const my=token;let i=0;
     q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-start',{{detail:{{labRef:'{safe}',stepCount:steps.length}},bubbles:true}}));
     const next=()=>{{
       if(my!==token)return;
       if(i>=steps.length){{
         q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-complete',{{detail:{{labRef:'{safe}',stepCount:steps.length}},bubbles:true}}));
         return;
       }}
       speakOne(i++,next);
     }};
     next();
   }}
  q('{safe}_prev').onclick=()=>{{token++;step=(step+steps.length-1)%steps.length;renderStep()}};
  q('{safe}_next').onclick=()=>{{token++;step=(step+1)%steps.length;renderStep()}};
  q('{safe}_speak').onclick=()=>{{token++;speakOne(step)}};
  q('{safe}_all').onclick=playAll;
  function stopTeaching(){{
     token++;try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}
     q('lab_{safe}').querySelectorAll('.geo-focus').forEach(x=>x.classList.remove('geo-focus'));
     q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}},bubbles:true}}));
   }}
   q('{safe}_stop').onclick=stopTeaching;
  q('{safe}_reset').onclick=()=>{{stopTeaching();step=0;renderStep()}};
  q('lab_{safe}').addEventListener('nabil:demo',playAll);
   q('lab_{safe}').addEventListener('nabil:teach-all',playAll);
   q('lab_{safe}').addEventListener('nabil:teach-stop',stopTeaching);
   q('lab_{safe}').addEventListener('nabil:teacher-stop',stopTeaching);
  buildTimeline();renderStep();installReferenceDrag();
 }})();
 </script>
</section>""", True
