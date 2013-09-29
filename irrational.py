from string import ascii_lowercase, digits

"irrational poetry: Given an irrational number or other stream of pseudorandom digits, uses simple substitution to convert them into letters, and clumps the letters into words."

def generate_numstring(length):

    """ generate_numstring(length): Generates a numerical string of length digits long.
    """

    import random
    
    for char in xrange(length):
        yield random.choice(digits)

def irrational_to_letters(irr_number):

    """ irrational_to_letters(irr_number): From a given number, returns a-z (1-26).  Attempts to evenly distribute the numerical values.
    """

    prev = None
    split_evenly = [0, 10, 20]

    for num in irr_number:

        num = int(num)

        if prev is not None:
            if (prev * 10) + num - 1 < 26:
                yield ascii_lowercase[(prev * 10) + num - 1]
            else:
                yield ascii_lowercase[num - 1]

            prev = None
            continue
        
        if num > 2:

            distribute = split_evenly.pop(0)
            split_evenly.append(distribute)

            try:
                yield ascii_lowercase[distribute + num - 1]
            except IndexError: # > 26
                distribute = split_evenly.pop()
                split_evenly.insert(0, distribute)
                yield ascii_lowercase[num - 1]
        else:
            prev = num


def letters_to_words(streaming_letters, min_wordsize = 4):

    """ letters_to_words(streaming_letters, min_wordsize): Given a generator of streaming_letters, find the largest word that can be made and yield each one.
    """

    word_list = get_wordlist(min_wordsize)

    prev = None
    
    for letter in streaming_letters:
        if prev is None:
            prev = letter
        else:
            # Partial or whole match; keep building
            if ("{0}{1}".format(prev, letter) in word_list[prev[0]]) or bool([prev for word in word_list[prev[0]] if prev in word[:len(prev)]]):
                prev = "{0}{1}".format(prev, letter)
            # The last addition made the whole match into garbage, yield all but the last letter
            elif prev[:-1] in word_list[prev[0]]:
                yield prev[:-1]
                prev = letter
            # No match; garbage - but retry the remaining letters
            else:
                prev = "{0}{1}".format(prev[-1:], letter)
    if prev in word_list[prev[0]]:
        yield prev[:-1]


def get_wordlist(min_size = 4):

    """ get_wordlist(min_size = 4): Helper function to open the wordlist file (specify minimum length of word between 1 and 9) and return it as a dict.
        Keys are the first letter; values are a list of all words starting with that letter.
        The smaller the number you specify, the more possible words you'll get - though it's likely most of them will be very short.
    """

    assert 1 <= int(min_size) <= 9

    filename = 'wordlists/words_{0}.txt'.format(int(min_size))

    words = {}.fromkeys(ascii_lowercase, [])

    with open(filename) as words_file:
        for word in words_file.xreadlines():
            words[word[0].lower()].append(word.strip())

        return words


if __name__ == '__main__':

    import sys

    try:
        min_wordsize = int(sys.argv[1])
    except IndexError:
        print """Arguments for irrational.py: python irrational.py min_wordsize
    Example: python irrational.py 4
    NOTE: The higher your word size, the longer it will take for irrational poetry to find a match."""
    else:
        for word in letters_to_words(irrational_to_letters(generate_numstring(1000000000)), min_wordsize):
            print word
