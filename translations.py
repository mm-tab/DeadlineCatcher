STR = {
    "en": {
        "skip": "Skip to main content",
        "switch_label": "Español",
        "switch_lang": "es",
        "index_title": "Find the deadlines in your letter",
        "index_intro": "Paste the text of a letter about benefits or services. We show every deadline we find, and the sentence it came from, so you can check it yourself.",
        "letter_label": "Letter text",
        "notice_label": "Date on the letter (optional)",
        "received_label": "Date you received it (optional)",
        "privacy": "Remove names and case numbers first. Nothing is saved. This app only finds dates in the text; it never decides if you qualify for anything.",
        "find_button": "Find deadlines",
        "error_empty": "Please paste some letter text first.",
        "results_title": "Deadlines we found",
        "none_found": "No deadlines found. The letter may use wording we do not recognize, so please read it yourself too.",
        "need_date_help": "Some deadlines count from a date we could not find. Enter it below and press Recalculate.",
        "recalculate": "Recalculate",
        "notice_short": "Date on the letter",
        "received_short": "Date you received it",
        "need_letter_date": "We need the letter date",
        "add_to_calendar": "Add to my calendar",
        "download": "Download calendar file (.ics)",
        "another": "Check another letter",
        "label_respond": "respond",
        "label_appeal": "appeal",
        "label_pay": "pay",
        "label_deadline": "deadline",
        "note_weekdays_only": "Counted weekdays only. Holidays are not excluded, so the real date may be later.",
        "note_anchor_unclear": "The letter does not say what the days count from. We counted from the letter date.",
        "note_past": "This date has already passed.",
        "note_year_assumed": "The letter did not give a year, so we used the next time this date comes up.",
        "note_ambiguous_date": "This date could be month/day or day/month. We read it as month/day.",
        "note_prefix": "Note:",
        "notfound_title": "Page not found",
        "notfound_text": "That page does not exist.",
        "back_home": "Back to Deadline Catcher",
    },
    "es": {
        "skip": "Saltar al contenido principal",
        "switch_label": "English",
        "switch_lang": "en",
        "index_title": "Encuentre las fechas límite de su carta",
        "index_intro": "Pegue el texto de una carta sobre beneficios o servicios. Le mostramos cada fecha límite que encontramos y la oración de donde salió, para que usted mismo la revise.",
        "letter_label": "Texto de la carta",
        "notice_label": "Fecha de la carta (opcional)",
        "received_label": "Fecha en que la recibió (opcional)",
        "privacy": "Quite primero los nombres y los números de caso. No se guarda nada. Esta aplicación solo encuentra fechas en el texto; nunca decide si usted califica para algo.",
        "find_button": "Buscar fechas límite",
        "error_empty": "Primero pegue el texto de la carta.",
        "results_title": "Fechas límite encontradas",
        "none_found": "No se encontraron fechas límite. Puede que la carta use palabras que no reconocemos, así que léala usted también.",
        "need_date_help": "Algunas fechas límite se cuentan desde una fecha que no encontramos. Escríbala abajo y oprima Recalcular.",
        "recalculate": "Recalcular",
        "notice_short": "Fecha de la carta",
        "received_short": "Fecha en que la recibió",
        "need_letter_date": "Necesitamos la fecha de la carta",
        "add_to_calendar": "Agregar a mi calendario",
        "download": "Descargar archivo de calendario (.ics)",
        "another": "Revisar otra carta",
        "label_respond": "responder",
        "label_appeal": "apelar",
        "label_pay": "pagar",
        "label_deadline": "fecha límite",
        "note_weekdays_only": "Solo se contaron los días de semana. No se excluyen los días festivos, así que la fecha real puede ser más tarde.",
        "note_anchor_unclear": "La carta no dice desde cuándo se cuentan los días. Contamos desde la fecha de la carta.",
        "note_past": "Esta fecha ya pasó.",
        "note_year_assumed": "La carta no indicó el año, así que usamos la próxima vez que llega esta fecha.",
        "note_ambiguous_date": "Esta fecha puede ser mes/día o día/mes. La leímos como mes/día.",
        "note_prefix": "Nota:",
        "notfound_title": "Página no encontrada",
        "notfound_text": "Esa página no existe.",
        "back_home": "Volver a Deadline Catcher",
    },
}

WEEKDAYS = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "es": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
}
MONTH_NAMES = {
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
}


def t(key, lang="en"):
    """Look up one sentence. Falls back to English if the language or key is missing."""
    return STR.get(lang, STR["en"]).get(key) or STR["en"][key]


def format_date(d, lang="en"):
    """date(2026, 11, 15) -> 'Sunday, November 15, 2026' or 'domingo, 15 de noviembre de 2026'"""
    lang = lang if lang in STR else "en"
    weekday = WEEKDAYS[lang][d.weekday()]
    month = MONTH_NAMES[lang][d.month - 1]
    if lang == "es":
        return f"{weekday}, {d.day} de {month} de {d.year}"
    return f"{weekday}, {month} {d.day}, {d.year}"