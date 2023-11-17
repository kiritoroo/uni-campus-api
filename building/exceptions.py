from fastapi import HTTPException, status


class BuildingNotFound(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_404_NOT_FOUND
    self.detail = "Building not found"