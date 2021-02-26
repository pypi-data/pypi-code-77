from shirkhan.syllable.alphabet import Alphabet


class SWord:
    pass

    def __init__(self, word: str):
        self.word = word

    # 吧非母语部分清理掉
    # todo

    def tokenize(self):
        """
        吧word 标识成 00100 这种形式，其中的1和0取决于它在 alphabet [2]中的标识
        :return:
        """
        tokens = []
        for alpha in self.word:
            info = Alphabet.alpha_info(alpha)
            if info is None:
                continue
            tokens.append(str(info[2]))

        return "".join(tokens)

    def __token_to_group(self, token):
        """
        吧给定的token 按照元音分组
        :param token:
        :return:
        """
        group = []
        tmp = []
        for index in range(len(token)):
            item = token[index]
            tmp.append(item)

            if item == '1':
                group.append(tmp)
                tmp = []
            elif index == len(token) - 1:
                group.append(tmp)
        return group

    def get_grouped_token(self):
        """
        吧单词向量化,分组得出：001010010 -> [001 01 001 0] 一样的分组
        :return:
        """
        return self.__token_to_group(self.tokenize())

    def get_grouped_retoken(self):
        """
        吧单词向量化并反转得出后：001010010 -> [001 01 001 0]
        :return:
        """
        retoken = (self.tokenize())[::-1]
        return self.__token_to_group(retoken)

    def get_positional_retoken(self, delimiter="x"):
        """
        给单词的向量反序植入符号生成分割点
        :return:
        """
        group = self.get_grouped_retoken()
        position = ""

        for index in range(len(group)):
            item = group[index]
            if len(item) == 0:
                continue
            if index == 0 or item[-1] != '1':  # 第一和最后一项
                position = position + ''.join(item)
                continue
            if ''.join(item) == '1':
                position = position + ''.join(item)
                continue

            c_count = len(item) - 1
            if c_count == 1:
                position = position + item[0] + delimiter + ''.join(item[1:])

            elif c_count == 2:
                position = position + item[0] + delimiter + ''.join(item[1:])
            elif c_count == 3:
                position = position + ''.join(item[0]) + delimiter + ''.join(item[1:])
            elif c_count == 4:
                position = position + ''.join(item[0]) + delimiter + ''.join(item[1:3]) + delimiter + ''.join(item[3:])
            elif c_count == 5:
                position = position + ''.join(item[0]) + delimiter + ''.join(item[1:4]) + delimiter + ''.join(item[4:])
            else:
                pass
                # print("不知道", c_count, item)
        return position

    def get_positional_token(self, delimiter="x"):
        pr = self.get_positional_retoken(delimiter)

        token = list(self.tokenize())
        for i in range(len(pr)):
            item = pr[i]
            if item == delimiter:
                token.insert(len(token) - i, delimiter)
        return ''.join(token)

    def get_positional_word(self, delimiter="x"):
        """
        给单词的每个音节分割点植入给定字符
        :return:
        """
        word = list(self.word)
        positional_word = self.get_positional_token(delimiter)
        for index, letter in enumerate(positional_word):
            if letter == delimiter:
                word.insert(index, delimiter)
        return ''.join(word)

    def syllable_count(self):
        """
        理论音节总数
        :return:
        """
        return len(self.tokenize().split("1")) - 1

    def syllabify(self):
        """
        思路：
        1. 把单词向量化，按照元音，辅音 的0，1 值生成token 0100100
        2. 从后往前分析 所以需要反转 retoken 0010010
        3. 把retoken 以元音为分界分组 001 001 0
        4. 按照分音节通用算法进行给retoken 植入分隔符
            - 两个元音之间有1个辅音它属于前面的音节
            - 两个元音之间有2个辅音它一个属于前面的，一个属于后面的
            - 两个元音之间有3个辅音 第一个属于前面的，后两个属于后面的
            - 两个元音之间有4个辅音 第一个属于前面的，其后的两个一组，最后一个属于后面的   【shirkhan 给自己出的规则，目前没有任何凭据这么做，而且是不对的】
            - 两个元音之间有5个辅音 第一个属于前面的，其后的三个一组，最后一个属于后面的   【shirkhan 给自己出的规则，目前没有任何凭据这么做，而且是不对的】

        5. 把嵌入分割符的retoken分割点坐标映射到原始内容上 i -> len(word)-i
        6. 按照分割符切割

        :param word:
        :return:
        """
        delimiter = "x"
        return self.get_positional_word(delimiter).split(delimiter)

    def get_similar_words(self):
        """
        把给定的单词先分音节，然后组合生成单词列表
        :param word:
        :return:
        """
        new_list = []
        syll = self.syllabify()
        for i in range(len(syll)):
            new_word = syll[:len(syll) - i]
            new_list.append(''.join(new_word))
        return sorted(list(set(new_list)))
