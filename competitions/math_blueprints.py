"""Local mathematics teaching blueprints used by NABIL's offline assessment engine.

These are instructional design guides, not official curriculum evidence. Each catalogue
lesson is mapped to a mathematical domain, observable skills, suitable task forms,
solution checks and common misconceptions. Keep this module dependency-free.
"""

# Explicit lesson-to-domain map. Unknown lessons fail closed instead of falling back
# to an unrelated algebra question.
LESSON_DOMAIN = {
    # Grade 7
    "Powers": "powers", "Prime Numbers": "prime",
    "Congruent Triangles": "congruence", "Signed Numbers (+ and -)": "signed_add",
    "Signed Numbers (× and ÷)": "signed_mult", "Angles and Lines": "angles",
    "Reduce Fractions": "fractions", "Decimal Fractions": "decimals",
    "Locating a Point": "coordinates", "Algebraic Expressions": "algebraic_expressions",
    "Perpendicular Bisectors": "perpendicular_bisector", "Locus": "locus",
    "Proportion": "proportion", "Statistics": "statistics", "Equations": "equations",
    # Grade 8
    "The Circle": "circle", "The Square": "square", "Powers of 10": "powers10",
    "The Rectangle": "rectangle", "Literal Fractions": "literal_fractions",
    "The Rhombus": "rhombus", "Square Roots": "roots",
    "The Parallelogram": "parallelogram", "Remarkable Identities": "identities",
    "Midpoint Theorem": "midpoint_theorem", "Arcs and Angles": "arcs",
    "Pythagoras' Theorem": "pythagoras", "Rational Fractions": "rational_fractions",
    "Right Triangle": "right_triangle", "Inequalities": "inequalities",
    "Plotting in a System": "plotting",
    # Grade 9
    "Real Numbers": "real_numbers", "Lines and Circles": "lines_circles",
    "Thales' Theorem": "thales", "Lines and Coordinate System": "line_coordinates",
    "Analytic Geometry": "analytic_geometry", "Trigonometry": "trigonometry",
    "System of Equations": "systems", "Vectors": "vectors",
    "Similar Triangles": "similarity",
    # Grade 10
    "Statistical Vocabulary": "statistics_vocab", "Statistical Indicators": "statistics_indicators",
    "Sets": "sets", "Powers of Real Numbers": "real_powers", "Order": "order",
    "Absolute Value": "absolute_value", "Coordinate Systems": "coordinate_systems",
    "Lines in Coordinate Planes": "coordinate_lines", "Scalar Product": "scalar_product",
    "Analytic Form of Scalar Product": "scalar_product_analytic",
    "Linear Equations": "linear_equations", "Linear Inequalities": "linear_inequalities",
    "Functions": "functions", "Basic Functions": "basic_functions",
    "Plane Geometry": "plane_geometry", "Graphical Solution": "graphical_solution",
    # Grade 11 LH
    "Quadratic Equations": "quadratic_equations", "Quadratic Functions": "quadratic_functions",
    "Limit Concept": "limit_concept", "Operations on Limits": "limit_operations",
    "Continuity": "continuity", "Derivatives": "derivatives",
    "Applications of Derivatives": "derivative_applications",
    "Variation of Functions": "function_variation", "Permutations": "permutations",
    "Events": "events", "Notion of Probability": "probability",
    "Rules of Probability": "probability_rules", "Arithmetic Sequences": "arithmetic_sequences",
    "Geometric Sequences": "geometric_sequences", "Antiderivatives": "antiderivatives",
    # Terminale GS
    "Signs of Quadratic Functions": "quadratic_signs",
    "Limits of Functions at Infinity": "limits_infinity",
    "Limits of a Function at a Point": "limits_point", "Probability I": "probability_i",
    "Probability II": "probability_ii", "Orthogonality": "orthogonality",
    "Vectors and Coordinate Systems": "vectors_coordinates", "Sequences": "sequences",
    "Trigonometric Equations": "trig_equations", "Trigonometric Formulas": "trig_formulas",
    "Circle": "circle_advanced", "Complex Numbers": "complex_numbers",
    # Terminale LS
    "Continuous Functions on an Interval": "continuous_interval",
    "Inverse Function": "inverse_function",
    "Second and Higher-Order Derivatives": "higher_derivatives",
    "Logarithm": "logarithm", "Exponential Function": "exponential",
    "Combinations": "combinations", "Conditional Probability": "conditional_probability",
    "Random Variable": "random_variable", "Integral": "integral",
    "Methods of Integration": "integration_methods",
    "Applications of Integral Calculus": "integral_applications",
    "Components of the Vector Product": "vector_product",
    "Planes and Lines": "planes_lines",
    "Parallelism and Orthogonality": "parallel_orthogonality",
    "Differential Equations": "differential_equations",
    # Terminale SE
    "Distribution of Two Variables": "two_variable_distribution",
    "Rational Functions": "rational_functions",
    "Functions of Economics": "economic_functions", "Exponential Functions": "exponential",
    "Conditional Probability and Total Probability": "total_probability",
    "Interest": "simple_interest", "Compound Interest": "compound_interest",
    "Annuity": "annuity", "Random Variables": "random_variables",
    # Terminale LH
    "Position Measures of Statistical Data": "position_statistics",
    "Dispersion": "dispersion", "Graphical Interpretation": "graphical_interpretation",
    "Equations and Inequalities": "equations_inequalities",
}

