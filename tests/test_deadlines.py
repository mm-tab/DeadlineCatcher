from datetime import date
from extractor import find_absolute_deadlines, split_sentences

def dates_of(text):
    return [d["date"] for d in find_absolute_deadlines(text)]

def test_by_cue():
    assert dates_of("Please return the form by November 15, 2026.") == [date(2026, 11, 15)]

def test_no_later_than():
    assert dates_of("Documents must arrive no later than 11/20/2026.") == [date(2026, 11, 20)]

def test_on_or_before():
    assert dates_of("Payment is due on or before 2026-12-01.") == [date(2026, 12, 1)]

def test_prepared_by_is_not_a_deadline():
    assert dates_of("This notice was prepared by staff on September 3, 2026.") == []

def test_plain_past_event_is_ignored():
    assert dates_of("Your case was opened on September 3, 2026.") == []

def test_abbreviations_do_not_split_sentences():
    text = "Dr. Lee mailed it on Oct. 5, 2026. Respond by Oct. 20, 2026."
    assert len(split_sentences(text)) == 2
    assert dates_of(text) == [date(2026, 10, 20)]

def test_evidence_is_the_sentence():
    result = find_absolute_deadlines("Hello. Return it by November 15, 2026. Thanks.")
    assert result[0]["sentence"] == "Return it by November 15, 2026."