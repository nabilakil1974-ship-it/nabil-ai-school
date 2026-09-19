"""Add real, editable OOXML Word footnotes for researcher-placed [FN:n] markers.

Only references explicitly supplied by the researcher can become notes. The
notes are labeled researcher-supplied/unverified; nothing is silently cited.
"""
from __future__ import annotations

import io
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
ET.register_namespace("w", W)
MARK = re.compile(r"\[FN:(\d{1,3})\]")
FOOTNOTE_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"
FOOTNOTE_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"


def _w(name: str) -> str:
    return f"{{{W}}}{name}"


def attach_researcher_footnotes(docx_bytes: bytes, bibliography: str) -> bytes:
    """Insert footnotes only for [FN:1]-style markers with a supplied source line.

    Unknown IDs are left in the manuscript as visible markers; never invent an
    author/title or silently bind an unmatched number to the wrong reference.
    """
    refs = [line.strip() for line in bibliography.splitlines() if line.strip()]
    if not refs or not MARK.search(_read_document(docx_bytes)):
        return docx_bytes

    with ZipFile(io.BytesIO(docx_bytes), "r") as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        footnotes = ET.Element(_w("footnotes"))
        used = set()
        for kind, number, symbol in (
            ("separator", "-1", "separator"),
            ("continuationSeparator", "0", "continuationSeparator"),
        ):
            f = ET.SubElement(footnotes, _w("footnote"),
                              {_w("type"): kind, _w("id"): number})
            p = ET.SubElement(f, _w("p"))
            run = ET.SubElement(p, _w("r"))
            ET.SubElement(run, _w(symbol))

        for paragraph in document.iter(_w("p")):
            for run in list(paragraph.findall(_w("r"))):
                for node in list(run.findall(_w("t"))):
                    text = node.text or ""
                    matches = list(MARK.finditer(text))
                    if not matches:
                        continue
                    # One run with split plain text and genuine footnoteReference
                    # elements in the correct reading order.
                    parent_index = list(paragraph).index(run) + 1
                    node.text = text[:matches[0].start()]
                    for position, match in enumerate(matches):
                        number = int(match.group(1))
                        marker = match.group(0)
                        if 1 <= number <= len(refs):
                            used.add(number)
                            reference_run = ET.Element(_w("r"))
                            rpr = ET.SubElement(reference_run, _w("rPr"))
                            ET.SubElement(rpr, _w("rStyle"), {_w("val"): "FootnoteReference"})
                            ET.SubElement(reference_run, _w("footnoteReference"),
                                          {_w("id"): str(number)})
                            paragraph.insert(parent_index, reference_run)
                            parent_index += 1
                            continuation = text[match.end():matches[position + 1].start()
                                                if position + 1 < len(matches) else len(text)]
                        else:
                            continuation = marker + text[match.end():matches[position + 1].start()
                                                         if position + 1 < len(matches) else len(text)]
                        if continuation:
                            plain_run = ET.Element(_w("r"))
                            ET.SubElement(plain_run, _w("t")).text = continuation
                            paragraph.insert(parent_index, plain_run)
                            parent_index += 1

        if not used:
            return docx_bytes

        for number in sorted(used):
            footnote = ET.SubElement(footnotes, _w("footnote"), {_w("id"): str(number)})
            p = ET.SubElement(footnote, _w("p"))
            ppr = ET.SubElement(p, _w("pPr"))
            ET.SubElement(ppr, _w("pStyle"), {_w("val"): "FootnoteText"})
            marker_run = ET.SubElement(p, _w("r"))
            ET.SubElement(marker_run, _w("footnoteRef"))
            text_run = ET.SubElement(p, _w("r"))
            ET.SubElement(text_run, _w("t")).text = (
                refs[number - 1] + " [Researcher-supplied reference; verify before submission.]"
            )

        relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        existing_ids = {rel.attrib.get("Id") for rel in relationships}
        ix = 1
        while f"rId{ix}" in existing_ids:
            ix += 1
        ET.SubElement(relationships, f"{{{R}}}Relationship",
                      {"Id": f"rId{ix}", "Type": FOOTNOTE_TYPE, "Target": "footnotes.xml"})
        types = ET.fromstring(archive.read("[Content_Types].xml"))
        ET.SubElement(types, f"{{{CT}}}Override",
                      {"PartName": "/word/footnotes.xml", "ContentType": FOOTNOTE_CONTENT_TYPE})
        updates = {
            "word/document.xml": ET.tostring(document, encoding="utf-8", xml_declaration=True),
            "word/footnotes.xml": ET.tostring(footnotes, encoding="utf-8", xml_declaration=True),
            "word/_rels/document.xml.rels": ET.tostring(relationships, encoding="utf-8", xml_declaration=True),
            "[Content_Types].xml": ET.tostring(types, encoding="utf-8", xml_declaration=True),
        }
        output = io.BytesIO()
        with ZipFile(output, "w") as result:
            for item in archive.infolist():
                result.writestr(item, updates.pop(item.filename, archive.read(item.filename)))
            for name, value in updates.items():
                result.writestr(name, value)
        return output.getvalue()


def _read_document(docx_bytes: bytes) -> str:
    with ZipFile(io.BytesIO(docx_bytes), "r") as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    return " ".join(node.text or "" for node in root.iter(_w("t")))
