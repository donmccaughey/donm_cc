from typing import Optional


def q(attribute_value) -> str:
    if attribute_value == '':
        return "''"

    if '"' in attribute_value and "'" in attribute_value:
        attribute_value = attribute_value.replace('"', '&quot;')

    if "'" in attribute_value:
        return f'"{attribute_value}"'

    special_chars = [' ', '"', '=', '<', '>', '`']
    if any(ch in attribute_value for ch in special_chars):
        return f"'{attribute_value}'"

    return attribute_value


def format_attribute(name: str, value: Optional[str]) -> str:
    if value is None:
        return name
    else:
        return f'{name}={q(value)}'
