from fastapi import HTTPException, status

class SpaceNotFound(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_404_NOT_FOUND
    self.detail = "Space not found"