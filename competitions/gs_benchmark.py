"""Substantive multi-part templates for the Terminale GS comparison benchmark."""
def terminal_gs_item(topic, lang):
    en = lang == "en"
    data = {
      "Derivatives": {
        "statement": ("Let f(x) = x^3 - 3x + 2 and let C_f be its graph." if en else "Soit f(x) = x^3 - 3x + 2 et C_f sa courbe représentative."),
        "parts": ([{"label":"a","statement":"Determine f'(x).","marks":2},{"label":"b","statement":"Calculate f'(1) and interpret it geometrically.","marks":1},{"label":"c","statement":"Find the tangent equation at x = 1.","marks":2}] if en else [{"label":"a","statement":"Déterminer f'(x).","marks":2},{"label":"b","statement":"Calculer f'(1) et interpréter géométriquement.","marks":1},{"label":"c","statement":"Déterminer l'équation de la tangente en x = 1.","marks":2}]),
        "steps": (["We differentiate: f'(x) = 3x^2 - 3.","We substitute x = 1: f'(1) = 3 - 3 = 0; this is the tangent slope.","We calculate f(1) = 1 - 3 + 2 = 0.","The tangent is y = f'(1)(x - 1) + f(1) = 0."] if en else ["On dérive : f'(x) = 3x^2 - 3.","On remplace x par 1 : f'(1) = 3 - 3 = 0 ; c'est le coefficient directeur de la tangente.","On calcule f(1) = 1 - 3 + 2 = 0.","La tangente a pour équation y = f'(1)(x - 1) + f(1) = 0."]),
        "answer": ("f'(x)=3x^2-3; f'(1)=0; tangent: y=0." if en else "f'(x)=3x^2-3 ; f'(1)=0 ; tangente : y=0."),
        "criteria": (["Correct derivative of x^3",0.75,"Correct derivative of -3x and constant",0.5,"Correct expression for f'(x)",0.75,"Correct substitution and value f'(1)",0.5,"Interpretation as tangent slope",0.5,"Correct value f(1)",0.5,"Correct tangent formula",0.75,"Correct final equation",0.75] if en else ["Dérivée correcte de x^3",0.75,"Dérivée correcte de -3x et de la constante",0.5,"Expression correcte de f'(x)",0.75,"Substitution et valeur correcte de f'(1)",0.5,"Interprétation comme coefficient directeur",0.5,"Valeur correcte de f(1)",0.5,"Formule correcte de la tangente",0.75,"Équation finale correcte",0.75])
      },
      "Probability I": {
        "statement": ("A fair six-sided die is rolled once. A is the event 'the score is even' and B is the event 'the score is greater than 4'." if en else "On lance une fois un dé équilibré à six faces. A est l'événement « obtenir un nombre pair » et B « obtenir un nombre supérieur à 4 »."),
        "parts": ([{"label":"a","statement":"Write Ω, A and B.","marks":2},{"label":"b","statement":"Calculate P(A) and P(B).","marks":1},{"label":"c","statement":"Determine A union B and calculate P(A union B).","marks":2}] if en else [{"label":"a","statement":"Écrire Ω, A et B.","marks":2},{"label":"b","statement":"Calculer P(A) et P(B).","marks":1},{"label":"c","statement":"Déterminer A union B et calculer P(A union B).","marks":2}]),
        "steps": (["Ω = {1,2,3,4,5,6}.","A = {2,4,6} and B = {5,6}.","P(A)=3/6=1/2 and P(B)=2/6=1/3.","A union B = {2,4,5,6}, so P(A union B)=4/6=2/3."] if en else ["Ω = {1,2,3,4,5,6}.","A = {2,4,6} et B = {5,6}.","P(A)=3/6=1/2 et P(B)=2/6=1/3.","A union B = {2,4,5,6}, donc P(A union B)=4/6=2/3."]),
        "answer": ("P(A)=1/2; P(B)=1/3; P(A union B)=2/3." if en else "P(A)=1/2 ; P(B)=1/3 ; P(A union B)=2/3."),
        "criteria": (["Correct sample space",1,"Correct event A",0.5,"Correct event B",0.5,"Correct P(A)",0.5,"Correct P(B)",0.5,"Correct union",1,"Correct union probability",1] if en else ["Univers correct",1,"Événement A correct",0.5,"Événement B correct",0.5,"P(A) correcte",0.5,"P(B) correcte",0.5,"Réunion correcte",1,"Probabilité de la réunion correcte",1])
      },
      "Vectors and Coordinate Systems": {
        "statement": ("In an orthonormal coordinate system, A(-1,2) and B(3,5).",""),
        "parts": ([{"label":"a","statement":"Find the coordinates of vector AB.","marks":2},{"label":"b","statement":"Find the midpoint M of [AB].","marks":1},{"label":"c","statement":"Calculate the distance AB.","marks":2}] if en else [{"label":"a","statement":"Déterminer les coordonnées du vecteur AB.","marks":2},{"label":"b","statement":"Déterminer le milieu M de [AB].","marks":1},{"label":"c","statement":"Calculer la distance AB.","marks":2}]),
        "steps": (["AB=(xB-xA,yB-yA)=(3-(-1),5-2)=(4,3).","M=((xA+xB)/2,(yA+yB)/2)=(1,7/2).","AB=sqrt((3+1)^2+(5-2)^2)=sqrt(25)=5."] if en else ["AB=(xB-xA ; yB-yA)=(3-(-1) ; 5-2)=(4 ; 3).","M=((xA+xB)/2 ; (yA+yB)/2)=(1 ; 7/2).","AB=sqrt((3+1)^2+(5-2)^2)=sqrt(25)=5."]),
        "answer": ("AB=(4,3); M(1,7/2); distance AB=5." if en else "AB=(4 ; 3) ; M(1 ; 7/2) ; AB=5."),
        "criteria": (["Correct vector formula",0.75,"Correct substitution",0.5,"Correct vector coordinates",0.75,"Correct midpoint formula",0.5,"Correct midpoint",0.5,"Correct distance formula",0.75,"Correct distance calculation",1.25] if en else ["Formule correcte du vecteur",0.75,"Remplacement correct",0.5,"Coordonnées correctes du vecteur",0.75,"Formule correcte du milieu",0.5,"Milieu correct",0.5,"Formule correcte de la distance",0.75,"Calcul correct de la distance",1.25])
      },
      "Statistics": {
        "statement": ("The table gives the number of books read by students.\nNumber x: 10 | 12 | 14 | 16\nFrequency n: 2 | 3 | 4 | 1" if en else "Le tableau donne le nombre de livres lus par les élèves.\nNombre x : 10 | 12 | 14 | 16\nEffectif n : 2 | 3 | 4 | 1"),
        "parts": ([{"label":"a","statement":"Find the total number of students.","marks":1},{"label":"b","statement":"Calculate the mean.","marks":1.5},{"label":"c","statement":"Determine the median.","marks":1.5},{"label":"d","statement":"State the mode.","marks":1}] if en else [{"label":"a","statement":"Déterminer l'effectif total.","marks":1},{"label":"b","statement":"Calculer la moyenne.","marks":1.5},{"label":"c","statement":"Déterminer la médiane.","marks":1.5},{"label":"d","statement":"Donner le mode.","marks":1}]),
        "steps": (["N=2+3+4+1=10.","Weighted sum=10*2+12*3+14*4+16*1=128.","Mean=128/10=12.8.","The 5th and 6th ordered values are 12 and 14; median=(12+14)/2=13.","The greatest frequency is 4, corresponding to 14; mode=14."] if en else ["N=2+3+4+1=10.","Somme pondérée=10*2+12*3+14*4+16*1=128.","Moyenne=128/10=12,8.","Les 5e et 6e valeurs ordonnées sont 12 et 14 ; médiane=(12+14)/2=13.","L'effectif maximal est 4, associé à 14 ; mode=14."]),
        "answer": ("N=10; mean=12.8; median=13; mode=14." if en else "N=10 ; moyenne=12,8 ; médiane=13 ; mode=14."),
        "criteria": (["Correct total frequency",1,"Correct weighted sum",0.75,"Correct mean",0.75,"Correct central values",0.75,"Correct median",0.75,"Correct mode",1] if en else ["Effectif total correct",1,"Somme pondérée correcte",0.75,"Moyenne correcte",0.75,"Valeurs centrales correctes",0.75,"Médiane correcte",0.75,"Mode correct",1])
      },
      "Quadratic Equations": {
        "statement": ("Consider the equation x^2 - 5x + 6 = 0." if en else "On considère l'équation x^2 - 5x + 6 = 0."),
        "parts": ([{"label":"a","statement":"Calculate the discriminant.","marks":1.5},{"label":"b","statement":"Solve the equation in R.","marks":2},{"label":"c","statement":"Verify both solutions by substitution.","marks":1.5}] if en else [{"label":"a","statement":"Calculer le discriminant.","marks":1.5},{"label":"b","statement":"Résoudre l'équation dans R.","marks":2},{"label":"c","statement":"Vérifier les deux solutions par substitution.","marks":1.5}]),
        "steps": (["a=1, b=-5, c=6, so Δ=b²-4ac=25-24=1.","The roots are x=(5±√1)/2, hence x₁=2 and x₂=3.","Check: 2²-5(2)+6=0 and 3²-5(3)+6=0."] if en else ["a=1, b=-5, c=6, donc Δ=b²-4ac=25-24=1.","Les racines sont x=(5±√1)/2, donc x₁=2 et x₂=3.","Vérification : 2²-5(2)+6=0 et 3²-5(3)+6=0."]),
        "answer": ("S={2,3}." if en else "S={2,3}."),
        "criteria": (["Correct identification of a, b and c",0.5,"Correct discriminant formula and calculation",1,"Correct root formula",1,"Both roots correct",1,"Both substitutions verified",1.5] if en else ["Identification correcte de a, b et c",0.5,"Formule et calcul corrects du discriminant",1,"Formule des racines correcte",1,"Les deux racines correctes",1,"Vérification des deux solutions",1.5])
      },
      "Signs of Quadratic Functions": {
        "statement": ("Let f(x)=x^2-5x+6. Determine its zeros and construct the sign table of f on R." if en else "Soit f(x)=x^2-5x+6. Déterminer ses zéros et dresser le tableau de signe de f sur R."),
        "parts": ([{"label":"a","statement":"Factorize f(x) and determine its zeros.","marks":2},{"label":"b","statement":"Determine the sign of f on each interval.","marks":2},{"label":"c","statement":"Solve f(x) ≤ 0.","marks":1}] if en else [{"label":"a","statement":"Factoriser f(x) et déterminer ses zéros.","marks":2},{"label":"b","statement":"Déterminer le signe de f sur chaque intervalle.","marks":2},{"label":"c","statement":"Résoudre f(x) ≤ 0.","marks":1}]),
        "steps": (["f(x)=(x-2)(x-3), so the zeros are 2 and 3.","The leading coefficient is positive: f is positive on (-∞,2), negative on (2,3), and positive on (3,+∞).","At x=2 and x=3, f(x)=0. Therefore f(x)≤0 on [2,3]."] if en else ["f(x)=(x-2)(x-3), donc les zéros sont 2 et 3.","Le coefficient dominant est positif : f est positive sur (-∞,2), négative sur (2,3), puis positive sur (3,+∞).","En x=2 et x=3, f(x)=0. Donc f(x)≤0 sur [2,3]."]),
        "answer": ("f>0 on (-∞,2)∪(3,+∞), f<0 on (2,3), and f≤0 on [2,3]." if en else "f>0 sur (-∞,2)∪(3,+∞), f<0 sur (2,3), et f≤0 sur [2,3]."),
        "criteria": (["Correct factorization",1,"Correct zeros",1,"Correct sign outside the roots",1,"Correct sign between the roots and at roots",1,"Correct solution interval",1] if en else ["Factorisation correcte",1,"Zéros corrects",1,"Signe correct à l'extérieur des racines",1,"Signe correct entre les racines et aux racines",1,"Intervalle solution correct",1])
      },
      "Probability II": {
        "statement": ("A box contains 3 red and 2 blue balls. Two balls are drawn successively without replacement. Let R₁ mean that the first ball is red and B₂ that the second is blue." if en else "Une urne contient 3 boules rouges et 2 boules bleues. On tire successivement deux boules sans remise. Soit R₁ : « la première boule est rouge » et B₂ : « la deuxième boule est bleue »."),
        "parts": ([{"label":"a","statement":"Calculate P(R₁).","marks":1},{"label":"b","statement":"Calculate P(B₂ | R₁).","marks":1.5},{"label":"c","statement":"Deduce P(R₁ ∩ B₂).","marks":1.5},{"label":"d","statement":"State P(B₂) and justify your answer.","marks":1}] if en else [{"label":"a","statement":"Calculer P(R₁).","marks":1},{"label":"b","statement":"Calculer P(B₂ | R₁).","marks":1.5},{"label":"c","statement":"En déduire P(R₁ ∩ B₂).","marks":1.5},{"label":"d","statement":"Donner P(B₂) et justifier la réponse.","marks":1}]),
        "steps": (["P(R₁)=3/5.","Given R₁, 4 balls remain, including 2 blue: P(B₂|R₁)=2/4=1/2.","P(R₁∩B₂)=P(R₁)P(B₂|R₁)=(3/5)(1/2)=3/10.","By symmetry of the two draw positions, P(B₂)=2/5."] if en else ["P(R₁)=3/5.","Sachant R₁, il reste 4 boules dont 2 bleues : P(B₂|R₁)=2/4=1/2.","P(R₁∩B₂)=P(R₁)P(B₂|R₁)=(3/5)(1/2)=3/10.","Par symétrie des positions de tirage, P(B₂)=2/5."]),
        "answer": ("P(R₁)=3/5; P(B₂|R₁)=1/2; P(R₁∩B₂)=3/10; P(B₂)=2/5." if en else "P(R₁)=3/5 ; P(B₂|R₁)=1/2 ; P(R₁∩B₂)=3/10 ; P(B₂)=2/5."),
        "criteria": (["Correct first-draw probability",1,"Correct conditional sample after a red first draw",1.5,"Correct multiplication rule and joint probability",1.5,"Correct marginal probability with justification",1] if en else ["Probabilité correcte au premier tirage",1,"Univers conditionnel correct après une rouge",1.5,"Règle du produit et probabilité conjointe correctes",1.5,"Probabilité marginale correcte et justifiée",1])
      },
      "Antiderivatives": {
        "statement": ("Find an antiderivative F of f(x)=6x+4 such that F(0)=3." if en else "Déterminer une primitive F de f(x)=6x+4 telle que F(0)=3."),
        "parts": ([{"label":"a","statement":"Determine the general form of an antiderivative of f.","marks":2},{"label":"b","statement":"Use the condition F(0)=3 to determine the constant.","marks":1.5},{"label":"c","statement":"Verify the result by differentiation.","marks":1.5}] if en else [{"label":"a","statement":"Déterminer la forme générale d'une primitive de f.","marks":2},{"label":"b","statement":"Utiliser la condition F(0)=3 pour déterminer la constante.","marks":1.5},{"label":"c","statement":"Vérifier le résultat par dérivation.","marks":1.5}]),
        "steps": (["Integrating term by term gives F(x)=3x²+4x+C.","F(0)=C=3, so C=3.","F(x)=3x²+4x+3 and F'(x)=6x+4=f(x)."] if en else ["Une primitive générale est F(x)=3x²+4x+C.","F(0)=C=3, donc C=3.","F(x)=3x²+4x+3 et F'(x)=6x+4=f(x)."]),
        "answer": ("F(x)=3x²+4x+3." if en else "F(x)=3x²+4x+3."),
        "criteria": (["Correct integration of 6x",1,"Correct integration of 4 and constant C",1,"Correct use of F(0)=3",1.5,"Correct final primitive and derivative check",1.5] if en else ["Primitive correcte de 6x",1,"Primitive correcte de 4 avec constante C",1,"Utilisation correcte de F(0)=3",1.5,"Primitive finale et vérification par dérivation correctes",1.5])
      },
      "Complex Numbers": {
        "statement": ("Let z=2+3i. Calculate z̄, |z|² and z·z̄. Then solve z w = 13 for w." if en else "Soit z=2+3i. Calculer z̄, |z|² et z·z̄. Puis résoudre zw=13 pour w."),
        "parts": ([{"label":"a","statement":"Give the conjugate of z.","marks":1},{"label":"b","statement":"Calculate |z|².","marks":1},{"label":"c","statement":"Calculate z·z̄.","marks":1},{"label":"d","statement":"Determine w from zw=13.","marks":2}] if en else [{"label":"a","statement":"Donner le conjugué de z.","marks":1},{"label":"b","statement":"Calculer |z|².","marks":1},{"label":"c","statement":"Calculer z·z̄.","marks":1},{"label":"d","statement":"Déterminer w sachant zw=13.","marks":2}]),
        "steps": (["The conjugate is z̄=2-3i.","|z|²=2²+3²=13.","z·z̄=(2+3i)(2-3i)=4+9=13.","13/z=13z̄/(z·z̄)=z̄, hence w=2-3i."] if en else ["Le conjugué est z̄=2-3i.","|z|²=2²+3²=13.","z·z̄=(2+3i)(2-3i)=4+9=13.","13/z=13z̄/(z·z̄)=z̄, donc w=2-3i."]),
        "answer": ("z̄=2-3i; |z|²=13; z·z̄=13; w=2-3i." if en else "z̄=2-3i ; |z|²=13 ; z·z̄=13 ; w=2-3i."),
        "criteria": (["Correct conjugate",1,"Correct modulus squared",1,"Correct product with conjugate",1,"Correct division by z using conjugate",1,"Correct value of w",1] if en else ["Conjugué correct",1,"Carré du module correct",1,"Produit par le conjugué correct",1,"Division par z à l'aide du conjugué",1,"Valeur de w correcte",1])
      },
    }
    if topic not in data:
        return None
    item = data[topic]
    statement = item["statement"]
    if isinstance(statement, tuple):
        statement = statement[0] if en else "Dans un repère orthonormé, on considère les points A(-1,2) et B(3,5)."
    flat = item["criteria"]
    criteria = [(flat[i], flat[i+1]) for i in range(0,len(flat),2)]
    return {"statement":statement,"parts":item["parts"],"steps":item["steps"],
            "answer":item["answer"],"criteria":criteria,
            "diagram":({"type":"coordinate_plane","caption":"Coordinate plane; schematic"} if topic=="Vectors and Coordinate Systems" else None)}
