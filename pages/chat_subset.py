import streamlit as st

try:
	from make_table_from_chat import make_table
	from day_stats import filter_interval_table
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

except ModuleNotFoundError:
	
	import sys
	import os

	sys_path = os.getcwd().split("/")
	sys_path.append("src")
	sys_path = "/".join(sys_path)
	sys.path.append(sys_path)
	
	from make_table_from_chat import make_table
	from day_stats import filter_interval_table
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
		
		input_json = matches
		
		df = make_table(input_json)

		df["message"] = df["message"].astype(str)

		return df
	
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
	
	df = read_input(input_json)
	
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

	if df is not None:
		
		df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
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
	
def Links_subset(input_json):
	
	df = read_input(input_json)
	
	days_interval = return_days_interval()
	
	if df is not None:
		
		df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)

		st.header("Links table")
		st.write(make_links_table(df))
		
		st.header("Links count")
		st.write(gini(links_count(df).links_count))
		st.write(links_count(df))
		
		st.header("Domains table")
		st.write(gini(domains_count(df).domain_count))
		st.write(domains_count(df))
	
def Hours_subset(input_json):
	
	df = read_input(input_json)
	
	days_interval = return_days_interval()
	
	if df is not None:
		df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
		
		st.header("Hour stats")
		st.write(gini(hour_count(df).messages))
		st.bar_chart(hour_count(df), x="hour", y="messages")
		
def Days_subset(input_json):
	
	df = read_input(input_json)
	
	days_interval = return_days_interval()
	
	title_label = "mon tue wed thu fri sat sun".split()
	
	if df is not None:
		df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)

		st.header("Day hour stats")
		with st.spinner("Loading..."):
			st.write(weekday_hour_df(df))
		
		st.header("Day hour heatmap")
		with st.spinner("Loading..."):
			plt.figure(figsize=(len(weekday_hour_df(df).columns)-1,6))
			sns.heatmap(weekday_hour_df(df), yticklabels=title_label, cmap="coolwarm")
			st.pyplot(plt)
	
def Weekdays_subset(input_json):
	
	df = read_input(input_json)
	
	days_interval = return_days_interval()
	
	if df is not None:
		df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
		
		st.header("Weekday stats")
		st.write(gini(weekday_count(df).messagesr))
		st.bar_chart(weekday_count(df), x="weekday", y="messages")
	
def Months_subset(input_json):
	
	df = read_input(input_json)
	
	days_interval = return_days_interval()
	
	if df is not None:
		df = filter_interval_table(df, df.date[len(df.date)-1], days_interval)
		st.header("Month stats")
		st.write(gini(month_count(df).messages))
		st.bar_chart(month_count(df), x="month", y="messages")
	
def Years_subset(input_json):
	
	df = read_input(input_json)
	
	if df is not None:
		st.header("Year stats")
		st.bar_chart(year_count(df), x="year", y="messages")
	
		st.header("Season stats")
		st.write(gini(season_count(df).messages))
		st.bar_chart(season_count(df), x="season", y="messages")
