import types
from typing import List

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl.field import Boolean, Date, Float, Integer, Keyword, Text
from mongoengine import fields as mongo_fields


def generate_default_mongo_field_dict():
    mongo_dict = {
        mongo_fields.StringField: Text,
        mongo_fields.ListField: Keyword,
        mongo_fields.IntField: Keyword,
        mongo_fields.BooleanField: Boolean,
        mongo_fields.ObjectIdField: Keyword,
    }
    return mongo_dict


def create_or_update_from_mongo(cls, data: dict):
    properties: dict = cls._doc_type.mapping.properties.to_dict().get("properties", {})

    _id = data.pop("_id")
    try:
        obj = cls.get(id=_id)
    except NotFoundError:
        obj = cls()
        obj.meta.id = _id
    for k, v in data.items():
        if k in properties:
            obj[k] = v
    obj.save()
    return obj


# def post_mongo_save(cls, sender, document, **kwargs):
#     cls.create_or_update_from_mongo(document.to_mongo().to_dict())


class MongoToEs:
    def __init__(
        self,
        mongo_document,
        mongo_dict: dict = None,
        keyword_max_length: int = 64,
        fields: List[str] = None,
        use_choice: bool = True,
    ):
        """
        由 mongoengine 的ORM，自动生成ES的Index mapping。
        :param mongo_document:对应的mongo
        :param mongo_dict: 字段映射，默认使用 generate_default_mongo_field_dict生成的dict
        :param keyword_max_length: 不超过此字段的长度的字符串类型会设置一个keyword选项
        :param fields: 需要同步的字段。如果不设置，则同步所有字段
        :param use_choice: 是否使用choice模式。如果使用，则当MongoDB定义的的字段有choice选项时，会使用keyword
        """
        self.mongo_document = mongo_document
        self.mongo_dict = mongo_dict or generate_default_mongo_field_dict()
        self.keyword_max_length: int = keyword_max_length
        self.use_choice: bool = use_choice
        self.fields = fields

    def wrapper(self, cls):
        # 获取用户已经自定义的字段
        properties: dict = cls._doc_type.mapping.properties.to_dict().get(
            "properties", {}
        )
        for k, v in self.mongo_document._fields.items():
            # 如果已经自定义了该字段，则跳过
            if k in properties:
                continue
            # 如果定义了fields，且该字段不在定义的字段中，则跳过
            if self.fields and k not in self.fields:
                continue
            cls._doc_type.mapping.field(k, self.get_mongo_to_es_field_define(v))
        setattr(
            cls,
            "create_or_update_from_mongo",
            types.MethodType(create_or_update_from_mongo, cls),
        )
        # setattr(cls, "post_mongo_save", types.MethodType(post_mongo_save, cls))
        return cls

    def get_mongo_to_es_field_define(self, field):
        """
        获取mongo的field到ES的field定义的转换
        :param field: mongo的field
        """
        field_name = type(field).__name__.lower()
        func = getattr(self, f"get_{field_name}_define", self.get_other_field_define)
        return func(field)

    def get_booleanfield_define(self, field: mongo_fields.BooleanField):
        return Boolean()

    def get_stringfield_define(self, field: mongo_fields.StringField):
        if self.use_choice and field.choices:
            return Keyword()
        if not field.max_length or field.max_length > self.keyword_max_length:
            return Text()
        else:
            return Text(fields={"keyword": Keyword()})

    def get_intfield_define(self, field: mongo_fields.IntField):
        if self.use_choice and field.choices:
            return Keyword()
        else:
            return Integer()

    def get_floatfield_define(self, field: mongo_fields.FloatField):
        if self.use_choice and field.choices:
            return Keyword()
        else:
            return Float()

    def get_datetimefield_define(self, field: mongo_fields.DateTimeField):
        return Date()

    def get_datefield_define(self, field: mongo_fields.DateField):
        return Date()

    def get_listfield_define(self, field: mongo_fields.StringField):
        return Keyword()

    def get_other_field_define(self, field):
        return Text()

    def __call__(self, *args, **kwargs):
        return self.wrapper(*args, **kwargs)
