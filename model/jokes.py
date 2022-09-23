from email import header
import requests
import json

header ={
    'Accept': 'application/json'
}

def GetRandomJokes():
    response = requests.get('https://icanhazdadjoke.com/', headers=header)
    data = response.text
    dataJson = json.loads(data)
    return dataJson


# if __name__ == "__main__":
#     print(GetRandomJokes())
    
# ex responses:
# {
# 'id': 'MZDtW0gi3g',
# 'joke': 'Yesterday I confused the words "jacuzzi" and "yakuza". Now I\'m in hot water with the Japanese mafia.',
# 'status': 200
#  }