from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame

def year_count(df: DataFrame, destination: str = None) -> DataFrame:

	years, years_tuple = [], []

	for i in df.date:
		year = i.split("-")[0]
		years.append(year)

	years = Counter(years)

	for i in years.items():
		years_tuple.append(i)
	
	df = DataFrame(years_tuple)
	df.rename(columns = {0:"year", 1:"messages"}, inplace = True)
	
	df = df.sort_values("year", ascending = False)
	
	if destination is not None:
		df.to_csv(destination)

	return df

def years_messages_list(df: DataFrame) -> list[int, int]:
	
	year_messages = []
	
	for i in range(len(df)):
		year_messages.append([int(df.year[i]), df.messages[i]])
		
	return year_messages

def year_dir(dfs_list: list[DataFrame], destination: str = None) -> DataFrame:
	
	dfs, total_list, dfs_values = [], [], []
	c = Counter()
	
	for i in dfs_list:
		dfs.append(years_messages_list(year_count(i)))
		
	for i in dfs:
		for j in i:
			total_list.append(j)
			
	for year, messages_count in total_list:
		c[year] += messages_count
		
	for i in c.items():
		dfs_values.append([i[0], i[1]])
		
	df = DataFrame(dfs_values)
	
	df.rename(columns = {0:"year", 1:"messages_count"}, inplace = True)
	df = df.sort_values("year", ascending = True)

	return df	

if __name__ == "__main__":
	
	df = make_table("input_json/group_chat.json")
	
	#print(year_count(df))

	print(year_dir(
	[make_table("input_json/group_chat.json"),
	make_table("input_json/polito.json")
	])
	)
