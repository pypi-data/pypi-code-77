import datetime
from types import MethodType, FunctionType

from flask import g
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, MetaData
from zm_user.conf import Config
import json

from zm_user.tools.string_help import is_none_str
from zm_user.tools.time import datetime_to_str

db = Config.zm_user_db


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, comment="自增ID")
    create_time = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now, comment="该数据创建时间")
    is_delete = Column(Boolean, default=False, comment='是否是管理员，0: 否，1: 是')
    update_time = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                         comment="该数据最后更新时间")
    delete_time = Column(TIMESTAMP, default=datetime.datetime.now, comment="删除时间")
    create_user_id = Column(Integer, comment="创建用户的ID")
    update_user_id = Column(Integer, comment="该数据最后更新用户的ID")
    delete_user_id = Column(Integer, comment="删除用户的ID")

    @classmethod
    def _q_all(cls, *args):
        # 查询所有,不分页
        with db.session.no_autoflush:
            return cls.query.filter(cls.is_delete != True, *args).all()

    @classmethod
    def _q_page(cls, *args):
        # 分页查询
        query_page = cls.query.filter(cls.is_delete != True, *args)
        key = g.params.get('key', '')
        if not is_none_str(key) and hasattr(cls, "search_text"):
            query_page = query_page.filter(cls.search_text.like('%' + key + '%'))
        query_page=query_page.order_by(cls.id.desc())
        total = query_page.count()
        return query_page.offset(g.page * g.page_size).limit(g.page_size).all(), total

    @classmethod
    def _q(cls, *args):
        # 查询单个
        with db.session.no_autoflush:
            return cls.query.filter(cls.is_delete != True, *args).first()

    @classmethod
    def _q_count(cls, *args):
        # 查询数量
        with db.session.no_autoflush:
            return cls.query.filter(cls.is_delete != True, *args).count()

    def set_search_text(self):
        pass

    def to_new(self):
        if g.user:
            self.create_user_id = g.user.id
            self.create_time = datetime.datetime.now()
        if hasattr(self, 'search_text'):
            self.set_search_text()
        db.session.add(self)
        db.session.commit()

    def to_save(self):
        if g.user:
            self.update_user_id = g.user.id
        if hasattr(self, 'search_text'):
            self.set_search_text()
        db.session.add(self)
        db.session.commit()

    def to_delete(self):
        self.is_delete = True
        if g.user:
            self.delete_user_id = g.user.id
            self.delete_time = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        res = {}
        attr_list = dir(Base)
        for attr in attr_list:
            if not attr.startswith("_") and hasattr(self, attr) and attr not in ["query_class"]:
                value = getattr(self, attr)
                if isinstance(value, BaseQuery) \
                        or isinstance(value, MetaData) \
                        or isinstance(value, MethodType) \
                        or isinstance(value, FunctionType):
                    continue
                res[attr] = getattr(self, attr)
        return str(res)

    def base_to_json(self):
        return {
            "key": str(self.id),
            "id": str(self.id),
            'create_time': datetime_to_str(self.create_time),
            'create_time_short': datetime_to_str(self.create_time, '%Y-%m-%d'),
            'update_time_short': datetime_to_str(self.update_time, '%Y-%m-%d') if self.update_time else "",
            'update_time': datetime_to_str(self.update_time) if self.update_time else "",
            'delete_time': datetime_to_str(self.delete_time) if self.update_time else "",
            "is_delete": self.is_delete,
        }
