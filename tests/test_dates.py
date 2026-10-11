from datetime import date
from extractor import find_dates

def test_iso():
    assert find_dates("Pay by 2026-12-01.") == [date(2026, 12, 1)]

def test_numeric_us():
    assert find_dates("Due 11/20/2026") == [date(2026, 11, 20)]

def test_two_digit_year():
    assert find_dates("Due 11/20/26") == [date(2026, 11, 20)]

def test_no_dates():
    assert find_dates("no dates here") == []

def test_impossible_date():
    assert find_dates("Due 2026-02-30") == []

def test_order_of_appearance():
    assert find_dates("From 2026-01-05 to 2026-01-09") == [date(2026, 1, 5), date(2026, 1, 9)]
