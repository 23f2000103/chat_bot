def similarity(a, b):

    a_words = set(a.lower().split())
    b_words = set(b.lower().split())

    intersection = len(a_words.intersection(b_words))

    union = len(a_words.union(b_words))

    if union == 0:
        return 0

    return intersection / union