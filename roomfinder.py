#https://stackoverflow.com/questions/11322430/how-to-send-post-request

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import re

#TODO URL includes database set - would want to update over time?

def getPage (url, post_fields):
    request = Request(url, urlencode(post_fields).encode())
    return urlopen(request).read().decode()

def parsePage (contents):
    
    rooms = []
    
    rows = re.findall("(<tr class=\".+?tr>)", contents, re.DOTALL)
    
    for row in rows:
        cols = re.findall("<td class=\"data\">(.+?)</td>", row)
        rooms.append(cols)
    
    return rooms

def timeToValue(time):
    #TODO DST shenanigans
    #TODO How should time be input?
    
    #Assuming time is a integer value 7-22
    return time * 2
    

url = "http://nss.cse.unsw.edu.au/tt/find_rooms.php?dbafile=2017-KENS-COFA.DBA&campus=KENS"

fr_time = timeToValue(input("From: "))
to_time = timeToValue(input("  To: "))

post_fields = {
                "search_rooms":"Search",
                "days[]": "Monday",
                "fr_time": str(fr_time),
                "to_time": str(to_time),
                "RU[]": "RU_GP-LEC",
                "RU[]": "RU_GP-TUTSEM"
            }

contents = getPage(url, post_fields)
rooms = parsePage(contents)

for room in rooms:
    print(room[1])
