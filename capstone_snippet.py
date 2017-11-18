# Capstone code - with NO API KEYS
# Alice Topping
# Python Capstone Project

# outline

# house members data: name, ID, state, district 
# finance: total distributions
# district info: total members, total votes in last election?

import requests

def members():
	url= "https://api.propublica.org/congress/v1/115/house/members.json"
	headers= {'X-API-Key':'API KEY'}
	m = requests.get(url,headers=headers).json()
	print m.status_code

def finance():
	url= "https://api.propublica.org/campaign-finance/v1/2016/filings/types/F5.json"
	headers= {'X-API-Key':'API KEY'}
	f = requests.get(url,headers=headers).json()
	print f.status_code

def district():
	# will likely have static district data in it

if __name__=="__main__":
	