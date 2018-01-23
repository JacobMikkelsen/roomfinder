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
    
    # True needed for array values
    params = urllib.urlencode(post_fields, True)
    
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

def getTimeDate ():
    env = os.environ.copy()
    env["TZ"] = "Australia/Sydney"
    
    timeFormat = ["%a", "%d", "%b", "%Y", "%A", "%H", "%M"]
    
    p = subprocess.Popen(["date", "+" + ' '.join(timeFormat)], env=env, stdout=subprocess.PIPE)
    output, _ = p.communicate()
    
    # print("Got output:")
    # print(output.rstrip())
    
    sections = re.findall("(\S+)", output.rstrip())
    print(sections)
    
    # Check if we have same number of matches as time format
    if len(sections) != len(timeFormat):
        print("Unexpected number of date outputs")
        print("Format: " + str(timeFormat))
        print("Output: " + str(sections))
        exit(1)
    
    timeInfo = {}
    
    # TODO Chuck this all into a datetime object instead? Probably a nicer way
    # of working with it....
    
    for i in range(len(timeFormat)):
        timeInfo[timeFormat[i]] = sections[i]
    
    print(timeInfo)
    
    return timeInfo
    
    

def main ():
    #TODO URL includes database set - would want to update over time?
    url = "http://nss.cse.unsw.edu.au/tt/find_rooms.php?dbafile=2018-KENS-COFA.DBA&campus=KENS"

    # TODO GOSH DARN TIMEZONES
    # Maybe we could handle this via javascript? Set the dropdown options to be
    # the local user's time?
    dt = datetime.datetime.now()
    
    # To get current hour in Sydney (24h mode), in shell:
    # TZ=Australia/Sydney date +"%H"
    # Run as another process, capture output, bingo?
    # Add other format options to grab more information?
    
    timeInfo = getTimeDate()
    
    # Need to close the subprocess or anything?

    currentTime = timeToValue(int(timeInfo["%H"]), int(timeInfo["%M"]))

    fr_time = str(currentTime)
    to_time = str(currentTime + 2)

    days = timeInfo["%A"]
    # TODO %e not supported by Windows?
    fr_date = ' '.join([timeInfo["%a"], timeInfo["%d"], timeInfo["%b"], timeInfo["%Y"]])
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

    contents = getPage(post_fields)
    rooms = parsePage(contents)

    print ("Found " + str(len(rooms)) + " rooms")

    for room in rooms:
        print(room[1])

main()
