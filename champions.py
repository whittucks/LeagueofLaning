import requests, json

def getLatestVersion():
  return requests.get(f'https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

def getChampions(version):
  
  champions = []
  champData = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json').json()
  champNames = [x for x in champData['data']]
  
  for x in champNames:
    champions.append([champData['data'][x]['key'], champData['data'][x]['name']])
  return champions
