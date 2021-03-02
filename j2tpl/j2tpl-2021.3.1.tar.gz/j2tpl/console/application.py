from cleo.application import Application as BaseApplication
from j2tpl import __name__, __version__
from j2tpl.loaders.lazy_command_loader import LazyCommandLoader


class Application(BaseApplication):
    def __init__(self) -> None:
        super(Application, self).__init__(__name__, __version__)

        self.set_display_name(__name__)
        self.set_command_loader(LazyCommandLoader(__name__))


def main() -> int:
    return Application().run()


if __name__ == "__main__":
    main()
