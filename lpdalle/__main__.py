from flask import Flask
from pydantic import ValidationError

from lpdalle.errors import AppError
from lpdalle.generations.generations import view_generations
from lpdalle.public.users import view_login
from lpdalle.user.users import view_users


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.code


def handle_validation_error(error: ValidationError):
    return {'message': str(error)}, 422


def handle_emptystring_error(err):
    return 'Empty data', 400


def main() -> None:
    app = Flask(__name__)
    app.register_blueprint(view_users, url_prefix='/api/v1/users')
    app.register_blueprint(view_login, url_prefix='/api/v1/public/users')
    app.register_blueprint(view_generations, url_prefix='/api/v1/generations')
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(400, handle_emptystring_error)  # noqa: WPS432
    app.run()


if __name__ == '__main__':
    main()
