import streamlit as st

try:
	from src.make_table_from_chat import make_table
	from src.words_stats import words_stats, count_user_messages, users_z_score
	from src.weekday_stats import weekday_count
	from src.make_links_table import make_links_table, links_count, domains_count
	from src.hour_stats import hour_count
	from src.month_stats import month_count
	from src.year_stats import year_count
	from src.season_stats import season_count
	from src.gini_user_table import gini
	from src.users_word_table import user_word_table
	from src.day_hour_stats import weekday_hour_df

except ModuleNotFoundError:
	
	import sys
	import os

	sys_path = os.getcwd().split("/")
	sys_path.append("src")
	sys_path = "/".join(sys_path)
	sys.path.append(sys_path)
	
	from make_table_from_chat import make_table
	from words_stats import words_stats, count_user_messages, users_z_score
	from weekday_stats import weekday_count
	from make_links_table import make_links_table, links_count, domains_count
	from hour_stats import hour_count
	from month_stats import month_count
	from year_stats import year_count
	from season_stats import season_count
	from gini_user_table import gini
	from users_word_table import user_word_table
	from day_hour_stats import weekday_hour_df

import seaborn as sns
import matplotlib.pyplot as plt

import os
from pathlib import Path

def read_input(input_json):
	
	if input_json is not None:
		
		file_path = os.path.abspath(input_json)

		root = Path.home()
		matches = list(root.rglob(input_json))[0]

		st.write(matches)
		
		input_json = matches
		
		df = make_table(input_json)

		df["message"] = df["message"].astype(str)

		return df
	
def Message_entire(input_json):
	
	df = read_input(input_json)

	if df is not None:
		# Constants
		positive_z_scores = len([i for i in users_z_score(df).z_score if i>0])
		users = len(users_z_score(df).z_score)
	
		st.header("Chat table")
		st.write(df)
	
		st.header("Words stats")
		st.write(gini(words_stats(df).word_count))
		st.write(words_stats(df))
	
		st.header("User messages")
		st.write(gini(count_user_messages(df).messages))
		st.write(count_user_messages(df))
	
		st.header("Messages z-score")
		st.write(positive_z_scores, positive_z_scores/users)
		st.write(users_z_score(df))
		
		st.header("Users word table")
		word = st.selectbox("Word", list(set(words_stats(df).word)))
		if word is not None:
			st.write(user_word_table(df, word))
	
def Links_entire(input_json):
	
	df = read_input(input_json)
	
	if df is not None:
	
		st.header("Links table")
		st.write(make_links_table(df))
		
		st.header("Links count")
		st.write(links_count(df))
		
		st.header("Domains table")
		st.write(domains_count(df))
		
def Days_entire(input_json):
	
	df = read_input(input_json)
	title_label = "mon tue wed thu fri sat sun".split()
	
	if df is not None:
		st.header("Day hour stats")
		with st.spinner("Loading..."):
			st.write(weekday_hour_df(df))
		
		st.header("Day hour heatmap")
		with st.spinner("Loading..."):
			plt.figure(figsize=(len(weekday_hour_df(df).columns)-1,6))
			sns.heatmap(weekday_hour_df(df), yticklabels=title_label, cmap="coolwarm")
			st.pyplot(plt)
	
def Hours_entire(input_json):
	
	df = read_input(input_json)
	
	if df is not None:
		st.header("Hour stats")
		st.write(gini(hour_count(df).messages))
		st.bar_chart(hour_count(df), x="hour", y="messages")
	
def Weekdays_entire(input_json):
	
	df = read_input(input_json)
	
	if df is not None:
		st.header("Weekday stats")
		st.write(gini(weekday_count(df).messages))
		st.bar_chart(weekday_count(df), x="weekday", y="messages")
	
def Months_entire(input_json):
	
	df = read_input(input_json)
	
	if df is not None:
		st.header("Month stats")
		st.write(gini(month_count(df).messages))
		st.bar_chart(month_count(df), x="month", y="messages")
	
def Years_entire(input_json):
	
	df = read_input(input_json)
	
	if df is not None:
		st.header("Year stats")
		st.bar_chart(year_count(df), x="year", y="messages")
	
		st.header("Season stats")
		st.bar_chart(season_count(df), x="season", y="messages")
