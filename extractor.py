import re
from dataclasses import dataclass, field
from datetime import date, timedelta

@dataclass
class Finding:
    kind: str                        
    label: str                      
    evidence: str                    
    matched: str                     
    deadline: date | None = None    
    needs: str | None = None         
    notes: list = field(default_factory=list)

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
    "dec": 12,
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
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
PATTERN_ES = rf"\b{_day}\s+de\s+{_month}\s+de\s+{_year}\b"
def make_date(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        return None# A month and day with NO year, like "March 3". Only used when we know a reference date.
PATTERN_YEARLESS = rf"\b{_month}{_dot}{_space}{_day}{_ordinal}\b"


def resolve_year(month, day, ref):
    """The first date on or after ref that falls on this month and day.
    resolve_year(3, 3, date(2026, 10, 1)) -> date(2027, 3, 3)"""
    for year in range(ref.year, ref.year + 9):     # 9 years is enough to find a Feb 29
        d = make_date(year, month, day)
        if d is not None and d >= ref:
            return d
    return None


def find_date_details(text, ref=None):
    """Return a sorted list of (start, end, date, notes).
    ref is the date used to guess a missing year. Without it, yearless dates are skipped."""
    results = []

    # ISO: 2026-12-01
    for match in re.finditer(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", text):
        d = make_date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        if d is not None:
            results.append((match.start(), match.end(), d, []))

    # Numeric with slashes: 11/20/2026, 25/12/2026, 11/12/2026
    for match in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(\d{4}|\d{2})\b", text):
        first = int(match.group(1))
        second = int(match.group(2))
        year = int(match.group(3))
        if year < 100:
            year += 2000
        notes = []
        if first > 12:                     # 25/12/2026 can only be day/month
            day, month = first, second
        else:                              # 11/20/2026 is month/day
            month, day = first, second
            if second <= 12 and first != second:
                notes.append("ambiguous_date")   # 11/12 could be either
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), match.end(), d, notes))

    # Month first: November 15, 2026
    for match in re.finditer(PATTERN_A, text, re.IGNORECASE):
        d = make_date(int(match.group(3)), MONTHS[match.group(1).lower()], int(match.group(2)))
        if d is not None:
            results.append((match.start(), match.end(), d, []))

    # Day first: 15 November 2026
    for match in re.finditer(PATTERN_B, text, re.IGNORECASE):
        d = make_date(int(match.group(3)), MONTHS[match.group(2).lower()], int(match.group(1)))
        if d is not None:
            results.append((match.start(), match.end(), d, []))

    # Month and day without a year: March 3
    for match in re.finditer(PATTERN_ES, text, re.IGNORECASE):
        d = make_date(int(match.group(3)), MONTHS[match.group(2).lower()], int(match.group(1)))
        if d is not None:
            results.append((match.start(), match.end(), d, []))
    if ref is not None:
        for match in re.finditer(PATTERN_YEARLESS, text, re.IGNORECASE):
            inside_another = any(s <= match.start() < e for (s, e, _, _) in results)
            if inside_another:             # this is the first half of "March 3, 2027"
                continue
            d = resolve_year(MONTHS[match.group(1).lower()], int(match.group(2)), ref)
            if d is not None:
                results.append((match.start(), match.end(), d, ["year_assumed"]))

    results.sort(key=lambda r: r[0])
    return results


def find_date_matches(text):
    """The old function from Day 4, kept so the older code and tests still work."""
    return [(start, end, d) for (start, end, d, _notes) in find_date_details(text)]


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
    r"\b(by|before|no later than|on or before|until|due"
    r"|antes del?|a m[aá]s tardar|hasta|fecha l[ií]mite)\s*:?\s*(the\s+|on\s+|el\s+)?$",
    re.IGNORECASE,
)


def classify_date(sentence, start):
    window = sentence[max(0, start - 40):start]
    if CUE_PATTERN.search(window):
        return "deadline"
    return "ignore"

def find_absolute_deadlines(text):
    findings = []
    for sentence in split_sentences(text):
        for (start, end, d) in find_date_matches(sentence):
            if classify_date(sentence, start) == "deadline":
                findings.append({"date": d, "sentence": sentence.strip()})
    return findings

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}


def words_to_int(text):
    text = text.strip().lower()
    if text.isdigit():
        return int(text)
    return sum(NUMBER_WORDS[part] for part in re.split(r"[-\s]+", text))

def _alternatives(words):
    return "|".join(sorted(words, key=len, reverse=True))


_units = [w for w, n in NUMBER_WORDS.items() if n < 10]
_tens = [w for w, n in NUMBER_WORDS.items() if n >= 20]
_small = [w for w, n in NUMBER_WORDS.items() if n < 20]

_NUM = (
    rf"(?:\d{{1,3}}"
    rf"|(?:{_alternatives(_tens)})(?:[-\s](?:{_alternatives(_units)}))?"
    rf"|{_alternatives(_small)})"
)
_PAREN = r"(?:\s*\((\d{1,3})\))?"                 
_KIND = r"(business\s+|working\s+|calendar\s+)?"
RELATIVE_WITHIN = rf"\b(?:within|in)\s+({_NUM}){_PAREN}\s+{_KIND}days?\b"
RELATIVE_HAVE = rf"\bhave\s+({_NUM}){_PAREN}\s+{_KIND}days\s+(?:to|from)\b"
RELATIVE_ES = r"\b(?:dentro\s+de|en|tiene)\s+(\d{1,3})\s+d[ií]as(\s+h[aá]biles)?"

