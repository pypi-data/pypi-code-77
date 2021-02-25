from sqlalchemy import Column, Boolean, String, Integer
from zm_user.models.base import Base


class Permission(Base):
    # 角色表
    __tablename__ = 'permission'
    short_name = Column(String(50), nullable=False, unique=True, comment="权限简称，建议英文")
    # 名称
    name = Column(String(50), nullable=False, comment='角色名称')
    search_text = Column(String(500),
                         nullable=False,
                         comment='搜索专用')

    def set_search_text(self):
        self.search_text = "{}{}".format(
            self.name,
            self.short_name,
        )
