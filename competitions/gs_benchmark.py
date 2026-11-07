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
      }
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
