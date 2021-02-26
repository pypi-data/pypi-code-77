import os 
import requests
from zipfile import ZipFile
import shutil
from IPython.display import display, Markdown
import pandas as pd
import yaml

class Citable:

    def __init__(self, DOI):
        
        # constructing the download url from the given DOI:
        self.doi = DOI.split('/')[-1].split('.')[1]
        self.url = 'https://zenodo.org/api/records/' + self.doi
        
        # make a data folder in the current directory if it not already exists:
        if not os.path.isdir('./data'):
            os.mkdir('./data')
    
    def download(self, showMarkdown = True, pandas = True):
        
        '''
        showMarkdown: Boolean, by default set to True, if you don't want the markdown displayed, insert the argument showMarkdown = False into the download function
        pandas: Boolean, by default set to True, if you don't want to return a list containing pandas DataFrames but rather want to do your own thing and just want to know where the downloaded data was stored, insert the argument pandas = False into the download function
        '''
        
        # retrieve the data from the url via requests:
        r = requests.get(self.url)
        
        # make a list of all the files contained under the url:
        links = [i['links']['self'] for i in r.json()['files']]
        
        # check which of the files of the url is already in the local data folder in the current directory, files already in the local data directory will not be downloaded again:
        linksfiles = [i['links']['self'] for i in r.json()['files'] if not (os.path.isfile('./data/' + i['key']) or os.path.isfile('./data/' + '.'.join(i['key'].split('.')[:-1])))]
        if not linksfiles:
            print('All files you want to download are already in the local data folder.\n')
        else:
            # for all the files not already downloaded, going through all links, download and extract all files:
            for URL in linksfiles:
                try:
                    dl = requests.get(URL)

                    # if the data is contained in a zip file, write the file into the 'data'-folder and name it test.zip:
                    if URL.split('.')[-1] == 'zip':
                        with open('./data/test.zip', 'wb') as f:  
                            f.write(dl.content)

                        # extract zip-file into data-folder
                        zf = ZipFile('./data/test.zip', 'r')
                        zf.extractall('./data')
                        zf.close()

                        # removing original zip-file and '__MACOSX'-folder, if it exists:
                        os.remove('./data/test.zip') 
                        if os.path.isdir('./data/__MACOSX'):
                            shutil.rmtree('./data/__MACOSX')
                            
                    # if the data is not in a zip file save the content of the download under is original file name:
                    else:
                        with open('./data/' + URL.split('/')[-1], 'wb') as f:  
                            f.write(dl.content)
                    print('Successfully downloaded and extracted data under ' + URL)
                except:
                    print('Something went wrong while downloading and extracting data under ' + URL) 
        
        # make a dictionary of all downloaded files and the path to which they have been downloaded:
        ds = []
        files = ['./data/' + URL.split('/')[-1].replace('.zip', '') for URL in links]
        dictDownload = {file.replace('./data/', ''): file for file in files}
        
        # filter out the files which are either json, csv or md because they will prepared for making a pandas object of them or being displayed via IPython.display:
        fil = [URL.split('/')[-1].replace('.zip', '') for URL in links if (URL.split('/')[-1].replace('.zip', '').split('.')[-1] == 'json' or URL.split('/')[-1].replace('.zip', '').split('.')[-1] == 'csv' or URL.split('/')[-1].replace('.zip', '').split('.')[-1] == 'md')]
        
        # go through all these files and open them as a pandas object (json, csv) or display them via IPython.display (md):
        for file in fil:         
            # making path and file extension:
            path = './data/' + file
            ending = path.split('.')[-1]

            # process file according to ending, json and csv are turned into DataFrames and md will be displayed if not manually disabled:
            if ending == 'json':
                try:
                    d = pd.read_json(path, orient = 'table')
                except:
                    d = pd.read_json(path)
            if ending == 'csv':
                try:
                    d = pd.read_csv(path, delimiter = ',')
                except:
                    d = pd.read_csv(path, delimiter = '\t')
            if ending == 'md':
                with open(path, encoding="utf8") as file:
                    d = file.read()
                if showMarkdown:
                    display(Markdown(d))
            
            # write all DataFrames and strings into a list:
            ds.append(d)
        
        # If you are working with pandas return a list of the suitable data converted into pandas DataFrames might be very handy for you. So this option returns a list of strings or DataFrames:
        if pandas:
            print('The download returns a list of either strings or DataFrames.')    
            print('List elements are in the order: ' + ', '.join(fil) + '\nIn order to work with the first element from the list "name_of_list", write: name_of_list[0].')        
            return ds
        
        # If you you are working with a different data handler than pandas or you just want to download the data and treat it afterwards in your style, this option will just return a dictionary where the data has been stored.
        else:
            print('The dictionary shows where the downloaded data has been stored: ' + str(dictDownload) + '\n')
            return dictDownload
        