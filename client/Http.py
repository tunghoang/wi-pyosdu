import requests

def httpGet(url, headers=None):
    return requests.get(url, headers=headers)

def httpPostForm(url, data=None, headers=None):
    return requests.post(url, data=data, headers=headers)

def httpPostJson(url, json=None, headers=None):
    return requests.post(url, json=json, headers=headers)

def httpPutJson(url, json=None, headers=None):
    return requests.put(url, json=json, headers=headers)
