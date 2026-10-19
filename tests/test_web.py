# tests/test_web.py
from app import app, split_around, parse_optional_date
from datetime import date

def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_deadline_is_shown():
    r = client().post("/analyze", data={"letter": "Return it by November 15, 2026."})
    assert r.status_code == 200
    assert "November 15, 2026" in r.get_data(as_text=True)

def test_pasted_html_is_escaped():
    r = client().post("/analyze", data={"letter": "Return it by Nov 15, 2026 <script>alert(1)</script>"})
    html = r.get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html

def test_empty_letter_is_friendly():
    r = client().post("/analyze", data={"letter": "   "})
    assert r.status_code == 400
    assert "paste some letter text" in r.get_data(as_text=True).lower()

def test_nothing_found_message():
    r = client().post("/analyze", data={"letter": "Thank you for your patience."})
    assert r.status_code == 200
    assert "No deadlines found" in r.get_data(as_text=True)

def test_split_around():
    assert split_around("Return it by Nov 15, 2026.", "Nov 15, 2026") == ("Return it by ", "Nov 15, 2026", ".")
    assert split_around("abc", "zzz") == ("abc", "", "")

def test_parse_optional_date():
    assert parse_optional_date("") is None
    assert parse_optional_date("2026-10-01") == date(2026, 10, 1)
    assert parse_optional_date("garbage") is None