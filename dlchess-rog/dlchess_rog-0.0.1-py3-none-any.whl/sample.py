from __future__ import print_function
from __future__ import absolute_import
import os
import random
import chess 
import chess.pgn
import requests


class Sampler:
    """Sample training and test data from zipped sgf files such that test data is kept stable."""
    def __init__(self, data_dir, num_test_games=100, seed=1337, gamers=['Hikaru','AlexandraBotez','GothamChess','FabianoCaruana', 'DanielNaroditsky', 'Jospem', 'exoticprincess'], month=['01','02''03','04','05','06','07','08','09','10','11','12'], year='2020'):
        self.data_dir = data_dir
        self.num_test_games = num_test_games
        self.test_games = []
        self.train_games = []
        self.test_folder = '/Users/rogermcgrath/Desktop/dlchess/data/test'
        self.gamers = gamers
        self.month = month
        self.year = year
        random.seed(seed)
        self.compute_test_samples()

    def draw_data(self, data_type, num_samples):
        if data_type == 'test':
            return self.test_games
        elif data_type == 'train' and num_samples is not None:
            return self.draw_training_samples(num_samples)
        elif data_type == 'train' and num_samples is None:
            return self.draw_all_training()
        else:
            raise ValueError(data_type + " is not a valid data type, choose from 'train' or 'test'")

    def draw_samples(self, num_sample_games):
        """Draw num_sample_games many training games from index."""
        # self.get_games(self.data_dir,self.gamers, self.month, self.year)
        available_games = []
        for subdir, dirs, files in os.walk(self.data_dir):
            for file in files:
                available_games.append(file)
        print('>>> Total number of games used: ' + str(len(available_games)))
        
        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in sample_set:
                sample_set.add(sample)
        print('Drawn ' + str(num_sample_games) + ' samples:')
        return list(sample_set)

    def draw_training_games(self):
        """Get list of all non-test games, that are no later than dec 2014
        Ignore games after cap_year to keep training data stable
        """
        available_games = []
        self.get_games(self.data_dir,self.gamers, self.month, self.year)
        print(self.data_dir)
        for subdir, dirs, files in os.walk(self.data_dir):
            for file in files:
                available_games.append(file)
        
        sample_set = set()
        while len(sample_set) < len(available_games):
            sample = random.choice(available_games)
            if sample not in sample_set:
                self.train_games.append(sample)
        print('Drawn ' + str(len(self.train_games)) + ' samples:')

    def compute_test_samples(self):
        """If not already existing, create local file to store fixed set of test samples"""
        for subdir, dirs, files in os.walk(self.test_folder):
            for file in files:
                self.test_games.append(file)

    def draw_training_samples(self, num_sample_games):
        """Draw training games, not overlapping with any of the test games."""
        available_games = []
        self.get_games(self.data_dir,self.gamers, self.month, self.year)
        for subdir, dirs, files in os.walk(self.data_dir):
            for file in files:
                available_games.append(file)
        
        sample_set = set()
        for i in range(num_sample_games):
            sample = random.choice(available_games)
            if sample not in sample_set:
                self.train_games.append(sample)
        print('Drawn ' + str(len(self.train_games)) + ' samples:')
        return(self.train_games)

    def draw_all_training(self):
        """Draw all available training games."""
        available_games = []
        self.get_games(self.data_dir,self.gamers, self.month, self.year)
        for subdir, dirs, files in os.walk(self.data_dir):
            for file in files:
                available_games.append(file)
        
        sample_set = set()
        for samples in available_games:
            sample = random.choice(available_games)
            if sample not in sample_set:
                self.train_games.append(sample)
        print('Drawn ' + str(len(self.train_games)) + ' samples:')

    def get_games(self, data_directory, gamers, months, year):
        if data_directory == '/Users/rogermcgrath/Desktop/dlchess/data/training':
            for gamer in gamers:
                for month in months:
                    link = 'https://api.chess.com/pub/player/' + gamer + '/' + 'games' + '/' + year + '/' + month + '/' + 'pgn'
                    pgns = requests.get(link)
                    print(data_directory + '/' + gamer + '_' + month + '.pgn')
                    write = open(data_directory + '/' + gamer + '_' + month + '.pgn', 'w')
                    write.write(pgns.text)
                    pgn = open(data_directory + '/' + gamer + '_' + month + '.pgn')
                    coutner = 0
                    while True:
                        headers = chess.pgn.read_headers(pgn)
                        if headers is None:
                            break
                        # elif gamer == 'Hikaru' and coutner == 122 or coutner == 41 or coutner == 34 or coutner == 33 or coutner == 32:
                        #     coutner += 1
                        #     break
                        file = open(data_directory + '/' + gamer + '_' + month + str(coutner) + '.pgn', 'w')
                        file.write(str(chess.pgn.read_game(pgn)))
                        coutner += 1
                    os.remove(pgn)
                gamer = ['Carlsen', 'Morphy']
                for game in gamer:
                    pgn = open(data_directory + '/' + game + '.pgn')
                    print(str(pgn))
                    coutner = 0 
                    while True:
                        headers = chess.pgn.read_headers(pgn)
                        if headers is None:
                            break
                        file = open(data_directory + '/' + game + '_' + str(coutner) + '.pgn', 'w')
                        file.write(str(chess.pgn.read_game(pgn)))
                        coutner += 1
                    os.remove(pgn)
        else:
            gamer = ['Caruana','Grischuk','Huebner','Kasparov','Nakamura']
            for game in gamer:
                pgn = open(data_directory + '/' + game + '.pgn')
                print(str(pgn))
                coutner = 0 
                while True:
                    headers = chess.pgn.read_headers(pgn)
                    if headers is None:
                        break
                    file = open(data_directory + '/' + game + '_' + str(coutner) + '.pgn', 'w')
                    file.write(str(chess.pgn.read_game(pgn)))
                    coutner += 1
                os.remove(pgn)

