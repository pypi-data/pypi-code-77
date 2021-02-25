import fileinput #replace into files
import Freya_alerce.catalogs # __path__
import os

"""
Class to replace words in files.
"""
class ListFiles(object):

    def replace_in_files(self,paths,raplace_word,word):
        """
        Replace a 'word' for 'new word' in specific file.
        """
        self.list_path = paths
        self.replace_word = raplace_word
        self.word = word
        for file in self.list_path:
            with fileinput.FileInput(f'{file}', inplace=True) as file_:
                for line in file_:
                    print(line.replace(f'{self.replace_word}', f'{self.word}'), end='')
    
    def files_api(self):
        """
        Return names files use in api.
        """
        return ['configure.py','__init__.py']

    def files_db(self):
        """
        Return names files use in data base.
        """
        return ['configure.py','connect.py','__init__.py']
