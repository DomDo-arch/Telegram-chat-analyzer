from make_table_from_chat import make_table
from collections import Counter
from pandas import DataFrame
import numpy as np

def words_stats(df: DataFrame, destination:str = None) -> DataFrame:

	messages, words = [], []

	punctuations = list("?!,.:;-<>()[]{}^_")
	punctuations = dict(zip(punctuations, ["" for i in range(len(punctuations))]))

	for message in df.message:
		if isinstance(message, str):
			messages.append(message.translate(str.maketrans(punctuations)).lower().split())

	for i in messages:
		for j in i:
			words.append(j)
		
	words = Counter(words)

	df = DataFrame(list(words.items()))
	df.rename(columns = {0:"word", 1:"word_count"}, inplace=True)

	df = df.sort_values("word_count", ascending = False)
	
	if destination is not None:
		df.to_csv(destination, index=False)

	return df

def count_user_messages(df: DataFrame, destination:str = None) -> DataFrame:
	
	users = Counter(df.user)
	users_tuple = []
	
	for i in users.items():
		users_tuple.append(i)
		
	df = DataFrame(users_tuple)
	df.rename(columns = {0:"user", 1:"messages"}, inplace = True)
	
	df = df.sort_values("messages", ascending = False)
	
	if destination is not None:
		df.to_csv(destination, index=False)
	
	return df

def users_z_score(df: DataFrame, destination:str = None) -> DataFrame:
	
	z_scores = []
	messages_a = count_user_messages(df)
	
	messages = list(messages_a.messages)
	
	std = np.std(messages)
	avg = sum(messages)/len(messages)
	
	for i in range(len(messages)):
		if avg != 0:
			if std != 0:
				z_scores.append([messages_a.user[i], (messages_a.messages[i]-avg)/std])
			else:
				z_scores.append([messages_a.user[i], 0])
		
	df = DataFrame(z_scores)
	df.rename(columns = {0:"user",1:"z_score"}, inplace = True)
	
	df = df.sort_values("z_score", ascending = False)
	
	positive_values = len([i for i in df.z_score if i>0])
	
	#print(positive_values, len(df.user))
	
	if destination is not None:
		df.to_csv(destination, index=False)
		
	return df

def total_messages_dir(folder, destination: str = None, title_list: list = None) -> DataFrame:
	
	cols = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			cols.append([title_list[i], len(folder[i])])
	else:
		for i in range(len(folder)):
			if title_list is not None:
				cols.append([title_list[i], len(make_table(folder[i]))])
			else:
				filename = folder[i].split("/")[len(folder[i].split())].replace(".json","")
				cols.append([filename, len(make_table(folder[i]))])	
				
	df = DataFrame(cols)
	df.rename(columns = {0:"chat",1:"messages_count"}, inplace=True)

	return df
	
if __name__ == "__main__":
	
	df = make_table("group_chat.json")
	words_df = words_stats(df)
	user_messages = count_user_messages(df)
	
	#print(309/sum(words_df.word_count))
	
	#print(user_messages)
	#print(users_z_score(df))
	
	#print(total_messages_dir(["input_json/group_chat.json"]))
	print(total_messages_dir([make_table("input_json/group_chat.json"), make_table("input_json/polito.json")], title_list=["test1","test2"]))
