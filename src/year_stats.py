from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame

def year_count(df: DataFrame, destination:str = None) -> DataFrame:

	days, days_tuple = [], []

	for i in df.date:
		day = i.split("-")[0]
		days.append(day)

	days = Counter(days)

	for i in days.items():
		days_tuple.append(i)
	
	df = DataFrame(days_tuple)
	df.rename(columns = {0:"year", 1:"messages"}, inplace = True)
	
	df = df.sort_values("year", ascending = False)
	
	if destination is not None:
		df.to_csv(destination)

	return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(year_count(df))