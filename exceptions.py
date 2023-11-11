from fastapi import HTTPException, status

class InternalServerException(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    self.detail = "Sometime error"
