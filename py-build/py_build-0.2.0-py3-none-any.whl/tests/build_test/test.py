from py_build import Builder
from py_build.funcs import print_step_name

def build_steps(builder: Builder):
    step = builder.composed_step(print_step_name(), builder.capture_results(print))

    @builder.capture_results(print)
    def test_me(*args):
        return ", ".join(args)

    @step
    def step_1():
        test_me('hello', 'world')
        test_me('bye')
        return 'Done'

    @step
    def step_2():
        test_me('bye', 'moon')
        test_me('hello')
        return 'Done'