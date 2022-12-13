
import json
json_string = '{ "1":"Red", "2":"Blue", "3":"Green"}'
parsed_json = json.loads(json_string)
print(parsed_json['1'])


TOKEN_MAP = {
    "SN-001": "Na5tkJmV9FRIUyhnqUEq",
    "SN-003": "soIsnoRIT6n7jsiN3J0B"
}

TIME_SCHEDULE = {}
device_name = "SN-003"
print(TOKEN_MAP[device_name])