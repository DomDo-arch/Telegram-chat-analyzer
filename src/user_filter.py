from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter

def user_table(df: DataFrame, username:str, destination: str = None) -> DataFrame:
	
	chat = []
	
	for i in range(len(df)):
		if df.user[i] == username:
			chat.append([df.date[i], df.hour[i], df.weekday[i], df.user[i], df.message[i]])
			
	df = DataFrame(chat)
	df.rename(columns = {0:"date",1:"hour",2:"weekday",3:"user",4:"message"}, inplace=True)
	
	if destination is not None:
		df.to_csv(destination)
	
	return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(user_table(df, "Dom"))