from make_table_from_chat import make_table
from pandas import DataFrame
from collections import Counter, defaultdict

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

def count_month_links(folder: DataFrame, destination: str = None, title_list = None) -> dict:

	df = make_links_table(folder)
	
	months_links = []
	
	for j in df.date:
		months_links.append(int(j.split("-")[1]))
	
	months_links = dict(Counter(months_links))
	
	links_dict = {k: v for k, v in sorted(months_links.items(), key=lambda item: item[0])}
	
	if len(links_dict) != 0:
		return links_dict
	else:
		links_dict = {1:0}
		return links_dict

def links_month_dir(folder: list[DataFrame], destination: str = None, title_list = None) -> DataFrame:
	
	links_list = []
	
	if isinstance(folder[0], DataFrame):
		for i in range(len(folder)):
			links_dict = count_month_links(folder[i])
			links_dict["title"] = title_list[i]
			links_list.append(links_dict)
			
	elif isinstance(folder, list):
		for i in range(len(folder)):
			links_list.append(folder[i])
			
	df = DataFrame(links_list)
	
	num_name_short = {1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}
	
	cols = df.columns.tolist()
	
	cols.remove("title")
	cols = sorted(cols)
	cols.append("title")
	cols = cols[-1:] + cols[:-1]
	
	df = df[cols]
	
	df.rename(columns = num_name_short, inplace = True)
			
	return df

def domains_count_dir(folder: list[DataFrame], title_list: list[str]) -> DataFrame:
	
	chat_domain = []
	
	for i in range(len(folder)):
		domain_num = sum(domains_count(folder[i]).domain_count)
		chat_domain.append([title_list[i], domain_num])
		
	df = DataFrame(chat_domain)
	df = df.rename(columns = {0:"title", 1:"domains_count"})
	
	return df

def group_chats_domains_dir(folder: list[DataFrame], title_list) -> DataFrame:
	
	chat_domain = []
	
	for i in range(len(folder)):
		domains = domains_count(folder[i])
		for j in range(len(domains)):
			chat_domain.append([domains.domain[j], title_list[i]])
			
	chat_domain_lists = chat_domain
	
	dd = defaultdict(list)
	
	for key, value in chat_domain_lists:
		dd[key].append(value)
		
	domain, chats = [], []
	
	for i in dd.items():
		domain.append(i[0])
		chats.append(i[1])
		
	df = DataFrame(data = 
	{"domain":domain, "chat":chats})
	
	return df

if __name__ == "__main__":

	df = make_table("input_json/polito.json")

	#print(df)
	
	links_table = make_links_table(df)#, "links.csv")

	count_links_df = links_count(df)
	
	domains_df = domains_count(df)
	
	#print(links_table)
	#print(count_links_df)
	#print(domains_count(df))
	
	#print(count_month_links(make_table("input_json/group_chat.json")))
	#count_links(df)
	
	#print(make_links_table(df))
	
	#print(links_month_dir([make_table("input_json/group_chat.json"), make_table("input_json/polito.json")], title_list=["group_chat", "polito"]))

	#print(make_table("input_json/personal_chat.json").date)
	
	# Fix count month links

	#try:
		#print(make_links_table(make_table("input_json/personal_chat.json")))
		#print(count_month_links(make_table("input_json/personal_chat.json")))
	#except AttributeError:
		#pass

	#print(links_month_dir([make_table("input_json/group_chat.json"), make_table("input_json/polito.json"), make_table("input_json/personal_chat.json")], title_list=["test1", "test2", "test3"]))
	
	#print(count_month)
	
	#print(domains_count_dir([df, make_table("input_json/group_chat.json")], title_list = ["polito", "group_chat"]))
	
	#print(group_chats_domains_dir([df, make_table("input_json/poliba.json")], title_list=["polito", "group_chat"]))
	
	print(domains_count(df))
