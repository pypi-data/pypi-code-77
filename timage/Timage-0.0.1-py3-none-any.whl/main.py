# Created by Hayk_Sardaryan at 03.12.2020 / 23:43
from time import time
from string import ascii_letters, digits, whitespace
import numpy as np
from PIL import Image
from change_system import ChangeSystem
from functools import wraps


class Decorators:
    @staticmethod
    def decor_time(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = time()
            func(*args, **kwargs)
            stop = time()
            print(func.__name__, 'work time: ', stop - start)
        return inner


class Text2Image:

    # x.shape[0] * x.shape[1] * 0.6
    # in A4 list 14 font are 1800 symbols
    # with this script you can put 54000 symbols into 300*300 pixels photo or 30 A4 list
    # 50*60 img is 1 A4

    def __init__(self):
        self.text_ternary = ''

    def _open_image(self, image):
        with Image.open(image) as img:
            self.x = np.array(img)
            self.max_length_text = int(self.x.shape[0] * self.x.shape[1] * 0.6)

    def _image_reshape(self):
        self.sk_shape = self.x.shape
        self.x = self.x.reshape(self.sk_shape[0] * self.sk_shape[1], self.sk_shape[2])

    def __shifr(self, pix):
        d = {"0": [0, 0, -1, -2, 1, 0, 0, -1, -2, 1], "1": [2, 1, 0, 0, -1, -2, 1, 0, 0, -1],
             "2": [-1, -2, 2, 1, 0, -1, -2, 2, 1, 0]}
        pix = str(pix)
        do = d[self.text_ternary[0]][int(pix[-1])]
        self.text_ternary = self.text_ternary[1:]
        return int(pix) + do

    def _open_text_file(self, text_file):
        text = ''
        with open(text_file) as f:
            for i in f.readlines():
                text += i
        if self._is_english_words_and_len_correct(text):
            return text
        else:
            raise ValueError('in text must be only latin letters and whitespaces')

    def _cut_white_and_black(self, text):
        for i in range((len(text) * 5 // 3) + 3):
            for k in range(3):
                if self.x[i][k] in (0, 1):
                    self.x[i][k] = 2
                if self.x[i][k] in (254, 255):
                    self.x[i][k] = 253

    def _text_to_ternary(self, text):
        text += "`"
        for t in text:
            self.text_ternary += str(ChangeSystem(str(ord(t)), 10, 3))
        self.tt_len = len(self.text_ternary)

    def _update_image(self):
        for j in range((self.tt_len // 3) + 1):
            try:
                for k in range(3):
                    self.x[j][k] = self.__shifr(int(self.x[j][k]))
            except:
                break

    def _reshape_and_save(self, image):
        self.x = self.x.reshape(self.sk_shape)
        s_image = Image.fromarray(self.x)
        s_image.save(image, format='png')

    def _is_english_words_and_len_correct(self, text):
        accepted_cars = ascii_letters + digits + r"""!"#$%&'()*+,-./:;<=>?@[\]^_{|}~""" + whitespace
        for i in text:
            if i not in accepted_cars:
                # raise ValueError(
                #     f"in text must be only <<{accepted_cars[:-5]}>> and whitespaces")
                print(f"in text must be only << {accepted_cars[:-5]} >> and whitespaces")
                return False

        if len(text) > self.max_length_text:
            print("length of your text too long: It must be small than (image_width * image_height * 0.6)")
            return False
            # raise ValueError("length of your text too long: It must be small than (image_width * image_height * 0.6)")
        return True

    @Decorators.decor_time
    def code(self, text_file_name, image):
        secret_image = f's_{image.split(".")[0]}.png'
        self._open_image(image)
        text = self._open_text_file(text_file_name)
        self._is_english_words_and_len_correct(text)
        self._image_reshape()
        self._cut_white_and_black(text)
        self._text_to_ternary(text)
        self._update_image()
        self._reshape_and_save(secret_image)
        print(f'done code -> {secret_image}')

    ############# DECODE #################################### DECODE #################### DECODE #######################
    #                                                                                                                  #
    #                                                 DECODE                                                           #
    #                                                                                                                  #
    ###### DECODE ##################### DECODE ############################### DECODE ##################################

    @staticmethod
    def __decode(cod):
        if cod in "0156":
            return 0
        elif cod in '2378':
            return 1
        elif cod in '49':
            return 2

    def _get_cod_of_text(self, max_shape):  # to go until max shape of image (all pixels), because we don't
        # know length of the text max_shape*3
        self.decodnoc = ''
        for j in range(max_shape):
            for k in range(3):
                self.decodnoc += str(self.__decode(str(int(self.x[j][k]))[-1]))
        self.sentence = ''

    def _get_text(self, secret_filename):
        for i in range(len(self.decodnoc)):
            try:
                a = self.decodnoc[:5]
                self.sentence += chr(int(ChangeSystem(a, 3, 10)))
                if chr(int(ChangeSystem(a, 3, 10))) == "`":
                    break
                self.decodnoc = self.decodnoc[5:]
            except Exception as e:
                break
        self.sentence = self.sentence[:-1]
        try:
            with open(secret_filename, 'w') as file:
                file.write(self.sentence)
        except:
            print(self.sentence)

    def _is_max_shape(self, max_char):
        if not max_char:
            max_shape = self.x.shape[0] * self.x.shape[1]  # max shape of image-vector
        elif max_char < self.x.shape[0] * self.x.shape[1]:
            max_shape = int(max_char * 5 / 3)
        else:
            raise ValueError('max_char must be small than (image_width * image_height * 0.6)')
        return max_shape

    @Decorators.decor_time
    def decode(self, secret_image_name, max_char=None, secret_filename='secret.txt'):
        self._open_image(secret_image_name)
        max_shape = self._is_max_shape(max_char)
        self._image_reshape()
        self._get_cod_of_text(max_shape)
        self._get_text(secret_filename)
        print(f'done decode -> {secret_filename}')


# if __name__ == '__main__':
    # A = Text2Image()
    # A.code('abc.txt', 'img.png')
    # A.decode('s_img.png', max_char=2500)
