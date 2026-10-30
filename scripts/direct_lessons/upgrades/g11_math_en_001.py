from scripts.direct_lessons.upgrades._systems import theory_extras, exercises


def upgrade(m):
    theory_extras(m, "Geometric picture", "Three possible outcomes", "Word problem")
    m.EXERCISES[:] = exercises()