DOMAIN_GUIDES = {
    "powers": ("Apply exponent laws to products, quotients and powers; distinguish zero and negative exponents where taught.", ["simplify an expression", "evaluate a numerical power", "justify the exponent law"], ["rewrite with a common base", "apply the law", "calculate and check"], ["adding bases instead of exponents", "confusing a^m·a^n with (a·a) exponents"]),
    "prime": ("Use divisibility and prime factorisation to classify an integer.", ["test primality", "factor into primes", "use factorisation"], ["test divisors up to the square root", "record repeated prime factors", "reconstruct the product"], ["calling 1 prime", "stopping before all factors are prime"]),
    "signed_add": ("Operate on signed numbers using number-line or additive-inverse reasoning.", ["add signed integers", "subtract signed integers", "explain sign"], ["identify signs", "compare absolute values when signs differ", "verify by inverse operation"], ["adding absolute values when signs differ", "losing the negative sign"]),
    "signed_mult": ("Multiply and divide signed numbers using sign rules and magnitude.", ["determine product/quotient sign", "calculate magnitude", "combine operations"], ["count negative factors", "apply sign rule", "calculate magnitude"], ["assuming every negative result stays negative"]),
    "fractions": ("Create equivalent fractions and reduce to lowest terms.", ["find common factors", "reduce a fraction", "verify irreducibility"], ["find gcd", "divide numerator and denominator by the same nonzero factor", "check gcd is 1"], ["subtracting the same number instead of dividing"]),
    "decimals": ("Represent and calculate with decimal fractions using place value.", ["convert decimal/fraction forms", "compare decimals", "perform decimal operations"], ["align place values", "calculate", "estimate to check"], ["misplacing decimal point"]),
    "proportion": ("Solve proportional relationships with units and a justified scale factor.", ["identify proportional quantities", "find unit rate", "scale up/down"], ["form ratio/table", "find coefficient", "apply and state units"], ["using additive rather than multiplicative change"]),
    "statistics": ("Interpret a data set or frequency table and calculate appropriate indicators.", ["read frequency table", "calculate total/mean/median/mode", "interpret result"], ["compute total frequency", "compute weighted sum", "order/cumulate data for median", "interpret units"], ["unweighted mean for frequency data", "wrong middle position"]),
    "equations": ("Solve an equation while preserving equality and verify the solution.", ["isolate unknown", "use inverse operations", "check by substitution"], ["perform same operation on both sides", "simplify", "substitute in original equation"], ["changing only one side", "sign error when transposing"]),
    "angles": ("Use angle relationships formed by intersecting and parallel lines.", ["identify corresponding/alternate/supplementary angles", "form an equation", "justify relation"], ["name the geometric relation", "write equality or sum", "solve"], ["assuming parallelism without given evidence"]),
    "congruence": ("Establish triangle congruence from sufficient corresponding data.", ["match vertices/sides", "select a valid congruence criterion", "deduce corresponding elements"], ["record given equalities", "verify criterion conditions", "state correspondence"], ["using AAA as a congruence criterion"]),
    "perpendicular_bisector": ("Use the equal-distance locus and perpendicular-bisector properties.", ["identify equidistance", "construct perpendicular bisector", "justify membership"], ["state PA=PB", "use perpendicularity and midpoint", "conclude locus"], ["confusing median with perpendicular bisector"]),
    "locus": ("Describe or construct the set of points satisfying a geometric condition.", ["translate condition into geometry", "identify locus", "justify both directions"], ["interpret distance/angle condition", "identify standard locus", "verify converse"], ["giving a single point instead of a set"]),
    "circle": ("Use circle vocabulary, radii, chords, arcs and angle properties appropriate to the selected lesson.", ["identify centre/radius/chord/arc", "apply a circle property", "calculate or justify"], ["mark relevant elements", "state theorem and conditions", "substitute"], ["confusing radius and diameter"]),
    "square": ("Apply defining properties of a square to perimeter, area, angles and diagonals.", ["identify equal sides/right angles", "calculate perimeter/area", "use diagonal property"], ["select formula/property", "substitute dimensions", "include correct units"], ["using perimeter formula as area"]),
    "rectangle": ("Apply rectangle properties to side lengths, diagonals, perimeter and area.", ["use opposite sides/equal diagonals", "calculate perimeter/area", "justify"], ["identify known dimensions", "choose formula", "calculate with units"], ["assuming all four sides equal"]),
    "rhombus": ("Use equal sides, perpendicular diagonals and area relations of a rhombus.", ["apply side/diagonal properties", "calculate area", "justify"], ["identify diagonals", "select valid formula", "substitute"], ["using rectangle properties without proof"]),
    "parallelogram": ("Use opposite sides/angles and area properties of a parallelogram.", ["identify parallel/equal opposite sides", "calculate area", "justify"], ["identify base and corresponding height", "apply property", "calculate"], ["using slanted side as height"]),
    "pythagoras": ("Apply the converse or theorem of Pythagoras only after establishing the right angle.", ["identify hypotenuse", "calculate a missing side", "test right triangle"], ["state right-angle condition", "write squared relation", "solve and check"], ["choosing wrong hypotenuse", "forgetting positive length"]),
    "thales": ("Apply Thales' theorem with explicit collinearity and parallelism conditions.", ["identify parallel lines", "write corresponding ratios", "solve for length"], ["state conditions", "match corresponding segments", "solve proportion"], ["mixing non-corresponding sides"]),
    "similarity": ("Use similarity ratios and corresponding angles/sides.", ["establish similarity", "find scale factor", "calculate missing length"], ["match vertices", "form consistent ratio", "check scale direction"], ["inverting only one ratio"]),
    "trigonometry": ("Relate trigonometric ratios to sides/angles in the stated geometric setting.", ["choose sine/cosine/tangent", "calculate angle or side", "respect domain/units"], ["identify opposite/adjacent/hypotenuse", "choose ratio", "substitute and evaluate"], ["mixing opposite and adjacent"]),
    "vectors": ("Use vector coordinates and vector operations with consistent orientation.", ["calculate vector coordinates", "combine vectors", "interpret"], ["write coordinate rule", "substitute endpoints/components", "check orientation"], ["reversing endpoint subtraction"]),
    "scalar_product": ("Calculate and interpret scalar products using coordinate or geometric forms.", ["apply dot-product formula", "test orthogonality", "relate to angle"], ["choose valid form", "substitute components", "interpret zero/sign"], ["confusing vector product and scalar product"]),
    "coordinates": ("Read and represent points in a coordinate system.", ["read ordered pairs", "plot points", "calculate midpoint/distance when included"], ["identify axes and scale", "plot x then y", "verify quadrant"], ["swapping x and y"]),
    "functions": ("Interpret a function through its domain, values, representations and properties.", ["evaluate image/preimage", "read graph/table", "state domain"], ["identify input/output", "substitute or read graph", "state conclusion"], ["confusing image with preimage"]),
    "quadratic": ("Analyse a quadratic expression/function through factorisation, discriminant, roots and sign as appropriate.", ["identify coefficients", "factorise or compute discriminant", "solve and interpret"], ["choose method", "show algebra", "verify roots/sign intervals"], ["sign error in discriminant or root formula"]),
    "limits": ("Evaluate limits using valid algebraic transformations and known limit rules.", ["identify indeterminate form", "simplify or compare dominant terms", "state limit"], ["name form", "apply valid transformation", "justify limiting terms"], ["substituting into 0/0 as a value"]),
    "derivatives": ("Differentiate using applicable rules and connect derivative to tangent/variation when requested.", ["apply derivative rules", "evaluate derivative", "interpret"], ["state rule", "differentiate term by term", "substitute and interpret"], ["forgetting chain/product rule where required"]),
    "antiderivatives": ("Find a primitive and use a condition to determine its constant; verify by differentiation.", ["integrate termwise", "include arbitrary constant", "apply initial condition", "differentiate to verify"], ["write general primitive", "use condition", "check derivative"], ["omitting constant", "answering with derivative instead of primitive"]),
    "probability": ("Model a random experiment and calculate probabilities with the correct sample space.", ["define outcomes/events", "calculate probability", "use conditional or total probability if selected"], ["define event", "count or apply rule", "check probability range"], ["assuming independence without evidence"]),
    "sequences": ("Identify sequence type and use recurrence or explicit term formula.", ["recognise arithmetic/geometric pattern", "find term", "derive general term"], ["identify first term and common difference/ratio", "apply formula", "verify term"], ["using arithmetic formula for geometric sequence"]),
    "complex": ("Operate with complex numbers using algebraic form and conjugation.", ["calculate conjugate/modulus", "multiply/divide", "solve equation"], ["expand using i²=-1", "simplify real/imaginary parts", "verify"], ["treating i² as +1"]),
    "sets": ("Use set notation and operations with clearly defined universal sets.", ["represent membership", "union/intersection/complement", "use inclusion relations"], ["define sets", "apply operation", "check membership"], ["confusing union and intersection"]),
    "identities": ("Expand and factorise using the relevant remarkable identities.", ["recognise identity", "expand/factorise", "verify equivalence"], ["match pattern", "substitute terms", "simplify"], ["sign error in middle term"]),
    "roots": ("Simplify square roots using factorisation and state domain constraints.", ["extract perfect-square factors", "compare radicals", "solve simple radical relation"], ["factor radicand", "apply root property under conditions", "check"], ["splitting square root over addition"]),
    "integrals": ("Evaluate integrals using valid antiderivatives and interpret area/accumulation where selected.", ["select integration method", "apply bounds", "interpret result"], ["identify integrand", "integrate", "apply bounds and units"], ["forgetting integration constant for indefinite integral"]),
    "logexp": ("Use logarithm/exponential definitions and laws with domain restrictions.", ["apply laws", "solve equations", "check domain"], ["state domain", "transform using laws", "solve and verify"], ["taking logarithm of nonpositive values"]),
    "geometry3d": ("Reason about lines and planes using incidence, parallelism and orthogonality conditions.", ["identify spatial relations", "use vector/coordinate representation", "justify"], ["translate diagram to conditions", "apply theorem", "state conclusion"], ["assuming a 2D relation proves a 3D relation"]),
    "finance": ("Model interest, annuity or economic change with explicit time periods and rates.", ["identify principal/rate/period", "choose simple/compound model", "interpret units"], ["convert rate and period consistently", "write recurrence/formula", "calculate and interpret"], ["mixing nominal rate and period rate"]),
    "algebra": ("Manipulate algebraic expressions with explicit operations and verification.", ["expand/reduce/factorise", "solve when an equation is given", "verify"], ["preserve equivalence", "collect like terms", "check"], ["combining unlike terms"]),
}

