from .slug import AbstractUniqueNameSlug
from .other import AbstractOrdering


class AbstractForeignKeySelect(AbstractUniqueNameSlug, AbstractOrdering):
    class Meta:
        abstract = True
