from .tracking import AbstractDeleteTime
from .uuid import AbstractUUID
from .slug import AbstractUniqueNameSlug
from .other import AbstractOrdering


class AbstractForeignKeySelect(AbstractUniqueNameSlug, AbstractDeleteTime, AbstractUUID, AbstractOrdering):

    class Meta:
        abstract = True
