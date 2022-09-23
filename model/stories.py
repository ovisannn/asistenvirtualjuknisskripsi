from email import header
import requests
import json

header ={
    'Accept': 'application/json'
}

def GetRandomStories():
    response = requests.get('https://shortstories-api.herokuapp.com/', headers=header)
    data = response.text
    dataJson = json.loads(data)
    return dataJson


# if __name__ == "__main__":
#     print(GetRandomStories())

# ex responses:
# {
#   "_id"     : "5ff6fb389f24d116ce28d716",
#   "title"   : "Jupiter and the Monkey",
#   "author"  : "Aesop's Fables",
#   "story"   : "There was once a baby show among the Animals in the forest. Jupiter provided the prize. Of course all the proud mammas from far and near brought their babies. But none got there earlier than Mother Monkey. Proudly she presented her baby among the other contestants. As you can imagine, there was quite a laugh when the Animals saw the ugly flat-nosed, hairless, pop-eyed little creature. \"Laugh if you will,\" said the Mother Monkey. \"Though Jupiter may not give him the prize, I know that he is the prettiest, the sweetest, the dearest darling in the world.\"",
#   "moral"   : "Mother love is blind."
# }