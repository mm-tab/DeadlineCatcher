import uuid
from datetime import date, datetime, timedelta, timezone

REMINDER_DAYS = (7, 3, 1)


def escape_text(text):
    """Escape the characters that have a special meaning in an .ics file."""
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\r\n", "\\n").replace("\n", "\\n")
    return text


def fold_line(line):
    """An .ics line may hold at most 75 BYTES. Longer lines are cut, and each
    continuation line starts with one space."""
    pieces = []
    current = ""
    for char in line:
        limit = 75 if not pieces else 74  # continuation lines lose 1 byte to the space
        if len((current + char).encode("utf-8")) > limit:
            pieces.append(current)
            current = char
        else:
            current += char
    pieces.append(current)
    return "\r\n ".join(pieces)


def _event(due, summary, today_stamp):
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}@deadlinecatcher.local",
        f"DTSTAMP:{today_stamp}",
        f"DTSTART;VALUE=DATE:{due:%Y%m%d}",
        f"DTEND;VALUE=DATE:{due + timedelta(days=1):%Y%m%d}",
        f"SUMMARY:{escape_text(summary)}",
        "END:VEVENT",
    ]
    return [fold_line(line) for line in lines]


def make_ics(items, today=None):
    """items is a list of (due_date, label). Returns the text of an .ics file."""
    today = today or date.today()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Deadline Catcher//EN"]
    for due, label in items:
        lines += _event(due, label.capitalize() + " (deadline)", stamp)
        for n in REMINDER_DAYS:
            remind = due - timedelta(days=n)
            if remind >= today:
                lines += _event(remind, f"Reminder: {label} in {n} day{'s' if n > 1 else ''}", stamp)
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"