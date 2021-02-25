from sqlalchemy import Column, Boolean, String, Integer, Table, ForeignKey

# from zm_user.models.base import Base
#
#
# class PlatformUser(Base):
#     __tablename__ = 'platform_user'
#     user_id = Column(Integer, ForeignKey("user.id"))
#     platform_id = Column(Integer, ForeignKey("platform.id"))
#
#
from zm_user.models.base import db

platform_user = db.Table(
    "platform_user",
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("platform_id", Integer, ForeignKey("platform.id"))
)
