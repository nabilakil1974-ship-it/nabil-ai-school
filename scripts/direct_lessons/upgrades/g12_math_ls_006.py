from scripts.direct_lessons.upgrades._invtrig import theory_extras, exercises


def upgrade(m):
    theory_extras(m, "Why a principal range?", "arcsin: worked example", "arccos and arctan", "arccos and arctan", "The cancellation trap")
    m.EXERCISES[:] = exercises()
