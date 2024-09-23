def gettext(s):
    return s


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

CSRF_COOKIE_AGE = 60 * 60 * 24 * 365

DATE_INPUT_FORMATS = [
    "%d %B %Y",  # '25 October 2006'
    "%d %B, %Y",  # '25 December, 2006'
]

FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

LANGUAGES = [
    ("es", gettext("Spanish")),
    ("en", gettext("English")),
]
