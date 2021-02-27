def get_age_description(age: int):
    if age < 0:
        return None
    if age < 1:
        return "Bobas"
    if age < 18:
        return "Dziecko"
    if age < 30:
        return "Młody"
    if age < 50:
        return "Dojrzały"
    if age < 65:
        return "Wiekowy"
    return "Emeryt"
