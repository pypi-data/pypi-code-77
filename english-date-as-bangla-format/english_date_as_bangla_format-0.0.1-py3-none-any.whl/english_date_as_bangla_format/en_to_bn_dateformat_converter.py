
month_to_bn_name = {
    "01":"জানুয়ারি",
    "02":"ফেব্রুয়ারি",
    "03":"মার্চ",
    "04":"এপ্রিল",
    "05":"মে",
    "06":"জুন",
    "07":"জুলাই",
    "08":"আগস্ট",
    "09":"সেপ্টেম্বর",
    "10":"অক্টোবর",
    "11":"নভেম্বর",
    "12":"ডিসেম্বর"
}

def bn_digit(input_value):
    """replaces english digits with bengali digits from the input string"""
    input_str = str(input_value)
    translated_string_chars = []

    for x in input_str:
        unicode_diff_with_zero = ord(x) - ord('0')
        if 0 <= unicode_diff_with_zero <= 9:  # it's a english digit
            bn_digit_code = ord('০') + unicode_diff_with_zero
            translated_string_chars.append(chr(bn_digit_code))
        else:
            translated_string_chars.append(x)

    return ''.join(translated_string_chars)

def bn_date(input_value):
    """replaces english digits with bengali digits from the input string"""
    input_str = str(input_value)
    translated_string_chars = []

    counter= 0
    for x in input_str.split("-")[::-1]:
        if counter==1:
            translated_string_chars.append( month_to_bn_name[x])
        else:
            translated_string_chars.append(bn_digit(x))
        counter = counter + 1
    return ' '.join(translated_string_chars)
