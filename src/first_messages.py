from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter
from datetime import datetime

def first_messages(df: DataFrame, destination: str = None) -> DataFrame:

	indexes = list(set([list(df.date).index(df.date[i]) for i in range(len(df))]))
	
	users = [df.user[i].strip() for i in indexes]
	
	users = dict(Counter(users))
	
	df = DataFrame(users.items())
	df.rename(columns = {0:"user", 1:"messages"}, inplace = True)
	df = df.sort_values("messages", ascending = False)
	
	if destination is not None:
		df.to_csv(destination)
	
	return df

def days_sending_messages(df: DataFrame) -> DataFrame:
	
	date1 = df.date[0]
	date2 = df.date[len(df.date)-1]
	
	date1 = datetime.strptime(date1, "%Y-%m-%d")
	date2 = datetime.strptime(date2, "%Y-%m-%d")
	
	chat_days_with_messages = len(set(df.date))
	chat_len = abs(date2-date1).days
	
	return chat_days_with_messages, chat_len

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(first_messages(df))
	print(days_sending_messages(df))