# Purpose

The purpose of this script is to consume an ICAL URL and return any events that are happening within the next hour

# Work In Progress

This is a work-in-progress. By no means will this handle all features of the ICAL RFC 5545 standard.

## Broken Stuff

Things this will NOT do:
 - Handle different timezones
 - Handle multiple properties with the same name (called "tags" in the code). Last propertie will override all previous with same name
 - Handle events with no start time
 - A lot more..
