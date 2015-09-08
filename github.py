#!/usr/bin/python
import requests
import json
import os
from time import strftime

session = ""

def getTrafficData(repo):
    cookie=dict(user_session=session)
    header = {'accept': 'application/json'}
    s = requests.Session()
    request = s.get("https://github.com/dlinknctu/"+repo+"/graphs/traffic-data",headers=header,cookies=cookie)
    if request.status_code==200:
        return request.content
def getCloneData(repo):
    cookie=dict(user_session=session)
    header = {'accept': 'application/json'}
    s = requests.Session()
    request = s.get("https://github.com/dlinknctu/"+repo+"/graphs/clone-activity-data",headers=header,cookies=cookie)
    if request.status_code==200:
        return request.content
def storeJson(repo,data,dataType):
    
    #github data
    jsonData = json.loads(data)
    jsonData = jsonData['counts']   
    print len(jsonData) 
    #disk data
    oldJson = open(repo+"/"+dataType+".json")
    jsonOld = json.load(oldJson)
    oldJson.close()
    
    #new disk data
    newJson = open(repo+"/"+dataType+".json","w")
    for i in range(len(jsonData)):
        if any(b for (index, b) in enumerate(jsonOld) if b["bucket"] == jsonData[i]['bucket']) == False:
            print jsonData[i]['bucket']
            jsonOld.append({
                    'bucket':jsonData[i]['bucket'],
                    'total':jsonData[i]['total'],
                    'unique':jsonData[i]['unique']
                })
        else:
            I = next(index for (index, b) in enumerate(jsonOld) if b["bucket"] == jsonData[i]['bucket'])
            jsonOld[I]['bucket'] = jsonData[i]['bucket']
            jsonOld[I]['total'] = jsonData[i]['total']
            jsonOld[I]['unique'] = jsonData[i]['unique']


    json.dump(jsonOld,newJson,indent=4)

def commit(repo):
    day = strftime('%Y-%m-%d')
    os.chdir(repo+"/")
    os.system("git add .")
    os.system("git commit -m \""+day+"\"")
    os.chdir("../")
def run(repo):
    storeJson(repo,getTrafficData(repo),"traffic")
    storeJson(repo,getCloneData(repo),"clone")
    #commit(repo)

run("openadm")
run("opennet")
