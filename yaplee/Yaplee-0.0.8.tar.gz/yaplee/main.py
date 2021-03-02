from yaplee.app_manager import Manager
import os
import pathlib
import sys

class Yaplee_Main:
    def __init__(self):
        self.user_path = os.getcwd()
        self.module_path = str(pathlib.Path(__file__).resolve().parent)
        self.argv = [argv.lower() for argv in sys.argv]
        self.argv.pop(0)

        self.manager = Manager(
            self.user_path,
            self.module_path,
            self.argv
        )

        if(self.argv == []):
            self.NoneCommand()

        elif(self.argv[0] == 'create'):
            self.Create()

        else:
            self.UnknownCommand()

    def NoneCommand(self):
        print('Usage: yaplee <command>\nUse help to show all commands')
        sys.exit(0)
    
    def GetArgv(self, index):
        try:
            return self.argv[index]
        except:
            return False
    
    def UnknownCommand(self):
        print('Unknown command : '+str(self.argv[0]).title())
        sys.exit(0)
    
    def Create(self):
        if(len(self.argv) == 1):
            print('Please enter the name of the Yaplee application')
            print('Usage: yaplee create <application name>')
            sys.exit(0)
        
        if(os.path.isdir(self.argv[1])):
            print('Warning: [{}] already exists'.format(str(os.path.join(self.user_path, self.argv[1]))))
            sys.exit(0)

        print('Starting a yaplee application...')
        self.manager.Create(self.argv[1])
        print(self.argv[1].title()+' application was started')
        if(self.GetArgv(2) in ['-c', '--vscode']):
            os.system('code '+str(self.argv[1]))
        sys.exit(0)