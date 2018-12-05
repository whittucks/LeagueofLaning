import requests, json, operator, time

def getAccountId(inputName): 
  from main import APIkey
  playerInfo = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{inputName}?api_key={APIkey}').json()  
  return playerInfo['accountId'];

#Gets a list of as users match ID's
def getMatchList(accountId):
  from main import APIkey
  matchList = requests.get(f'https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/{accountId}?api_key={APIkey}').json()
  return [x['gameId'] for x in matchList['matches']]

#Gets overall game data including lane and champ selected
def getGameInfo(matchid, inputName):
  from main import APIkey
  gameInfo = requests.get(f'https://na1.api.riotgames.com/lol/match/v3/matches/{matchid}?api_key={APIkey}').json()
  gameData = {}

  for x in gameInfo['participantIdentities']:
    if x['player']['summonerName'] == inputName:
      gameData['myParticipantID'] = x['participantId']
	
  for x in gameInfo['participants']:
    if x['participantId'] == gameData['myParticipantID']:
      gameData['myChampID'] = x['championId']
      gameData['myLane'] = x['timeline']['lane']
      gameData['myRole'] = x['timeline']['role']
      gameData['goldPerMinDeltas'] = x['timeline']['goldPerMinDeltas']["0-10"]
  for x in gameInfo['participants']:
    if x['participantId'] != gameData['myParticipantID'] and x['timeline']['lane'] == gameData['myLane'] and x['timeline']['role'] == gameData['myRole']:
      gameData['enemyChampID'] = x['championId']
	#print("--- %s seconds ---" % (time.time() - start_time))
  return gameData;

#Gets the specific information from the firs ten minutes of the game
def getGameTimeLine(matchId,participantId):
  from main import APIkey
  timeline = requests.get(f'https://na1.api.riotgames.com/lol/match/v3/timelines/by-match/{matchId}?api_key={APIkey}').json()
  gameData = {}
  gameData['deaths'] = []
  gameData['csCounts'] = []
  gameData['gold'] = []
  gameData['inBase'] = []

  for frames in timeline['frames']:
    if frames['timestamp'] <= 600200:
      gameData['gold'].append([frames['timestamp'], frames['participantFrames'][str(participantId)]['totalGold']])
      gameData['csCounts'].append([frames['timestamp'],frames['participantFrames'][str(participantId)]['minionsKilled'] + frames['participantFrames'][str(participantId)]['jungleMinionsKilled']])
    
      for event in frames['events']:
        if 'victimId' in event and event['victimId'] == participantId:
          if len(event['assistingParticipantIds']) > 0:
            gameData['deaths'].append([frames['timestamp'],True])
          else:
            gameData['deaths'].append([frames['timestamp'],False])
        if event['type'] == 'ITEM_PURCHASED'and event['participantId'] == participantId:
          gameData['inBase'].append(event['timestamp'])
  return gameData
