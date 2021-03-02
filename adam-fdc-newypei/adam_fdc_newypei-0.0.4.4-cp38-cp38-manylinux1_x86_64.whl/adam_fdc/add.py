from add_wrapper import add


def add_up(n):
    result = 0;

    for i in range(0, n):
        result = add(result, i);

    return result;
