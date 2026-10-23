# tests/test_languages.py
from datetime import date

from app import app
from extractor import analyze
from translations import STR, format_date

TODAY = date(2026, 10, 9)


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_both_languages_have_the_same_keys():
    assert set(STR["en"]) == set(STR["es"])


def test_spanish_page_loads():
    r = client().get("/?lang=es")
    assert r.status_code == 200
    assert "Buscar fechas límite" in r.get_data(as_text=True)


def test_unknown_language_falls_back_to_english():
    r = client().get("/?lang=xx")
    assert r.status_code == 200
    assert "Find deadlines" in r.get_data(as_text=True)


def test_format_date_in_both_languages():
    assert format_date(date(2026, 11, 15), "en") == "Sunday, November 15, 2026"
    assert format_date(date(2026, 11, 15), "es") == "domingo, 15 de noviembre de 2026"


def test_spanish_results_page():
    letter = "Fecha del aviso: 1 de octubre de 2026\nDebe responder dentro de 10 días a partir de la fecha de este aviso."
    r = client().post("/analyze", data={"letter": letter, "lang": "es"})
    html = r.get_data(as_text=True)
    assert "domingo, 11 de octubre de 2026" in html
    assert "Agregar a mi calendario" in html


def test_spanish_letter_with_a_fixed_date():
    got = analyze("Debe devolver el formulario antes del 15 de noviembre de 2026.", today=TODAY)
    assert [f.deadline for f in got] == [date(2026, 11, 15)]
    assert got[0].label == "respond"


def test_spanish_business_days():
    text = "Fecha del aviso: 5 de octubre de 2026\nPresente los documentos dentro de 10 días hábiles."
    got = analyze(text, today=TODAY)
    assert got[0].deadline == date(2026, 10, 19)
    assert "weekdays_only" in got[0].notes