#!/usr/bin/env python3

# Gitlist will walk the directory tree from the current directory, looking for
# git repos. It will report back repos with untracked files, uncommitted
# changes.

import subprocess
import os


class NotReadyError(Exception):
    pass


class Display:
    def __init__(self, mode):
        self.mode = mode
        self.m = None
        self.width1 = 60
        self.width = 30
        self.col2 = False

    def msg(self, m, column):
        col2 = False
        if column == 1:
            spaces = " " * (self.width1 - len(m))
            m = "\33[0;32m" + m + "\33[0m"
            self.m = m + spaces
        elif column == 2:
            spaces = " " * (self.width - len(m))
            m = "\33[1;33m" + m + "\33[0m"
            self.m += m + spaces
            self.col2 = True
        elif column == 3 and self.col2:
            m = "\33[1;33m" + m + "\33[0m"
            self.m += m
        elif column == 3 and not self.col2:
            m = "\33[1;33m" + m + "\33[0m"
            self.m += " " * self.width
            self.m += m

    def flush(self):
        output = self.m
        self.m = None
        self.col2 = False
        return output


class GitList:
    def ready(self):
        # Assert preconditions: git installed
        result = subprocess.run(["which", "git"], capture_output=True, text=True)
        if "git" in result.stdout:
            return True
        else:
            raise NotReadyError("Git is not installed")

    def find(self, start_directory):
        out = Display("console")
        found = False
        for directory, subdirs, files in os.walk(start_directory):
            if "vendor" in subdirs:
                subdirs.remove("vendor")
            if ".git" in subdirs or ".git" in files:
                found = True
                out.msg("{d}/".format(d=directory), 1)
                if self.uncommitted_change(directory):
                    out.msg(" -- has uncommitted changes", 2)
                if self.unpushed_changes(directory):
                    out.msg(" -- has unpushed local changes", 3)
                print(out.flush())

        return found

    def uncommitted_change(self, directory):
        cwd = os.getcwd()
        os.chdir(directory)
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        os.chdir(cwd)
        if "modified" in result.stdout or "untracked" in result.stdout:
            return True
        else:
            return False

    def unpushed_changes(self, directory):
        cwd = os.getcwd()
        os.chdir(directory)
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        os.chdir(cwd)
        if "ahead" in result.stdout:
            return True
        else:
            return False

    def main():
        import sys

        try:
            directory = sys.argv[1]
        except IndexError:
            directory = "."
        gl = GitList()
        gl.ready()
        gl.find(directory)


if __name__ == "__main__":
    import sys

    try:
        directory = sys.argv[1]
    except IndexError:
        directory = "."
    gl = GitList()
    gl.ready()
    gl.find(directory)
