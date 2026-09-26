from make_table_from_chat import make_table

import tempfile
import json
import os

import shutil

with open(os.path.abspath("group_chat.json")) as json_file:
	
	file = json.load(json_file)
	
	with tempfile.NamedTemporaryFile(delete = False, suffix = ".json") as temp_file:
		
		with open(temp_file.name, "w") as out_file:
			json.dump(file, out_file)


if __name__ == "__main__":
	
	#df = make_table("group_chat.json")
	
	#print(df)
	pass