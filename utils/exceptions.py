class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_type: str = "AppException"
    ):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type

        super().__init__(message)