from scripts.direct_lessons.upgrades._invtrig import theory_extras, exercises


def upgrade(m):
    theory_extras(m, "Can sine have an inverse?", "arcsin", "arccos", "arctan", "Exact value and composition")
    m.EXERCISES[:] = exercises()
