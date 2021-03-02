import sys

def yaplee_app():
    try:
        from yaplee.core import AppStarter
    except ImportError as as_exec:
        raise ImportError(
            "There is a problem importing yaplee, "
            "Please make sure yaplee is installed"
        ) from as_exec
    AppStarter(sys.argv)

if __name__ == '__main__':
    yaplee_app()