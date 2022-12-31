from flask import Flask
from pydantic import ValidationError

from lpdalle.db import db_session
from lpdalle.errors import AppError
from lpdalle.generation.generation import view_generation
from lpdalle.public.users import view_login
from lpdalle.user.users import view_users


def shutdown_session(exception=None):
    db_session.remove()


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.code


def handle_validation_error(error: ValidationError):
    return {'message': str(error)}, 422


def handle_emptystring_error(error):
    return {'Empty data': str(error)}, 400


def main() -> None:
    app = Flask(__name__)
    app.register_blueprint(view_users, url_prefix='/api/v1/users')
    app.register_blueprint(view_login, url_prefix='/api/v1/public/login')
    app.register_blueprint(
        view_generation,
        url_prefix='/api/v1/users/<int:user_id>/generation',
    )
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(400, handle_emptystring_error)  # noqa: WPS432
    app.teardown_appcontext(shutdown_session)
    app.run()


if __name__ == '__main__':
    main()
