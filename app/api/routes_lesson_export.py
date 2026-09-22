"""Export existing lesson cards, not invented lesson content, as PPTX or printable reference."""
import io
import base64
import re
import math
from html import escape
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel, Field
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from bs4 import BeautifulSoup
from app.api.routes_interactive_lessons import _resolve, _service, _download

router = APIRouter(prefix="/lesson-export", tags=["lesson-export"])

class Cards(BaseModel):
    title: str = Field(max_length=200)
    cards: list[str] = Field(min_length=1, max_length=65)
    source: str = Field(default="بطاقات الدرس المعروضة", max_length=200)
    images: list[list[str]] = Field(default_factory=list, max_length=65)

def _plain(text):
    return re.sub(r"\s+", " ", BeautifulSoup(str(text), "html.parser").get_text(" ", strip=True)).strip()[:5000]

def _source_image(tag):
    """Render only figures embedded in the authenticated lesson HTML; no external fetch."""
    src = str(tag.get("src", "")).strip()
    if src.startswith(("data:image/png;base64,", "data:image/jpeg;base64,")):
        return src
    if tag.name == "svg":
        try:
            import cairosvg
            svg = str(tag)
            if len(svg) > 1_000_000:
                return None
            png = cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                                   output_width=1100)
            if len(png) <= 3_000_000:
                return "data:image/png;base64," + base64.b64encode(png).decode("ascii")
        except Exception:
            return None
    return None


def _from_drive(grade, subject, lesson, language):
    item = _resolve(grade, subject, lesson, language)
    html = _download(_service(), item["drive_file_id"]).decode("utf-8-sig")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "button"]):
        tag.decompose()
    heading = soup.find("h1") or soup.title
    title = _plain(heading.get_text(" ", strip=True) if heading else item["lesson"])
    main = soup.find("main") or soup.body or soup
    # Collect top-level teaching cards; do not repeat nested paragraphs as slides.
    nodes = main.select(":scope > section, :scope > article")
    if not nodes:
        nodes = main.select("section.card, article.card, .row")
    if not nodes:
        nodes = main.select("h2, h3, p, li")
    cards, images = [], []
    for node in nodes:
        value = _plain(node.get_text(" ", strip=True))
        figs = [encoded for tag in node.select("img,svg")
                if (encoded := _source_image(tag))][:4]
        if (len(value) >= 20 or figs) and value not in cards:
            cards.append(value)
            images.append(figs)
    if not cards:
        raise HTTPException(422, "الدرس لا يحتوي بطاقات قابلة للاستخراج.")
    return Cards(title=title, cards=cards[:65], images=images[:65],
                 source="الدرس المحضّر في Google Drive")


def _picture_bytes(value):
    """Only inline browser-rendered PNG/JPEG; never fetch arbitrary remote URLs."""
    if not isinstance(value, str) or not re.match(r"^data:image/(?:png|jpeg);base64,", value):
        return None
    try:
        raw = base64.b64decode(value.split(",", 1)[1], validate=True)
        if len(raw) > 3_000_000 or len(raw) < 30:
            return None
        from PIL import Image
        img = Image.open(io.BytesIO(raw))
        img.verify()
        return raw
    except Exception:
        return None


