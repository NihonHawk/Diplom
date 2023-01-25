from datetime import datetime as date
from datetime import timedelta
import json 

path = "data/tracker.json"

def tracker():
    with open(path, "r") as file:
        data_dict = json.loads(file.read()) 

    day = date.strptime(data_dict["date"], "%Y-%m-%d").date()
    today = date.today().date()

    if 0 < int(date.now().strftime("%H")) < 5:
        today -= timedelta(1)

    if day != today:
        # Every monday or week
        if today.isoweekday() == 1 or day.isocalendar()[1] != today.isocalendar()[1]:
            for items in data_dict["bosses"]:
                data_dict["bosses"][items] = 0
            for items in data_dict["reputation"]:
                data_dict["reputation"][items] = 0

        # 1 and 16 in last session
        if (today.day == 1 or today.day == 16) or (16 in range(day.day, today.day+1)) or (day.month != today.month and today.day >= 1):
            data_dict["abyss"] = 0

        # each day reset
        data_dict["daily"] = 0
        data_dict["date"] = str(today)

    with open(path, "w") as file:
        file.write(json.dumps(data_dict, indent=4))

    return data_dict

def update(name):
    with open(path, "r") as file:
        data_dict = json.loads(file.read())

    if name in data_dict["bosses"]:
        data_dict["bosses"][name] = 1 if data_dict["bosses"][name] == 0 else 0
    if name in data_dict["reputation"]:
        data_dict["reputation"][name] = 1 if data_dict["reputation"][name] == 0 else 0
    if name == "daily":
        data_dict[name] = 1 if data_dict[name] == 0 else 0
    if name == "abyss":
        data_dict[name] = 1 if data_dict[name] == 0 else 0

    with open(path, "w") as file:
        file.write(json.dumps(data_dict, indent=4))