import requests

def get_data(route="", params={}):
    r = requests.get(f"https://temp.jensderuiter.dev/{route}", params=params).json()
    return r["data"]
