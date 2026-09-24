# داخل دالة render_master_html في ملف scripts/nabil_lesson_factory.py:

MASTER_STYLES = """
<style>
:root {
  --bg-main: #061325;           /* خلفية عامة داكنة ومريحة للعين */
  --text-main: #f8fafc;         /* نص أبيض ناصع عالي المقروئية */
  --text-muted: #94a3b8;        /* نص فرعي رمادي ناعم */
  --card-bg: #0c1e36;           /* خلفية البطاقات الأساسية */
  --card-border: #1e3a5f;       /* حدود البطاقات */
  
  /* ألوان التمييز الوظيفية المريحة */
  --c-hook-border: #38bdf8;     /* أزرق سماوي للمدخل والأهداف */
  --c-exp-bar: #38bdf8;         /* أزرق للتجربة */
  --c-obs-bar: #fbbf24;         /* عنبري دافئ للملاحظة */
  --c-concl-bar: #34d399;       /* زمردي مشرق للاستنتاج */
  --c-lab-border: #06b6d4;       /* تركواز للمختبر التفاعلي */
  --c-ex-border: #10b981;        /* أخضر واضح لتمارين الكتاب */
  --c-sol-bg: #052e24;          /* خلفية داكنة جداً للحل لضمان تباين الخط */
  --c-sol-text: #ecfdf5;        /* نص أبيض مائل للخضرة ناصع للحل */
  --c-card-gold: #f59e0b;       /* ذهبي دافئ للبطاقة المرجعية */
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg-main);
  color: var(--text-main);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  line-height: 1.65;
  font-size: 16px;
}

header {
  background: linear-gradient(135deg, #0f2744 0%, #034275 100%);
  padding: 16px 22px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  border-bottom: 2px solid var(--c-hook-border);
}
header .bar {
  max-width: 1150px;
  margin: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.source { color: var(--c-obs-bar); font-size: 0.95rem; font-weight: bold; }

nav a {
  color: #ffffff;
  text-decoration: none;
  background: #0b294a;
  border: 1px solid var(--c-hook-border);
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  margin-left: 6px;
  transition: all 0.25s ease;
}
nav a:hover {
  background: var(--c-hook-border);
  color: #061325;
  transform: translateY(-1px);
}

main { max-width: 1150px; margin: auto; padding: 20px 16px; }
h1 { font-size: clamp(1.6rem, 3.5vw, 2.3rem); margin: 0.2em 0; color: #ffffff; font-weight: 800; }
h2 { color: var(--c-hook-border); margin-top: 0; font-size: 1.4rem; }
h3 { color: #bae6fd; font-size: 1.15rem; }

/* بطاقات الدروس مع تنغيم مريح */
.card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 16px;
  padding: 22px;
  margin: 22px 0;
  box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}

/* بطاقة الأهداف */
.card.teacher {
  border-left: 6px solid var(--c-hook-border);
  background: #092038;
}

/* خطوات الشرح العلمي */
.stage-exp {
  border-left: 4px solid var(--c-exp-bar);
  padding: 12px 16px;
  margin: 10px 0;
  background: #0a2544;
  border-radius: 8px;
}
.stage-obs {
  border-left: 4px solid var(--c-obs-bar);
  padding: 12px 16px;
  margin: 10px 0;
  background: #241d08;
  border-radius: 8px;
}
.stage-concl {
  border-left: 4px solid var(--c-concl-bar);
  padding: 12px 16px;
  margin: 10px 0;
  background: #062b21;
  border-radius: 8px;
}

/* الرسوم المتجهة الكبيرة والواضحة */
.figure {
  background: #051424;
  border: 1px solid #1a3d64;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
  text-align: center;
}
.figure svg {
  width: 100%;
  max-width: 650px;
  min-height: 200px;
  height: auto;
  display: block;
  margin: auto;
}
.figure svg text {
  font-family: system-ui, sans-serif;
  font-weight: 600;
  fill: #e2e8f0;
}

/* بطاقات التمارين وحلولها المتباينة */
.exercise {
  background: #0b223c;
  border: 1px solid #1b456f;
  border-left: 5px solid var(--c-ex-border);
  border-radius: 14px;
  padding: 20px;
  margin: 20px 0;
}
.exhead {
  display: flex;
  justify-content: space-between;
  font-weight: bold;
  color: #6ee7b7;
  font-size: 1.05rem;
  border-bottom: 1px solid #1a4268;
  padding-bottom: 10px;
  margin-bottom: 12px;
}
.prompt {
  background: #05182c;
  border-radius: 8px;
  padding: 14px;
  margin: 12px 0;
  font-size: 15.5px;
  color: #f1f5f9;
}
.answer {
  background: var(--c-sol-bg);
  border: 1px solid var(--c-concl-bar);
  color: var(--c-sol-text);
  padding: 14px 18px;
  border-radius: 8px;
  margin-top: 12px;
  font-weight: 500;
}

/* البطاقة المرجعية الشاملة */
.summary {
  border: 2px solid var(--c-card-gold);
  background: #0c1a2d;
  box-shadow: 0 0 25px rgba(245, 158, 11, 0.15);
}
.sc-panel {
  background: #061527;
  border: 1px solid #1c3d63;
  border-radius: 12px;
  padding: 16px;
}

/* طباعة نظيفة بالأبيض والأسود */
@media print {
  body * { visibility: hidden; }
  #printableCard, #printableCard * { visibility: visible; }
  #printableCard {
    position: absolute;
    left: 0;
    top: 0;
    width: 100% !important;
    background: #ffffff !important;
    color: #000000 !important;
    border: 2pt solid #000 !important;
  }
  .sc-panel {
    background: #ffffff !important;
    border: 1pt solid #333 !important;
    color: #000000 !important;
  }
}
</style>
"""
