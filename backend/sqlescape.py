"""Stolen from https://gist.github.com/jeremyBanks/1083518/b36ae606e41bf2a377549ec04cef6cd931323231"""

ERROR = object()


def __sanitise_characters(string, replace_invalid_with=ERROR):
    for character in string:
        point = ord(character)

        if point == 0:
            if replace_invalid_with is ERROR:
                raise ValueError("SQLite identifier contains NUL character.")
            else:
                yield replace_invalid_with
        elif 0xD800 <= point <= 0xDBFF:
            if replace_invalid_with is ERROR:
                raise ValueError("SQLite identifier contains high-surrogate character.")
            else:
                yield replace_invalid_with

        elif 0xDC00 <= point <= 0xDFFF:
            if replace_invalid_with is ERROR:
                raise ValueError("SQLite identifier contains low-surrogate character.")
            else:
                yield replace_invalid_with

        elif 0xFDD0 <= point <= 0xFDEF or (point % 0x10000) in (0xFFFE, 0xFFFF):
            if replace_invalid_with is ERROR:
                raise ValueError("SQLite identifier contains non-character character.")
            else:
                yield replace_invalid_with

        else:
            yield character


def escape(identifier, replace_invalid_with=""):
    if isinstance(identifier, int):
        return identifier
    elif isinstance(identifier, float):
        return identifier
    elif identifier is None:
        return None
    else:
        identifier = str(identifier)
        sanitized = "".join(__sanitise_characters(identifier, replace_invalid_with))
        return '"' + sanitized.replace('"', '""') + '"'


def escape_without_literal(identifier, replace_invalid_with=""):
    if isinstance(identifier, int):
        return identifier
    elif isinstance(identifier, float):
        return identifier
    elif identifier is None:
        return None
    else:
        identifier = str(identifier)
        sanitized = "".join(__sanitise_characters(identifier, replace_invalid_with))
        return sanitized.replace('"', '""')
