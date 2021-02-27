from .utils import chunks


def clear(term):
    print(term.home + term.clear)


def title(term, split):
    return (
        term.cyan(term.bold + term.underline + term.center(split.name))
        + term.normal
        + term.down(2)
    )


def render(term, data, split_index, note_index):
    split = data.splits[split_index]
    notes = split.notes[note_index:]

    with term.location(0, 0):
        print(title(term, split))

    with term.location(0, 3):
        for idx, note in enumerate(notes):
            output_str = ""
            chunked = chunks(note, term.width - 4)

            if idx == 0:
                output_str += f"{term.bold} -> "
            else:
                output_str += " " * 4

            for line in chunked:
                output_str += line + "\n" + (" " * 4)

            print(output_str + term.normal)


def ui_loop(term, data):
    split_index = 0
    note_index = 0

    clear(term)
    render(term, data, split_index, note_index)

    while True:
        key = term.inkey(timeout=1)

        if not key:
            continue

        lower = key.lower()
        current_split = data.splits[split_index]

        if lower == "q" or key.code == term.KEY_ESCAPE:
            break

        if key.code == term.KEY_RIGHT and split_index < len(data.splits) - 1:
            split_index += 1
            note_index = 0

        if key.code == term.KEY_LEFT and split_index > 0:
            split_index -= 1
            note_index = 0

        if key.code == term.KEY_DOWN and note_index < len(current_split.notes) - 1:
            note_index += 1

        if key.code == term.KEY_UP and note_index > 0:
            note_index -= 1

        clear(term)
        render(term, data, split_index, note_index)
