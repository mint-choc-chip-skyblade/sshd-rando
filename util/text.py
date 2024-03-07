from pathlib import Path
from filepathconstants import TEXT_DATA_PATH
from gui.dialogs.dialog_header import print_progress_text
from sslib.msb import CONTROL_REPLACEMENTS
from typing import Union
import copy
import yaml


class Text:
    # en_US is the default case. That *must* be in this list last as, if any text replacements
    # happen to en_US before another language uses its text as a default, it will try and perform
    # the replacement again. The same principle applies to fr_US and es_US (defaults for fr_FR and
    # es_ES).
    SUPPORTED_LANGUAGES = [  # uncomment languages which get support
        # "zh_CN",  # Chinese
        "nl_NL",  # Dutch
        "fr_FR",  # French (FR)
        "fr_US",  # French (US)
        "de_DE",  # German
        "it_IT",  # Italian
        # "ja_JP",  # Japanese
        # "ko_KR",  # Korean
        # "ru_RU",  # Russian
        "es_ES",  # Spanish (ES)
        "es_US",  # Spanish (US)
        # "zh_TW",  # Taiwanese
        "en_GB",  # English (GB)
        "en_US",  # English (US)
    ]

    def __init__(self, text: str = "") -> None:
        self.text: dict[str, str] = {}
        for lang in Text.SUPPORTED_LANGUAGES:
            self.text[lang] = text

    def __str__(self) -> str:
        return self.text["en_US"]

    def __add__(self, text: Union[str, "Text"]) -> "Text":
        new_text = copy.deepcopy(self)
        for lang in Text.SUPPORTED_LANGUAGES:
            if type(text) != Text:
                new_text.text[lang] += text
            else:
                new_text.text[lang] += text.text[lang]
        return new_text

    def __iadd__(self, text: Union[str, "Text"]) -> "Text":
        for lang in Text.SUPPORTED_LANGUAGES:
            if type(text) != Text:
                self.text[lang] += text
            else:
                self.text[lang] += text.text[lang]
        return self

    def get(self, lang: str) -> str:
        if lang not in Text.SUPPORTED_LANGUAGES or len(self.text[lang]) == 0:
            if lang == "fr_FR":
                return self.get("fr_US")
            elif lang == "es_ES":
                return self.get("es_US")

            return self.text["en_US"]  # Default to english if not found
            # raise RuntimeError(f'Unsupported language "{lang}"')
        return self.text[lang]

    def replace(self, old: str, new: Union[str, "Text"], count: int = -1) -> "Text":
        text_with_replace = copy.deepcopy(self)

        for lang in Text.SUPPORTED_LANGUAGES:
            full_text = self.text[lang]

            if full_text == "":
                full_text = self.text["en_US"]

            if type(new) != Text:
                text_with_replace.text[lang] = full_text.replace(old, new, count)
            else:
                new_text = new.text[lang]

                if new_text == "":
                    new_text = new.text["en_US"]

                text_with_replace.text[lang] = full_text.replace(old, new_text, count)
        return text_with_replace

    def apply_text_color(self, color: str) -> "Text":
        new_text = copy.deepcopy(self)
        if color == "":
            return new_text

        if color not in [
            "r",
            "rd",
            "y+",
            "b",
            "g",
            "y",
            "g+",
            "b+",
            "r+",
            "s",
            "ye",
            "blk",
        ]:
            raise RuntimeError(f'Unknown color specification "{color}"')

        for lang in Text.SUPPORTED_LANGUAGES:
            text = new_text.get(lang)
            if "<" not in text and ">" not in text:
                text = f"<{color}<{text}>>"
            else:
                text = text.replace("<", f"<{color}<").replace(">", ">>")
            new_text.text[lang] = text

        return new_text

    def break_lines(self) -> None:
        for lang in Text.SUPPORTED_LANGUAGES:
            self.text[lang] = break_lines(self.text[lang])


# text table keyed by english name and type
text_table: dict[str, dict[str, Text]] = {}


def load_text_data() -> None:
    # Clear the text table for multiple generations
    if text_table:
        text_table.clear()

    print_progress_text("Loading text data")

    for language in Text.SUPPORTED_LANGUAGES:
        filename = f"{language}.yaml"
        filepath = TEXT_DATA_PATH / filename

        with open(filepath, "r") as text_data_file:
            text_data = yaml.safe_load(text_data_file)

            if text_data is None or len(text_data) == 0:
                continue

            for element in text_data:
                name = element["name"]
                if name not in text_table:
                    text_table[name] = {}

                for field, text in element.items():
                    if field == "name":
                        continue
                    if field not in text_table[name]:
                        text_table[name][field] = Text()
                    # Insert the text into the appropriate Text objects
                    # language
                    text_table[name][field].text[language] = (
                        text if text is not None else ""
                    )


