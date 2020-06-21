import requests
import json
import re
import time
from datetime import datetime  
import json
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def log(x):
	print('[' + str(datetime.now()) + "] - "+x)

def redeem(key):
	r = requests.post("http://127.0.0.1:1242/Api/Command" , json=({"Command":"addlicense ASF "+str(key)}))
	log(json.loads(r.text)["Result"])


print("Sit back and enjoy while we collect games for you.")
while True:
	new = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0002/",headers=headers).text
	apps = json.loads(new)["applist"]["apps"]
	appIDs = []
	del new
	for i in range(len(apps)):
		appIDs.append(apps[i]["appid"])
	del apps
	log("Found all games, now crawling through them to check if any is free..")

	freeGames = []
	for id in appIDs:
		appInfo=requests.get("https://store.steampowered.com/api/appdetails?appids="+str(id),headers=headers).text
		if "discount_percent" in appInfo:
			s = re.search("discount_percent\":(\d+)",appInfo).group(1)
			if s == "100":
				freeGames.append(re.search("packageid\":(\d+)",appInfo).group(1))
				log("Found game "+str(id))
	
	redeem("s/"+",s/".join(freeGames))
	log("Waiting 24 hours so we're not rate limited..")
	del freeGames
	time.sleep((60*60)*24)
