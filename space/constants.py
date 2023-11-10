from fastapi import status
from space.models import SpaceModel

GETS_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "List spaces",
  'response_description': "Get spaces list success",
  'response_model': list[SpaceModel],
}

GET_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "Detail space",
  'response_description': "Get space success",
  'response_model': SpaceModel,
}

POST_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_201_CREATED,
  'description': "Create a new space",
  'response_description': "Space created successfully",
  'response_model': SpaceModel,
}

PUT_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "Update a space",
  'response_description': "Space updated successfully",
  'response_model': SpaceModel,
}

DELETE_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_204_NO_CONTENT,
  'description': "Delete a space",
  'response_description': "Space deleted successfully",
}