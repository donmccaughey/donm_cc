from typing import Optional


# See "ASCII whitespace" in https://infra.spec.whatwg.org/#ascii-whitespace
ASCII_WHITESPACE = {
    '\t',  # tab
    '\n',  # new line
    '\f',  # form feed
    '\r',  # carriage return
    ' ',
}

# See "Unquoted attribute value syntax" in section 13.1.2.3 "Attributes" of
# https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
SPECIAL_CHARS = ASCII_WHITESPACE | {
    '"',
    "'",
    '=',
    '<',
    '>',
    '`',
}


def q(attribute_value) -> str:
    if attribute_value == '':
        return "''"

    attribute_value_chars = set(attribute_value)

    if "'" in attribute_value_chars:
        if '"' in attribute_value_chars:
            attribute_value = attribute_value.replace('"', '&quot;')
        return f'"{attribute_value}"'

    if attribute_value_chars & SPECIAL_CHARS:
        return f"'{attribute_value}'"

    return attribute_value


def format_attribute(name: str, value: Optional[str]) -> str:
    if value is None:
        return name
    else:
        return f'{name}={q(value)}'
