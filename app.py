from datetime import date

from flask import Flask, Response, render_template, request

from calendar_ics import make_ics
from extractor import analyze
from translations import STR, format_date, t

app = Flask(__name__)

MAX_LETTER_CHARS = 20000

# Allow big form posts (up to 2 MB) so we can cut the letter down to size ourselves.
app.config["MAX_FORM_MEMORY_SIZE"] = 2_000_000
app.config["MAX_CONTENT_LENGTH"] = 2_000_000

ALLOWED_LABELS = {"respond", "appeal", "pay", "deadline"}


def get_lang():
    """'en' or 'es', read from ?lang=es in the link or the hidden lang field in a form."""
    lang = request.values.get("lang", "en")
    return lang if lang in STR else "en"


@app.context_processor
def inject_helpers():
    """Everything returned here can be used in every template."""
    lang = get_lang()
    return {
        "lang": lang,
        "t": lambda key: t(key, lang),
        "nice_date": lambda d: format_date(d, lang),
        "note_text": lambda code: t("note_" + code, lang),
    }


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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_letter():
    letter = request.form.get("letter", "").strip()
    if not letter:
        return render_template("index.html", error=t("error_empty", get_lang())), 400
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404