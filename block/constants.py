from fastapi import status
from block.models import BlockModel
from block.schemas import BlockPopulateSchema
from typing import Union


GETS_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "List blocks",
  'response_description': "Get blocs list success",
  'response_model': Union[list[BlockModel], list[BlockPopulateSchema]],
}

GET_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "Detail block",
  'response_description': "Get block success",
  'response_model': Union[BlockModel, BlockPopulateSchema],
}

POST_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_201_CREATED,
  'description': "Create a new block",
  'response_description': "Block created successfully",
  'response_model': BlockModel,
}

PUT_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "Update a block",
  'response_description': "Block updated successfully",
  'response_model': BlockModel,
}

DELETE_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_204_NO_CONTENT,
  'description': "Delete a block",
  'response_description': "Block deleted successfully",
}
