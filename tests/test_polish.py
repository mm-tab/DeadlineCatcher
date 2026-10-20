from datetime import date
from extractor import analyze, find_dates, join_wrapped_lines
from app import app

TODAY = date(2026, 10, 9)

def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_weekdays_warning_is_shown():
    letter = "Date of notice: October 5, 2026\nSubmit documents within 10 business days."
    html = client().post("/analyze", data={"letter": letter}).get_data(as_text=True)
    assert "Counted weekdays only" in html

def test_wrapped_sentence_is_joined():
    assert join_wrapped_lines("You must respond within\n30 days of the date.") == ["You must respond within 30 days of the date."]

def test_field_lines_stay_separate():
    text = "Date of Notice: October 1, 2026\nYou must respond within 30 days."
    assert join_wrapped_lines(text) == ["Date of Notice: October 1, 2026", "You must respond within 30 days."]

def test_blank_line_separates_paragraphs():
    assert join_wrapped_lines("First paragraph without a period\n\nSecond paragraph.") == ["First paragraph without a period", "Second paragraph."]

def test_huge_input_is_capped():
    r = client().post("/analyze", data={"letter": "Return it by November 15, 2026. " * 20000})
    assert r.status_code == 200

def test_bad_date_input_is_ignored():
    r = client().post("/analyze", data={"letter": "Respond within 30 days.", "notice_date": "garbage"})
    assert r.status_code == 200

def test_unknown_page_is_friendly():
    r = client().get("/nope")
    assert r.status_code == 404
    assert "Page not found" in r.get_data(as_text=True)

def test_yearless_date_uses_letter_date_as_reference():
    text = "Date of Notice: October 1, 2026\nPlease respond by March 3."
    got = analyze(text, today=TODAY)[0]
    assert got.deadline == date(2027, 3, 3)
    assert "year_assumed" in got.notes

def test_yearless_date_later_in_the_same_year():
    text = "Date of Notice: October 1, 2026\nPlease respond by October 15."
    assert analyze(text, today=TODAY)[0].deadline == date(2026, 10, 15)

def test_yearless_leap_day_stretch():
    text = "Date of Notice: October 1, 2026\nPlease respond by February 29."
    assert analyze(text, today=TODAY)[0].deadline == date(2028, 2, 29)

def test_day_first_when_first_number_is_over_12():
    assert find_dates("Due 25/12/2026") == [date(2026, 12, 25)]

def test_ambiguous_numeric_date_gets_a_note():
    got = analyze("Return it by 11/12/2026.", today=TODAY)[0]
    assert got.deadline == date(2026, 11, 12)
    assert "ambiguous_date" in got.notes