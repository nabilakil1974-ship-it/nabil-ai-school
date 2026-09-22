# NABIL AI — protected Drive lesson integration baseline (2026-09-22)

Owner-approved architecture: ChatGPT authors and verifies each complete interactive lesson from the original official textbook; the finished HTML and source map live in Google Drive. NABIL looks up by grade, subject, lesson title and language, downloads and displays that HTML. Do NOT copy individual lesson HTML into the repository. The existing indexed-PDF AI teaching path is a fallback, not a substitute for the authored Drive HTML.

## First test lesson
- Grade 9 Physics, French title: Conducteurs ohmiques.
- Drive collection folder: 19Y7wVw2hBYG6_aHe6nygXVZmRJXoHvoM
- Preferred bilingual HTML: 10R64fk9N7bjQ8twGBHHaKuznup9YWYIp
- Earlier French-only HTML: 1cZBiHYyCkCfU7yqOka-8GUWPbYi7skrO
- Original textbook EB 09.pdf: 11dqVqafG9zhr1sQzsjD3kxc5thA2DvZC
- The bilingual version is preferred when two files have the same normalized title. Translated English content does not establish independent English-book exercise/page citations.

## Source files and responsibilities
- app/api/routes_interactive_lessons.py: Drive discovery, exact matching, HTML download and /api/interactive-lessons/resolve + /view.
- app/static/nabil_drive_prepared_lesson_v1.js: intercept Start Lesson, embed Drive HTML in iframe, preserve normal fallback if missing.
- app/main.py: registers router and JS.
- app/static/nabil_lesson_worksheet_card_v1.js: generic final card / worksheet CTA for AI-generated full lessons; authored HTML already includes its own final card and worksheet.
- app/static/nabil_worksheet_v1.js: existing dynamic worksheet engine.
- app/services/textbook_page_request.py: exact indexed printed page and exercise retrieval from original Drive PDF.
- app/api/routes_chat.py: full lesson/page/exercise AI fallback.

## Baseline commits (GitHub history, not local-only memory)
- 48107cee5348f16294701ec0f76ce3f563a8f36c — Drive resolver bilingual preference
- f35159ac0bf1cf83ef71838a44f536cd303f4f9a — sandbox the lesson iframe
- The current integration baseline is the commit creating this file. Compare future Claude commits against this file and the source paths above. Do not revert unrelated changes without reviewing diffs.

## Deployment and access requirements
- Railway must deploy the current GitHub main commit successfully.
- Backend service account from GOOGLE_DRIVE_CREDENTIALS_JSON must have viewer access to the collection folder and HTML files; personal OAuth Drive access alone does not grant the Railway service account access.
- Optional env NABIL_INTERACTIVE_LESSONS_FOLDER_ID sets the folder; NABIL_INTERACTIVE_LESSONS_CATALOG_FILE_ID points to a JSON catalog for future multi-folder lesson discovery.
- Test resolve and view for grade=الصف التاسع, subject=فيزياء, lesson=Conducteurs ohmiques; test French/English toggle, diagrams, lab, worksheet and final card on mobile.
- Never report a live pass solely from a successful GitHub commit.
