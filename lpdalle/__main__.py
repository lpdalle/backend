from flask import Flask
from lpdalle.user.users import users_view, users_view_login



def main():
    app = Flask(__name__)
    app.register_blueprint(users_view, url_prefix='/api/v1/users')
    app.register_blueprint(users_view_login, url_prefix='/api/v1/public/users')
    app.run()

if __name__ == '__main__':
    main()
