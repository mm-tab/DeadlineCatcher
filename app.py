from datetime import date

from flask import Flask, Response, render_template, request

from calendar_ics import make_ics
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

ALLOWED_LABELS = {"respond", "appeal", "pay", "deadline"}


@app.route("/calendar", methods=["POST"])
def calendar_file():
    items = []
    for pick in request.form.getlist("pick"):
        try:
            iso_date, label = pick.split("|", 1)
            due = date.fromisoformat(iso_date)
        except ValueError:
            return "Bad request.", 400
        if label not in ALLOWED_LABELS:
            return "Bad request.", 400
        items.append((due, label))

    if not items:
        return "Select at least one deadline.", 400

    return Response(
        make_ics(items),
        mimetype="text/calendar",
        headers={"Content-Disposition": "attachment; filename=deadlines.ics"},
    )

# Allow big form posts (up to 2 MB) so we can cut the letter down to size ourselves.
# Without this, Flask rejects anything over about 500 KB with a 413 error.
app.config["MAX_FORM_MEMORY_SIZE"] = 2_000_000
app.config["MAX_CONTENT_LENGTH"] = 2_000_000


NOTE_TEXT = {
    "weekdays_only": "Counted weekdays only. Holidays are not excluded, so the real date may be later.",
    "anchor_unclear": "The letter does not say what the days count from. We counted from the letter date.",
    "past": "This date has already passed.",
    "year_assumed": "The letter did not give a year, so we used the next time this date comes up.",
    "ambiguous_date": "This date could be month/day or day/month. We read it as month/day.",
}


@app.template_filter("note_text")
def note_text(code):
    """Turn a short note code like 'past' into a sentence a person can read."""
    return NOTE_TEXT.get(code, code)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404