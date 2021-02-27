from os.path import exists, join
from os import listdir
from shutil import copy

def copy_content (current_dir, target_dir, extension):
    if exists(current_dir) and exists(target_dir):
        current_dir_filename = [f for f in listdir(current_dir)]
        only_extension_files = [f for f in current_dir_filename if f.endswith(extension)]
        for f in only_extension_files:
            copy(join(current_dir, f), target_dir)
        massage = 'Completed'
        return print(massage)
    else:
        massage = 'Some error occur'
        return print(massage)

def main ():
    current_dir = input("Enter your current/scr directory\n")
    target_dir = input("Enter your target/dst directory\n")
    extension = input("Enter the required extension (eg: .txt, .jpg, .exe)\n")
    copy_content(current_dir=current_dir,
                 target_dir=target_dir,
                 extension=extension)
    return

if __name__ == '__main__':
    main()