import re 
from datetime import date 

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
    
    results.sort()
    for (pos, d) in results:
        the_dates.append(d)
    return the_dates
        
        
