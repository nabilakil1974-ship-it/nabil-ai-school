# Railway deployment trigger — 2026-09-19

Owner requested an explicit new main-branch push to distinguish GitHub build success from Railway deployment trigger. This commit follows clean student-card code commit `5bbac8a1e6817fcac53365464c96fa54995eb37e` and Work QA handoff `092b03c09028bb619612e5e169adac04945f9bf5`.

Expected Railway behavior when automatic GitHub main deployments are enabled: deployment queued for this new commit, running the current app and displaying standalone figure cards. If no new Railway deployment appears, inspect source branch, autodeploy, paused deploys, GitHub webhook integration, and deployment events; a successful GitHub Action does not by itself deploy to Railway.
