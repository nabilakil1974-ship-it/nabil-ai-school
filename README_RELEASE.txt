NABIL AI RELEASE CANDIDATE — 2026-10-02

FIRST LESSON / GOLDEN PATH:
lesson_id -> local LessonPackage cache -> Google Drive service account -> local cache -> student.
A supplied Golden lesson_id never falls through to RAG/LLM. Opening a published lesson is zero-AI.

PAYMENT:
Whish receipt may be paid from ANY phone. Identity is the NABIL student/account phone written in the payment email.
Every 30 minutes the workflow reads unseen mail sent to paymentnabilai@gmail.com.
Receipt OCR is LOCAL Tesseract only; no AI provider is called.
Auto verification requires: Transaction ID, exact amount, configured receiver phone, success marker, recent date.
An already-used Transaction ID is rejected. Unclear receipts stay unactivated/manual review.
Verified payment receives a signed activation code. Activation marks the transaction activated and adds 30 days.

COUNTDOWN:
subscription_countdown.js reads the server subscription endpoint and displays trial/paid time remaining.
It requires nabil_student_id in localStorage/sessionStorage, matching the existing student_id contract.

IMPORTANT:
No GitHub or Railway write was performed by ChatGPT. Owner uploads these files.
Existing Railway AI keys remain server-side. Never place AI keys in browser JavaScript.
