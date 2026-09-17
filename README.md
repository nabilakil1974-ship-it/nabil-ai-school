NABIL AI — MASTER CURRICULUM LINKED

Replace exactly:
1) app/static/chat.html
2) app/static/teacher_assessment.html
3) app/api/routes_chat.py
4) app/static/crdp_master_curriculum_index.json

What changed:
- Lesson page loads crdp_master_curriculum_index.json first.
- Teacher assessment uses the same master index.
- Secondary branch keys are mapped to the combined master grade keys.
- Secondary languages are excluded in the current phase.
- Kindergarten is excluded in the current phase.
- Sociology/economics/history/geography/philosophy are excluded from the current UI scope.
- Assessment rejects lesson titles that are not in the current verified catalog.
- Backend lesson grounding resolves the master catalog before legacy fallback.
- Legacy scientific index remains only an emergency fallback for scopes not present in master.
