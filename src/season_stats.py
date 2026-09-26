from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame

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

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(season_count(df, "season.csv"))