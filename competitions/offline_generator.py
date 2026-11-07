from __future__ import annotations

"""Deterministic, offline mathematics assessment generator. No model/API dependency."""
import hashlib
import math

def _family(topic: str) -> str:
    t = topic.lower()
    rules = [
        (("prime",), "prime"), (("power", "exponent"), "powers"),
        (("signed number", "order", "absolute value"), "signed"),
        (("fraction",), "fraction"), (("decimal",), "decimal"),
        (("proportion", "interest", "annuity", "distribution of two variables"), "proportion"),
        (("statistic", "dispersion", "position measures", "graphical interpretation"), "statistics"),
        (("probab", "event", "random variable", "combination", "permutation"), "probability"),
        (("sequence",), "sequence"), (("antiderivative",), "antiderivative"), (("derivative",), "derivative"),
        (("limit", "continuity", "continuous"), "limit"),
        (("integral", "integration"), "integral"),
        (("logarithm", "exponential"), "logexp"),
        (("quadratic",), "quadratic"), (("equation", "inequalit", "system"), "equation"),
        (("trigon",), "trig"), (("pythagoras", "right triangle"), "pythagoras"),
        (("vector", "scalar product", "orthogonality", "vector product"), "vector"),
        (("coordinate", "plotting", "graph", "line in", "analytic geometry"), "coordinate"),
        (("circle", "arc", "angle", "line", "perpendicular", "locus", "midpoint", "thales", "similar triangle", "congruent", "square", "rectangle", "rhombus", "parallelogram", "plane geometry", "planes and lines", "parallelism"), "geometry"),
        (("function", "inverse"), "function"), (("set",), "sets"),
        (("complex",), "complex"), (("real number", "square root"), "real"),
        (("signed number", "absolute value", "order"), "signed"),
        (("locating a point",), "coordinate"),
        (("economics", "compound", "interest"), "finance"),
    ]
    for needles, family in rules:
        if any(n in t for n in needles):
            return family
    return "algebra"

