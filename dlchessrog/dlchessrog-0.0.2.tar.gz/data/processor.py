from __future__ import absolute_import

# tag::base_imports[]
import os.path
import tarfile
import gzip
import glob
import shutil
import sys
import chess
import chess.pgn

import numpy as np
from keras.utils import to_categorical
# end::base_imports[]
from sample import Sampler
from generator import DataGenerator
sys.path.append('/Users/rogermcgrath/Desktop/dlchess/encoders')
from oneplane import OnePlaneEncoder

class ChessDataProcessor:
    def __init__(self, encoder='oneplane', data_directory='data'):
        self.encoder = OnePlaneEncoder((8,8))
        self.data_dir = data_directory
# end::processor_init[]

# tag::load_go_data[]
    def load_chess_data(self, data_type='train', num_samples=1000,
                     use_generator=False):

        sampler = Sampler(data_dir=self.data_dir)
        data = sampler.draw_data(data_type, num_samples)

        zip_names = set()
        for filename in data:
            if not filename == '.DS_Store':
                zip_names.add(filename)  # <5>
        for zip_name in zip_names:
            base_name = zip_name.replace('.pgn', '')
            data_file_name = base_name + data_type
            if not os.path.isfile(self.data_dir + '/' + data_file_name):
                self.process_zip(zip_name, data_file_name)
        if use_generator:
            generator = DataGenerator(self.data_dir, data)
            return generator  # <2>
        else:
            features_and_labels = self.consolidate_games(data_type, data)
            return features_and_labels  # <3>

# <1> As `data_type` you can choose either 'train' or 'test'.
# <2> `num_samples` refers to the number of games to load data from.
# <3> We download all games from KGS to our local data directory. If data is available, it won't be downloaded again.
# <4> The `Sampler` instance selects the specified number of games for a data type.
# <5> We collect all zip file names contained in the data in a list.
# <6> Then we group all SGF file indices by zip file name.
# <7> The zip files are then processed individually.
# <8> Features and labels from each zip are then aggregated and returned.
# end::load_go_data[]

# tag::unzip_data[]

# <1> Unpack the `gz` file into a `tar` file.
# <2> Remove ".gz" at the end to get the name of the tar file.
# <3> Copy the contents of the unpacked file into the `tar` file.
# end::unzip_data[]

# tag::read_sgf_files[]
    def process_zip(self, zip_file_name, data_file_name):
        total_examples = self.num_total_examples(zip_file_name)  # <1>
        shape = self.encoder.shape()  # <2>
        feature_shape = np.insert(shape, 0, np.asarray([total_examples]))
        features = np.zeros(feature_shape)
        labels = np.zeros((total_examples,))

        counter = 0
        pgn = open(self.data_dir + '/' + zip_file_name)
        game = chess.pgn.read_game(pgn)
        board = chess.Board()
        for move in game.mainline_moves():
            if counter == total_examples:
                break
            board.push(move)
            features[counter] = self.encoder.encode(board)
            labels[counter] = self.encoder.encode_point(move)
            counter += 1

        feature_file_base = self.data_dir + '/' + data_file_name + '_features_%d'
        label_file_base = self.data_dir + '/' + data_file_name + '_labels_%d'

        chunk = 0  # Due to files with large content, split up after chunksize
        chunksize = 40
        while features.shape[0] >= chunksize:  # <1>
            feature_file = feature_file_base % chunk
            label_file = label_file_base % chunk
            chunk += 1
            current_features, features = features[:chunksize], features[chunksize:]
            current_labels, labels = labels[:chunksize], labels[chunksize:]  # <2>
            np.save(feature_file, current_features)
            np.save(label_file, current_labels)  # <3>
# <1> We process features and labels in chunks of size 1024.
# <2> The current chunk is cut off from features and labels...
# <3> ...  and then stored in a separate file.
# end::store_features_and_labels[]

# tag::consolidate_games[]
    def consolidate_games(self, data_type, samples):
        files_needed = set(file_name for file_name in samples)
        file_names = []
        for zip_file_name in files_needed:
            file_name = zip_file_name.replace('.pgn', '') + data_type
            file_names.append(file_name)

        feature_list = []
        label_list = []
        for file_name in file_names:
            file_prefix = file_name.replace('.pgn', '')
            base = self.data_dir + '/' + file_prefix + '_features_*.npy'
            for feature_file in glob.glob(base):
                label_file = feature_file.replace('features', 'labels')
                x = np.load(feature_file)
                y = np.load(label_file)
                x = x.astype('float32')
                y = to_categorical(y.astype(int), 64 * 64)
                feature_list.append(x)
                label_list.append(y)
        features = np.concatenate(feature_list, axis=0)
        labels = np.concatenate(label_list, axis=0)
        np.save('{}/features_{}.npy'.format(self.data_dir, data_type), features)
        np.save('{}/labels_{}.npy'.format(self.data_dir, data_type), labels)

        return features, labels

    def num_total_examples(self, zip_file):
        total_examples = 0
        pgn = open(self.data_dir + '/' + zip_file)
        game = chess.pgn.read_game(pgn)
        board = chess.Board()
        num_moves = 0
        for move in game.mainline_moves():
            if move in board.pseudo_legal_moves:
                board.push(move)
                num_moves += 1
            else:
                break
        total_examples = total_examples + num_moves
        return num_moves