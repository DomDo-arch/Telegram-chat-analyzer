from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter

def media_type_stats(df: DataFrame, destination: str = None) -> DataFrame:
	
	media_types = Counter(df.media_type)
	media_types_tuple = []
	
	for i in media_types.items():
		media_types_tuple.append(i)
		
	df = DataFrame(media_types_tuple)
	df.rename(columns = {0:"media_type", 1:"media_count"}, inplace = True)
	
	if destination is not None:
		df.to_csv(destination)
	
	return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(media_type_stats(df))