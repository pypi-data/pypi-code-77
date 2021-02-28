from py_build.funcs import print_step_name
from typing import Callable, List
from py_build import Builder
import pathlib

def build_steps(builder: Builder):
    build_step = builder.composed_step(
        builder.capture_results(print),
        print_step_name(),
    )

    @build_step
    def remove_residual_files():
        remove_in = [
            pathlib.Path('dist'),
            pathlib.Path('py_build.egg-info'),
        ]
        def remove(remove_in: List[pathlib.Path]):
            for file in remove_in:
                if file.is_dir():
                    remove(file.glob('*'))
                    try:
                        file.rmdir()
                    except OSError as ex:
                        print(ex.strerror.strip(), ': ' , ex.filename, sep='')
                        continue
                else:
                    try:
                        file.unlink()
                    except OSError as ex:
                        print(ex.strerror, ': ' , ex.filename, sep='')
                        continue
                print('Removed: ' + str(file))
        remove(remove_in)
        return "[Removed files]\n"
