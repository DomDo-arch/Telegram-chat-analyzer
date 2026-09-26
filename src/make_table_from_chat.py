from json import load
from pandas import DataFrame
from datetime import date

def make_table(json_script: str, destination: str = None) -> DataFrame:
	
	chat = []

	with open(json_script) as file:
		d = load(file)
		messages_dict = d["messages"]
		
		#print(d["type"])

		for i in messages_dict:
			dates = i["date"].split("T")[0]
			hour = i["date"].split("T")[1]
			if isinstance(i["text"], str):
				message = i["text"]
			elif isinstance(i["text"], list):
				message = i["text"]
			
			#print(type(message))

			# Get weekday
			date_a = dates.split("-")
			
			day = int(date_a[2])
			month = int(date_a[1])
			year = int(date_a[0])
			
			weekday = date(year, month, day).weekday()
		
			if d["type"] == "private_supergroup":
				if i["type"] == "message":
					user = i["from"]

					chat.append([dates, weekday, hour, user, message])
					
			elif d["type"] == "personal_chat":
				user = i["from"]
				
				chat.append([dates, weekday, hour, user, message])

	df = DataFrame(chat)
	df.rename(columns = {0:"date", 1:"weekday", 2:"hour", 3:"user", 4:"message", 5:"media_type"}, inplace=True)
	
	if destination is not None:
		df.to_csv(destination, index=False)
	
	return df

if __name__ == "__main__":
	
	script = "group_chat.json"
	table = make_table(script)#, destination = "group_chat.csv")
	
	#print(type(table))
	#print(make_table.__annotations__)

	print(table)