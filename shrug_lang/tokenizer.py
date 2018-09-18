from typing import List

from shrug_lang.tokens import Tokens


def parse_line(line: str):
    if len(line) == 0:
        return [(Tokens.EOL,)]
    unparsed_tokens = filter(None, join_strings(line.split(' ')))
    tokens = [parse_token(unparsed) for unparsed in unparsed_tokens]
    tokens.append((Tokens.EOL,))
    return tokens


def join_strings(unparsed_tokens: List[str]):
    """Join strings that have spaces in them"""
    new_unparsed = []
    reading_string = False
    current_string = []
    for unparsed_token in unparsed_tokens:
        if reading_string:
            if unparsed_token.endswith('"'):
                reading_string = False
                current_string.append(unparsed_token)
                new_unparsed.append(' '.join(current_string))
                current_string.clear()
            else:
                current_string.append(unparsed_token)
        elif (unparsed_token.startswith('"') and
              (len(unparsed_token) == 1 or
               not unparsed_token.endswith('"'))):
            reading_string = True
            current_string.append(unparsed_token)
        else:
            new_unparsed.append(unparsed_token)
    if len(current_string):
        new_unparsed.append(' '.join(current_string))
    return new_unparsed


def parse_token(unparsed_token: str):
    """Get token from given string"""
    if unparsed_token == '':
        return None
    if unparsed_token == '¯\_(ツ)_/¯':
        return Tokens.SHRUG,
    if (len(unparsed_token) >= 2 and
            unparsed_token.startswith('"') and
            unparsed_token.endswith('"')):
        return Tokens.STRING, unparsed_token[1:-1]
    if unparsed_token.isalpha():
        return Tokens.ID, unparsed_token
    if unparsed_token.isnumeric():
        return Tokens.NUMBER, int(unparsed_token)
    return Tokens.INVALID, unparsed_token


