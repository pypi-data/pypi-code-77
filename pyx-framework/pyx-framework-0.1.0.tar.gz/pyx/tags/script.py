from .default import DEFAULT_TAG
from ..utils import __extra__


@DEFAULT_TAG
class script:
    def __init__(self, scoped=True, children='', src='', **kwargs):
        self.scoped = scoped
        self.children = children
        self.src = src
        self.kwargs = kwargs

    def __render__(self, tag):
        if not self.scoped:
            __extra__.js += str(tag.kw.pop('children'))
            return
        return tag.__render__(self.children)
