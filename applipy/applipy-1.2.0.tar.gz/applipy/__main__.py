import os
import json
import sys
from pydoc import locate
from applipy import Application, Config
from applipy_inject import Injector
from applipy.application.application import (
    BindFunction,
    ModuleManager,
    RegisterFunction,
)
from logging import Logger, getLevelName, ERROR

try:
    import yaml
except ImportError:
    yaml = None


class LoadFromConfigModuleManager(ModuleManager):

    def set_application(self, app: Application) -> None:
        self.app = app

    def configure_all(self, bind_function: BindFunction,
                      register_function: RegisterFunction) -> None:
        config = self.injector.get(Config)

        module_names = config.get('app.modules')
        if module_names:
            for module, name in ((locate(name), name) for name in module_names):
                if module:
                    self.app.install(module)
                else:
                    self._log(ERROR, f'Could not load module `{name}`')
                    raise ImportError(name)

        super().configure_all(bind_function, register_function)

    def _log(self, level, *args, **kwargs):
        try:
            self.injector.get(Logger).log(level, *args, **kwargs)
        except Exception:
            print(f"[{getLevelName(level)}]", *args)


def _is_file(path):
    return os.path.isfile(path) or (os.path.exists(path) and not os.path.isdir(path))


def load_config_from_json(config_file):
    if _is_file(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    return config


def load_config_from_yaml(config_file):
    is_file = _is_file(config_file)
    if yaml and is_file:
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)
    else:
        if is_file:
            print('[WARN] Found yaml file but no yaml module installed')
        config = {}
    return config


def load_raw_config(config_path, env):
    return {
        **load_config_from_yaml(os.path.join(config_path, f'{env.lower()}.yaml')),
        **load_config_from_json(os.path.join(config_path, f'{env.lower()}.json')),
    }


def build_config(config_raw):
    config = Config(config_raw)

    provider_names = config.get('config.protocols')
    if provider_names:
        for provider, name in ((locate(name), name) for name in provider_names):
            if provider:
                print(f'[INFO] Adding configuration provider `{name}`')
                config.addProtocol(provider())
            else:
                print(f'[ERROR] Could not load configuration provider `{name}`')
                raise ImportError(name)

    return config


def start(config):
    injector = Injector()
    module_manager = LoadFromConfigModuleManager(injector)
    app = Application(config, injector=injector, module_manager=module_manager)
    module_manager.set_application(app)
    app.run()


def main(config_path, env):
    start(build_config(load_raw_config(config_path, env)))


def main_cmd_yaml(config_file):
    config = load_config_from_yaml(config_file)
    start(build_config(config))


def entrypoint():
    config_file = None
    try:
        idx = sys.argv.index('-f')
        config_file = sys.argv[idx + 1]
    except IndexError:
        config_file = '/dev/stdin'
    except ValueError:
        ...

    if config_file:
        main_cmd_yaml(config_file)
    else:
        main(os.environ.get('APPLIPY_CONFIG_PATH', os.path.curdir), os.environ.get('APPLIPY_ENV', 'DEV'))


if __name__ == '__main__':
    entrypoint()
