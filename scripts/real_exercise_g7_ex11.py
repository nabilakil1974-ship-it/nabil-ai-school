"""Real Grade-7 book exercise (Building up Mathematics Gr.7, ch.4 ex.11) -> solver JSON (normalised by the REAL
app.services.exercise_solver.normalise_solution) -> served through the real local app -> NABIL Golden V6 board.
HONESTY: the solution content here was authored by Claude in-session (no provider key / network in the sandbox);
it is NOT the output of the platform's ai_gateway. Angles are computed here, not typed by hand."""
import sys,json,math,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from app.services.exercise_solver import normalise_solution
STATEMENT=("تمرين 11 (كتاب Building up Mathematics الصف السابع): ABC مثلث فيه B = 60° و C = 40°. "
 "أ) احسب الزاوية A. ب) ارسم الارتفاع [AH] المرسوم من A، وجد قياس زوايا المثلثين ABH و AHC. "
 "ج) ليكن [BM) منصّف الزاوية B، جد قياس زوايا المثلثين AMB و BMC.")
Bd,Cd=60.0,40.0;Ad=180-Bd-Cd;a=6.0
c=a*math.sin(math.radians(Cd))/math.sin(math.radians(Ad))
B=(0.0,0.0);C=(a,0.0);A=(c*math.cos(math.radians(Bd)),c*math.sin(math.radians(Bd)));H=(A[0],0.0)
t=math.tan(math.radians(Bd/2));(ax,ay),(cx,cy)=A,C;s=(ay-t*ax)/(t*(cx-ax)-(cy-ay))*-1
# M on AC with y = t*x : A + u(C-A)
u=(t*ax-ay)/((cy-ay)-t*(cx-ax));M=(ax+u*(cx-ax),ay+u*(cy-ay))
assert abs(M[1]-t*M[0])<1e-9
ABH=90-Bd;HAC=90-Cd;ABM=MBC=Bd/2;AMB=180-Ad-ABM;BMC=180-MBC-Cd
assert ABH+HAC==Ad and AMB+BMC==180
r=lambda v:[round(v[0],3),round(v[1],3)]
d=lambda x:f"{x:g}°"
raw={"title":"تمرين 11 — زوايا المثلث ABC","given":["ABC مثلث","B = 60°","C = 40°"],
 "required":["أ) احسب الزاوية A","ب) زوايا المثلثين ABH و AHC حيث [AH] ارتفاع","ج) زوايا المثلثين AMB و BMC حيث [BM) منصّف B"],
 "figure":{"points":{"A":r(A),"B":r(B),"C":r(C),"H":r(H),"M":r(M)},
   "segments":[["A","B"],["B","C"],["A","C"]],"marks":[{"type":"angle","at":"B","text":"60°"},{"type":"angle","at":"C","text":"40°"}],"show":["A","B","C"]},
 "steps":[
 {"say":"أولًا نحسب الزاوية A","text":"مجموع زوايا أي مثلث 180°، فنطرح B و C من 180°.","formula":f"A = 180° − 60° − 40° = {d(Ad)}","justification":"مجموع زوايا المثلث يساوي 180°",
  "figure_step":{"marks":[{"type":"angle","at":"A","text":d(Ad)}]}},
 {"say":"ثانيًا نرسم الارتفاع AH","text":"الارتفاع [AH] عمودي على BC، فالزاوية AHB قائمة وكذلك AHC.","formula":"AHB = AHC = 90°","justification":"الارتفاع عمودي على القاعدة",
  "figure_step":{"segments":[["A","H","","dash"]],"marks":[{"type":"right_angle","at":"H","between":["A","B"]}],"show":["H"]}},
 {"say":"زوايا المثلث ABH","text":"في المثلث ABH الزاوية H قائمة و B تساوي 60°، فنحسب الزاوية BAH.","formula":f"BAH = 180° − 90° − 60° = {d(ABH)}","justification":"مجموع زوايا المثلث 180°"},
 {"say":"زوايا المثلث AHC","text":"في المثلث AHC الزاوية H قائمة و C تساوي 40°، فنحسب الزاوية HAC.","formula":f"HAC = 180° − 90° − 40° = {d(HAC)}","justification":"مجموع زوايا المثلث 180°"},
 {"say":"نتحقق من الارتفاع","text":"مجموع الزاويتين الصغيرتين يجب أن يساوي الزاوية A.","formula":f"{d(ABH)} + {d(HAC)} = {d(Ad)} = A  ✓"},
 {"say":"ثالثًا نرسم المنصّف BM","text":"المنصّف يقسم الزاوية B إلى زاويتين متساويتين.","formula":f"ABM = MBC = 60° ÷ 2 = {d(ABM)}","justification":"المنصّف يقسم الزاوية إلى نصفين",
  "figure_step":{"segments":[["B","M"]],"show":["M"]}},
 {"say":"زوايا المثلث AMB","text":"في المثلث AMB نعرف A = 80° و ABM = 30°، فنحسب الزاوية AMB.","formula":f"AMB = 180° − 80° − 30° = {d(AMB)}","justification":"مجموع زوايا المثلث 180°"},
 {"say":"زوايا المثلث BMC","text":"في المثلث BMC نعرف MBC = 30° و C = 40°، فنحسب الزاوية BMC.","formula":f"BMC = 180° − 30° − 40° = {d(BMC)}","justification":"مجموع زوايا المثلث 180°"},
 {"say":"نتحقق","text":"الزاويتان AMB و BMC متجاورتان على المستقيم AC فمجموعهما 180°.","formula":f"{d(AMB)} + {d(BMC)} = 180°  ✓"}],
 "answer":f"A = {d(Ad)} | ABH: H=90°, B=60°, BAH={d(ABH)} | AHC: H=90°, C=40°, HAC={d(HAC)} | AMB: A=80°, ABM=30°, AMB={d(AMB)} | BMC: MBC=30°, C=40°, BMC={d(BMC)}"}
sol=normalise_solution(raw);sol["statement"]=STATEMENT;sol["lang"]="ar"
sol["verification"]={"status":"not_checked","detail":"تحقق عددي في الكود: مجموع الزوايا = 180° في كل مثلث"}
if __name__=="__main__":
    pathlib.Path(sys.argv[1]).write_text(json.dumps(sol,ensure_ascii=False,indent=1),encoding="utf-8");print("angles",Ad,ABH,HAC,ABM,AMB,BMC,"M",[round(x,3) for x in M])
