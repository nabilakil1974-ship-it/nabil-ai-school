/* NABIL Classroom — configuration only. */
export const LANG_AR = v => /[\u0600-\u06ff]/.test(String(v || ''));

export const CARD_ROLES = [
  ['prerequisite', /prereq|متطلبات/i, '🧭'],
  ['hook', /hook|مدخل|تهيئة/i, '✨'],
  ['discover', /discover|اكتشف|لاحظ|think|فكّر/i, '🔎'],
  ['concept', /explain|concept|شرح|الفكرة|why|لماذا/i, '📘'],
  ['rule', /rule|definition|theorem|property|قاعدة|تعريف|نظرية|خاصية/i, '📐'],
  ['example', /worked example|example|مثال/i, '🧩'],
  ['solution', /solution|الحل|answer|جواب/i, '✅'],
  ['check', /checkpoint|check|تحقق|سؤال/i, '🎯'],
  ['practice', /practice|exercise|student try|your turn|تمرين|تمارين|دورك|تطبيق/i, '✍️'],
  ['assessment', /assessment|تقييم|challenge|تحدي/i, '🏁'],
  ['visual', /visual|diagram|figure|graph|رسم|شاهد/i, '📊'],
  ['lab', /\bLAB-\d+\b|FINAL MASTER LAB|experiment|lab|manipulat|مختبر|تجربة/i, '🧪'],
  ['summary', /golden card|visual summary|summary|synthesis|الخلاصة|البطاقة|تركيب/i, '🌟']
];

export function getRole(title){
  for(const [r,re,icon] of CARD_ROLES){
    if(re.test(String(title || ''))) return {r,icon};
  }
  return {r:'concept',icon:'📘'};
}
