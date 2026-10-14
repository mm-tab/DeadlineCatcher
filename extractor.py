import re 
from datetime import date

MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "sept": 9,
    "october": 10,
    "november": 11,
    "december": 12,
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12
}

months_names = sorted(MONTHS, key=len, reverse=True)
MONTH_PATTERN = '|'.join(months_names)
_month   = rf"({MONTH_PATTERN})"   
_dot     = r"\.?"                  
_space   = r"\s+"                  
_day     = r"(\d{1,2})"            
_ordinal = r"(?:st|nd|rd|th)?"     
_sep     = r",?\s+"                
_year    = r"(\d{4})"              

PATTERN_A = rf"\b{_month}{_dot}{_space}{_day}{_ordinal}{_sep}{_year}\b"
PATTERN_B = rf"\b{_day}{_space}{_month}{_dot}{_sep}{_year}\b"
def make_date(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        return None
def find_date_matches(text):
    results = []

    for match in re.finditer(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", text):
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), match.end(), d))

    for match in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(\d{4}|\d{2})\b", text):
        month = int(match.group(1))
        day = int(match.group(2))
        year = int(match.group(3))
        if year < 100:
            year += 2000
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), match.end(), d))

    for match in re.finditer(PATTERN_A, text, re.IGNORECASE):
        month = MONTHS[match.group(1).lower()]
        day = int(match.group(2))
        year = int(match.group(3))
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), match.end(), d))

    for match in re.finditer(PATTERN_B, text, re.IGNORECASE):
        day = int(match.group(1))
        month = MONTHS[match.group(2).lower()]
        year = int(match.group(3))
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), match.end(), d))

    results.sort()
    return results


def find_dates(text):
    return [d for (start, end, d) in find_date_matches(text)]

ABBREVIATIONS = {
    "dr.", "mr.", "mrs.", "ms.", "no.", "st.", "jr.", "sr.", "vs.",
    "jan.", "feb.", "mar.", "apr.", "jun.", "jul.", "aug.",
    "sep.", "sept.", "oct.", "nov.", "dec.",
}


def split_sentences(text):
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    sentences = []
    for piece in pieces:
        if sentences and sentences[-1].split()[-1].lower() in ABBREVIATIONS:
            # The previous piece ended with an abbreviation: glue this one on.
            sentences[-1] = sentences[-1] + " " + piece
        else:
            sentences.append(piece)
    return sentences

CUE_PATTERN = re.compile(
    r"\b(by|before|no later than|on or before|until|due)\s*:?\s*(the\s+|on\s+)?$",
    re.IGNORECASE,
)


def classify_date(sentence, start):
    window = sentence[max(0, start - 40):start]
    if CUE_PATTERN.search(window):
        return "deadline"
    return "ignore"

def find_absolute_deadlines(text):
    """Return [{"date": ..., "sentence": ...}] for dates that are deadlines."""
    findings = []
    for sentence in split_sentences(text):
        for (start, end, d) in find_date_matches(sentence):
            if classify_date(sentence, start) == "deadline":
                findings.append({"date": d, "sentence": sentence.strip()})
    return findings
    



        
        
