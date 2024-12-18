import urllib.parse
import sqlite3, traceback, json, uuid, os, requests, secrets_parser

DB_IP=secrets_parser.parse("variables.txt")["DB_IP"]

class Connection:
    def __init__(self, collection) -> None:
        self.collection = collection

    def set(self, key, value):
        requests.get(f"http://{DB_IP}:7777/set?key="+urllib.parse.quote(self.collection+"/"+key)+"&val="+urllib.parse.quote(json.dumps(value)))

    def get(self, key):
        response=requests.get(f"http://{DB_IP}:7777/get?key="+urllib.parse.quote(self.collection+"/"+key)).text
        if json.loads(response)["Ok"]==False:
            return None
        return json.loads(json.loads(response)["Value"])

    def get_all(self):
        response=requests.get(f"http://{DB_IP}:7777/get_all?key="+urllib.parse.quote(self.collection)).text
        if json.loads(response)["Ok"]==False:
            return {}
        items=json.loads(json.loads(response)["Value"])
        out={}
        for key in items:
            out[key[len(self.collection)+1:]]=json.loads(items[key])
        return out

    def delete(self, key):
        requests.get(f"http://{DB_IP}:7777/delete?key="+urllib.parse.quote(self.collection+"/"+key))

def get_conn(name):
    return Connection(name)
