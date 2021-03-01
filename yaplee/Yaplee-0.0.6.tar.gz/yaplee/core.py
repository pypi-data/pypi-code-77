import os
import sys
import time
import shutil
import pathlib
import imp
from yaplee.server import Server
from distutils.dir_util import copy_tree
import subprocess
from bs4 import BeautifulSoup

class AppStarter:
    def __init__(self, argv):
        self.__TRUE_PAGE_FILES = ['__init__.py', 'config.py', 'controller.py']
        self.__TRUE_PAGE_FOLDERS = ['static', 'template']
        self.__DAMAGED_APPS = []
        self.__LOADED_PAGES = []
        self.__ERRORS = 0

        self.user_path = os.getcwd()
        self.module_path = str(pathlib.Path(__file__).resolve().parent)
        self.argv = [a.lower() for a in argv]
        self.argv.pop(0)

        self.ScanApplication()
        
        if(self.argv == []):
            print('Usage: python application.py <command>')
            sys.exit(0)

        elif(self.argv[0] == 'run'):
            print('Loading application files...')
            time.sleep(0.5)
            self.RunServer()

        elif(self.argv[0] == 'newpage'):
            if(len(self.argv) == 1):
                print('Usage: python application.py newpage <page name>')
            else:
                print('Creating page...')
                time.sleep(0.5)
                self.NewPage(page_name=self.argv[1])
        else:
            self.UnknownCommand()


    
    def ScanApplication(self):
        for page_r, page_d, page_f in os.walk(os.path.join(self.user_path), 'pages'):
            for page in page_d:
                if(page in self.GetApplicationConfig()['APP_PAGES']):
                    for r,d,f in os.walk(os.path.join(self.user_path, 'pages', str(page))):
                        if(r == os.path.join(self.user_path, 'pages', str(page))):
                            for TAF in self.__TRUE_PAGE_FOLDERS:
                                if(TAF not in d):
                                    self.__DAMAGED_APPS.append(page); self.__ERRORS += 1
                                    continue
                                else:
                                    if(page not in self.__LOADED_PAGES):
                                        self.__LOADED_PAGES.append(page)
                        
                            for TAF in self.__TRUE_PAGE_FILES:
                                if(TAF not in f and page not in self.__DAMAGED_APPS):
                                    self.__DAMAGED_APPS.append(page); self.__ERRORS += 1
                                    continue
                                else:
                                    if(page not in self.__LOADED_PAGES):
                                        self.__LOADED_PAGES.append(page)
                
        if(len(self.__DAMAGED_APPS) > 2):
            self.not_loaded_pages = str(', '.join(self.__DAMAGED_APPS[:2]))+' and '+str(len(self.__DAMAGED_APPS)-2)+' more pages'
        else:
            self.not_loaded_pages = str(', '.join(self.__DAMAGED_APPS))
    
    def GetApplicationConfig(self):
        config = imp.load_source('application.config', os.path.join(self.user_path, 'config.py'))
        return_it = {'APP_PAGES':config.APP_PAGES, 'DEVELOPMENT_SERVER_PORT':config.DEVELOPMENT_SERVER_PORT}
        return return_it

    def Load_Controllers(self, page, server_path):
        try:
            config = imp.load_source('page.config', os.path.join(self.user_path, 'pages', page, 'config.py'))
            app = config.page
            for key, value in app.GetRegisterList().items():
                for i in value:
                    if(i != ''):
                        os.mkdir(server_path+'/'+i)
                section = app.GetSections()[key]
                for url in value:
                    for template in section['templates']:
                        sub_path = server_path+'/'+url if url != '' else server_path
                        shutil.copy(
                            'pages/'+section['page_name']+'/template/'+template,
                            sub_path+'/'+template
                        )
                    with open(sub_path+'/'+template, 'r+') as template_file:
                        template_content = template_file.read()
                        soup = BeautifulSoup(template_content, 'html.parser')

                    for static in section['statics']:
                        link_style = soup.new_tag('link')
                        link_style['rel'] = 'stylesheet'
                        link_style['href'] = static
                        soup.head.append(link_style)

                    with open(sub_path+'/'+template, 'w+') as template_file:
                        template_file.write(soup.prettify())
                        
                    for static in section['statics']:
                        shutil.copy(
                            'pages/'+section['page_name']+'/static/'+static,
                            sub_path+'/'+static
                        )
        except:
            pass
        

    def RunServer(self):
        print(
            'No error found in the application'
            if self.__DAMAGED_APPS == [] else
            str(self.__ERRORS)+' errors were found in the application, ('+str(self.not_loaded_pages)+') were not loaded.'
        )
        print('Note: Use CTRL+C to quit development server')
        server = Server(int(self.GetApplicationConfig()['DEVELOPMENT_SERVER_PORT']))
        try:
            server.CheckSystem()
            if(self.__LOADED_PAGES == []):
                print('There is no page to run! Stopping WebServer...')
                sys.exit()
            for page in self.__LOADED_PAGES:
                self.Load_Controllers(page, server.server_foldername) # Load Pages
            subprocess.run('python -m http.server '+str(self.GetApplicationConfig()['DEVELOPMENT_SERVER_PORT'])+' --bind 127.0.0.1 --directory "'+str(os.path.join(self.user_path, 'pages', '.server'))+'"')
        except KeyboardInterrupt:
            server.Stop()
            
    def UnknownCommand(self):
        print('Unknown command : '+str(self.argv[0]).title())
        sys.exit(0)

    def NewPage(self, page_name):
        if(os.path.isdir(os.path.join(self.user_path, 'pages', str(page_name)))):
            print('There is already a page with this name')
            sys.exit(0)
        os.mkdir(os.path.join(self.user_path, 'pages', str(page_name)))
        copy_tree(
            os.path.join(self.module_path, 'app', 'Blank'),
            os.path.join(self.user_path, 'pages', str(page_name))
        )
        with open(os.path.join(self.module_path, 'app', 'Blank', 'config.py'), 'r+') as config_text:
            with open(os.path.join(self.user_path, 'pages', str(page_name), 'config.py'), 'w+') as config:
                config.write(config_text.read().replace('[PAGE_NAME]', str(page_name)))
        print(str(page_name).title()+' page created')