from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class Copy(Function):
    """Copy files and folder."""

    src = Inputs.path(
        description='Path to a input file or folder.', path='input_path'
    )

    @command
    def copy_file(self):
        return 'echo copying input path...'

    dst = Outputs.path(
        description='Output file or folder.', path='input_path'
    )
