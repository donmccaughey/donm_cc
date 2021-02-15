from typing import List


def wrap_tokens(tokens: List[str], width: int) -> List[str]:
    wrapped = []
    line_len = 0
    end_of_sentence = False
    for token in tokens:
        if token.endswith('.'):
            end_of_sentence = True
        if line_len + len(token) < width:
            if token.isspace():
                if end_of_sentence:
                    token = '  '
                end_of_sentence = False
            wrapped.append(token)
            line_len += len(token)
        elif line_len + len(token) == width:
            if token.isspace():
                wrapped.append('\n')
                line_len = 0
                end_of_sentence = False
            else:
                wrapped.append(token)
                line_len += len(token)
        else:
            if token.isspace():
                wrapped += '\n'
                line_len = 0
                end_of_sentence = False
            else:
                if wrapped:
                    i = len(wrapped) - 1
                    while i > 0 and wrapped[i] != '\n':
                        if wrapped[i].isspace():
                            wrapped[i] = '\n'
                            line_len = sum(
                                [len(token) for token in wrapped[i + 1:]])
                            break
                        i -= 1
                wrapped.append(token)
                line_len += len(token)
    return wrapped