# Topic-specific domain assignment overrides broad word matching.
TOPIC_DOMAIN_OVERRIDES = {
    "Powers": "powers", "Powers of 10": "powers", "Powers of Real Numbers": "powers",
    "Signed Numbers (+ and -)": "signed_add", "Signed Numbers (× and ÷)": "signed_mult",
    "Prime Numbers": "prime", "Congruent Triangles": "congruence",
    "Perpendicular Bisectors": "perpendicular_bisector", "Locus": "locus",
    "Reduce Fractions": "fractions", "Decimal Fractions": "decimals",
    "Literal Fractions": "algebra", "Rational Fractions": "algebra",
    "Remarkable Identities": "identities", "Square Roots": "roots",
    "Pythagoras' Theorem": "pythagoras", "Thales' Theorem": "thales",
    "Midpoint Theorem": "similarity", "Similar Triangles": "similarity",
    "Angles and Lines": "angles", "Arcs and Angles": "circle",
    "Lines and Circles": "circle", "Lines in Coordinate Planes": "coordinates",
    "Lines and Coordinate System": "coordinates", "Plotting in a System": "coordinates",
    "Analytic Geometry": "coordinates", "Graphical Solution": "functions",
    "Scalar Product": "scalar_product", "Analytic Form of Scalar Product": "scalar_product",
    "Vectors": "vectors", "Vectors and Coordinate Systems": "vectors",
    "Orthogonality": "scalar_product", "Parallelism and Orthogonality": "geometry3d",
    "Planes and Lines": "geometry3d", "Components of the Vector Product": "vectors",
    "Quadratic Equations": "quadratic", "Quadratic Functions": "quadratic",
    "Signs of Quadratic Functions": "quadratic", "Limits of Functions at Infinity": "limits",
    "Limits of a Function at a Point": "limits", "Limit Concept": "limits",
    "Operations on Limits": "limits", "Continuity": "limits",
    "Derivatives": "derivatives", "Applications of Derivatives": "derivatives",
    "Second and Higher-Order Derivatives": "derivatives", "Variation of Functions": "derivatives",
    "Antiderivatives": "antiderivatives", "Integral": "integrals",
    "Methods of Integration": "integrals", "Applications of Integral Calculus": "integrals",
    "Probability I": "probability", "Probability II": "probability",
    "Notion of Probability": "probability", "Rules of Probability": "probability",
    "Conditional Probability": "probability", "Conditional Probability and Total Probability": "probability",
    "Permutations": "probability", "Combinations": "probability",
    "Random Variable": "probability", "Random Variables": "probability",
    "Sequences": "sequences", "Arithmetic Sequences": "sequences", "Geometric Sequences": "sequences",
    "Complex Numbers": "complex", "Sets": "sets",
    "Logarithm": "logexp", "Exponential Function": "logexp", "Exponential Functions": "logexp",
    "Interest": "finance", "Compound Interest": "finance", "Annuity": "finance",
    "Functions of Economics": "finance", "Distribution of Two Variables": "statistics",
    "Statistical Vocabulary": "statistics", "Statistical Indicators": "statistics",
    "Position Measures of Statistical Data": "statistics", "Dispersion": "statistics",
    "Graphical Interpretation": "statistics", "The Circle": "circle", "Circle": "circle",
    "The Square": "square", "The Rectangle": "rectangle", "The Rhombus": "rhombus",
    "The Parallelogram": "parallelogram", "Right Triangle": "pythagoras",
}

