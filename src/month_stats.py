from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame, concat

def month_count(df: DataFrame, destination:str = None) -> DataFrame:

	months, months_tuple = [], []
	num_name_short={1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}

	for i in df.date:
		month = int(i.split("-")[1])
		months.append(num_name_short[month])

	months = Counter(months)

	for i in months.items():
		months_tuple.append(i)
	
	df = DataFrame(months_tuple)
	df.rename(columns = {0:"month", 1:"messages"}, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index=False)

	return df

def month_count_dict(df: DataFrame) -> dict[str: int]:
	
	months_list = []
	

	months = [int(i.split("-")[1]) for i in df.date]

	months_dict = dict(Counter(months))
	
	return months_dict

def month_dir(folder: list[DataFrame], title_list = None) -> DataFrame:
	
	month_list = []
	months_name = {1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}
	
	for i in range(len(folder)):
		month_dict = month_count_dict(folder[i])
		month_dict["title"] = title_list[i]
		month_list.append(month_dict)
		
	df = DataFrame(month_list)
	cols = df.columns.tolist()
	
	cols.remove("title")
	cols = sorted(cols)

	cols.insert(0, "title")
	
	df = df[cols]
	
	df.rename(columns = months_name, inplace = True)
	
	return df

def month_percentage(df: DataFrame, title) -> DataFrame:
	
	df = month_dir([df], title_list = [title])
	df = df.set_index("title")
	
	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100
	
	return res.reset_index()

def month_percentage_folder(folder: list[DataFrame], title_list: list[str]) -> DataFrame:
	
	dfs = []
	
	for i in range(len(folder)):
		dfs.append(month_percentage(folder[i], title=title_list[i]))
	
	df = concat(dfs)
	
	return df

def find_max_month(df: DataFrame, index: int) -> list[str, str, float]:

	max_value = max([i for i in df.iloc[index, :] if isinstance(i, float)])
	titles = [i for i in df.title]
	
	max_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == max_value:
			max_index += i
			
	return [titles[index], df.columns[max_index], max_value]

def find_max_month_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	titles = [i for i in df.title]
	
	for i in range(len(df)):
		cols.append(find_max_month(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "month", 2:"percentage"}, inplace = True)
	
	return df

def find_min_month(df: DataFrame, index: int) -> list[str, str, float]:

	max_value = min([i for i in df.iloc[index, :] if isinstance(i, float)])
	titles = [i for i in df.title]
	
	max_index = 0
	for i in range(len(df.columns)):
		if df.iloc[index, i] == max_value:
			max_index += i
			
	return [titles[index], df.columns[max_index], max_value]

def find_min_month_dir(df: DataFrame) -> DataFrame:
	
	cols = []
	titles = [i for i in df.title]
	
	for i in range(len(df)):
		cols.append(find_min_month(df, i))
		
	df = DataFrame(cols)
	df.rename(columns = {0: "chat", 1: "month", 2:"percentage"}, inplace = True)
	
	return df

if __name__ == "__main__":
	
	df = make_table("input_json/poliba.json")
	
	#print(month_count(df))
	
	#print(month_dir([df, make_table("input_json/polito.json")], title_list = ["group_chat", "polito"]))
	
	#print(month_percentage(df, title=["poliba"]))
	
	df = month_percentage_folder([df, 
	make_table("input_json/polito.json"),
	make_table("input_json/trento.json")
	], 
	title_list=["poliba", "polito", "trento"])
	
	#print(find_max_month(df, 1))
	
	print(find_max_month_dir(df))
	print(find_min_month_dir(df))
