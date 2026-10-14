from extractor import classify_date
s = "This notice was prepared by staff on September 3, 2026."
print(classify_date(s, s.index("September")))
s = "Return it by September 3, 2026."
print(classify_date(s, s.index("September")))