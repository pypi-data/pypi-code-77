from py_build.funcs import print_step_name
from py_build import Builder
import subprocess

def build_steps(builder: Builder):
    build_step = builder.composed_step(
        builder.capture_results(print),
        print_step_name(),
    )

    def run(*args):
        return subprocess.run(args, capture_output=True, text=True,).stdout

    @build_step
    def create_virtural_environment():
        return run('python', '-m', 'venv', 'env')