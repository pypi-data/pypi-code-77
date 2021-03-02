import sys
import os
import pathlib

class PageController:
    def __init__(self, page_name):
        self.__PAGE = page_name
        self.__SECTIONS = {}
        self.__URLS = {}
        self.user_path = os.getcwd()
        self.module_path = str(pathlib.Path(__file__).resolve().parent)

    def Section(self, name):
        if(name in self.__SECTIONS):
            print(str(name)+' section can\'t be defined more than once!')
            sys.exit(0)

        self.__SECTIONS[name] = {
            'page_name':self.__PAGE,
            'templates':[],
            'statics':[]
            }
        
        self.__URLS[name] = []
    
    def Template(self, path, section):
        AVALIABLE_TEMPLATES = []

        for root, directory, file_ in os.walk(os.path.join(self.user_path, 'pages', str(self.__PAGE), 'template')):
            for f in file_:
                if(f != '__init__.py'):
                    AVALIABLE_TEMPLATES.append(f)
        
        if(path not in AVALIABLE_TEMPLATES):
            print('Template ['+self.__PAGE+':'+path+'] not found!')
            sys.exit(0)

        if(section not in self.__SECTIONS):
            print('Section ['+self.__PAGE+':'+section+'] not found!')
            sys.exit(0)
        
        self.__SECTIONS[section]['templates'].append(path)
        
    def Static(self, path, section):
        AVALIABLE_STATICS = []

        for root, directory, file_ in os.walk(os.path.join(self.user_path, 'pages', str(self.__PAGE), 'static')):
            for f in file_:
                if(f != '__init__.py'):
                    AVALIABLE_STATICS.append(f)
        
        if(path not in AVALIABLE_STATICS):
            print('Static file ['+self.__PAGE+':'+path+'] not found!')
            sys.exit(0)

        if(section not in self.__SECTIONS):
            print('Section ['+self.__PAGE+':'+section+'] not found!')
            sys.exit(0)
        
        self.__SECTIONS[section]['statics'].append(path)
    
    def Register(self, section, url):
        self.__URLS[section].append(url)
    
    def GetRegisterList(self):
        return self.__URLS
    
    def GetSections(self):
        return self.__SECTIONS