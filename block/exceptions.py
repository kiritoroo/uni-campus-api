from fastapi import HTTPException, status

class BlockNotFound(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_404_NOT_FOUND
    self.detail = "Block not found"