from make_table_from_chat import make_table

import tempfile
import json
import os

import shutil

file = os.path.abspath("group_chat.json")
	
with tempfile.NamedTemporaryFile(delete = False, suffix = ".json") as temp_file:
		
	file_len = len(temp_file.name.split("/"))
	temp_file_folder = '/'.join((temp_file.name).split("/")[:file_len-1])
	
	#print(temp_file_folder)
	#print(file)
	
	shutil.copy(file, temp_file_folder+"/")


if __name__ == "__main__":
	
	#df = make_table("group_chat.json")
	
	#print(df)
	pass