from sqlalchemy import Column, Boolean, String, Integer
from sqlalchemy.orm import relationship

from zm_user.models.base import Base

class Role(Base):
    # 角色表
    __tablename__ = 'role'

    # 名称
    name = Column(String(50), nullable=False, comment='角色名称')
    # 等级，数值越小，权限越大，root权限为0，默认为10
    level = Column(Integer, nullable=False, default=10, comment='管理员等级，0: 超级管理员, 10: 普通管理员,100：项目管理员')
    # 是否可以修改，默认可以修改，但是可以删除
    is_variable = Column(Boolean, nullable=False, default=True, comment='是否可以修改，默认可以修改，0: 否，1: 是')
    search_text = Column(String(500),
                         nullable=False,
                         comment='搜索专用')

    def set_search_text(self):
        self.search_text = "{}{}".format(
            self.name,
            self.level,
        )

    def to_json(self):
        res = super().base_to_json()
        res.update({
            "name": self.name,
            "level": self.level,
            "is_variable": self.is_variable
        })
        return res
