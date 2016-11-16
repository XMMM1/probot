import requests

def getRandomJoke():
    r = requests.get('http://api.icndb.com/jokes/random')
    r = r.json()
    if r['type'] == "success":
        if r['value'] and r['value']['joke']:
            return r['value']['joke']
    return None
