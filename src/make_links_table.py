from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter

def make_links_table(df: DataFrame, destination: str = None) -> DataFrame:
			
	chat = []
	
	df["message"] = df["message"].astype(str)
		
	for i in range(len(df.message)):
		
		message = df.message[i]
		
		if "http" in message:
			for j in message.split():
				if "http" in j:
					link = j.replace("'","").replace("},","").replace("}]","")
					chat.append([df.date[i], df.weekday[i], df.hour[i], df.user[i], link])
	
	df = DataFrame(chat)
	df.rename(columns = {0:"date", 1:"weekday", 2:"hour", 3:"user", 4:"link"}, inplace = True)
		
	if destination is not None:
		df.to_csv(destination)
	
	return df

def links_count(df: DataFrame, destination: str = None) -> DataFrame:
	
	links_tuple = []
	
	df = make_links_table(df)
	links = list(df.link)

	links = Counter(links)
	
	for i in links.items():
		links_tuple.append(i)
		
	df = DataFrame(links_tuple)
	df.rename(columns = {0:"link", 1:"links_count"}, inplace = True)
	df = df.sort_values("links_count", ascending = False)

	if destination is not None:
		df.to_csv(destination)
	
	return df

def domains_count(df: DataFrame, destination: str = None) -> DataFrame:

	df = links_count(df)
	
	domains, domains_tuple = [], []
	
	for i in df.link:
		domain = i.split("://")[1]
		domain = domain.split("/")[0]
		domains.append(domain)
		
	domains = Counter(domains)
	
	for domain in domains.items():
		domains_tuple.append(domain)
		
	df = DataFrame(domains_tuple)
	df.rename(columns = {0:"domain", 1:"domain_count"}, inplace = True)
	
	df = df.sort_values("domain_count", ascending = False)
	
	if destination is not None:
		df.to_csv(destination)
		
	return df

if __name__ == "__main__":

	df = make_table("group_chat.json")
	
	#print(df)
	
	links_table = make_links_table(df)#, "links.csv")

	count_links_df = links_count(df)
	
	domains_df = domains_count(df)
	
	#print(links_table)
	#print(count_links_df)
	print(domains_count(df))