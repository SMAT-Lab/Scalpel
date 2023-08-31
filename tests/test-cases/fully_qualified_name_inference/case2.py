import datetime
import json

import to_import

to_import.call_funcs()

now = datetime.datetime.now()

data = {"name": "John", "age": 30, "city": "New York"}
json_string = json.dumps(data)
