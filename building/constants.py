from fastapi import status

from building.models import BuildingModel


GETS_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "List buildings",
  'response_description': "Get buildings list success",
  'response_model': list[BuildingModel],
}

GET_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "Detail buildings",
  'response_description': "Get building success",
  'response_model': BuildingModel,
}

POST_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_201_CREATED,
  'description': "Create a new building",
  'response_description': "Building created successfully",
  'response_model': BuildingModel,
}

PUT_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "Update a building",
  'response_description': "Building updated successfully",
  'response_model': BuildingModel,
}

DELETE_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_204_NO_CONTENT,
  'description': "Delete a building",
  'response_description': "Building deleted successfully",
}