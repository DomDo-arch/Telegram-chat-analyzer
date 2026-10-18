try:
	from src.make_table_from_chat import make_table
	from src.words_stats import words_stats, count_user_messages, users_z_score, total_messages_dir
	from src.weekday_stats import weekday_count, weekday_folder, weekday_percentage_folder
	from src.make_links_table import make_links_table, links_count, domains_count, links_month_dir, domains_count_dir, group_chats_domains_dir
	from src.hour_stats import hour_count, hour_dir
	from src.month_stats import month_count, month_dir, month_percentage_folder
	from src.year_stats import year_count, year_dir
	from src.season_stats import season_count, season_dir, season_percentage_folder
	from src.gini_user_table import gini
	from src.users_word_table import user_word_table
	from src.day_hour_stats import weekday_hour_df, day_hour_dir, hour_percentage_dir, weekday_hour_percentage
	from src.first_messages import days_sending_messages

except ModuleNotFoundError:
	
	import sys
	import os

	sys_path = os.getcwd().split("/")
	sys_path.append("src")
	sys_path = "/".join(sys_path)
	sys.path.append(sys_path)
	
	from make_table_from_chat import make_table
	from words_stats import words_stats, count_user_messages, users_z_score, total_messages_dir
	from weekday_stats import weekday_count, weekday_folder, weekday_percentage_folder
	from make_links_table import make_links_table, links_count, domains_count, links_month_dir, domains_count_dir, group_chats_domains_dir
	from hour_stats import hour_count, hour_dir
	from month_stats import month_count, month_dir, month_percentage_folder
	from year_stats import year_count, year_dir
	from season_stats import season_count, season_dir, season_percentage_folder
	from gini_user_table import gini
	from users_word_table import user_word_table
	from day_hour_stats import weekday_hour_df, day_hour_dir, hour_percentage_dir, weekday_hour_percentage
	from first_messages import days_sending_messages
	
import streamlit as st

import os

import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path

import json

from datetime import date

from pandas import DataFrame

def read_input(input_json: str, destination: str = None) -> list[DataFrame]:

	def return_table(input_json: str) -> DataFrame:

		data = json.loads(input_json.read())
		
		chat = []
		
		messages_dict = data["messages"]
		
		for i in messages_dict:
			if i["type"] == "message":
				dates = i["date"].split("T")[0]
				hour = i["date"].split("T")[1]
				if isinstance(i["text"], str):
					message = i["text"]
				elif isinstance(i["text"], list):
					message = i["text"]
				
				date_a = dates.split("-")
				
				day = int(date_a[2])
				month = int(date_a[1])
				year = int(date_a[0])
				
				weekday = date(year, month, day).weekday()
		
			if i["type"] == "message":
				user = i["from"]
				chat.append([dates, weekday, hour, user, message])

		df = DataFrame(chat)
		df.rename(columns = {0:"date", 1:"weekday", 2:"hour", 3:"user", 4:"message", 5:"media_type"}, inplace=True)
		
		df["message"] = df["message"].astype(str)
	
		return df
	
	if input_json is not None:
		return return_table(input_json)
	else:
		return None
	
def Message_entire(input_json: list) -> None:

	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None

	if df is not None:
		if len(input_json) == 1:
			# Constants
			positive_z_scores = len([i for i in users_z_score(df).z_score if i>0])
			users = len(users_z_score(df).z_score)
	
			st.header("Chat table")
			st.write(df)
	
			try:
				st.header("Words stats")
				st.write(gini(words_stats(df).word_count))
				st.write(words_stats(df))
			except KeyError:
				pass
	
			st.header("User messages")
			st.write(gini(count_user_messages(df).messages))
			st.write(count_user_messages(df))
	
			st.header("Messages z-score")
			st.write(positive_z_scores, positive_z_scores/users)
			st.write(users_z_score(df))
		
			try:
				st.header("Users word table")
				word = st.selectbox("Word", list(set(words_stats(df).word)))
				if word is not None:
					st.write(user_word_table(df, word))
			except KeyError:
				pass
		else:
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			df = total_messages_dir(dfs, title_list=titles)
			df = df.sort_values("chat")
			df = df.reset_index(drop=True)
			
			st.header("Chat messages")
			st.write(df)	
	
def Links_entire(input_json) -> None:
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		if len(input_json) == 1:
			st.header("Links table")
			st.write(make_links_table(df))
			
			st.header("Links count")
			df1 = links_count(df)
			df1 = df1.reset_index(drop=True)
			st.write(df1)
			
			#try:
			st.header("Domains table")
			df = domains_count(df)
			df = df.reset_index(drop=True)
			st.write(df)

		else:
			
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			#from streamlit_dynamic_filters import DynamicFilters

			try:
				st.header("Links for each month")
				df = links_month_dir(dfs, title_list = titles)
				df = df.sort_values("title")
				df = df.reset_index(drop=True)
				st.write(df)
				
				st.header("Domains count")
				df = domains_count_dir(dfs, titles)
				df = df.sort_values("title")
				df = df.reset_index(drop=True)
				with st.spinner("Loading..."):
					st.write(df)
				
				st.header("Group chats by domain")
				
				#dynamic_filters = DynamicFilters(df = group_chats_domains_dir(dfs, titles), filters = ["domain"])
				
				#dynamic_filters.display_filters()
				
				df = group_chats_domains_dir(dfs, titles)
				df = df.sort_values("chat")
				df = df.reset_index(drop=True)

				with st.spinner("Loading..."):
					st.write(df)

			except AttributeError as e:
				st.write("To fix. Detected at least a json containing 0 links.")
	
