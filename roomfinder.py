#!/usr/bin/python

import urllib
import httplib

import re
import datetime

def getPage (url, post_fields):
    # https://docs.python.org/2.4/lib/httplib-examples.html
    headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"
            }
    
    # True needed for array values
    params = urllib.urlencode(post_fields, True)
    
    conn = httplib.HTTPConnection("nss.cse.unsw.edu.au")
    conn.request("POST", "/tt/find_rooms.php?dbafile=2018-KENS-COFA.DBA&campus=KENS", params, headers)
    
    response = conn.getresponse().read()
    
    return response

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

def main ():
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

main()
