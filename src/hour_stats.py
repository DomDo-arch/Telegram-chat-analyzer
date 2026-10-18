from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame

def hour_count(df: DataFrame, destination:str = None) -> DataFrame:
	
	hours = [int(i.split(":")[0]) for i in df.hour]
	
	hours = dict(Counter(hours))
	
	hour_num = {k: v for k, v in sorted(hours.items(), key=lambda item: item[0])}
	
	#print(hour_num)
	
	df = DataFrame(hour_num.items())
	
	df.rename(columns = {0:"hour",1:"messages"}, inplace=True)
	
	if destination is not None:
		df.to_csv(destination, index=False)

	return df

def day_part(df: DataFrame) -> list[int]:
	
	half_day1, half_day2 = 0, 0
	
	for i in df.hour:
		
		hour = int(i.split(":")[0])
		
		if 0 <= hour <= 11:
			half_day1 += 1
		else:
			half_day2 += 1
			
	return [half_day1, half_day2]

def hour_dir(folder: list[DataFrame], destination: str = None, title_list = None) -> DataFrame:
	
	hour_list = []
	
	for file in range(len(folder)):
		day_parts = day_part(folder[file])
		hour_list.append([title_list[file], day_parts[0], day_parts[1]])
			
	df = DataFrame(hour_list)
	
	df.rename(columns = {0:"title", 1:"first_half_day", 2:"second_half_day"}, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index=False)

	return df

if __name__ == "__main__":
	
	df = make_table("input_json/group_chat.json")
	
	#print(hour_count(df))
	#print(day_part(df))
	
	print(hour_dir([df, make_table("input_json/polito.json")], title_list=["group_chat", "polito"]))
