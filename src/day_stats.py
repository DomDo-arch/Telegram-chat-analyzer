from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame
import numpy as np
from datetime import datetime, timedelta

def filter_interval_table(df: DataFrame, start_date:str, days_interval:int, destination:str = None) -> DataFrame:
	
	chat = []
	
	start_date = datetime.strptime(start_date, "%Y-%m-%d")
	end_date = start_date - timedelta(days = days_interval)
	
	for i in range(len(df)):
		if end_date <= datetime.strptime(df.date[i], "%Y-%m-%d") <= start_date:
			chat.append([df.date[i], df.hour[i], df.weekday[i], df.user[i], df.message[i]])
			
	df = DataFrame(chat)
	df.rename(columns = {0:"date",1:"hour",2:"weekday",3:"user",4:"message"}, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index=False)

	return df
	
if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(filter_interval_table(df, "2026-06-21", 20))
	
	#print(df)