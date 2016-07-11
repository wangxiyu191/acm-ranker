import subprocess
import json
import os
import sys
import yaml

BASEPATH=sys.path[0]

def getCompetitionInfo(cid,password):
    
    dataFilePath=os.path.join(BASEPATH,'competition_data',str(cid)+'.json')
    if os.path.isfile(dataFilePath):
        dataFile=open(dataFilePath)
        infoJSON=dataFile.read(-1)
        dataFile.close()

    else :
        infoJSON=subprocess.check_output(['casperjs', 'fetch.js', str(cid), str(password)])

        dataFile=open(dataFilePath,'wb')
        dataFile.write(infoJSON)
        dataFile.close()

    info=json.loads(infoJSON)
    return info
def getCompetitionRank(cid,password):
    info=getCompetitionInfo(cid,password)
    return info['ranks']

def readConfig():
    configFilePath=os.path.join(BASEPATH,'config.yaml')
    configFile=open(configFile)

    yaml.load_all(configFile)
