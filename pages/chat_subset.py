try:
	from make_table_from_chat import make_table
	from day_stats import filter_interval_table
	from words_stats import words_stats, count_user_messages, users_z_score, total_messages_dir
	from weekday_stats import weekday_count, weekday_folder
	from make_links_table import make_links_table, links_count, domains_count, links_month_dir
	from hour_stats import hour_count, hour_dir
	from month_stats import month_count, month_dir
	from year_stats import year_count, year_dir
	from season_stats import season_count, season_dir
	from gini_user_table import gini
	from users_word_table import user_word_table
	from day_hour_stats import weekday_hour_df, day_hour_dir

except ModuleNotFoundError:
	
	import sys
	import os

	sys_path = os.getcwd().split("/")
	sys_path.append("src")
	sys_path = "/".join(sys_path)
	sys.path.append(sys_path)
	
	from make_table_from_chat import make_table
	from day_stats import filter_interval_table
	from words_stats import words_stats, count_user_messages, users_z_score, total_messages_dir
	from weekday_stats import weekday_count, weekday_folder
	from make_links_table import make_links_table, links_count, domains_count, links_month_dir
	from hour_stats import hour_count, hour_dir
	from month_stats import month_count, month_dir
	from year_stats import year_count, year_dir
	from season_stats import season_count, season_dir
	from gini_user_table import gini
	from users_word_table import user_word_table
	from day_hour_stats import weekday_hour_df, day_hour_dir

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
	
def return_days_interval():
	
	period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
	
	days_interval = 7

	if period == "7d":
		days_interval = 7
	elif period == "30d":
		days_interval = 30
	elif period == "90d":
		days_interval = 90
	elif period == "150d":
		days_interval = 150
	elif period == "365d":
		days_interval = 365
		
	if period is not None:
		st.write(period)
	
	return days_interval
	
def Message_subset(input_json):
		
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		
		period = st.menu_button("Period", options = ["7d","30d","90d","150d","365d"])
	
		days_interval = 7

		if period == "7d":
			days_interval = 7
		elif period == "30d":
			days_interval = 30
		elif period == "90d":
			days_interval = 90
		elif period == "150d":
			days_interval = 150
		elif period == "365d":
			days_interval = 365
		
		if period is not None:
			st.write(period)

		if len(input_json) == 1:
		
			df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
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
			
			dfs = [filter_interval_table(df, df.date[len(df.date)-1], days_interval)  for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Chat messages")
			
			df = total_messages_dir(dfs, title_list=titles)
			df = df.sort_values("chat")
			df = df.reset_index(drop=True)
			
			st.write(df)
	
def Links_subset(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		days_interval = return_days_interval()

		if len(input_json) == 1:
		
			df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)

			st.header("Links table")
			st.write(make_links_table(df))
		
			try:
				st.header("Links count")
				st.write(gini(links_count(df).links_count))
				st.write(links_count(df))
		
				st.header("Domains table")
				st.write(gini(domains_count(df).domain_count))
				st.write(domains_count(df))
			except AttributeError:
				pass
		else:
			#start_date = df.date[len(df.date)-100]
			
			#dfs = [filter_interval_table(read_input(input_json[i]), start_date, days_interval) for i in range(1, len(input_json))]
			#df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
			#dfs = [filter_interval_table(df, df.date[len(df.date)-1], days_interval) for i in range(1, len(input_json))]
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Links for each month")
			df = links_month_dir(dfs, title_list = titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
			
def Hours_subset(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		days_interval = return_days_interval()
		if len(input_json) == 1:
			df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
		
			st.header("Hour stats")
			st.write(gini(hour_count(df).messages))
			st.bar_chart(hour_count(df), x="hour", y="messages")
		else:
			
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Day part stats")
			df = hour_dir(dfs, title_list = titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
		
def Days_subset(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	title_label = "mon tue wed thu fri sat sun".split()
	
	if df is not None:
		days_interval = return_days_interval()
		if len(input_json) == 1:
			df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)

			st.header("Day hour stats")
			with st.spinner("Loading..."):
				st.write(weekday_hour_df(df))
		
			st.header("Day hour heatmap")
			with st.spinner("Loading..."):
				plt.figure(figsize=(len(weekday_hour_df(df).columns)-1,6))
				sns.heatmap(weekday_hour_df(df), annot=True, yticklabels=title_label, cmap="coolwarm")
				st.pyplot(plt)
		else:
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Day hour stats")
			df = day_hour_dir(dfs, title_list = titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
	
def Weekdays_subset(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None

	if df is not None:
		days_interval = return_days_interval()
		if len(input_json) == 1:
			df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
		
			st.header("Weekday stats")
			st.write(gini(weekday_count(df).messages))
			st.bar_chart(weekday_count(df), x="weekday", y="messages")
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
	
def Months_subset(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None
	
	if df is not None:
		days_interval = return_days_interval()
		if len(input_json) == 1:
			df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
			st.header("Month stats")
			st.write(gini(month_count(df).messages))
			st.bar_chart(month_count(df), x="month", y="messages")
		else:
			
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Month messages")
			df = month_dir(dfs, titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
	
def Years_subset(input_json):
	
	try:
		df = read_input(input_json[0])
	except IndexError:
		df = None

	if df is not None:
		#days_interval = return_days_interval()
		if len(input_json) == 1:
			#df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
			st.header("Year stats")
			st.bar_chart(year_count(df), x="year", y="messages")
	
			st.header("Season stats")
			st.write(gini(season_count(df).messages))
			st.bar_chart(season_count(df), x="season", y="messages")
		else:
			
			dfs = [read_input(input_json[i]) for i in range(1, len(input_json))]
			dfs.append(df)
			
			titles = [i.name.replace(".json","") for i in input_json]
			titles = [titles[(i+1)%len(titles)] for i in range(len(titles))]
			
			st.header("Year stats")
			st.bar_chart(year_dir(dfs, titles), x="year", y="messages_count")
			
			st.header("Season stats")
			df = season_dir(dfs, titles)
			df = df.sort_values("title")
			df = df.reset_index(drop=True)
			st.write(df)
	
if __name__ == "__main__":
	
	#input_json = "group_chat.json"
	input_json = st.file_uploader(label="upload", type=["json"], accept_multiple_files = True)

	
	def Message():
		Message_subset(input_json)
		
	def Links():
		Links_subset(input_json)
		
	def Days():
		Days_subset(input_json)
		
	def Hours():
		Hours_subset(input_json)
		
	def Weekdays():
		Weekdays_subset(input_json)
		
	def Months():
		Months_subset(input_json)
		
	def Years():
		Years_subset(input_json)
	
	pg = st.navigation([Message, Links, Hours, Days, Weekdays, Months, Years])
	pg.run()
