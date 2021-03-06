import requests
import json
import re
import time
from datetime import datetime  
import json
from os import path
from os import remove

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
configfile = "progress.json"

def log(x):
  print('[' + str(datetime.now()) + "] - "+x)

def redeem(key):
  r = requests.post("http://127.0.0.1:1242/Api/Command" , json=({"Command":"addlicense ASF "+str(key)})) #Send the games to ASF
  log(json.loads(r.text)["Result"])

if not path.exists(configfile):
  with open(configfile, "w") as config:
    config.write("{\"stopped_at\":0}") #create file

f = open(configfile,"r")
i = json.loads(f.read())['stopped_at'] #Total game count
f.close()

print("Sit back and enjoy while we collect games for you.")
while True:
  new = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0002/",headers=headers).text #Request list of all games and their IDs
  apps = json.loads(new)["applist"]["apps"] 
  appIDs = []
  del new
  for a in range(len(apps)):
    appIDs.append(apps[a]["appid"]) #Keep only the game IDs
  del apps
  log("Found all games, now crawling through them to check if any is free..")

  freeGames = []
  ratelimit = 0 #Rate limit
  k = 0 #loop cnt
  for id in appIDs:
    if k > i-2:
      i+=1
      ratelimit+=1
      appInfo=requests.get("https://store.steampowered.com/api/appdetails?appids="+str(id),headers=headers) #Get info about the current game from steamAPI
      if appInfo.status_code != 200:
        log("We're being rate limited! Waiting 60 seconds..")
        time.sleep(60)
        appInfo=requests.get("https://store.steampowered.com/api/appdetails?appids="+str(id),headers=headers)
      appInfo = appInfo.text
      if "discount_percent" in appInfo:
        s = re.search("discount_percent\":(\d+)",appInfo).group(1)
        if s == "100": #If there is a 100% reduction keep the game
          freeGames.append(re.search("packageid\":(\d+)",appInfo).group(1))
          log("Found game "+str(id)+'   ') 
      if re.search("packageid\":(\d+)",appInfo):
        print("Searched through "+str(i)+'/'+str(len(appIDs))+ " titles. Current subID: "+re.search("packageid\":(\d+)",appInfo).group(1)+"    ",end="\r")
      else:
        print("Searched through "+str(i)+'/'+str(len(appIDs))+ " titles.",end="\r")
      if ratelimit == 20:
        print("Sleeping 60 seconds to avoid being rate limited! ("+str(i)+"/"+str(len(appIDs))+")   ",end="\r")
        ratelimit = 0
        content = ""
        with open(configfile, 'r+') as f:
          content = json.loads(f.read())
          content["stopped_at"] = i
          content["found"] = freeGames
          f.seek(0)
        remove(configfile)
        with open(configfile,"w") as f:
          json.dump(content, f)
        time.sleep(60)
    else:
      k+=1
  redeem("a/"+",a/".join(freeGames)) #Redeem the games found
  redeem("s/"+",s/".join(freeGames)) #Redeem the games found
  del freeGames
  remove(configfile)
  with open(configfile, "w") as f:
    f.write("{\"stopped_at\":0}")
