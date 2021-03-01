from .gitlist import GitList

def main():
    import sys

    try:
        directory = sys.argv[1]
    except IndexError:
        directory = "."
    gl = GitList()
    gl.ready()
    gl.find(directory)
