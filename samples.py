"""Invented sample letters used to measure accuracy.
NONE of these are real letters or real people.

Each case has an 'expected' set of deadline dates that we worked out
with Python's date math (never by hand).
"""
from datetime import date, timedelta

NOTICE = date(2026, 10, 1)

CASES = [
    {
        "name": "relative from the letter date",
        "text": "Date of Notice: October 1, 2026\nYou must respond within 30 days.",
        "notice": None, "received": None,
        "expected": {NOTICE + timedelta(days=30)},
        "known_gap": False,
    },
    {
        "name": "absolute date with 'by'",
        "text": "Please return the enclosed form by November 15, 2026.",
        "notice": None, "received": None,
        "expected": {date(2026, 11, 15)},
        "known_gap": False,
    },
    {
        "name": "hearing window from the mailing date",
        "text": "Mailed: 10/05/2026\nIf you disagree, you may request a hearing within 90 days "
                "from the date this notice was mailed.",
        "notice": None, "received": None,
        "expected": {date(2026, 10, 5) + timedelta(days=90)},
        "known_gap": False,
    },
    {
        "name": "two deadlines in one letter",
        "text": "Date of Notice: October 1, 2026\nReturn the form within 10 days. "
                "You have 60 days to appeal this decision.",
        "notice": None, "received": None,
        "expected": {NOTICE + timedelta(days=10), NOTICE + timedelta(days=60)},
        "known_gap": False,
    },
    {
        "name": "nothing to find",
        "text": "Your appointment is on Tuesday. Thank you for your patience.",
        "notice": None, "received": None,
        "expected": set(),
        "known_gap": False,
    },
    {
        "name": "a date with no deadline cue is ignored",
        "text": "Your case was opened on September 3, 2026. We will contact you if we need more information.",
        "notice": None, "received": None,
        "expected": set(),
        "known_gap": False,
    },
    {
        "name": "'prepared by' is not a deadline",
        "text": "This notice was prepared by staff on September 3, 2026.",
        "notice": None, "received": None,
        "expected": set(),
        "known_gap": False,
    },
    {
        "name": "number written as words and digits",
        "text": "Date of Notice: October 1, 2026\nYou must reply within thirty (30) days.",
        "notice": None, "received": None,
        "expected": {NOTICE + timedelta(days=30)},
        "known_gap": False,
    },
    {
        "name": "US numeric date",
        "text": "Documents must arrive no later than 11/20/2026.",
        "notice": None, "received": None,
        "expected": {date(2026, 11, 20)},
        "known_gap": False,
    },
    {
        "name": "ISO date",
        "text": "Payment is due on or before 2026-12-01.",
        "notice": None, "received": None,
        "expected": {date(2026, 12, 1)},
        "known_gap": False,
    },
    {
        "name": "business days skip weekends",
        "text": "Date of notice: October 5, 2026\nSubmit the requested documents within 10 business days.",
        "notice": None, "received": None,
        "expected": {date(2026, 10, 19)},
        "known_gap": False,
    },
    {
        "name": "counts from the date received",
        "text": "Date of Notice: October 1, 2026\nRespond within 10 days of receiving this letter.",
        "notice": None, "received": date(2026, 10, 6),
        "expected": {date(2026, 10, 6) + timedelta(days=10)},
        "known_gap": False,
    },
    {
        "name": "relative deadline, no letter date anywhere",
        "text": "You must respond within 30 days of the date of this notice.",
        "notice": None, "received": None,
        "expected": set(),
        "known_gap": False,
    },
    {
        "name": "letter date typed into the form",
        "text": "You must respond within 30 days of the date of this notice.",
        "notice": NOTICE, "received": None,
        "expected": {NOTICE + timedelta(days=30)},
        "known_gap": False,
    },
    {
        "name": "realistic three-paragraph letter",
        "text": ("COUNTY SERVICES NOTICE\n"
                 "Date of Notice: October 2, 2026\n\n"
                 "Dear Resident,\n\n"
                 "We need more information to keep your file active. Please send proof of\n"
                 "income by October 30, 2026. If we do not receive it, your benefits may\n"
                 "end. You have 90 days from the date of this notice to ask for a hearing.\n\n"
                 "Thank you for your help.\n"),
        "notice": None, "received": None,
        "expected": {date(2026, 10, 30), date(2026, 10, 2) + timedelta(days=90)},
        "known_gap": False,
    },
    {
        "name": "reply and appeal in one sentence",
        "text": "Date of Notice: October 1, 2026\nReply within 10 days and you have 90 days to appeal.",
        "notice": None, "received": None,
        "expected": {NOTICE + timedelta(days=10), NOTICE + timedelta(days=90)},
        "known_gap": False,
    },
    # ---- Known gaps: we expect these to fail today, and we say so out loud ----
    {
        "name": "line break in the middle of a sentence",
        "text": "Date of Notice: October 1, 2026\nYou must respond within\n30 days of the date of this notice.",
        "notice": None, "received": None,
        "expected": {NOTICE + timedelta(days=30)},
        "known_gap": True,
    },
    {
        "name": "date with no year",
        "text": "Date of Notice: October 1, 2026\nPlease respond by March 3.",
        "notice": None, "received": None,
        "expected": {date(2027, 3, 3)},
        "known_gap": True,
    },
    {
        "name": "Spanish letter",
        "text": "Fecha del aviso: 1 de octubre de 2026\nDebe responder dentro de 10 días a partir de la fecha de este aviso.",
        "notice": None, "received": None,
        "expected": {NOTICE + timedelta(days=10)},
        "known_gap": True,
    },
    {
        "name": "appointment date (not a deadline word)",
        "text": "Your phone check-in is on November 4, 2026.",
        "notice": None, "received": None,
        "expected": {date(2026, 11, 4)},
        "known_gap": True,
    },
]