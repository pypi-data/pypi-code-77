from doctrans.models.option import Option


SUPPORT_EXCEPTION_MESSAGE = "NOT SUPPORTED WITH THIS OPTION."


class Translator:
    def __init__(self, option: Option):
        if not self.support(option):
            raise Exception(SUPPORT_EXCEPTION_MESSAGE)
        self.option = option

    @classmethod
    def support(cls, option: Option) -> bool:
        raise NotImplementedError

    def read(self, input_path: str) -> None:
        raise NotImplementedError

    def translate(self) -> None:
        raise NotImplementedError

    def save(self, output_path: str) -> None:
        raise NotImplementedError

    def run(self, input_path: str, output_path: str) -> None:
        self.read(input_path)
        self.translate()
        self.save(output_path)
