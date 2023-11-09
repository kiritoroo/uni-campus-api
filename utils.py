async def write_file(file_data, file_location):
  with open(file_location, "wb+") as file_object:
    file_object.write(file_data.file.read())
