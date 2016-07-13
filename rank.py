import subprocess
import json
import os
import sys
import yaml
import xlwt

BASEPATH = sys.path[0]
CONFIG = {}


def fetchCompetitionInfo(cid, password):
    print("FETCHING:", cid)
    global BASEPATH
    dataFilePath = os.path.join(
        BASEPATH, 'competition_data', str(cid) + '.json')
    infoJSON = subprocess.check_output(
        ['casperjs', 'fetch.js', str(cid), str(password)])

    dataFile = open(dataFilePath, 'wb')
    dataFile.write(infoJSON)
    dataFile.close()


def getCompetitionInfo(cid, password):
    global BASEPATH
    dataFilePath = os.path.join(
        BASEPATH, 'competition_data', str(cid) + '.json')

    if not os.path.isfile(dataFilePath):
        fetchCompetitionInfo(cid, password)

    dataFile = open(dataFilePath)
    infoJSON = dataFile.read(-1)
    dataFile.close()

    info = json.loads(str(infoJSON))
    return info


def getCompetitionRank(cid, password):
    info = getCompetitionInfo(cid, password)
    rawRanks = info['ranks']
    ranks = []
    for rank in rawRanks:
        ranks.append({
            'rank': rank[0],
            'id': rank[1],
            'solve': rank[2],
            'penalty': rank[3]
        })
    return ranks


def loadConfig():
    global CONFIG, BASEPATH
    configFilePath = os.path.join(BASEPATH, 'config.yaml')
    configFile = open(configFilePath)
    CONFIG = yaml.load(configFile)
    configFile.close()


def printPlayers():
    global CONFIG
    for player in CONFIG['players']:
        print(player['id'], player['name'])
        if 'usernames' in player:
            print("其他用户名：", player['usernames'])


def calcRank():
    global CONFIG
    players = CONFIG['players']
    playerMap = {}

    for i in range(0, len(players)):
        player = players[i]
        playerMap[player['id']] = i
        player['score'] = 0
        player['competitionNum'] = 0
        player['competitionsRank'] = []
        if 'usernames' in player:
            for username in player['usernames']:
                playerMap[username] = i

    for competition in CONFIG['competitions']:

        ranks = getCompetitionRank(competition['cid'], competition['password'])
        # 删除吃瓜围观人员ˊ_>ˋ
        ranks = [rank for rank in ranks if rank['id'] in playerMap]

        presentition = [False for i in range(0, len(players))]

        for i in range(0, len(ranks)):
            rank = ranks[i]
            player = players[playerMap[rank['id']]]
            player['score'] += (i + 1) / len(ranks)
            player['competitionNum'] += 1
            player['competitionsRank'].append(i + 1)
            presentition[playerMap[rank['id']]] = True

        for i in range(0, len(players)):
            if presentition[i] == False:
                players[i]['competitionsRank'].append('N/A')

    for key in range(0, len(players)):
        player = players[key]
        player['score'] = (1 - player['score'] /
                           player['competitionNum']) * 100
        #print (player['id'], player['name'], player['score'])

    players.sort(key=lambda player: player['score'], reverse=True)
    return players


def xlsOutput(data):
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=False)
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            sheet1.write(i, j, cell)
    workbook.save('rank.xls')


if __name__ == '__main__':
    loadConfig()
    players = calcRank()

    outputDatas = []
    title = []
    title.extend(['序号', '学号', '姓名'])
    for competition in CONFIG['competitions']:
        title.append(competition['name'])
    title.append('初步参考排名积分')
    outputDatas.append(title)

    No = 1

    for key in range(0, len(players)):
        outputData = []
        player = players[key]
        if player['competitionNum'] <= 2:
            continue
        outputData.extend([No, player['id'], player['name']])
        outputData.extend(player['competitionsRank'])
        outputData.append(player['score'])

        No += 1
        outputDatas.append(outputData)

    # 比赛次数不够计算排名的人
    for key in range(0, len(players)):
        outputData = []
        player = players[key]
        if player['competitionNum'] > 2:
            continue
        outputData.extend(['N/A', player['id'], player['name']])
        outputData.extend(player['competitionsRank'])
        outputData.append(player['score'])
        outputDatas.append(outputData)

    xlsOutput(outputDatas)
