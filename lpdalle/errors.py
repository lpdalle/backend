class AppError(Exception):
    def __init__(self, reason: str, code: int) -> None:
        super().__init__(reason)
        self.reason = reason
        self.code = code


class ConflictError(AppError):
    def __init__(self, entity: str, uid: int) -> None:
        super().__init__(f'{entity}[{uid}]', code=409)  # noqa: WPS432
        self.entity = entity
        self.uid = uid


class NotFoundError(AppError):
    def __init__(self, entity: str, uid: int) -> None:
        super().__init__(f'{entity}[{uid}]', code=404)  # noqa: WPS432
        self.entity = entity
        self.uid = uid


class BadRequestError(AppError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason, code=400)  # noqa: WPS432
        self.reason = reason
