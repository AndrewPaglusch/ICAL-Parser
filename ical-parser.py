#!/usr/bin/env python3

import requests
import re
from datetime import datetime

ICAL = 'https://calendar.google.com/path/to/your/ical/file.ics'

try:
    r = requests.get(ICAL)
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    exit(1)

events = []

tag_regex = re.compile(r'^[A-Z-]+(?=[;:])')

# loop each event
for i in r.text.split('END:VEVENT'):
    last_tag = ''
    curr_event = {}

    # loop each line in this event
    for j in i.splitlines():
        if len(j) == 0:
            continue

        tag = tag_regex.match(j)

        if tag:
            data = j.split(tag.group())[1]
            curr_event[tag.group().lower().strip()] = data[1:].strip()
            last_tag = tag.group().lower().strip()
        else:
            # this line has no valid tag. Prob a cont of previous tag
            # take contents and add to end of last tag's value
            curr_event[last_tag] = curr_event.get(last_tag, '') + j[1:]

    events.append(curr_event)

for event in events:
    # skip over strange dtstart data that we won't parse
    #   Ex: DTSTART;TZID=America/Chicago:20170909T060000
    #   Ex: DTSTART;VALUE=DATE:20181116
    #   Ex: DTSTART:20170909T060000Z
    if not re.match(r'^\d{8}T\d{6}', event.get('dtstart', '')):
        continue

    date = event['dtstart'].split('T')[0]
    time = event['dtstart'].split('T')[1][:-1]

    t = datetime.strptime(f'{date} {time}', '%Y%m%d %H%M%S')
    min_until_event = int((t - datetime.utcnow()).total_seconds() / 60)

    if min_until_event <= 60 and min_until_event >= 0:
        print(f"You have an event in {min_until_event} minutes!\n\n",
              f"	Summary: {event['summary']}\n",
              f"	Start Time: {event['dtstart']}\n",
              f"	End Time: {event['dtend']}\n",
              f"	Location: {event['location']}\n",
              f"	Description: {event['description']}\n")
