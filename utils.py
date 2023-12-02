import json

async def write_file(file_data, file_location):
  with open(file_location, "wb+") as file_object:
    file_object.write(file_data.file.read())

def pp_json(json_thing, sort=True, indents=4):
  if type(json_thing) is str:
    print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
  else:
    print(json.dumps(json_thing, sort_keys=sort, indent=indents))
  return None
