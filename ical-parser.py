#!/usr/bin/env python3

import requests
from datetime import datetime

ICAL = 'https://calendar.google.com/path/to/your/ical/file.ics'

try:
    r = requests.get(ICAL)
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    exit(1)

raw_events = []
curr_event = {}
curr_tag = ''
for i in r.text.splitlines():
    lasttag = i.split(':')[0] if i.split(':')[0].isupper() else lasttag

    if i.startswith('END:VEVENT'):
        raw_events.append(curr_event)
        curr_event = {}
        curr_tag = ''
    elif i.startswith(' '):
        if lasttag == 'DESCRIPTION':
            curr_event['description'] = curr_event.get('description', '') + i[1:]
    else:
        tag = i.split(':')[0]
        data = i.split(tag)[1]
        curr_event[tag.lower()] = data[1:]

for event in raw_events:

    # skip items that have no start time
    if not event.get('dtstart', None):
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
