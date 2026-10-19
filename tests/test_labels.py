from extractor import pick_label

def test_labels():
    assert pick_label("You may request a hearing within 90 days.") == "appeal"
    assert pick_label("Payment is due on or before 2026-12-01.") == "pay"
    assert pick_label("Please return the form by November 15, 2026.") == "respond"
    assert pick_label("Something else is due by 2026-12-01.") == "deadline"