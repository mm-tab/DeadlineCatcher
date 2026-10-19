from datetime import date
from calendar_ics import make_ics

TODAY = date(2026, 10, 9)

def test_event_count_with_all_reminders():
    ics = make_ics([(date(2026, 11, 15), "Respond")], today=TODAY)
    assert ics.count("BEGIN:VEVENT") == 4  # due date + 7, 3, and 1 days before

def test_past_reminders_are_skipped():
    ics = make_ics([(date(2026, 10, 11), "Respond")], today=TODAY)
    assert ics.count("BEGIN:VEVENT") == 2  # due date + the Oct 10 reminder

def test_structure_and_line_endings():
    ics = make_ics([(date(2026, 11, 15), "Respond")], today=TODAY)
    assert ics.startswith("BEGIN:VCALENDAR\r\n")
    assert ics.endswith("END:VCALENDAR\r\n")
    assert "VERSION:2.0" in ics
    assert "DTSTART;VALUE=DATE:20261115" in ics
    assert "DTEND;VALUE=DATE:20261116" in ics

def test_reminder_dates():
    ics = make_ics([(date(2026, 11, 15), "Respond")], today=TODAY)
    for expected in ("20261108", "20261112", "20261114"):
        assert f"DTSTART;VALUE=DATE:{expected}" in ics

def test_special_characters_are_escaped():
    ics = make_ics([(date(2026, 11, 15), "Respond, appeal; pay")], today=TODAY)
    assert "Respond\\, appeal\\; pay" in ics

def test_lines_are_75_bytes_or_less():
    ics = make_ics([(date(2026, 11, 15), "é" * 80)], today=TODAY)
    for line in ics.split("\r\n"):
        assert len(line.encode("utf-8")) <= 75

def test_uids_are_unique():
    ics = make_ics([(date(2026, 11, 15), "A")], today=TODAY)
    uids = [l for l in ics.split("\r\n") if l.startswith("UID:")]
    assert len(uids) == len(set(uids))