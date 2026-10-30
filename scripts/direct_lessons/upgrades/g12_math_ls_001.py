from scripts.direct_lessons.upgrades._systems import theory_extras, exercises


def upgrade(m):
    theory_extras(m, "Three planes", "Infinite family", "Challenge and summary")
    m.EXERCISES[:] = exercises()
