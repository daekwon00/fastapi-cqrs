from starlette import status


class BusinessException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(BusinessException):
    def __init__(self, message: str = "리소스를 찾을 수 없습니다."):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(BusinessException):
    def __init__(self, message: str = "인증이 필요합니다."):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(BusinessException):
    def __init__(self, message: str = "접근 권한이 없습니다."):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)
