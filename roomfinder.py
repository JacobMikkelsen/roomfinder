#!/usr/bin/python

import urllib
import httplib

import os
import subprocess

import re
import datetime

def getPage (post_fields):
    # https://docs.python.org/2.4/lib/httplib-examples.html
    headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"
            }
    
    # True needed for array values in POST
    params = urllib.urlencode(post_fields, True)
    
    #TODO URL includes database set - would want to update over time?
    host = "nss.cse.unsw.edu.au"
    url = "/tt/find_rooms.php?dbafile=2018-KENS-COFA.DBA&campus=KENS"
    
    conn = httplib.HTTPConnection(host)
    conn.request("POST", url, params, headers)
    
    response = conn.getresponse().read()
    
    return response

def parsePage (contents):
    
    rooms = []
    
    rows = re.findall("(<tr class=\".+?tr>)", contents, re.DOTALL)
    
    for row in rows:
        cols = re.findall("<td class=\"data\">(.+?)</td>", row)
        rooms.append(cols)
    
    return rooms

def timeToValue(hour, minute):
    half = 1 if minute >= 30 else 0
    
    return 2 * hour + half

def getDateTime ():
    env = os.environ.copy()
    env["TZ"] = "Australia/Sydney"
    
    # TODO Need to close the subprocess or anything?
    p = subprocess.Popen(["date", "+%Y %m %d %H %M"], env=env, stdout=subprocess.PIPE)
    output, _ = p.communicate()

    sections = re.findall("(\S+)", output.rstrip())
    print(sections)
    
    values = [int(value) for value in sections]
    
    dt = datetime.datetime(*values)
    
    return dt

def getPostFields():
    dt = getDateTime()

    currentTime = timeToValue(dt.hour, dt.minute)

    fr_time = str(currentTime)
    to_time = str(currentTime + 2)

    days = dt.strftime("%A")
    
    fr_week = to_week = dt.strftime("%V")
    
    print("week " + fr_week + " to week " + to_week)

    print("Times between " + fr_time + " and " + to_time)

    # Maybe the Requests library or whatever makes constructing this nicer?
    return {
            "search_rooms": "Search",
            "days[]": days,
            "fr_week": fr_week,
            "to_week": to_week,
            "fr_time": fr_time,
            "to_time": to_time,
            "RU[]": ["RU_GP-LEC", "RU_GP-TUTSEM"]
            }

def main ():
    post_fields = getPostFields()

    contents = getPage(post_fields)
    rooms = parsePage(contents)

    print ("Found " + str(len(rooms)) + " rooms")

    for room in rooms:
        print(room[1])

main()
