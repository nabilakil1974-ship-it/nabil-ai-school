"""Analyze actual, de-identified survey CSV without fabricating SPSS output.

The statistical report is descriptive. Significance tests require an explicit
research design and validated assumptions; do not infer causality from survey
means. Respondent records are processed in memory and never sent to an LLM.
"""
from __future__ import annotations

import csv
import io
import math
import statistics
from collections import Counter

MAX_UPLOAD = 2_000_000
MAX_ROWS = 15_000
MAX_COLUMNS = 120
LIKERT = {1, 2, 3, 4, 5}


class SurveyDataError(ValueError):
    pass


def _float_score(text: str) -> int | None:
    if not text.strip():
        return None
    try:
        value = float(text.strip())
    except ValueError as exc:
        raise SurveyDataError("Likert answers must be integers 1–5 or blank.") from exc
    if not value.is_integer() or int(value) not in LIKERT:
        raise SurveyDataError("Likert answers must be integers 1–5 or blank.")
    return int(value)


def parse_survey(data: bytes, axes: dict[str, list[str]]):
    if len(data) > MAX_UPLOAD:
        raise SurveyDataError("CSV exceeds 2 MB; upload a smaller de-identified file.")
    try:
        decoded = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise SurveyDataError("CSV must use UTF-8 encoding.") from exc
    rows = csv.DictReader(io.StringIO(decoded, newline=""))
    headers = rows.fieldnames or []
    if not headers or len(headers) > MAX_COLUMNS or len(set(headers)) != len(headers):
        raise SurveyDataError("CSV needs unique column headers (maximum 120).")
    if not axes or len(axes) > 12:
        raise SurveyDataError("Provide 1–12 non-empty questionnaire axes.")
    seen = set()
    for name, cols in axes.items():
        if not name.strip() or not cols or len(cols) > 40:
            raise SurveyDataError("Each axis must contain 1–40 item columns.")
        for col in cols:
            if col not in headers or col in seen:
                raise SurveyDataError("Each survey item must match a unique CSV header.")
            seen.add(col)
    records = []
    for row in rows:
        if len(records) >= MAX_ROWS:
            raise SurveyDataError("Survey exceeds the 15,000-response limit.")
        if None in row:
            raise SurveyDataError("CSV has inconsistent field counts.")
        records.append({col: _float_score(row[col] or "") for col in seen})
    if not records:
        raise SurveyDataError("CSV has no participant responses.")
    return headers, records


def _r(value: float | None, digits: int = 3):
    return round(value, digits) if value is not None and math.isfinite(value) else None


def summarize_survey(data: bytes, axes: dict[str, list[str]]):
    headers, records = parse_survey(data, axes)
    item_rows = []
    axis_rows = []
    for axis, cols in axes.items():
        axis_scores = []
        complete = []
        for record in records:
            values = [record[col] for col in cols]
            if all(v is not None for v in values):
                complete.append(values)
            valid = [v for v in values if v is not None]
            if valid:
                axis_scores.append(statistics.mean(valid))
        for col in cols:
            scores = [record[col] for record in records if record[col] is not None]
            freq = Counter(scores)
            item_rows.append({
                "axis": axis, "item": col, "valid_n": len(scores),
                "missing_n": len(records) - len(scores),
                "mean": _r(statistics.mean(scores)) if scores else None,
                "sd": _r(statistics.stdev(scores)) if len(scores) >= 2 else None,
                **{f"n_{i}": freq[i] for i in range(1, 6)},
            })
        alpha = None
        if len(cols) > 1 and len(complete) > 1:
            totals = [sum(values) for values in complete]
            total_var = statistics.variance(totals)
            if total_var > 0:
                k = len(cols)
                alpha = k / (k - 1) * (
                    1 - sum(statistics.variance([v[i] for v in complete])
                            for i in range(k)) / total_var
                )
        axis_rows.append({
            "axis": axis, "item_count": len(cols),
            "participant_n": len(records), "valid_axis_n": len(axis_scores),
            "complete_case_n": len(complete),
            "mean": _r(statistics.mean(axis_scores)) if axis_scores else None,
            "sd": _r(statistics.stdev(axis_scores)) if len(axis_scores) > 1 else None,
            "cronbach_alpha_complete_cases": _r(alpha),
        })
    return {
        "participant_n": len(records),
        "headers": headers,
        "axes": axis_rows, "items": item_rows,
        "method": "Descriptive statistics; item-wise available cases; axis respondent mean of answered items; alpha uses complete cases only.",
        "warnings": [
            "Only uploaded actual responses are analyzed; no invented participants or p-values.",
            "The observed number of respondents is not proof of a representative sample or statistical power.",
            "Interpret Likert means cautiously and report missing observations and selection bias.",
            "Cronbach alpha is not validity; small samples and reverse-coded items require researcher review.",
            "No raw respondent records are stored or sent to the AI model.",
        ],
    }


