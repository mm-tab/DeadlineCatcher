from datetime import date, timedelta
from extractor import add_business_days, detect_anchor, analyze

TODAY = date(2026, 10, 9)

def test_monday_plus_ten_business_days():
    # Check this number on a real calendar, not with your own code.
    assert add_business_days(date(2026, 10, 5), 10) == date(2026, 10, 19)

def test_friday_plus_one_is_monday():
    assert add_business_days(date(2026, 10, 9), 1) == date(2026, 10, 12)

def test_saturday_plus_one_is_monday():
    assert add_business_days(date(2026, 10, 10), 1) == date(2026, 10, 12)

def test_zero_days():
    assert add_business_days(date(2026, 10, 9), 0) == date(2026, 10, 9)

def test_never_lands_on_a_weekend():
    for offset in range(14):
        start = date(2026, 10, 1) + timedelta(days=offset)
        for n in range(1, 15):
            assert add_business_days(start, n).weekday() < 5

def test_receipt_anchor():
    assert detect_anchor("Respond within 10 days of receiving this letter.") == ("received", True)

def test_notice_anchor():
    assert detect_anchor("Respond within 30 days of the date of this notice.") == ("notice", True)

def test_unclear_anchor():
    assert detect_anchor("Respond within 30 days.") == ("notice", False)

def test_agency_receiving_is_not_your_receipt():
    s = "If we do not receive your form within 10 days, benefits may end."
    assert detect_anchor(s) == ("notice", False)

def test_received_date_is_used():
    text = "Date of Notice: October 1, 2026\nRespond within 10 days of receiving this letter."
    got = analyze(text, received_date=date(2026, 10, 6), today=TODAY)[0]
    assert got.deadline == date(2026, 10, 6) + timedelta(days=10)

def test_received_anchor_without_date_needs_it():
    text = "Date of Notice: October 1, 2026\nRespond within 10 days of receiving this letter."
    got = analyze(text, today=TODAY)[0]
    assert got.deadline is None and got.needs == "received_date"

def test_business_days_note():
    text = "Date of notice: October 5, 2026\nSubmit documents within 10 business days."
    got = analyze(text, today=TODAY)[0]
    assert got.deadline == date(2026, 10, 19)
    assert "weekdays_only" in got.notes

def test_unclear_anchor_note():
    text = "Date of Notice: October 1, 2026\nRespond within 30 days."
    assert "anchor_unclear" in analyze(text, today=TODAY)[0].notes

def test_past_note():
    assert "past" in analyze("Return it by September 1, 2026.", today=TODAY)[0].notes