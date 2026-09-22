/* Grade 7 Physics — Solids and Liquids: local, no-AI interactive laboratory. */
(()=>{
 if(document.getElementById("nabil-g7-lab"))return;
 const main=document.querySelector("main");
 if(!main)return;
 const box=document.createElement("section");
 box.id="nabil-g7-lab";
 box.style.cssText="margin:24px auto;padding:20px;max-width:1010px;border:2px solid #29c5db;border-radius:20px;background:#102b42;color:#f5fbff;font:inherit;box-sizing:border-box";
 box.innerHTML=`<h2 style="color:#8de9ff">🔬 Interactive laboratory · مختبر تفاعلي</h2>
 <p>Experiment 1 — Free surface of a liquid at rest: move the container. The liquid surface remains horizontal relative to gravity.</p>
 <label for="g7-tilt">Tilt the container · إمالة الوعاء: <output id="g7-angle">0°</output></label>
 <input id="g7-tilt" type="range" min="-30" max="30" value="0" step="1" style="width:100%;accent-color:#4ce3d6">
 <svg id="g7-surface" viewBox="0 0 520 235" role="img" aria-label="Tilted vessel and horizontal free liquid surface" style="width:100%;max-width:620px;display:block;margin:10px auto;background:#f4fbff;border-radius:12px">
 <defs><clipPath id="g7-vessel-clip"><rect x="170" y="35" width="180" height="170" rx="5"/></clipPath></defs>
 <g id="g7-vessel" transform="rotate(0 260 120)"><path d="M170 35 V205 H350 V35" fill="none" stroke="#263c52" stroke-width="7" stroke-linecap="round"/><path d="M173 126 H347 V201 H173 Z" fill="#35aeea" fill-opacity=".25"/></g>
 <path id="g7-water" d="M173 126 H347 V201 H173 Z" fill="#35aeea" fill-opacity=".68" clip-path="url(#g7-vessel-clip)"/>
 <path id="g7-line" d="M173 126 H347" stroke="#0065b4" stroke-width="3" stroke-dasharray="7 5"/>
 <text x="20" y="26" fill="#17324b" font-size="15">Horizontal free surface (schematic)</text></svg>
 <p id="g7-surface-result" aria-live="polite">At rest, the free surface is horizontal.</p>
 <hr style="border:0;border-top:1px solid #44758b;margin:20px 0">
 <p>Experiment 2 — Communicating vessels: connected open arms containing the same liquid at rest have the same surface height.</p>
 <label for="g7-level">Water level · مستوى الماء: <output id="g7-level-out">50%</output></label>
 <input id="g7-level" type="range" min="15" max="85" value="50" step="1" style="width:100%;accent-color:#4ce3d6">
 <svg id="g7-tubes" viewBox="0 0 520 240" role="img" aria-label="Connected vessels with equal water levels" style="width:100%;max-width:620px;display:block;margin:10px auto;background:#f4fbff;border-radius:12px">
 <path d="M95 22 V203 H425 V22 M95 203 H425" fill="none" stroke="#243d54" stroke-width="8" stroke-linejoin="round"/>
 <path d="M220 22 V165 H300 V22" fill="none" stroke="#243d54" stroke-width="8"/>
 <path id="g7-tube-water" d="" fill="#39aee8" fill-opacity=".75"/>
 <path id="g7-tube-level" d="" stroke="#0062a4" stroke-width="2" stroke-dasharray="7 5"/>
 <text x="16" y="17" fill="#17324b" font-size="14">Same liquid · same horizontal level</text></svg>
 <p id="g7-tube-result" aria-live="polite">Both arms show the same level: 50%.</p>
 <p style="font-size:.85em;color:#b5d7e4">Conceptual simulation, not a reproduction of the textbook's original figures. Assumes a stationary, connected liquid, open to the same atmospheric pressure.</p>`;
 const title=main.querySelector("h1");
 if(title&&title.parentElement===main)title.insertAdjacentElement("afterend",box);else main.insertBefore(box,main.firstChild);
 const tilt=box.querySelector("#g7-tilt"),vessel=box.querySelector("#g7-vessel"),water=box.querySelector("#g7-water"),line=box.querySelector("#g7-line");
 function drawTilt(){
  const a=Number(tilt.value),rad=a*Math.PI/180;
  vessel.setAttribute("transform",`rotate(${a} 260 120)`);
  // In vessel-local coordinates a horizontal world surface has slope -tan(angle).
  // Clip to the rotated vessel by transforming the water shape with the vessel.
  const left=126+90*Math.tan(rad),right=126-90*Math.tan(rad);
  water.setAttribute("d",`M173 ${left.toFixed(2)} L347 ${right.toFixed(2)} V201 H173 Z`);
  water.setAttribute("transform",`rotate(${a} 260 120)`);
  line.setAttribute("d",`M173 ${left.toFixed(2)} L347 ${right.toFixed(2)}`);
  line.setAttribute("transform",`rotate(${a} 260 120)`);
  box.querySelector("#g7-angle").textContent=a+"°";
  box.querySelector("#g7-surface-result").textContent=a===0?"At rest, the free surface is horizontal.":"The container tilts "+a+"°, but the water surface remains horizontal.";
 }
 tilt.addEventListener("input",drawTilt);drawTilt();
 const level=box.querySelector("#g7-level");
 function drawLevel(){
  const n=Number(level.value),y=198-n*1.75;
  box.querySelector("#g7-tube-water").setAttribute("d",`M99 ${y} H216 V165 H304 V${y} H421 V199 H99 Z`);
  box.querySelector("#g7-tube-level").setAttribute("d",`M98 ${y} H216 M304 ${y} H422`);
  box.querySelector("#g7-level-out").textContent=n+"%";
  box.querySelector("#g7-tube-result").textContent="Both connected arms: "+n+"% — equal surface heights.";
 }
 level.addEventListener("input",drawLevel);drawLevel();
})();