from datetime import date

from flask import Flask, render_template, request

from extractor import analyze

app = Flask(__name__)

MAX_LETTER_CHARS = 20000


def parse_optional_date(text):
    """'2026-10-01' -> date(2026, 10, 1). Empty or invalid text -> None."""
    try:
        return date.fromisoformat((text or "").strip())
    except ValueError:
        return None


def split_around(evidence, matched):
    """Cut the evidence sentence into (before, matched words, after) so the
    matched words can be highlighted. Ignores upper/lower case."""
    index = evidence.lower().find(matched.lower())
    if index == -1:
        return (evidence, "", "")
    end = index + len(matched)
    return (evidence[:index], evidence[index:end], evidence[end:])


@app.template_filter("nice_date")
def nice_date(d):
    """date(2026, 11, 15) -> 'Sunday, November 15, 2026' (no leading zero on the day)"""
    return f"{d.strftime('%A, %B')} {d.day}, {d.year}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_letter():
    letter = request.form.get("letter", "").strip()
    if not letter:
        return render_template("index.html", error="Please paste some letter text first."), 400
    letter = letter[:MAX_LETTER_CHARS]

    notice_date = parse_optional_date(request.form.get("notice_date"))
    received_date = parse_optional_date(request.form.get("received_date"))
    findings = analyze(letter, notice_date=notice_date, received_date=received_date)

    rows = []
    for f in findings:
        before, match, after = split_around(f.evidence, f.matched)
        rows.append({"f": f, "before": before, "match": match, "after": after})

    return render_template(
        "results.html",
        rows=rows,
        letter=letter,
        needs={f.needs for f in findings if f.needs},
        notice_date=notice_date.isoformat() if notice_date else "",
        received_date=received_date.isoformat() if received_date else "",
    )