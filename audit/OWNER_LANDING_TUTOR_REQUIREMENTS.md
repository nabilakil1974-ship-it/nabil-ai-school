# Open landing tutor — owner acceptance criteria (2026-09-19)

Status: REQUESTED, NOT IMPLEMENTED OR VERIFIED.

The existing blue NABIL robot screen is to be the main home page. Remove the separate welcome and grade-only entry screens. Keep grade/subject/language/lesson selection inside the lesson area, but never require these selections for an open spoken or typed question.

The home screen shall greet the student briefly and let students submit typed questions, record a voice question, and see an answer card with the same lesson/solution layout as the main platform. Voice and text share the same backend question understanding, pedagogical rules, transcription, response context, scientific terminology and synthetic voice configuration. No separate simplified voice engine.

Understand colloquial Lebanese Arabic and mixed French/English subject terms and spelling, but answer in the question's language for open questions: an English request to study or draw a function gets the full correct English function study and graph, without switching to Arabic. French requests likewise. When a learner speaks Arabic about a selected English/French lesson, use accessible conversational Arabic while preserving the textbook scientific terms, unless the learner asks for an entirely English/French answer.

The answer board near the robot must render verified subject-appropriate graphs and diagrams using the SAME renderer as in full and interactive lessons; preserve image-uploaded source diagrams and add valid step-by-step annotations only if the renderer supports them. Cards should be readable on mobile. Do not invent figure coordinates.

Improve first-response latency and provide bounded errors, input and processing indicators. Unify the blue visual style across robot, explanation and figure backgrounds. Retain all textbook grounding and source-integrity rules.

Implementation is not done merely by recording this request. Inspect the actual landing HTML/scripts, implement and commit, then verify the current Railway deployment. Beware the existing large legacy app/static/chat.html and raw JavaScript leaking into DOM.
