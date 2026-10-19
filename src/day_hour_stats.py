from collections import Counter
from pandas import DataFrame, concat
from make_table_from_chat import make_table

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

def hour(df: DataFrame) -> dict[int:int]:
	
	hours = []
	
	for i in df.hour:
		hour = int(i.split(":")[0])
		hours.append(hour)
	
	hours = Counter(hours)
	
	hour_num = {k: v for k, v in sorted(hours.items(), key=lambda item: item[0])}
	
	return hour_num

def day_hour_dir(folder: list[DataFrame], destination: str = None, title_list = None) -> DataFrame:
	
	hour_list = []
	
	for i in range(len(folder)):
		hour_dicts = hour(folder[i])
		hour_dicts["title"] = title_list[i]
		
		hour_list.append(hour_dicts)
		
	df = DataFrame(hour_list)
	
	cols = df.columns.tolist()
	
	cols.remove("title")
	cols = sorted(cols)
	cols.append("title")
	cols = cols[-1:] + cols[:-1]
	
	df = df[cols]
	
	return df

def hour_percentage(df:	DataFrame, title: list[str]) -> DataFrame:
	
	df = day_hour_dir([df], title_list = title)
	df = df.set_index("title")
	
	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100

	return res.reset_index()

def hour_percentage_dir(folder: list[DataFrame], title_list: list[str]) -> DataFrame:
	
	dfs = []
	
	for i in range(len(folder)):
		dfs.append(hour_percentage(folder[i], title = [title_list[i]]))
		
	df = concat(dfs)
	
	return df

def weekday_hour_percentage(df: DataFrame) -> DataFrame:
	
	df = weekday_hour_df(df)
	
	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100
	
	return res#res.reset_index()

def find_min_weekday_hour(df: DataFrame, index: int) -> list[str, str, float]:

	min_value = min([i for i in df.iloc[index, :].dropna() if isinstance(i, float)])
	titles = list(df.title)
	
	min_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == min_value:
			min_index = i
			
	return [titles[index], df.columns[min_index], min_value]

def find_min_weekday_hour_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	titles = list(df.title)
	
	for i in range(len(df)):
		cols.append(find_min_weekday_hour(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "hour", 2:"percentage"}, inplace = True)
	
	return df

def find_max_weekday_hour(df: DataFrame, index: int) -> list[str, str, float]:

	max_value = max([i for i in df.iloc[index, :].dropna() if isinstance(i, float)])
	titles = list(df.title)
	
	max_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == max_value:
			max_index = i
			
	return [titles[index], df.columns[max_index], max_value]

def find_max_weekday_hour_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	
	for i in range(len(df)):
		cols.append(find_max_weekday_hour(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "hour", 2:"percentage"}, inplace = True)
	
	return df

if __name__ == "__main__":
	
	df = make_table("input_json/poliba.json")
	
	#print(weekday_count(df))
	
	#print(day_hour_count(df, 2))
	#print(weekday_hour_df(df))
	
	#print(day_hour_dir([df, make_table("input_json/polito.json")], title_list=["poliba", "polito"]))
	
	#print(hour(df))
	
	#print(hour_percentage(df, title=["poliba"]))
	
	#print(hour_percentage_dir([df, make_table("input_json/polito.json")], title_list=["poliba", "polito"]))
	
	#print(weekday_hour_df(df))
	
	#print(weekday_hour_percentage(df))
	
	df = hour_percentage_dir([df, make_table("input_json/pisa.json")], title_list = ["poliba", "pisa"])
	
	#print(find_min_weekday_hour(df, 1))
	
	print(find_min_weekday_hour_dir(df))
	print(find_max_weekday_hour_dir(df))
