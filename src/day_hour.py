from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter

def user_word_table(df: DataFrame, word:str, destination: str = None) -> DataFrame:
	
	hours = []
	
	for i in df.hour:
		hours.append(int(i.split(":")[0]))
		
	hour_num = Counter(hours)
	
	hour_num = {k: v for k, v in sorted(hour_num.items(), key=lambda item: item[0])}
	
	print(hour_num)

	if destination is not None:
		df.to_csv(destination)
	
	#return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(user_word_table(df, "io"))