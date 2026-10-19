from extractor import find_relative

def days_and_flags(sentence):
    return [(d, b) for d, _, b in find_relative(sentence)]

def test_within_digits():
    assert days_and_flags("You must respond within 30 days.") == [(30, False)]

def test_business_days():
    assert days_and_flags("Reply within 10 business days.") == [(10, True)]

def test_have_n_days_to():
    assert days_and_flags("You have 60 days to appeal.") == [(60, False)]

def test_words_and_parentheses():
    assert days_and_flags("Reply within thirty (30) days.") == [(30, False)]

def test_words_only():
    assert days_and_flags("Reply within thirty days.") == [(30, False)]

def test_two_in_one_sentence():
    s = "Reply within 10 days and you have 90 days to appeal."
    assert days_and_flags(s) == [(10, False), (90, False)]

def test_phone_number_is_not_a_deadline():
    assert days_and_flags("Please call us at 555-0100.") == []

def test_matched_text_is_in_the_sentence():
    s = "Reply within 10 days."
    assert all(m in s for _, m, _ in find_relative(s))

def test_have_n_days_from():
    assert days_and_flags("You have 90 days from the date of this notice to ask for a hearing.") == [(90, False)]