def get_blueprint(topic: str):
    """Return a stable local teaching profile, or None for an untrained topic."""
    domain = TOPIC_DOMAIN_OVERRIDES.get(topic) or LESSON_DOMAIN.get(topic)
    aliases = {
        "algebraic_expressions": "algebra", "decimal_fractions": "decimals",
        "literal_fractions": "algebra", "rational_fractions": "algebra",
        "real_numbers": "algebra", "order": "algebra", "absolute_value": "algebra",
        "linear_equations": "algebra", "linear_inequalities": "algebra",
        "equations_inequalities": "algebra", "inequalities": "algebra",
        "sets": "sets", "powers10": "powers", "real_powers": "powers",
        "square": "geometry3d", "rectangle": "geometry3d", "rhombus": "geometry3d",
        "parallelogram": "geometry3d", "plane_geometry": "geometry3d",
        "right_triangle": "pythagoras", "lines_circles": "circle",
        "arcs": "circle", "circle_advanced": "circle",
        "line_coordinates": "coordinates", "analytic_geometry": "coordinates",
        "coordinate_systems": "coordinates", "coordinate_lines": "coordinates",
        "plotting": "coordinates", "graphical_solution": "functions",
        "basic_functions": "functions", "inverse_function": "functions",
        "rational_functions": "functions", "economic_functions": "finance",
        "quadratic_equations": "quadratic", "quadratic_functions": "quadratic",
        "quadratic_signs": "quadratic",
        "limit_concept": "limits", "limit_operations": "limits",
        "limits_infinity": "limits", "limits_point": "limits",
        "continuity": "limits", "continuous_interval": "limits",
        "derivative_applications": "derivatives", "function_variation": "derivatives",
        "higher_derivatives": "derivatives",
        "permutations": "probability", "events": "probability",
        "probability_i": "probability", "probability_ii": "probability",
        "conditional_probability": "probability", "total_probability": "probability",
        "combinations": "probability", "random_variable": "probability",
        "random_variables": "probability",
        "arithmetic_sequences": "sequences", "geometric_sequences": "sequences",
        "vectors_coordinates": "vectors", "vector_product": "vectors",
        "orthogonality": "scalar_product", "trig_equations": "trigonometry",
        "trig_formulas": "trigonometry",
        "logarithm": "logexp", "exponential": "logexp",
        "integral": "integrals", "integration_methods": "integrals",
        "integral_applications": "integrals",
        "two_variable_distribution": "statistics", "statistics_vocab": "statistics",
        "statistics_indicators": "statistics", "position_statistics": "statistics",
        "dispersion": "statistics", "graphical_interpretation": "statistics",
        "simple_interest": "finance", "compound_interest": "finance",
        "annuity": "finance", "sets": "sets",
    }
    domain = aliases.get(domain, domain)
    guide = DOMAIN_GUIDES.get(domain)
    if not guide:
        t = topic.lower()
        if "statistic" in t or "dispersion" in t or "position measure" in t or "distribution of two" in t:
            domain = "statistics"
        elif "equation" in t or "inequalit" in t or "system" in t or "expression" in t:
            domain = "algebra"
        elif "fraction" in t:
            domain = "algebra"
        elif "function" in t or "inverse" in t:
            domain = "functions"
        elif "coordinate" in t or "graph" in t or "point" in t:
            domain = "coordinates"
        elif "triangle" in t or "geometry" in t or "line" in t or "plane" in t:
            domain = "geometry3d"
        elif "probab" in t or "event" in t or "permutation" in t or "combination" in t:
            domain = "probability"
        elif "sequence" in t:
            domain = "sequences"
        elif "trigon" in t:
            domain = "trigonometry"
        elif "proportion" in t:
            domain = "proportion"
        elif "power" in t:
            domain = "powers"
        guide = DOMAIN_GUIDES.get(domain)
    if not guide:
        return None
    concept, skills, protocol, errors = guide
    return {
        "domain": domain,
        "learning_focus": concept,
        "observable_skills": list(skills),
        "solution_protocol": list(protocol),
        "common_misconceptions": list(errors),
        "source_status": "local_pedagogical_blueprint_not_official_curriculum",
    }
