import requests
import json
import re
import time
from datetime import datetime  
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def log(x):
	print('[' + str(datetime.now()) + "] - "+x)

def redeem(key):
	r = requests.post("http://127.0.0.1:1242/Api/Command" , json=({"Command":"addlicense ASF "+str(key)}))
	log(json.loads(r.text)["Result"])


print("Sit back and enjoy while we collect games for you.")
while True:
	new = requests.get(url="https://www.reddit.com/r/FreeGamesOnSteam/new.json",headers=headers).text
	if new != '{"message": "Too Many Requests", "error": 429}':
		subID = ""
		pages = re.findall("steampowered.com/app/\d+",new)
		for i in pages:
			p = requests.get("https://store."+i).text
			s = re.search("subid\" value=\"(\d+)",p).group(1)
			subID = "s/"+s+", "+subID
		log(subID)
		redeem(subID)
	else:
		log("We're being ratelimited!")
	time.sleep(60*60)
