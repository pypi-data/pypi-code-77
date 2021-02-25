from sqlalchemy import Column, Boolean, String, Integer

from zm_user.models.base import Base


class Unit(Base):
    # 单位
    __tablename__ = 'unit'

    # 名称
    name = Column(String(50), nullable=False, comment='单位名称')
    # 简称
    short_name = Column(String(50), nullable=False, comment='单位简称')
    search_text = Column(String(500),
                         nullable=False,
                         comment='搜索专用')

    def set_search_text(self):
        self.search_text = "{}{}".format(
            self.name,
            self.short_name,
        )

    def to_json(self):
        res = super().base_to_json()
        res.update({
            "name": self.name,
            "short_name": self.short_name,
        })
        return res
