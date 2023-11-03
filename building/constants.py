from fastapi import status
from building.models import BuildingModel

GET_METHOD_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "List buildings",
  'response_description': "Success",
  'response_model': BuildingModel,
}