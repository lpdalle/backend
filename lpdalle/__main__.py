from flask import Flask
from lpdalle.user.users import users_view



def main():
    app = Flask(__name__)
    app.register_blueprint(users_view, url_prefix='/api/v1/users')
    app.run()

if __name__ == '__main__':
    main()

