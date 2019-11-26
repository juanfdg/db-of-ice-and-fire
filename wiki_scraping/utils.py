def beautify_string(word):
    if type(word) == list:
        for i in range(len(word)):
            word[i] = _bs(word[i])
        return word

    return _bs(word)


def _bs(w):
    w = w.replace(u"\u00a0", " ")
    w = w.replace(u"\u2013", " ")
    w = w.replace(u"\u00e9", " ")
    w = w.replace(u"\n", " ")
    return w