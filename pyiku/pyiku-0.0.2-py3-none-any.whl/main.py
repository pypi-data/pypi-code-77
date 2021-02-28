import random
import re


def sylco(word):
    # pulled from https://github.com/eaydin/sylco/blob/master/sylco.py
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    exception_add = ['serious', 'crucial']
    exception_del = ['fortunately', 'unfortunately']

    co_one = ['cool', 'coach', 'coat', 'coal', 'count', 'coin', 'coarse', 'coup', 'coif', 'cook', 'coign', 'coiffe',
              'coof', 'court']
    co_two = ['coapt', 'coed', 'coinci']

    pre_one = ['preach']

    syls = 0  # added syllable number
    disc = 0  # discarded syllable number

    # 1) if letters < 3 : return 1
    if len(word) <= 3:
        syls = 1
        return syls

    # 2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed":
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]', word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]', word)) > 1:
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[
                                                                                                       -3:] == "ies":
                pass
            else:
                disc += 1

    # 3) discard trailing "e", except where ending is "le"

    le_except = ['whole', 'mobile', 'pole', 'male', 'female', 'hale', 'pale', 'tale', 'sale', 'aisle', 'whale', 'while']

    if word[-1:] == "e":
        if word[-2:] == "le" and word not in le_except:
            pass

        else:
            disc += 1

    # 4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]', word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]', word))
    disc += doubleAndtripple + tripple

    # 5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]', word))

    # 6) add one if starts with "mc"
    if word[:2] == "mc":
        syls += 1

    # 7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui":
        syls += 1

    # 8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i, j in enumerate(word):
        if j == "y":
            if (i != 0) and (i != len(word) - 1):
                if word[i - 1] not in "aeoui" and word[i + 1] not in "aeoui":
                    syls += 1

    # 9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui":
        syls += 1

    if word[:2] == "bi" and word[2] in "aeoui":
        syls += 1

    # 10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian":
        # and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian":
            pass
        else:
            syls += 1

    # 11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not,
    # check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui':

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two:
            syls += 1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one:
            pass
        else:
            syls += 1

    # 12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary,
    # if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui':
        if word[:6] in pre_one:
            pass
        else:
            syls += 1

    # 13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't", "wouldn't"]

    if word[-3:] == "n't":
        if word in negative:
            syls += 1
        else:
            pass

            # 14) Handling the exceptional words.

    if word in exception_del:
        disc += 1

    if word in exception_add:
        syls += 1

        # calculate the output
    return numVowels - disc + syls


def check_roman(word):
    roman_pattern = r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"

    if re.search(roman_pattern, word.strip(), re.I):
        return True
    else:
        # print(word)
        return False


def random_word(words: list):
    random_word = random.choice(words)
    random_word = ''.join(e for e in random_word if e.isalpha() and not check_roman(random_word))
    syllable_count = sylco(random_word)
    word_cnt = {random_word: syllable_count}
    return word_cnt


def build_line(words: list, cnt):
    dd = random_word(words)
    retries = 0
    while sum(dd.values()) < cnt:
        try:
            up = random_word(words)
            dd.update(up)
            if sum(dd.values()) == cnt:
                return [dd]
            else:
                if sum(dd.values()) > cnt:
                    dd = {}
                    retries += 1
                    if retries > 5:
                        return False
        except Exception:
            pass
    return [dd]


def build_hiaku(words: list):
    """
    Build a haiku out of a list of words.
    Fails (returns a blank string) if process is taking too long or is failing internally
    Fails (returns a blank string) if less than 5 words provided to use.

    :param words: list of words to use to build the haiku. Numbers and Roman numerals are filtered out internally.
    :type words: list
    :return: A three-line haiku, following the 5-7-5 syllable pattern
    :rtype: str
    """
    if len(words) < 5:
        return ""

    line5_1 = build_line(words, 5)
    if not line5_1:
        return ""
    m_list = line5_1

    line7 = build_line(words, 7)
    if not line7:
        return ""
    m_list += line7

    line5_2 = build_line(words, 5)
    if not line5_2:
        return ""
    m_list += line5_2

    stanz1 = ' '.join(m_list[0].keys())
    stanz2 = ' '.join(m_list[1].keys())
    stanz3 = ' '.join(m_list[2].keys())
    lines = stanz1, stanz2, stanz3
    haiku = '\n'.join(lines).lower()
    return haiku
