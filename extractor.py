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

def find_dates(text): 
    results = []
    the_dates = []

    for match in re.finditer(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", text):
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), d)) 
    
    for match in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(\d{4}|\d{2})\b", text):
        month = int(match.group(1))
        day = int(match.group(2))
        year = int(match.group(3))
        if year < 100:
            year += 2000
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), d))
    
    for match in re.finditer(PATTERN_A, text, re.IGNORECASE):
        month = MONTHS[match.group(1).lower()]
        day   = int(match.group(2))
        year  = int(match.group(3))
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), d))
    
    for match in re.finditer(PATTERN_B, text, re.IGNORECASE):
        month = MONTHS[match.group(2).lower()]
        day   = int(match.group(1))
        year  = int(match.group(3))
        d = make_date(year, month, day)
        if d is not None:
            results.append((match.start(), d))
    
    results.sort()
    for (pos, d) in results:
        the_dates.append(d)
    return the_dates


        
        
