from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter
from datetime import datetime

def days_sending_messages(df: DataFrame) -> int:
	
	date1 = df.date[0]
	date2 = df.date[len(df.date)-1]
	
	date1 = datetime.strptime(date1, "%Y-%m-%d")
	date2 = datetime.strptime(date2, "%Y-%m-%d")
	
	chat_days_with_messages = len(set(df.date))
	chat_len = abs(date2-date1).days
	
	return chat_days_with_messages, chat_len

def days_activity(df: DataFrame) -> DataFrame:
		
	chat = [
	["Days", days_sending_messages(df)[0]], 
	["Date range", days_sending_messages(df)[1]]]
	#["Chat ratio", "{:.2f}".format(days_sending_messages(df)[0]/days_sending_messages(df)[1])]]
	
	df = DataFrame(chat)
	df.rename(columns = {0:"chat_info",1:"days"}, inplace=True)
	
	return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")

	print(days_sending_messages(df))
	print(days_activity(df))