def report_markdown(result: dict, language: str = "ar") -> str:
    lines = [
        "## تحليل نتائج الاستبيان — بيانات فعلية" if language == "ar"
        else "## Survey findings — uploaded data",
        f"Respondents (observed N): {result['participant_n']}",
        result["method"],
        "",
        "| Axis | Items | Available N | Complete N | Mean | SD | Cronbach α |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["axes"]:
        shown = lambda v: "—" if v is None else str(v)
        lines.append("| " + " | ".join(map(str, [
            row["axis"], row["item_count"], row["valid_axis_n"],
            row["complete_case_n"], shown(row["mean"]), shown(row["sd"]),
            shown(row["cronbach_alpha_complete_cases"]),
        ])) + " |")
    lines.extend(["", "### Item frequencies (Likert: 1–5)",
                  "| Axis | Item | Valid | Missing | Mean | SD | 1 | 2 | 3 | 4 | 5 |",
                  "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"])
    for row in result["items"]:
        lines.append("| " + " | ".join("—" if value is None else str(value)
            for value in [row["axis"], row["item"], row["valid_n"], row["missing_n"],
            row["mean"], row["sd"], *[row[f"n_{i}"] for i in range(1, 6)]]) + " |")
    lines.extend(["", "### Interpretation / تعليق وتحليل",
       "تصف المتوسطات والانتشارات اتجاهات إجابات هذه العينة فقط؛ "
       "لا تثبت سببًا أو علاقة سببية ولا تمثيلًا للمجتمع الأصلي. "
       "تُراجع المحاور الأعلى والأدنى مع أسئلة البحث والدراسات الموثقة، "
       "ولا يُفسَّر أي معامل ثبات باعتباره دليلًا منفردًا على الصدق.",
       "", "### General conclusion / استنتاج عام وخلاصة",
       "هذه نتائج وصفية للعينة المستجيبة. لا تُستنتج دلالة إحصائية أو "
       "تُقبل فرضية دون اختبار ملائم وتحقيق افتراضاته وتحديد التصميم والعينة.",
       "", "### Limitations", *[f"- {text}" for text in result["warnings"]]])
    return "\n".join(lines)


def tables_csv(result: dict) -> bytes:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["TABLE: AXIS SUMMARY"])
    fields = ["axis", "item_count", "participant_n", "valid_axis_n",
              "complete_case_n", "mean", "sd", "cronbach_alpha_complete_cases"]
    writer.writerow(fields)
    for row in result["axes"]:
        writer.writerow([row[key] for key in fields])
    writer.writerow([])
    writer.writerow(["TABLE: ITEM FREQUENCIES"])
    fields = ["axis", "item", "valid_n", "missing_n", "mean", "sd",
              "n_1", "n_2", "n_3", "n_4", "n_5"]
    writer.writerow(fields)
    for row in result["items"]:
        writer.writerow([row[key] for key in fields])
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def spss_syntax(result: dict, filename: str = "survey.csv") -> str:
    """Portable SPSS script for the SAME selected item columns and frequency/alpha.

    Respondent CSV must remain in the same folder as the syntax, in UTF-8.
    All original fields are read as strings before explicitly recoding items
    to numeric; irrelevant personal fields are not displayed or summarized.
    """
    if '"' in filename or "\n" in filename or "\r" in filename:
        raise SurveyDataError("Unsafe CSV filename.")
    headers = result["headers"]
    mapping = {column: f"v{n}" for n, column in enumerate(headers, 1)}
    selected = {row["item"] for row in result["items"]}
    lines = [
        "* NABIL AI / SPSS — generated syntax for actual uploaded questionnaire.",
        "* Open the CSV with UTF-8 encoding and keep it in the same folder.",
        "* SPSS computes the figures independently; do not present this as an SPSS run.",
        f'GET DATA /TYPE=TXT /FILE="{filename}" /ENCODING="UTF8"',
        " /DELCASE=LINE /DELIMITERS=\",\" /QUALIFIER=' + "'\"'",
        " /ARRANGEMENT=DELIMITED /FIRSTCASE=2",
        " /VARIABLES=",
    ]
    lines.extend(f" {mapping[h]} A255" for h in headers)
    lines += [".", "DATASET NAME ResearchSurvey.", "EXECUTE.",
              "* Original CSV variable mapping (SPSS-safe v1..vN):"]
    for h in headers:
        lines.append(f"* {mapping[h]} = {h.replace(chr(10), ' ').replace(chr(13), ' ')[:120]}")
    for col in headers:
        if col in selected:
            name = mapping[col]
            lines.append(f"COMPUTE {name}_num = NUMBER({name},F8.2).")
            lines.append(f"IF (NOT RANGE({name}_num,1,5)) {name}_num = $SYSMIS.")
    lines.append("EXECUTE.")
    for axis in result["axes"]:
        cols = [mapping[row["item"]] + "_num" for row in result["items"]
                if row["axis"] == axis["axis"]]
        lines.append("* Axis: " + axis["axis"].replace("\n", " ")[:120])
        lines.append("FREQUENCIES VARIABLES=" + " ".join(cols) + " /STATISTICS=MEAN STDDEV.")
        if len(cols) > 1:
            lines.append("RELIABILITY /VARIABLES=" + " ".join(cols) +
                         " /MODEL=ALPHA /MISSING=LISTWISE.")
    return "\n".join(lines) + "\n"
