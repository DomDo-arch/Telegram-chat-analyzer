from make_table_from_chat import make_table
from pandas import DataFrame, concat
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

def weekday(df: DataFrame) -> dict[str:int]:
	
	weekdays_list = []
	num_name_short = {0:"mon",1:"tue",2:"wed",3:"thu",4:"fri",5:"sat",6:"sun"}
	
	weekdays = Counter(df.weekday)
	
	weekdays_num = []
	for i in weekdays.items():
		weekdays_num.append([i[0], i[1]])
		
	weekdays_num = sorted(weekdays_num)
	
	for i in weekdays_num:
		weekdays_list.append([num_name_short[i[0]], i[1]])
		
	weekdays_dict = {item[0]: item[1] for item in weekdays_list}
	
	return weekdays_dict

def weekday_folder(folder: list[DataFrame], destination: str = None, title_list = None) -> DataFrame:
	
	weekday_list = []
	
	for i in range(len(folder)):
		weekday_dicts = weekday(folder[i])
		weekday_dicts["title"] = title_list[i]
		weekday_list.append(weekday_dicts)
		
	df = DataFrame(weekday_list)
	
	cols = df.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	
	df = df[cols]
	
	if destination is not None:
		df.to_csv(destination, index = False)
	
	return df

def weekday_percentage(df: DataFrame, title) -> DataFrame:
	
	df = weekday_folder([df], title_list = [title])
	df = df.set_index("title")

	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100
	
	return res.reset_index()

def weekday_percentage_folder(folder: list[DataFrame], title_list:list[str]) -> DataFrame:
	
	dfs = []	

	for i in range(len(folder)):
		dfs.append(weekday_percentage(folder[i], title_list[i]))

	df = concat(dfs)
	
	return df

if __name__ == "__main__":
	
	df = make_table("input_json/polito.json")
	
	#print(weekday_count(df))
	
	#print(weekday(df))
	
	#print(weekday_folder([df, make_table("input_json/group_chat.json")], title_list=["polito","group_chat"]))
	
	#print(weekday_percentage(df, "group"))
	
	print(weekday_percentage_folder([df, make_table("input_json/poliba.json")], title_list = ["polito", "group_chat"]))
