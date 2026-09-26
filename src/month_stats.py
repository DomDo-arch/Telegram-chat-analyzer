from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame

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

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(month_count(df))