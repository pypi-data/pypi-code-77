from sqlalchemy import Column, Boolean, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from zm_user.models.base import Base


# from zm_user.models.platform_user_center import platform_user

def set_search_text(context):
    return "{}".format(context.get_current_parameters()['name'],
                       )


class Platform(Base):
    # 平台表
    __tablename__ = 'platform'
    # 名称
    name = Column(String(50), nullable=False, comment='平台名称')
    # 所关联的平台
    # user_list = relationship("User", secondary=platform_user)
    search_text = Column(String(500),
                         nullable=False,
                         comment='搜索专用')

    def set_search_text(self):
        self.search_text = "{}".format(
            self.name,
        )

    def to_json(self):
        res = super().base_to_json()
        res.update({
            "name": self.name,
        })
        return res