def _pptx(payload):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    palette = [(36, 187, 219), (255, 187, 91), (107, 219, 181),
               (183, 161, 249), (246, 153, 184), (128, 194, 255)]

    def textbox(slide, x, y, w, h, text, size=20, color=(246,250,255),
                bold=False):
        shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(.06)
        tf.margin_top = tf.margin_bottom = Inches(.06)
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor(*color)
        return shape

    def slide(title, body, figures=(), index=0, last=False):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = RGBColor(9, 30, 52)
        accent = palette[index % len(palette)]
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(.4),
                                 Inches(.35), Inches(.11), Inches(6.7))
        bar.fill.solid()
        bar.fill.fore_color.rgb = RGBColor(*accent)
        bar.line.fill.background()
        textbox(s, .72, .37, 11.8, .7, title[:120], 27, accent, True)
        textbox(s, .75, 7.12, 11.9, .2,
                "NABIL AI  •  " + payload.source[:95], 9, (151,190,207))
        good = [raw for value in figures[:4] if (raw := _picture_bytes(value))]
        # Images get a dedicated visual area, rather than shrinking into the text.
        body_w = 6.4 if good else 11.7
        # Keep font legible: distribute lengthy source text over multiple slides.
        textbox(s, .82, 1.36, body_w, 5.55, body,
                23 if len(body)<170 else 20 if len(body)<320
                else 17 if len(body)<500 else 15)
        if good:
            from PIL import Image
            for j, raw in enumerate(good[:2]):
                try:
                    with Image.open(io.BytesIO(raw)) as im:
                        w,h=im.size
                    max_w,max_h=5.0,(2.45 if len(good)>1 else 5.1)
                    scale=min(max_w/w,max_h/h)
                    pw,ph=w*scale,h*scale
                    s.shapes.add_picture(io.BytesIO(raw),
                        Inches(7.65+(max_w-pw)/2),
                        Inches(1.45+j*2.75+(max_h-ph)/2),
                        width=Inches(pw),height=Inches(ph))
                except Exception:
                    continue
        if last:
            textbox(s, .82, 6.65, 11.4, .35,
                    "Reference card • Review / Révision", 13, accent, True)
        return s

    slide(payload.title, payload.source, index=0)
    for i, card in enumerate(payload.cards, 1):
        body = _plain(card)
        figs = payload.images[i-1] if i-1 < len(payload.images) else []
        # Bound content by visual capacity, not arbitrary 1200-character blocks.
        chunk = 260 if figs else 360
        parts = [body[j:j+chunk] for j in range(0,len(body),chunk)] or [""]
        for j, part in enumerate(parts,1):
            slide(payload.title + " · " + str(i) +
                  (f" ({j}/{len(parts)})" if len(parts)>1 else ""),
                  part, figs if j==1 else (), index=i)
    # Dedicated final reference card, editable text, not a screenshot.
    summary = " • ".join(_plain(x)[:100] for x in payload.cards[-4:])
    slide("Final reference card | البطاقة المرجعية",
          summary[:350], index=len(payload.cards)+1, last=True)
    out=io.BytesIO()
    prs.save(out)
    out.seek(0)
    return StreamingResponse(out,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": 'attachment; filename="NABIL_Lesson.pptx"',
                 "Cache-Control":"no-store"})

def _reference(payload):
    blocks = []
    for i, card in enumerate(payload.cards, 1):
        imgs = payload.images[i-1] if i-1 < len(payload.images) else []
        pictures = "".join('<img alt="رسم من الدرس" src="' + escape(value, quote=True) +
                           '" style="display:block;max-width:100%;height:auto;margin:12px auto">'
                           for value in imgs[:3] if _picture_bytes(value))
        blocks.append("<section><h2>بطاقة " + str(i) + "</h2><p>" +
                      escape(_plain(card)) + "</p>" + pictures + "</section>")
    return HTMLResponse('<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' +
        escape(payload.title) + '</title><style>*,*:before,*:after{box-sizing:border-box}body{font:18px Arial;background:#eaf4fa;color:#122b41;max-width:900px;margin:auto;padding:clamp(10px,3vw,20px);overflow-wrap:anywhere}section{background:white;border-right:7px solid #13a4bd;padding:clamp(12px,3vw,18px);margin:15px 0;border-radius:12px;break-inside:avoid}h1{color:#06647a}p{white-space:pre-wrap;line-height:1.8}button{min-height:44px;padding:10px;border-radius:9px}@media print{body{background:white}button{display:none}section{border:1px solid #aaa}}</style><button onclick="print()">🖨️ طباعة / حفظ PDF</button><h1>📘 البطاقة المرجعية — ' +
        escape(payload.title) + '</h1><p>' + escape(payload.source) + '</p>' +
        "".join(blocks) + '</html>', headers={"Cache-Control":"no-store"})

@router.get("/prepared")
def prepared(grade: str, subject: str, lesson: str, language: str="", format: str="pptx"):
    if format not in ("pptx","reference"):
        raise HTTPException(400,"Unsupported format")
    payload=_from_drive(grade,subject,lesson,language)
    return _pptx(payload) if format=="pptx" else _reference(payload)

@router.post("/cards")
def cards(payload: Cards, format: str="pptx"):
    if format not in ("pptx","reference"):
        raise HTTPException(400,"Unsupported format")
    return _pptx(payload) if format=="pptx" else _reference(payload)
