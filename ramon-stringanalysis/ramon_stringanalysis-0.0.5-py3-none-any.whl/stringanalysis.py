import jellyfish


class StringAnalysis:

    def __init__(self, string_stream):
        self.string_stream = string_stream

    def get_most_similar_word(self, word):
        scores = list(map(lambda x: jellyfish.jaro_distance(x, word),
                          self.string_stream))
        max_score = max(zip(scores, range(len(scores))))[1]
        return self.string_stream[max_score]
