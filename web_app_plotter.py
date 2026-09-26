from streamlit import file_uploader, segmented_control, navigation, write, checkbox

from pages.entire_chat import Message_entire, Links_entire, Hours_entire, Days_entire, Weekdays_entire, Months_entire, Years_entire
from pages.chat_subset import Message_subset, Links_subset, Hours_subset, Days_subset, Weekdays_subset, Months_subset, Years_subset
from pages.user_subset import Message_user_subset, Links_user_subset, Hours_user_subset, Days_user_subset, Weekdays_user_subset, Months_user_subset, Years_user_subset

input_json = file_uploader(label="upload", type=["json"])
#print(input_json)

if input_json is not None:
	input_json = input_json.name
		
options = ["Entire chat", "Chat subset", "User subset"]
selection = segmented_control("Option page", options, selection_mode="single", default="Entire chat", required=True)

def Messages():
	Message_entire(input_json)
		
def Links():
	Links_entire(input_json)
		
def Hours():
	Hours_entire(input_json)
	
def Days():
	Days_entire(input_json)
		
def Weekday():
	Weekdays_entire(input_json)
		
def Months():
	Months_entire(input_json)
		
def Years():
	Years_entire(input_json)
	
if selection == "Entire chat":
	pg = navigation([Messages, Links, Days, Hours, Weekday, Months, Years])
	pg.run()
	
def Messages():
	Message_subset(input_json)
		
def Links():
	Links_subset(input_json)
		
def Hours():
	Hours_subset(input_json)
	
def Days():
	Days_subset(input_json)
		
def Weekdays():
	Weekdays_subset(input_json)
		
def Months():
	Months_subset(input_json)
		
def Years():
	Years_subset(input_json)
	
if selection == "Chat subset":
	pg = navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
	pg.run()
	
def Messages():
	Message_user_subset(input_json)
		
def Links():
	Links_user_subset(input_json)
		
def Hours():
	Hours_user_subset(input_json)
	
def Days():
	Days_user_subset(input_json)
		
def Weekdays():
	Weekdays_user_subset(input_json)
		
def Months():
	Months_user_subset(input_json)
		
def Years():
	Years_user_subset(input_json)
	
if selection == "User subset":
	pg = navigation([Messages, Links, Hours, Days, Weekdays, Months, Years])
	pg.run()