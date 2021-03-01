class Reporter:

    def __init__(self, *analyzers):
        self.analyzers = analyzers

    def show(self, **kwargs):
        for analyzer in self.analyzers:
            analyzer.run()
            analyzer.show()
