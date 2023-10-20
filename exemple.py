import requests

resultado = requests.get('https://blaze-4.com/api/roulette_games/recent').json()
num = [int(i["roll"]) for i in resultado]
nova = []
num.reverse()
for i in num:
    nova.append(i)

print(nova)