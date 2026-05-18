from typing import Any


class CustomException(Exception):
	def __init__(self, message: str, status_code: int = 400):
		super().__init__(message)
		self.message = message
		self.status_code = status_code


class NotAdminException(CustomException):
	def __init__(self, message: str = "Action requires admin privileges"):
		super().__init__(message, status_code=403)


class ResourceNotFoundException(CustomException):
	def __init__(self, message: str = "Resource not found"):
		super().__init__(message, status_code=404)


class ConflictException(CustomException):
	def __init__(self, message: str = "Conflict"):
		super().__init__(message, status_code=409)


class UnauthorizedException(CustomException):
	def __init__(self, message: str = "Unauthorized"):
		super().__init__(message, status_code=401)

# class UserNotFoundException(CustomException):
# 	def __init__(self,message:str="User not found"):
# 		super().__init__(message,status_code=)

# Backwards-compatible alias used in handlers registration
AppException = CustomException

