from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter

def user_word_table(df: DataFrame, word:str, destination: str = None) -> DataFrame:
	
	punctuations = list("?!,.:;-<>()[]{}^_")
	punctuations = dict(zip(punctuations, ["" for i in range(len(punctuations))]))
	
	users = []
	
	for i in range(len(df)):
		for j in str(df.message[i]).split():
			message = j.translate(str.maketrans(punctuations)).lower()
			if message == word:
				users.append(df.user[i])
				
	users = Counter(users)
	
	df = DataFrame(list(users.items()))
	df.rename(columns = {0:"user",1:"messages"}, inplace = True)
	df = df.sort_values("messages", ascending = False)
	
	if destination is not None:
		df.to_csv(destination, index=False)
	
	return df

if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	
	print(user_word_table(df, "io"))