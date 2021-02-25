import os
from sample import app, db
from zm_user import ZmUser

zm = ZmUser(db, app, need_init=True, is_test=True)
User = zm.User
Role = zm.Role



@app.route("/")
def index():
    print(Role._q_all())
    print(User._q_all())
    return "index"


if __name__ == '__main__':
    print("http://0.0.0.0:9999/api/")
    print("http://0.0.0.0:9999/api/bb/init_user")
    PORT = int(os.getenv('PORT', 9999))
    app.run(port=PORT, host='0.0.0.0')
