import requests
import json

def register(user_id):
    r = requests.get(f"http://95.217.177.249/casino/createacc?id={user_id}").text
    return json.loads(r)

def make_bet(mode, user_id, money, number):
    r = requests.get(f"http://95.217.177.249/casino/play{mode}?id={user_id}&bet={money}&number={number}").text
    return json.loads(r)# r["realNumber"]