def find_relative(sentence):
    found = {}  
    for pattern in (RELATIVE_WITHIN, RELATIVE_HAVE):
        for match in re.finditer(pattern, sentence, re.IGNORECASE):
            if match.group(2):               
                days = int(match.group(2))
            else:
                days = words_to_int(match.group(1))
            kind = (match.group(3) or "").strip().lower()
            is_business = kind in ("business", "working")
            found[match.start()] = (days, match.group(0), is_business)
    for match in re.finditer(RELATIVE_ES, sentence, re.IGNORECASE):
        found[match.start()] = (int(match.group(1)), match.group(0), bool(match.group(2)))
    return [found[start] for start in sorted(found)]

NOTICE_LABEL = re.compile(
    r"\b(date of (this )?notice|notice date|date mailed|mailed( on)?|dated"
    r"|fecha del aviso|fecha de la carta)\s*:?\s*$",
    re.IGNORECASE,
)


def find_notice_date(text):
    for (start, end, d) in find_date_matches(text):
        window = text[max(0, start - 40):start]
        if NOTICE_LABEL.search(window):
            return d
    return None

def sentences_of(text):
    sentences = []
    for paragraph in join_wrapped_lines(text):
        sentences.extend(split_sentences(paragraph))
    return sentences

def analyze(text, notice_date=None, received_date=None, today=None):
    """Return a list of Finding objects, soonest deadline first."""
    today = today or date.today()
    notice = notice_date or find_notice_date(text)
    ref = notice or today          # used to guess a missing year
    findings = []
    for sentence in sentences_of(text):
        evidence = sentence.strip()

        for (start, end, d, notes) in find_date_details(sentence, ref):
            if classify_date(sentence, start) == "deadline":
                findings.append(Finding(
                    kind="absolute", label=pick_label(sentence), evidence=evidence,
                    matched=sentence[start:end], deadline=d, notes=list(notes),
                ))

        for (days, matched, is_business) in find_relative(sentence):
            anchor, is_clear = detect_anchor(sentence)
            if anchor == "received":
                base, missing = received_date, "received_date"
            else:
                base, missing = notice, "notice_date"

            finding = Finding(kind="relative", label=pick_label(sentence),
                              evidence=evidence, matched=matched)
            if base is None:
                finding.needs = missing
            elif is_business:
                finding.deadline = add_business_days(base, days)
            else:
                finding.deadline = base + timedelta(days=days)

            if is_business:
                finding.notes.append("weekdays_only")
            if not is_clear:
                finding.notes.append("anchor_unclear")
            findings.append(finding)

    for f in findings:
        if f.deadline is not None and f.deadline < today:
            f.notes.append("past")

    findings.sort(key=lambda f: (f.deadline is None, f.deadline or date.max))
    return findings

def add_business_days(start, n):
    current = start
    counted = 0
    while counted < n:
        current += timedelta(days=1)          
        if current.weekday() < 5:             
            counted += 1
    return current

RECEIVED_WORDS = re.compile(
    r"\b(?:of|from|after|upon)\s+(?:your\s+|the\s+date\s+(?:you\s+)?)?"
    r"(?:receiving|receipt|receive|received)\b"
    r"|\ba\s+partir\s+de\s+(?:su\s+)?(?:recibo|recibir)",
    re.IGNORECASE,
)
NOTICE_WORDS = re.compile(
    r"\b(?:date\s+of\s+(?:this|the)\s+(?:notice|letter)"
    r"|date\s+(?:this\s+)?(?:notice|letter)\s+was\s+(?:mailed|sent|issued)"
    r"|notice\s+date|mailing\s+date|mailed|dated"
    r"|a\s+partir\s+de\s+la\s+fecha\s+de\s+(?:este|la)\s+(?:aviso|carta))\b",
    re.IGNORECASE,
)


def detect_anchor(sentence):
    """Return (anchor, is_clear): what the clock counts from, and whether the text says so."""
    if RECEIVED_WORDS.search(sentence):
        return ("received", True)
    if NOTICE_WORDS.search(sentence):
        return ("notice", True)
    return ("notice", False)       

def pick_label(sentence):
    """Return "appeal", "pay", "respond" or "deadline". The order of the checks matters."""
    s = sentence.lower()
    if "appeal" in s or "hearing" in s or "apel" in s or "audiencia" in s:
        return "appeal"
    if re.search(r"\b(pay(ment|ments)?|pagar|pago)\b", s):
        return "pay"
    if re.search(r"\b(respond|return|submit|send|responder|devolver|presente|presentar|enviar)\b", s):
        return "respond"
    return "deadline"

FIELD_LINE = re.compile(r"^[A-Z][\w#]*(?: [\w#]+){0,3}:\s+[A-Z0-9].{0,40}$")


def _line_is_complete(line):
    """True if nothing should be glued onto the end of this line."""
    return (
        line.endswith((".", "!", "?", ":"))     # a finished sentence or "Dear Mr. Lee:"
        or line.isupper()                       # a heading like "NOTICE OF ACTION"
        or FIELD_LINE.match(line) is not None   # a form field
    )


def join_wrapped_lines(text):
    """Glue wrapped lines back into whole paragraphs. Returns a list of strings."""
    paragraphs = []
    current = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:                         # a blank line always ends a paragraph
            if current:
                paragraphs.append(current)
                current = ""
            continue
        current = (current + " " + line) if current else line
        if _line_is_complete(line):
            paragraphs.append(current)
            current = ""
    if current:
        paragraphs.append(current)
    return paragraphs


        
        
