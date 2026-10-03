/* NABIL Golden Classroom interrupt contract fix v17.
 * Converts the legacy JSON lesson-interrupt request emitted by the reference
 * classroom into the real /api/chat multipart FormData contract.
 * Keeps the renderer's saved card/line resume state untouched.
 */
(()=>{
  'use strict';
  if (window.__NABIL_INTERRUPT_FIX_V17__) return;
  window.__NABIL_INTERRUPT_FIX_V17__ = true;

  const nativeFetch = window.fetch.bind(window);
  const langLabel = code => ({EN:'English',FR:'French',AR:'Arabic'})[String(code||'').toUpperCase()] || String(code||'English');

  function metaFromLessonId(lessonId, payload={}) {
    const lid = String(lessonId || payload.lesson_id || '').trim().toUpperCase();
    const parts = lid.split('-').filter(Boolean);
    const gm = (parts[0] || '').match(/^G(\d{2})$/);
    const grade = String(payload.grade || (gm ? parseInt(gm[1],10) : ''));
    const subject = String(payload.subject || parts[1] || '');
    const langCode = String(payload.language || parts.find(x => ['EN','FR','AR'].includes(x)) || 'EN').toUpperCase();
    return {lid, grade, subject, language: langLabel(langCode)};
  }

  window.fetch = async function(input, init={}) {
    const url = typeof input === 'string' ? input : String(input?.url || '');
    if (url !== '/api/chat' || String(init?.method || 'GET').toUpperCase() !== 'POST') {
      return nativeFetch(input, init);
    }

    const headers = new Headers(init.headers || {});
    const contentType = headers.get('Content-Type') || '';
    if (!contentType.toLowerCase().includes('application/json') || typeof init.body !== 'string') {
      return nativeFetch(input, init);
    }

    let body;
    try { body = JSON.parse(init.body); } catch (_) { return nativeFetch(input, init); }
    if (body?.mode !== 'lesson_interrupt') return nativeFetch(input, init);

    const payload = window.__NABIL_GOLDEN__ || {};
    const m = metaFromLessonId(body.lesson_id, payload);
    const fd = new FormData();
    fd.append('student_id', localStorage.getItem('nabil_student_id') || 'golden_classroom');
    fd.append('activity_mode', 'lesson');
    fd.append('teaching_mode', 'interactive');
    fd.append('grade', m.grade);
    fd.append('subject', m.subject);
    fd.append('lesson', m.lid);
    fd.append('language', m.language);
    fd.append('message', String(body.message || ''));
    if (body.context) fd.append('lesson_interrupt_context', String(body.context));

    const next = {...init, body: fd};
    const nextHeaders = new Headers(init.headers || {});
    nextHeaders.delete('Content-Type');
    next.headers = nextHeaders;
    return nativeFetch(input, next);
  };
})();
