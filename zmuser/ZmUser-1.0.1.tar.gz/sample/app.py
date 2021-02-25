import os

from flask_migrate import Migrate

from sample import app, db
from zm_user import ZmUser

zm = ZmUser(db, app)
User = zm.User
Role = zm.Role

migrate = Migrate(app, db)
