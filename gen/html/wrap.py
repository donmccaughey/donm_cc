from typing import List


def wrap_tokens(tokens: List[str], width: int) -> List[str]:
    wrapped = []
    line_len = 0
    for token in tokens:
        token_len = len(token)
        if line_len + token_len < width:
            wrapped.append(token)
            line_len += token_len
        elif line_len + token_len == width:
            if token.isspace():
                wrapped.append('\n')
                line_len = 0
            else:
                wrapped.append(token)
                line_len += token_len
        else:
            if token.isspace():
                wrapped += '\n'
                line_len = 0
            else:
                if wrapped:
                    i = len(wrapped) - 1
                    while i > 0 and wrapped[i] != '\n':
                        if wrapped[i].isspace():
                            wrapped[i] = '\n'
                            line_len = sum([len(token) for token in wrapped[i+1:]])
                            break
                        i -= 1
                wrapped.append(token)
                line_len += token_len
    return wrapped
