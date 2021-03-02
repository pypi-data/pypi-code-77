from distutils.dir_util import copy_tree
from yaplee.defaults import HELLOWORLD_CSS, HELLOWORLD_TEMPLATE
import shutil
import time
import os

class Manager:
    def __init__(self, user_path, module_path, argv):
        self.user_path = user_path
        self.module_path = module_path
        self.argv = argv

    def clearCache(self, path):
        for directories, subfolder, files in os.walk(path):
            if os.path.isdir(directories):
                if directories[::-1][:11][::-1] == '__pycache__':
                                shutil.rmtree(directories)
    
    def Create(self, app_name):
        copy_tree(
            os.path.join(str(self.module_path), 'app', 'HelloWorld'),
            os.path.join(str(self.user_path), str(app_name))
        )
        time.sleep(0.5)
        self.clearCache(os.path.join(str(self.user_path), str(app_name)))
        os.unlink(os.path.join(str(self.user_path), str(app_name), '__init__.py'))
        with open(os.path.join(str(self.user_path), str(app_name), 'pages', 'HelloWorld', 'static', 'style.css'), 'w+') as style:
            style.write(HELLOWORLD_CSS)
        with open(os.path.join(str(self.user_path), str(app_name), 'pages', 'HelloWorld', 'template', 'index.html'), 'w+') as templtae:
            templtae.write(HELLOWORLD_TEMPLATE)