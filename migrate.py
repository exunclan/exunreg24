import litedb, json
import hashlib

events=litedb.get_conn("events")

data=json.loads(open("data/events.json").read())

for event in data["events"]:
    events.set(hashlib.sha256(event.encode()).hexdigest()[:6], data["default"] | {"image":data["events"][event], "name":event, "descriptions":{
        "long":data["descriptions"][event]["long"],
        "short":data["descriptions"][event]["short"]
    }})