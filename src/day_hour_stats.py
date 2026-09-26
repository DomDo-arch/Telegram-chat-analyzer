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

def day_hour_count(df: DataFrame, week_day: int) -> dict:
	
	hours = []
	
	for i in range(len(df.weekday)):
		if df.weekday[i] == week_day:
			hour = int(df.hour[i].split(":")[0])
			hours.append(hour)
			
	hours = dict(Counter(hours))
	
	hours = {k:v for k, v in sorted(hours.items(), key = lambda item: item[0])}
	
	return hours

def weekday_hour_df(df: DataFrame) -> DataFrame:
	
	weekday_hour = []
	
	for i in list(set(df.weekday)):
		weekday_hour.append(day_hour_count(df, i))
		
	df = DataFrame(weekday_hour)
	df.sort_index(axis=1, inplace=True)
	
	return df
	

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	#print(weekday_count(df))
	
	#print(day_hour_count(df, 2))
	print(weekday_hour_df(df))