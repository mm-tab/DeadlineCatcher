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

def test_month_name():
    assert find_dates("Return the form by November 15, 2026.") == [date(2026, 11, 15)]

def test_abbreviation_with_period():
    assert find_dates("Nov. 15, 2026") == [date(2026, 11, 15)]

def test_day_first():
    assert find_dates("15 November 2026") == [date(2026, 11, 15)]

def test_sept_abbreviation():
    assert find_dates("Sept 3, 2026") == [date(2026, 9, 3)]

def test_impossible_month_date():
    assert find_dates("February 30, 2026") == []

def test_may_the_verb():
    assert find_dates("You may request a hearing.") == []

def test_mixed_formats_in_order():
    assert find_dates("October 1, 2026 and 11/20/2026") == [date(2026, 10, 1), date(2026, 11, 20)]

