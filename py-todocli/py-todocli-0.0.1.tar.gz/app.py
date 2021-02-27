import os.path
from Commands import commandsDict


def parse(command):
    '''
    Takes the command as input and returns the command name and args
    '''
    cmd_list = command.split()
    cmd_type = cmd_list[0]
    if (cmd_type == 'help' or cmd_type == 'quit' or cmd_type == 'exit'):
        return cmd_type, []
    elif (cmd_type == './todo'):
        cmd_name = cmd_list[1]
        if (cmd_name in ['add', 'ls', 'del', 'done', 'help', 'report']):
            return cmd_name, cmd_list[2:]
        else:
            return 'invalid', []
    else:
        return 'invalid', []


def main():
    t = open('todo.txt', 'w')
    d = open('done.txt', 'w')
    with open('help.txt', 'r') as help_file:
        print(help_file.read())

    while(1):
        command = input('$ ')
        # command name, command args
        # split the string separated by space
        command_name, command_args = parse(command)
        if(command_name == 'quit' or command_name == 'exit'):
            break
        elif(command_name == 'help'):
            with open('help.txt', 'r') as help_file:
                print(help_file.read())
        else:
            commandsDict[command_name](command_args)


if __name__ == '__main__':
    main()
