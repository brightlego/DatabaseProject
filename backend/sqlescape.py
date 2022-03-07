"""Stolen from https://gist.github.com/jeremyBanks/1083518/b36ae606e41bf2a377549ec04cef6cd931323231

Escapes strings for use in sql
"""

ERROR = object()


def __sanitise_characters(string, replace_invalid_with=ERROR):
    """A generator function to sanitise the characters

    Arguments:
        string (str)
            -- the string to search through
    Keyword Arguments
        replace_invalid_with (str) default ERROR
            -- Character to replace the invalid with

    Yields * length of string:
        character (str)
            -- The character
    """

    # Iterate through the string
    for character in string:

        # Get the caracter number
        point = ord(character)

        # Check if that character is valid
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

        # If it is valid, yield the character
        else:
            yield character


def escape(identifier, replace_invalid_with=""):
    """Escapes a string

    Argument:
        identifier (str)
            -- The literal to escape
        replace_invalid_with (str)
            -- What to replace any invalid characters with

    Returns:
        escaped (str)
            -- The escaped string
    """
    return '"' + escape_without_literal(identifier, replace_invalid_with) + '"'


def escape_without_literal(identifier, replace_invalid_with=""):
    """Escapes a literal

    Argument:
        identifier (Any)
            -- The literal to escape
        replace_invalid_with (str)
            -- What to replace any invalid characters with


        Returns:
            escaped (Any)
                -- The escaped literal
    """

    # If the identifier is an int, float or None, it does not need to be
    # escaped
    if isinstance(identifier, int):
        return identifier
    elif isinstance(identifier, float):
        return identifier
    elif identifier is None:
        return None
    else:
        # Otherwise, stringify it and sanatise it
        identifier = str(identifier)
        sanitized = "".join(__sanitise_characters(identifier, replace_invalid_with))
        return sanitized.replace('"', '""')