def get_text_data(key: str, type_: str = "standard") -> Text:
    if key not in text_table:
        raise RuntimeError(f'Unknown hint data key "{key}"')
    elif type_ not in text_table[key]:
        raise RuntimeError(f'Unknown hint data type "{type_}"')
    else:
        return text_table[key][type_]


def add_text_data(key: str, text: Text, type_: str = "standard") -> None:
    if key in text_table:
        raise RuntimeError(f'Data for "{key}" already exists in text table')
    text_table[key] = {}
    text_table[key][type_] = text


def make_text_listing(texts: list[Text]) -> Text:
    if len(texts) == 1:
        return texts[0]

    en_US = ""
    # TODO: Add rules for other languages when we get to them
    for i, text in enumerate(texts):
        # Change formatting depending on how many items we're listing
        if i == 0:
            en_US += text.get("en_US")
        elif i == len(texts) - 1 and len(texts) == 2:
            en_US += " and " + text.get("en_US")
        elif i == len(texts) - 1:
            en_US += ", and " + text.get("en_US")
        else:
            en_US += ", " + text.get("en_US")

    listing_text = Text()
    listing_text.text["en_US"] = en_US
    return listing_text


def break_and_make_multiple_textboxes(texts: list[Text]) -> Text:
    for text in texts:
        text.break_lines()
    return make_mutliple_textboxes(texts)


def make_mutliple_textboxes(texts: list[Text]) -> Text:
    final_text = Text()
    for text in texts:
        for lang in Text.SUPPORTED_LANGUAGES:
            if text.text[lang] == "":
                lang = "en_US"

            text.text[lang] = text.text[lang].rstrip("\n")
            lines = text.text[lang].count("\n") + 1
            needed_linebreaks = -lines % 4 + 1
            text.text[lang] += "\n" * needed_linebreaks
        final_text += text

    return final_text


def break_lines(text: str) -> str:
    # Widths of all characters in pixels
    char_widths = {
        "a": 17,
        "b": 17,
        "c": 15,
        "d": 18,
        "e": 15,
        "f": 15,
        "g": 17,
        "h": 18,
        "i": 9,
        "j": 10,
        "k": 20,
        "l": 10,
        "m": 27,
        "n": 19,
        "o": 17,
        "p": 18,
        "q": 18,
        "r": 15,
        "s": 13,
        "t": 12,
        "u": 18,
        "v": 16,
        "w": 24,
        "x": 17,
        "y": 16,
        "z": 15,
        "A": 23,
        "B": 22,
        "C": 23,
        "D": 24,
        "E": 22,
        "F": 20,
        "G": 26,
        "H": 27,
        "I": 13,
        "J": 18,
        "K": 26,
        "L": 21,
        "M": 30,
        "N": 24,
        "O": 25,
        "P": 21,
        "Q": 24,
        "R": 24,
        "S": 18,
        "T": 22,
        "U": 24,
        "V": 24,
        "W": 30,
        "X": 23,
        "Y": 24,
        "Z": 21,
        "0": 18,
        "1": 18,
        "2": 18,
        "3": 18,
        "4": 18,
        "5": 18,
        "6": 18,
        "7": 18,
        "8": 18,
        "9": 18,
        " ": 10,
        "-": 10,
        "/": 16,
        "'": 7,
        ".": 7,
        ",": 7,
        "!": 7,
    }

    max_line_length = 700
    cur_line_width = 0

    i = 0
    previous_space = 0
    text_chars = list(text)
    while i < len(text_chars):
        code = ""

        # Skip over control codes since they don't get displayed
        control_code = False
        for code in CONTROL_REPLACEMENTS:
            if i + len(code) <= len(text_chars) and text[i : i + len(code)] == code:
                control_code = True
                break

        if control_code:
            # Assume worst case for player name width
            # 8 chars max * max char width
            if code == "<heroname>":
                cur_line_width += 8 * 30
            i += len(code)
            continue

        # Keep track of the previous space to replace with
        # a line break when we reach the maximum pixel width
        if text[i] == " ":
            previous_space = i
        # If we encounter an already inserted newline, reset
        # the counter
        elif text[i] == "\n":
            cur_line_width = 0
            i += 1
            continue

        if text[i] not in char_widths:
            raise RuntimeError(
                f"Char '{text[i]}' has no defined width in text \"{text}\""
            )

        cur_line_width += char_widths[text[i]]
        # If we exceed the maximum line width, replace the
        # previous space with a newline and starting counting
        # from the newline again
        if cur_line_width > max_line_length:
            text_chars[previous_space] = "\n"
            i = previous_space
            cur_line_width = 0

        i += 1

    return "".join(text_chars)
