from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame

def hour_count(df: DataFrame, destination:str = None) -> DataFrame:
	
	hours = [int(i.split(":")[0]) for i in df.hour]
	
	hours = dict(Counter(hours))
	
	hour_num = {k: v for k, v in sorted(hours.items(), key=lambda item: item[0])}
	
	df = DataFrame(hour_num.items())
	
	df.rename(columns = {0:"hour",1:"messages"}, inplace=True)
	
	if destination is not None:
		df.to_csv(destination, index=False)

	return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(hour_count(df))
