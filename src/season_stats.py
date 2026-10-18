from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame, concat

def season_count(df: DataFrame, destination:str = None) -> DataFrame:
	
	months = []
	
	autumn, winter, spring, summer = 0,0,0,0
	
	for i in df.date:
		month = int(i.split("-")[1])
		
		if 3 <= month <= 5:
			spring += 1
		elif 6 <= month <= 8:
			summer += 1
		elif 9 <= month <= 11:
			autumn += 1
		else:
			winter += 1
			
	seasons = [["autumn",autumn], ["winter",winter],["spring",spring],["summer",summer]]
	
	df = DataFrame(seasons)
	df.rename(columns = {0:"season",1:"messages"}, inplace = True)
	
	if destination is not None:
		df.to_csv(destination, index = False)

	return df

def season(df: DataFrame) -> dict[str, int]:
		
	df = season_count(df).messages
	season_dict = {"aut":df[0], "win":df[1], "spr":df[2], "sum":df[3]}
	
	return season_dict

def season_dir(folder: list[DataFrame], title_list: list[str], destination:str = None) -> DataFrame:
	
	seasons_list = []
	
	for i in range(len(folder)):
		season_dict = season(folder[i])
		season_dict["title"] = title_list[i]
		seasons_list.append(season_dict)
		
	df = DataFrame(seasons_list)
	cols = df.columns.tolist()
	
	cols = cols[-1:] + cols[:-1]
	df = df[cols]
	
	return df

def season_percentage(df: DataFrame, title) -> DataFrame:
	
	df = season_dir(df, title_list=title)
	df = df.set_index('title')
	
	res = df.div(df.sum(axis = 1), axis = 0)
	res *= 100
	
	return res.reset_index()

def season_percentage_folder(folder: list[DataFrame], title_list: list[str]) -> DataFrame:
	
	dfs = []
	
	for i in range(len(folder)):
		dfs.append(season_percentage([folder[i]], [title_list[i]]))
		
	df = concat(dfs)
	
	return df

if __name__ == "__main__":
	
	df = make_table("input_json/poliba.json")
	
	#print(season_count(df))
	
	#print(season_dir([make_table("input_json/group_chat.json"),make_table("input_json/polito.json")],title_list = ["group_chat", "polito"]))
	
	#print(season(make_table("input_json/group_chat.json")))
	
	#print(season_percentage([make_table("input_json/group_chat.json")], title=["group_chat"]))
	
	print(season_percentage_folder([make_table("input_json/poliba.json"),make_table("input_json/polito.json")],title_list = ["poliba", "polito"]))
