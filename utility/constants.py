"""Constants Module."""
from enum import Enum


class Constants(Enum):
    """This class has all the hardcoded values required."""

    PARENT_URL = "https://www.cermati.com/karir"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    SCRIPT = "script"

    ID_INITIALS = "initials"

    HTML_PARSER = "html.parser"