def Hours_entire(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		if len(input_json) == 1:
			st.header("Hour stats")
			st.write(gini(hour_count(df).messages))
			st.bar_chart(hour_count(df), x="hour", y="messages")
		else:
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Day part stats")
			df = hour_dir(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
def Days_entire(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None

	title_label = "mon tue wed thu fri sat sun".split()
	
	if df is not None:
		if len(input_json) == 1:
		
			st.header("Day stats")
			st.write("Chat length:", days_sending_messages(df)[0])
			st.write("Days sending at least a message:", days_sending_messages(df)[1])
			st.write(days_sending_messages(df)[0]/days_sending_messages(df)[1])
		
			st.header("Day hour stats")
			with st.spinner("Loading..."):
				st.write(weekday_hour_df(df))
			
			st.header("Weekday percentage")
			df1 = weekday_hour_percentage(df)
			with st.spinner("Loading..."):
				st.write(df1)
			
			st.header("Day hour percentage heatmap")
			with st.spinner("Loading..."):
				plt.figure(figsize=(len(df1.columns)-1,6))
				sns.heatmap(df1, annot = True, yticklabels=title_label, cmap="coolwarm")
				st.pyplot(plt)
				
		else:
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Day hour stats")
			df = day_hour_dir(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
			st.header("Day hour percentage")
			df = hour_percentage_dir(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			
			st.write(df)
			
			df = df.drop(columns=["title"])
			
			st.header("Day hour percentage heatmap")
			with st.spinner("Loading..."):
				plt.figure(figsize=(len(df.columns)-1,len(df)))
				sns.heatmap(df, annot=True, yticklabels=titles[::-1], cmap="coolwarm")
				st.pyplot(plt)
	
def Weekdays_entire(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		if len(input_json) == 1:
			st.header("Weekday stats")
			st.write(gini(weekday_count(df).messages))
			st.bar_chart(weekday_count(df), x="weekday", y="messages", sort=False)

		else:
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Weekday stats")
			df = weekday_folder(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
			st.header("Weekday percentage")
			df = weekday_percentage_folder(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
			df = weekday_percentage_folder(dfs, titles)
			df = df.sort_values("title")
			df = df.drop(columns=["title"])
	
			st.header("Weekday percentage heatmap")
			with st.spinner("Loading..."):
				plt.figure(figsize=(len(df.columns), len(df)))
				sns.heatmap(df, annot=True, yticklabels=titles[::-1], cmap="coolwarm")
				st.pyplot(plt)
	
def Months_entire(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		if len(input_json) == 1:
			st.header("Month stats")
			st.write(gini(month_count(df).messages))
			st.bar_chart(month_count(df), x="month", y="messages", sort=False)
		else:
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Month messages")
			df = month_dir(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
			st.header("Month messages percentage")
			df = month_percentage_folder(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
			df = df.drop(columns=["title"])
			
			st.header("Month messages percentage heatmap")
			with st.spinner("Loading..."):
				plt.figure(figsize=(len(df.columns), len(df)))
				sns.heatmap(df, annot=True, yticklabels=titles[::-1], cmap="coolwarm")
				st.pyplot(plt)
	
def Years_entire(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		if len(input_json) == 1:
			st.header("Year stats")
			st.bar_chart(year_count(df), x="year", y="messages")
	
			st.header("Season stats")
			st.bar_chart(season_count(df), x="season", y="messages")
		else:
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Year stats")
			st.bar_chart(year_dir(dfs), x="year", y="messages_count")
			
			st.header("Season stats")
			df = season_dir(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
			st.header("Season percentage")
			df = season_percentage_folder(dfs, title_list=titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			
			st.write(df)
			
			df = df.drop(columns = ["title"])
			
			st.header("Season percentage heatmap")
			with st.spinner("Loading..."):
				plt.figure(figsize=(len(df.columns), len(df)))
				sns.heatmap(df, annot=True, yticklabels=titles[::-1], cmap="coolwarm")
				st.pyplot(plt)
	
if __name__ == "__main__":
	
	#input_json = "group_chat.json"
	input_json = st.file_uploader(label="Files", type="json", accept_multiple_files = True)
	
	#st.write(input_json)
	
	#if input_json is not None: st.write(input_json)
	
	def Messages():
		Message_entire(input_json)
		
	def Links():
		Links_entire(input_json)
		
	def Hours():
		Hours_entire(input_json)
		
	def Days():
		Days_entire(input_json)
		
	def Weekdays():
		Weekdays_entire(input_json)
		
	def Months():
		Months_entire(input_json)
		
	def Years():
		Years_entire(input_json)
	
	pg = st.navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
	pg.run()
