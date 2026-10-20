from datetime import date, timedelta
import pytest
from extractor import analyze, find_notice_date

TODAY = date(2026, 10, 9)

def test_notice_date_label():
    assert find_notice_date("Date of Notice: October 1, 2026") == date(2026, 10, 1)

def test_mailed_label():
    assert find_notice_date("Mailed: 10/05/2026") == date(2026, 10, 5)

def test_unrelated_date_is_not_the_notice_date():
    assert find_notice_date("Your case was opened on Sept 3, 2026.") is None

def test_relative_uses_notice_date_from_text():
    text = "Date of Notice: October 1, 2026\nYou must respond within 30 days."
    assert analyze(text, today=TODAY)[0].deadline == date(2026, 10, 1) + timedelta(days=30)

def test_relative_without_notice_date_needs_it():
    result = analyze("You must respond within 30 days.", today=TODAY)
    assert result[0].deadline is None
    assert result[0].needs == "notice_date"

def test_provided_notice_date_beats_detected():
    text = "Date of Notice: October 1, 2026\nRespond within 10 days."
    result = analyze(text, notice_date=date(2026, 10, 5), today=TODAY)
    assert result[0].deadline == date(2026, 10, 5) + timedelta(days=10)

def test_sorted_by_date():
    text = "Date of Notice: October 1, 2026\nReturn it by November 15, 2026.\nYou have 60 days to appeal."
    got = [f.deadline for f in analyze(text, today=TODAY)]
    assert got == [date(2026, 11, 15), date(2026, 10, 1) + timedelta(days=60)]

def test_line_break_in_the_middle_of_a_sentence():
    text = "Date of Notice: October 1, 2026\nYou must respond within\n30 days of the date of this notice."
    assert analyze(text, today=TODAY)[0].deadline == date(2026, 10, 1) + timedelta(days=30)