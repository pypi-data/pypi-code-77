from re import findall, match, sub

from colorifix.colorifix import erase


def multisub(sub_dict, string):
    """Infinite sub in one iteration # sub_dict: {what_to_sub:substitution}"""
    rgx = "|".join(f"({s})" for s in sub_dict.keys())
    return sub(rgx, lambda m: sub_dict.get(m.group()), string)


def strict_input(
    text, wrong_text=None, choices=None, regex=None, flush=False, check=None
):
    """Get user input with some requirements"""
    inp = input(text)
    if flush:
        erase(len(findall(r"\n", text)) + 1)
    while (
        (not choices or choices and inp not in choices)
        and (not regex or regex and not match(regex, inp))
        and (not check or check and not check(inp))
    ):
        if wrong_text:
            inp = input(wrong_text)
        else:
            inp = input(text)
        if flush:
            erase(len(findall(r"\n", wrong_text or text)) + 1)
    return inp
