def url_param_sorted(query):
    """
    Сортирует параметры url в порядке их возрастания
    """
    param = None

    if isinstance(query, str):
        param = {}
        for i in query.split("&"):
            z = i.split("=", maxsplit=1)
            if len(z) == 1:
                x, y = z[0], None
            else:
                x, y = z
            param.setdefault(x, [])
            param[x].append(y)
    elif isinstance(query, dict):
        param = query
    else:
        raise TypeError("Аргумент может быть только str или dict")


    key = lambda s: "" if s is None else f"={s}"

    new_query = []
    for k in sorted(param.keys(), key=str):
        v = param[k]
        if not isinstance(v, list):
            v = [v]
        for i in sorted(v, key=key):
            if i is None:
                i = k
            else:
                i = f"{k}={i}"
            new_query.append(i)

    return "&".join(new_query)
