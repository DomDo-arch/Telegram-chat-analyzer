from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter

def weekday_count(df: DataFrame, destination: str = None) -> DataFrame:
	
	weekdays_list = []
	num_name_short = {0:"mon",1:"tue",2:"wed",3:"thu",4:"fri",5:"sat",6:"sun"}
	
	weekdays = Counter(df.weekday)
	
	weekdays_num = []
	for i in weekdays.items():
		weekdays_num.append([i[0], i[1]])
		
	weekdays_num = sorted(weekdays_num)
	
	for i in weekdays_num:
		weekdays_list.append([num_name_short[i[0]], i[1]])
	
	df = DataFrame(weekdays_list)
	df.rename(columns = {0:"weekday", 1:"messages"}, inplace=True)
	
	if destination is not None:
		df.to_csv(destination, index=False)
	
	return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(weekday_count(df))