def _make(topic: str, lang: str, n: int):
    family = _family(topic)
    en = lang == "en"
    # Stable variation by lesson name; every task is solvable without external services.
    seed = int(hashlib.sha256(topic.encode()).hexdigest()[:8], 16)
    a, b = 2 + seed % 7, 3 + (seed // 7) % 8
    if family == "powers":
        x = 2 + seed % 4; p, q = 2 + seed % 3, 1 + (seed // 5) % 3
        statement = (f"Simplify {x}^{p} × {x}^{q}, then calculate its value." if en else f"Simplifier {x}^{p} × {x}^{q}, puis calculer sa valeur.")
        ans = f"{x}^{p+q} = {x**(p+q)}"
        steps = ([f"We write: {x}^{p} × {x}^{q}", f"We substitute: same base, add exponents: {x}^{p+q}", f"We calculate: {x**(p+q)}", f"We conclude: {ans}"] if en else [f"On écrit : {x}^{p} × {x}^{q}", f"On remplace : même base, on additionne les exposants : {x}^{p+q}", f"On calcule : {x**(p+q)}", f"On conclut : {ans}"])
    elif family == "prime":
        x = 30 + seed % 40
        factors=[]; v=x; d=2
        while d*d<=v:
            while v%d==0: factors.append(d); v//=d
            d+=1
        if v>1:factors.append(v)
        statement = (f"Write {x} as a product of prime factors. State whether {x} is prime." if en else f"Décomposer {x} en produit de facteurs premiers. Dire si {x} est premier.")
        ans=" × ".join(map(str,factors)) + (f"; {x} is not prime." if en else f" ; {x} n'est pas premier.")
        steps=([f"We divide successively by prime numbers: {ans}",f"We conclude: {x} is composite."] if en else [f"On divise successivement par les nombres premiers : {ans}",f"On conclut : {x} est composé."])
    elif family in ("equation","algebra"):
        x=2+seed%9; c=2+(seed//9)%9; k=x+c
        statement=(f"Solve the equation x + {c} = {k}. Verify your result." if en else f"Résoudre l'équation x + {c} = {k}. Vérifier le résultat.")
        ans=f"x = {x}"
        steps=([f"We write: x + {c} = {k}",f"We subtract {c} from both sides: x = {k} − {c}",f"We calculate: x = {x}",f"We conclude: x = {x}; verification: {x}+{c}={k}."] if en else [f"On écrit : x + {c} = {k}",f"On soustrait {c} des deux membres : x = {k} − {c}",f"On calcule : x = {x}",f"On conclut : x = {x} ; vérification : {x}+{c}={k}."])
    elif family == "signed":
        x=3+seed%8; y=2+seed%7
        statement=(f"Calculate (−{x}) + {y} and (−{x}) × (−{y})." if en else f"Calculer (−{x}) + {y} et (−{x}) × (−{y}).")
        ans=f"{y-x} and {x*y}"
        steps=([f"Additive calculation: −{x}+{y}={y-x}.",f"Product of two negative numbers is positive: (−{x})×(−{y})={x*y}.",f"We conclude: {ans}."] if en else [f"Somme : −{x}+{y}={y-x}.",f"Le produit de deux nombres négatifs est positif : (−{x})×(−{y})={x*y}.",f"On conclut : {ans}."])
    elif family in ("fraction","decimal"):
        den=4+seed%6; num=den*(2+seed%4)
        statement=(f"Reduce the fraction {num}/{den*2} to its simplest form." if en else f"Réduire la fraction {num}/{den*2} à sa forme irréductible.")
        g=math.gcd(num,den*2); ans=f"{num//g}/{den*2//g}"
        steps=([f"We find the GCD of {num} and {den*2}: {g}.",f"We divide numerator and denominator by {g}.",f"We conclude: {ans}."] if en else [f"On trouve le PGCD de {num} et {den*2} : {g}.",f"On divise le numérateur et le dénominateur par {g}.",f"On conclut : {ans}."])
    elif family in ("proportion","finance"):
        unit=3+seed%9; qty=2+seed%5; total=unit*qty
        statement=(f"{qty} identical items cost {total} dollars. Find the cost of one item and of {qty+2} items." if en else f"{qty} articles identiques coûtent {total} dollars. Trouver le prix d'un article et de {qty+2} articles.")
        ans=f"{unit} dollars each; {(qty+2)*unit} dollars"
        steps=([f"Unit price = {total} ÷ {qty} = {unit}.",f"Cost of {qty+2} items = {qty+2} × {unit} = {(qty+2)*unit}.",f"We conclude: {ans}."] if en else [f"Prix unitaire = {total} ÷ {qty} = {unit}.",f"Prix de {qty+2} articles = {qty+2} × {unit} = {(qty+2)*unit}.",f"On conclut : {ans}."])
    elif family == "statistics":
        vals=[a,b,a+2,b+1,a+4]
        mean=sum(vals)/len(vals); med=sorted(vals)[2]
        statement=(f"Consider the data: {', '.join(map(str,vals))}. Calculate the mean and the median." if en else f"On considère les données : {', '.join(map(str,vals))}. Calculer la moyenne et la médiane.")
        ans=f"Mean = {mean:g}; median = {med}"
        steps=([f"Sum = {' + '.join(map(str,vals))} = {sum(vals)}.",f"Mean = {sum(vals)}/5 = {mean:g}.",f"Ordered data: {', '.join(map(str,sorted(vals)))}; median = {med}.",f"We conclude: {ans}."] if en else [f"Somme = {' + '.join(map(str,vals))} = {sum(vals)}.",f"Moyenne = {sum(vals)}/5 = {mean:g}.",f"Données ordonnées : {', '.join(map(str,sorted(vals)))} ; médiane = {med}.",f"On conclut : {ans}."])
    elif family == "probability":
        red=2+seed%4; blue=3+seed%5; tot=red+blue
        statement=(f"A bag contains {red} red and {blue} blue balls. One ball is chosen at random. Find the probability of choosing a red ball." if en else f"Un sac contient {red} boules rouges et {blue} boules bleues. On tire une boule au hasard. Calculer la probabilité d'obtenir une boule rouge.")
        g=math.gcd(red,tot); ans=f"{red}/{tot} = {red//g}/{tot//g}"
        steps=([f"Favourable outcomes = {red}; total outcomes = {tot}.",f"P(red) = {red}/{tot} = {red/tot:.3f}.",f"We conclude: {ans}."] if en else [f"Cas favorables = {red} ; cas possibles = {tot}.",f"P(rouge) = {red}/{tot} = {red/tot:.3f}.",f"On conclut : {ans}."])
    elif family == "sequence":
        u1=2+seed%6; r=2+seed%4
        statement=(f"An arithmetic sequence has first term u₁ = {u1} and common difference r = {r}. Find u₅ and give the general term uₙ." if en else f"Une suite arithmétique a pour premier terme u₁ = {u1} et raison r = {r}. Calculer u₅ et donner le terme général uₙ.")
        ans=f"uₙ = {u1} + (n−1)×{r}; u₅ = {u1+4*r}"
        steps=([f"uₙ = u₁ + (n−1)r = {u1} + (n−1)×{r}.",f"u₅ = {u1} + 4×{r} = {u1+4*r}.",f"We conclude: {ans}."] if en else [f"uₙ = u₁ + (n−1)r = {u1} + (n−1)×{r}.",f"u₅ = {u1} + 4×{r} = {u1+4*r}.",f"On conclut : {ans}."])
    elif family == "antiderivative":
        m=2+seed%5; c=1+seed%6; value=2+seed%5
        statement=(f"Find an antiderivative F of f(x)={m}x+{c} such that F(0)={value}." if en else f"Déterminer une primitive F de f(x)={m}x+{c} telle que F(0)={value}.")
        ans=f"F(x)=({m}/2)x²+{c}x+{value}"
        steps=([f"Integrate term by term: F(x)=({m}/2)x²+{c}x+C.",f"Use F(0)={value}: C={value}.",f"Differentiate to verify: F′(x)={m}x+{c}=f(x).",f"We conclude: {ans}."] if en else [f"On intègre terme à terme : F(x)=({m}/2)x²+{c}x+C.",f"On utilise F(0)={value} : C={value}.",f"Vérification : F′(x)={m}x+{c}=f(x).",f"On conclut : {ans}."])
    elif family == "derivative":
        m=2+seed%5; c=1+seed%7
        statement=(f"Let f(x) = {m}x² + {c}x. Find f′(x) and f′(1)." if en else f"Soit f(x) = {m}x² + {c}x. Déterminer f′(x) et f′(1).")
        ans=f"f′(x) = {2*m}x + {c}; f′(1) = {2*m+c}"
        steps=([f"Using (x²)′=2x and (x)′=1: f′(x)={2*m}x+{c}.",f"f′(1)={2*m}+{c}={2*m+c}.",f"We conclude: {ans}."] if en else [f"En utilisant (x²)′=2x et (x)′=1 : f′(x)={2*m}x+{c}.",f"f′(1)={2*m}+{c}={2*m+c}.",f"On conclut : {ans}."])
    elif family == "quadratic":
        r1=1+seed%5; r2=2+seed%4
        statement=(f"Consider f(x)=(x−{r1})(x+{r2}). Expand the expression and find its roots." if en else f"Soit f(x)=(x−{r1})(x+{r2}). Développer et déterminer ses racines.")
        ans=f"f(x)=x²+{r2-r1}x−{r1*r2}; roots: {r1}, −{r2}"
        steps=([f"Expand: x² + {r2}x − {r1}x − {r1*r2}.",f"Collect terms: x² + {r2-r1}x − {r1*r2}.",f"From the factorised form, roots are {r1} and −{r2}.",f"We conclude: {ans}."] if en else [f"Développer : x² + {r2}x − {r1}x − {r1*r2}.",f"Réduire : x² + {r2-r1}x − {r1*r2}.",f"La forme factorisée donne les racines {r1} et −{r2}.",f"On conclut : {ans}."])
    elif family == "pythagoras":
        x=3+seed%5; y=4+seed%5; h=math.sqrt(x*x+y*y)
        statement=(f"A right triangle has perpendicular sides {x} cm and {y} cm. Find the hypotenuse." if en else f"Un triangle rectangle a des côtés perpendiculaires de {x} cm et {y} cm. Calculer l'hypoténuse.")
        ans=f"√({x*x}+{y*y}) = √{x*x+y*y} = {h:g} cm"
        steps=([f"By Pythagoras: c² = {x}² + {y}².",f"c² = {x*x+y*y}; c = √{x*x+y*y} = {h:g} cm.",f"We conclude: {ans}."] if en else [f"D'après Pythagore : c² = {x}² + {y}².",f"c² = {x*x+y*y} ; c = √{x*x+y*y} = {h:g} cm.",f"On conclut : {ans}."])
    elif family == "trig":
        statement=("In a right triangle, the opposite side to angle θ is 3 cm and the hypotenuse is 5 cm. Find sin θ." if en else "Dans un triangle rectangle, le côté opposé à l'angle θ mesure 3 cm et l'hypoténuse 5 cm. Calculer sin θ.")
        ans="sin θ = 3/5 = 0.6"
        steps=(["We write: sin θ = opposite side / hypotenuse.","We substitute: sin θ = 3/5.","We calculate: sin θ = 0.6.","We conclude: sin θ = 0.6."] if en else ["On écrit : sin θ = côté opposé / hypoténuse.","On remplace : sin θ = 3/5.","On calcule : sin θ = 0,6.","On conclut : sin θ = 0,6."])
    elif family == "coordinate":
        x1,y1,x2,y2=1+seed%4,2+seed%5,5+seed%4,6+seed%5
        statement=(f"Given A({x1},{y1}) and B({x2},{y2}), find the coordinates of the midpoint of [AB]." if en else f"Soient A({x1},{y1}) et B({x2},{y2}). Déterminer les coordonnées du milieu de [AB].")
        ans=f"M(({x1+x2}/2),({y1+y2}/2)) = ({(x1+x2)/2:g},{(y1+y2)/2:g})"
        steps=([f"M = ((xA+xB)/2 ; (yA+yB)/2).",f"M = (({x1}+{x2})/2 ; ({y1}+{y2})/2).",f"We conclude: {ans}."] if en else [f"M = ((xA+xB)/2 ; (yA+yB)/2).",f"M = (({x1}+{x2})/2 ; ({y1}+{y2})/2).",f"On conclut : {ans}."])
    elif family == "vector":
        statement=("Let u=(2,3) and v=(4,−1). Calculate the scalar product u·v." if en else "Soient u=(2,3) et v=(4,−1). Calculer le produit scalaire u·v.")
        ans="u·v = 2×4 + 3×(−1) = 5"
        steps=(["We write: u·v = x₁x₂ + y₁y₂.","We substitute: 2×4 + 3×(−1).","We calculate: 8−3=5.","We conclude: u·v=5."] if en else ["On écrit : u·v = x₁x₂ + y₁y₂.","On remplace : 2×4 + 3×(−1).","On calcule : 8−3=5.","On conclut : u·v=5."])
    elif family == "geometry":
        t=topic.lower()
        if "circle" in t or "arc" in t:
            statement=("A circle has radius 4 cm. Calculate its diameter and circumference (use π=3.14)." if en else "Un cercle a un rayon de 4 cm. Calculer son diamètre et sa circonférence (π=3,14).")
            ans="diameter = 8 cm; circumference = 25.12 cm"
            steps=(["d=2r=8 cm.","C=2πr=2×3.14×4=25.12 cm.","We conclude: 8 cm and 25.12 cm."] if en else ["d=2r=8 cm.","C=2πr=2×3,14×4=25,12 cm.","On conclut : 8 cm et 25,12 cm."])
        elif "square" in t:
            statement=("A square has side 6 cm. Find its perimeter and area." if en else "Un carré a un côté de 6 cm. Calculer son périmètre et son aire.")
            ans="perimeter = 24 cm; area = 36 cm²"
            steps=(["P=4×6=24 cm.","A=6²=36 cm².","We conclude: P=24 cm and A=36 cm²."] if en else ["P=4×6=24 cm.","A=6²=36 cm².","On conclut : P=24 cm et A=36 cm²."])
        elif "rectangle" in t:
            statement=("A rectangle has length 8 cm and width 3 cm. Find its perimeter and area." if en else "Un rectangle a une longueur de 8 cm et une largeur de 3 cm. Calculer son périmètre et son aire.")
            ans="perimeter = 22 cm; area = 24 cm²"
            steps=(["P=2(8+3)=22 cm.","A=8×3=24 cm².","We conclude: P=22 cm and A=24 cm²."] if en else ["P=2(8+3)=22 cm.","A=8×3=24 cm².","On conclut : P=22 cm et A=24 cm²."])
        elif "rhombus" in t:
            statement=("A rhombus has diagonals 6 cm and 8 cm. Find its area." if en else "Un losange a des diagonales de 6 cm et 8 cm. Calculer son aire.")
            ans="24 cm²"
            steps=(["A=(d₁×d₂)/2.","A=(6×8)/2=24 cm².","We conclude: 24 cm²."] if en else ["A=(d₁×d₂)/2.","A=(6×8)/2=24 cm².","On conclut : 24 cm²."])
        elif "parallelogram" in t:
            statement=("A parallelogram has base 9 cm and corresponding height 4 cm. Find its area." if en else "Un parallélogramme a une base de 9 cm et une hauteur correspondante de 4 cm. Calculer son aire.")
            ans="36 cm²"
            steps=(["A=base×height.","A=9×4=36 cm².","We conclude: 36 cm²."] if en else ["A=base×hauteur.","A=9×4=36 cm².","On conclut : 36 cm²."])
        elif "angle" in t or "line" in t:
            statement=("Two adjacent angles on a straight line are x and 68°. Find x." if en else "Deux angles adjacents sur une droite mesurent x et 68°. Déterminer x.")
            ans="x=112°"
            steps=(["Angles on a straight line sum to 180°.","x+68=180 ⇒ x=112°.","We conclude: x=112°."] if en else ["Les angles adjacents sur une droite sont supplémentaires.","x+68=180 ⇒ x=112°.","On conclut : x=112°."])
        elif "thales" in t:
            statement=("In triangle ABC, M lies on AB and N on AC, with MN ∥ BC. If AM=3 cm, AB=9 cm and AC=12 cm, find AN." if en else "Dans le triangle ABC, M appartient à AB et N à AC, avec MN ∥ BC. Si AM=3 cm, AB=9 cm et AC=12 cm, calculer AN.")
            ans="AN=4 cm"
            steps=(["By Thales' theorem: AM/AB = AN/AC.","3/9 = AN/12, hence AN=12×3/9=4 cm.","We conclude: AN=4 cm."] if en else ["D'après le théorème de Thalès : AM/AB = AN/AC.","3/9 = AN/12, donc AN=12×3/9=4 cm.","On conclut : AN=4 cm."])
        elif "midpoint" in t:
            statement=("In triangle ABC, M and N are the midpoints of AB and AC. If BC=10 cm, find MN." if en else "Dans le triangle ABC, M et N sont les milieux de AB et AC. Si BC=10 cm, calculer MN.")
            ans="MN=5 cm"
            steps=(["By the midpoint theorem, MN is parallel to BC and MN=BC/2.","MN=10/2=5 cm.","We conclude: MN=5 cm."] if en else ["D'après le théorème des milieux, MN est parallèle à BC et MN=BC/2.","MN=10/2=5 cm.","On conclut : MN=5 cm."])
        elif "congruent" in t:
            statement=("Triangles ABC and DEF have AB=DE=5 cm, AC=DF=7 cm and BC=EF=8 cm. Which congruence criterion applies?" if en else "Les triangles ABC et DEF vérifient AB=DE=5 cm, AC=DF=7 cm et BC=EF=8 cm. Quel critère de congruence s'applique ?")
            ans="SSS (three corresponding sides); the triangles are congruent."
            steps=(["The three pairs of corresponding sides are equal: 5, 7 and 8 cm.","The Side-Side-Side (SSS) criterion applies.","We conclude: the triangles are congruent."] if en else ["Les trois paires de côtés correspondants sont égales : 5, 7 et 8 cm.","Le critère côté-côté-côté (CCC) s'applique.","On conclut : les triangles sont isométriques."])
        elif "similar triangle" in t:
            statement=("Two similar triangles have corresponding sides 4 cm and 10 cm. A second side of the smaller triangle is 6 cm. Find the corresponding side of the larger triangle." if en else "Deux triangles semblables ont des côtés correspondants de 4 cm et 10 cm. Un deuxième côté du petit triangle mesure 6 cm. Calculer le côté correspondant du grand triangle.")
            ans="15 cm"
            steps=(["Scale factor = 10/4 = 2.5.","Corresponding side = 6×2.5=15 cm.","We conclude: 15 cm."] if en else ["Rapport de similitude = 10/4 = 2,5.","Côté correspondant = 6×2,5=15 cm.","On conclut : 15 cm."])
        elif "locus" in t or "perpendicular" in t:
            statement=("Describe the locus of points equidistant from two fixed points A and B." if en else "Décrire le lieu des points équidistants de deux points fixes A et B.")
            ans="The perpendicular bisector of segment [AB]."
            steps=(["By definition, every point on the locus has equal distances to A and B.","The set of such points forms the perpendicular bisector of [AB].","We conclude: the perpendicular bisector of [AB]."] if en else ["Par définition, chaque point du lieu est à égale distance de A et B.","L'ensemble de ces points forme la médiatrice de [AB].","On conclut : la médiatrice de [AB]."])
        else:
            statement=("State and apply one defining property of the geometric figure or theorem named in this lesson, using a labelled sketch." if en else "Énoncer et appliquer une propriété caractéristique de la figure ou du théorème de cette leçon, avec une figure légendée.")
            ans=("The exact property depends on the construction and theorem studied; teacher validation is required." if en else "La propriété exacte dépend de la construction et du théorème étudiés ; validation par l'enseignant requise.")
            steps=([f"Identify the figure/theorem: {topic}.","State its defining property and conditions.","Apply the property to the labelled figure.","Teacher validation is required for the lesson-specific theorem."] if en else [f"Identifier la figure/le théorème : {topic}.","Énoncer sa propriété caractéristique et ses conditions.","Appliquer la propriété à la figure légendée.","La validation de l'enseignant est requise pour ce théorème spécifique."])
    elif family == "function":
        statement=("Let f(x)=2x+3. Calculate f(0), f(2), and solve f(x)=9." if en else "Soit f(x)=2x+3. Calculer f(0), f(2), puis résoudre f(x)=9.")
        ans="f(0)=3; f(2)=7; x=3"
        steps=(["f(0)=2×0+3=3.","f(2)=2×2+3=7.","2x+3=9 ⇒ 2x=6 ⇒ x=3.","We conclude: f(0)=3, f(2)=7, x=3."] if en else ["f(0)=2×0+3=3.","f(2)=2×2+3=7.","2x+3=9 ⇒ 2x=6 ⇒ x=3.","On conclut : f(0)=3, f(2)=7, x=3."])
    elif family == "sets":
        statement=("Let A={1,2,3,4} and B={3,4,5}. Determine A∩B and A∪B." if en else "Soient A={1,2,3,4} et B={3,4,5}. Déterminer A∩B et A∪B.")
        ans="A∩B={3,4}; A∪B={1,2,3,4,5}"
        steps=(["The intersection contains elements common to both sets: {3,4}.","The union contains each element once: {1,2,3,4,5}.","We conclude: A∩B={3,4}; A∪B={1,2,3,4,5}."] if en else ["L'intersection contient les éléments communs : {3,4}.","La réunion contient chaque élément une seule fois : {1,2,3,4,5}.","On conclut : A∩B={3,4} ; A∪B={1,2,3,4,5}."])
    elif family == "complex":
        statement=("For z=3+2i, state its real and imaginary parts and calculate its conjugate." if en else "Pour z=3+2i, donner les parties réelle et imaginaire et calculer son conjugué.")
        ans="Re(z)=3; Im(z)=2; conjugate = 3−2i"
        steps=(["Read the coefficients in z=a+bi.","Re(z)=3 and Im(z)=2.","Change the sign of the imaginary part: conjugate=3−2i.","We conclude: 3, 2, 3−2i."] if en else ["On identifie les coefficients dans z=a+bi.","Re(z)=3 et Im(z)=2.","On change le signe de la partie imaginaire : conjugué=3−2i.","On conclut : 3, 2, 3−2i."])
    elif family == "limit":
        statement=("Evaluate lim(x→2) (3x+1)." if en else "Calculer lim(x→2) (3x+1).")
        ans="7"
        steps=(["The function is continuous (polynomial).","Substitute x=2: 3×2+1=7.","We conclude: the limit is 7."] if en else ["La fonction est polynomiale donc continue.","On remplace x par 2 : 3×2+1=7.","On conclut : la limite vaut 7."])
    elif family == "integral":
        statement=("Calculate the integral ∫₀² 3x² dx." if en else "Calculer l'intégrale ∫₀² 3x² dx.")
        ans="8"
        steps=(["An antiderivative of 3x² is x³.","Evaluate: [x³]₀² = 2³−0³ = 8.","We conclude: the integral is 8."] if en else ["Une primitive de 3x² est x³.","Évaluer : [x³]₀² = 2³−0³ = 8.","On conclut : l'intégrale vaut 8."])
    elif family == "logexp":
        statement=("Solve eˣ=1 and calculate ln(e²)." if en else "Résoudre eˣ=1 et calculer ln(e²).")
        ans="x=0; ln(e²)=2"
        steps=(["eˣ=1=e⁰, hence x=0.","Using ln(eᵃ)=a: ln(e²)=2.","We conclude: x=0 and 2."] if en else ["eˣ=1=e⁰, donc x=0.","En utilisant ln(eᵃ)=a : ln(e²)=2.","On conclut : x=0 et 2."])
    elif family == "real":
        statement=("Simplify √50 and state whether the result is rational or irrational." if en else "Simplifier √50 et préciser si le résultat est rationnel ou irrationnel.")
        ans="5√2, irrational"
        steps=(["√50=√(25×2)=5√2.","√2 is irrational, so 5√2 is irrational.","We conclude: 5√2 is irrational."] if en else ["√50=√(25×2)=5√2.","√2 est irrationnel, donc 5√2 est irrationnel.","On conclut : 5√2 est irrationnel."])
    else:
        statement=(f"For the lesson “{topic}”, state its main theorem or definition and illustrate it with a fully labelled mathematical example." if en else f"Pour la leçon « {topic} », énoncer le théorème ou la définition principale et l'illustrer par un exemple mathématique correctement légendé.")
        ans=("Teacher must validate the theorem/example against the lesson taught." if en else "L'enseignant doit valider le théorème/l'exemple selon la leçon étudiée.")
        steps=([f"Identify the central definition/theorem of {topic}.","State all required conditions.","Give a labelled example and justify each step.","Teacher validation is required for this lesson-specific item."] if en else [f"Identifier la définition/le théorème central de {topic}.","Énoncer toutes les conditions nécessaires.","Donner un exemple légendé et justifier chaque étape.","La validation de l'enseignant est requise pour cet élément spécifique."])
    return statement, steps, ans

def _diagram_for(topic: str):
    t = topic.lower()
    if any(x in t for x in ("triangle", "thales", "midpoint", "pythagoras", "congruent", "similar")):
        return {"type": "triangle", "caption": "Schematic triangle; not to scale"}
    if any(x in t for x in ("circle", "arc")):
        return {"type": "circle", "caption": "Schematic circle; not to scale"}
    if any(x in t for x in ("coordinate", "plotting", "graph", "analytic geometry", "line in")):
        return {"type": "coordinate_plane", "caption": "Coordinate plane; schematic"}
    if any(x in t for x in ("angle", "perpendicular bisector", "locus", "lines")):
        return {"type": "angle", "caption": "Geometric sketch; not to scale"}
    return None


from competitions.gs_benchmark import terminal_gs_item
from competitions.math_blueprints import get_blueprint


def build_offline_assessment(req):
    en=req.language=="en"
    selected=list(req.lessons)
    if not selected:
        raise ValueError("Select at least one lesson.")
    total=float(req.total_marks)
    base=round(total/len(selected),2)
    allocations=[base]*len(selected)
    allocations[-1]=round(total-sum(allocations[:-1]),2)
    questions=[]; solutions=[]; rubric=[]
    for i,topic in enumerate(selected,1):
        mark=allocations[i-1]
        blueprint = get_blueprint(topic)
        if blueprint is None:
            raise ValueError(f"No local mathematics teaching blueprint exists yet for: {topic}. This lesson is blocked rather than generating a misleading question.")
        specialized = terminal_gs_item(topic, req.language) if req.grade == "terminal_gs" else None
        if req.grade == "terminal_gs" and specialized is None:
            raise ValueError(f"No validated offline Terminale GS question template exists yet for: {topic}. This lesson is blocked rather than generating a generic or misleading question.")
        if specialized:
            scale = mark / 5.0
            parts = [dict(part, marks=round(float(part["marks"]) * scale, 2)) for part in specialized["parts"]]
            if parts:
                parts[-1]["marks"] = round(mark - sum(float(p["marks"]) for p in parts[:-1]), 2)
            criteria = [{"criterion":label,"marks":round(float(points) * scale, 2)} for label,points in specialized["criteria"]]
            if criteria:
                criteria[-1]["marks"] = round(mark - sum(float(x["marks"]) for x in criteria[:-1]), 2)
            questions.append({"number":i,"lesson":topic,"title":(f"Question {i}: {topic}" if en else f"Question {i} : {topic}"),"statement":specialized["statement"],"marks":mark,"parts":parts,"diagram":specialized["diagram"],"table":specialized.get("table"),"pedagogical_blueprint":blueprint})
            solution_steps=list(specialized["steps"])
            if solution_steps and solution_steps[-1].lower().startswith(("we conclude:", "on conclut :")):
                solution_steps.pop()
            solutions.append({"number":i,"steps":solution_steps,"final_answer":specialized["answer"]})
            rubric.append({"number":i,"total":mark,"criteria":criteria})
            continue
        statement,steps,answer=_make(topic,req.language,i)
        questions.append({"number":i,"lesson":topic,"title":(f"Question {i}: {topic}" if en else f"Question {i} : {topic}"),"statement":statement,"marks":mark,"parts":[],"diagram":_diagram_for(topic),"pedagogical_blueprint":blueprint})
        solution_steps=list(steps)
        if solution_steps and solution_steps[-1].lower().startswith(("we conclude:", "on conclut :")):
            solution_steps.pop()
        solutions.append({"number":i,"steps":solution_steps,"final_answer":answer})
        criteria=[]
        allocated=0.0
        for j,step in enumerate(steps):
            points=round(mark/len(steps),2) if j<len(steps)-1 else round(mark-allocated,2)
            allocated=round(allocated+points,2)
            criteria.append({"criterion":step,"marks":points})
        rubric.append({"number":i,"total":mark,"criteria":criteria})
    title=("Mathematics Training Competition" if en else "Épreuve d'entraînement de mathématiques")
    grade_labels={"g7":"Grade 7","g8":"Grade 8","g9":"Grade 9 / EB9","g10":"Grade 10","g11_lh":"Grade 11 — Literary","terminal_gs":"Terminale — General Sciences","terminal_ls":"Terminale — Life Sciences","terminal_se":"Terminale — Economics & Sociology","terminal_lh":"Terminale — Literature & Humanities"}
    note=("Training draft generated locally from deterministic question templates. The preliminary lesson map is not official curriculum evidence; teacher review is required." if en else "Sujet d'entraînement généré localement à partir de modèles déterministes. La liste préliminaire des leçons ne constitue pas une preuve du programme officiel ; validation par l'enseignant requise.")
    return {"title":title,"grade_label":grade_labels.get(req.grade,req.grade),"curriculum_status":"teacher_review_required","curriculum_note":note,"sources":[],"questions":questions,"solutions":solutions,"rubric":rubric,"request":req.model_dump(),"quality_gate":{"question_solution_rubric_alignment":True,"marks_total":total,"curriculum_verified":False,"generator":"offline-deterministic","status":"limited_offline_template","semantic_review":"No AI model is configured; this is a deterministic local question template guided by a lesson-domain teaching blueprint. It has not received independent mathematical review.","local_blueprints_attached":len(questions),"local_blueprint_status":"instructional guidance only; not official curriculum evidence"}}
