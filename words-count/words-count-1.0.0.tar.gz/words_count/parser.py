import re


class WordsCount:

    def __init__(self, chunk_size=3, top_number=100):
        self._chunk_size = chunk_size
        self._top_number = top_number
        self._prepend_words = []
        self._counts = {}
        self._result = {}

    @property
    def result(self):
        sorted_keys = sorted(self._counts, key=self._counts.get, reverse=True)[:self._top_number]
        self._result = {}
        for words in sorted_keys:
            self._result[words] = self._counts[words]
        return self._result

    @staticmethod
    def clean_and_split_lie(line):
        line_words = re.split(r'\W+', re.sub(r'[^A-Za-z0-9 ]+', '',  line.lower().strip()))
        line_words = list(filter(None, line_words))
        return line_words

    def count(self, line):
        self._prepend_words = self._process_line(line, self._prepend_words)

    def _process_line(self, line, words_prepend):
        words = words_prepend + self.clean_and_split_lie(line)
        for index in range(len(words) - (self._chunk_size-1)):
            chunk_of_words = ' '.join(words[index:index + self._chunk_size])
            if chunk_of_words not in self._counts:
                self._counts[chunk_of_words] = 0
            self._counts[chunk_of_words] += 1
        return words[-(self._chunk_size-1):]

    def count_in_files(self, files_path):
        for file_path in files_path:
            self._prepend_words = []
            with open(file_path) as file_to_read:
                for line in file_to_read:
                    self.count(line)
