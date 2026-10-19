from datetime import date
from calendar_ics import make_ics, escape_text
print(make_ics([(date(2026, 11, 15), "respond")], today=date(2026, 10, 9)).replace("\r\n", "\n"))
print(escape_text("Respond, appeal; pay"))