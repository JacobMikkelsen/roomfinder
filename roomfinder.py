#https://stackoverflow.com/questions/11322430/how-to-send-post-request
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import re
import datetime

def getPage (url, post_fields):
    # Note: True in urlencode is needed to handle the forms array data fields
    request = Request(url, urlencode(post_fields, True).encode())
    return urlopen(request).read().decode()

def parsePage (contents):
    
    rooms = []
    
    rows = re.findall("(<tr class=\".+?tr>)", contents, re.DOTALL)
    
    for row in rows:
        cols = re.findall("<td class=\"data\">(.+?)</td>", row)
        rooms.append(cols)
    
    return rooms

def timeToValue(dt):
    hour = dt.hour
    half = 1 if dt.minute >= 30 else 0
    
    return 2 * hour + half

#TODO URL includes database set - would want to update over time?
url = "http://nss.cse.unsw.edu.au/tt/find_rooms.php?dbafile=2018-KENS-COFA.DBA&campus=KENS"

dt = datetime.datetime.now()

currentTime = timeToValue(dt)

fr_time = str(currentTime)
to_time = str(currentTime + 2)

days = dt.strftime("%A")
# TODO %e not supported by Windows?
fr_date = dt.strftime("%a %e %b %Y")
to_date = fr_date

print("Date: " + fr_date)

print("Times between " + fr_time + " and " + to_time)

# Maybe the Requests library or whatever makes constructing this nicer?
post_fields = {
                "search_rooms": "Search",
                "days[]": days,
                "fr_date": fr_date,
                "fr_time": fr_time,
                "to_date": to_date,
                "to_time": to_time,
                "RU[]": ["RU_GP-LEC", "RU_GP-TUTSEM"]
            }

contents = getPage(url, post_fields)
rooms = parsePage(contents)

print ("Found " + str(len(rooms)) + " rooms")

for room in rooms:
    print(room[1])
