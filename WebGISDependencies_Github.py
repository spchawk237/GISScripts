# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# WebGIS_Dependencies.py
# Created on: 2023-03-23
# Works in ArcGIS Pro
#
# Author: Andrew Parkin/GIS Manager
#
# Description:
# Will show FCs and all their dependencies across your enterprise or AGOL environments
#
#
# Works with Enterprise GIS & ArcGIS Online
#
#
# ---------------------------------------------------------------------------

from arcgis.gis import GIS
import pandas as pd

# Logging in works with Enterprise and AGOL

print("Logging into AGOL..")

gis = GIS('Insert url to AGOL OR ENTERPRISE HERE', 'Username', 'Password')

print('Logged into AGOL!')

# File Location you want the excel output
ExcelOutput = r'Insert File Path Here!!!!'

# Master Data Frame Variable
MasterDF = pd.DataFrame()

# Dictionaries
AGOLFCName_dict = {}
AGOLFCURL_dict = {}
AGOLFCOwner_dict = {}
AGOLWMID_dict = {}
AGOLWMName_dict = {}
AGOLWMOwner_dict = {}
AGOLWAID_dict = {}
AGOLWAName_dict = {}
AGOLWAOwner_dict = {}

# Find Url IDs for all feature Classes
print('Collecting Data...')

# Grabbing all Feature Classes, Webmaps, and Web apps in Portal or AGOL

FeatureClasses = gis.content.search('', item_type='Feature Service', max_items=-1)
webmaps = gis.content.search('', item_type='Web Map', max_items=-1)
webapps = gis.content.search('', item_type='Application', max_items=-1)
dashboard = gis.content.search('', item_type='Dashboard', max_items=-1)
form = gis.content.search('', item_type='Form', max_items=-1)
hubpage = gis.content.search('', item_type='Hub Page', max_items=-1)
solution = gis.content.search('', item_type='Solution', max_items=-1)
storymap = gis.content.search('', item_type='StoryMap', max_items=-1)

for fc in FeatureClasses:
    print('Starting ' + str(fc.title))
    URL = gis.content.get(fc.id).url
    # Adding Key to Dictionaries
    AGOLFCName_dict[fc.id] = []
    AGOLFCURL_dict[fc.id] = []
    AGOLFCOwner_dict[fc.id] = []
    AGOLWMID_dict[fc.id] = []
    AGOLWMName_dict[fc.id] = []
    AGOLWMOwner_dict[fc.id] = []
    AGOLWAID_dict[fc.id] = []
    AGOLWAName_dict[fc.id] = []
    AGOLWAOwner_dict[fc.id] = []
    # Collecting all Feature Class Names and appending them to FeatureClassName Variable
    AGOLFCName_dict[fc.id].append(fc.title)
    # Collecting all Feature Class URLs and appending them to FeatureClassURL Variable
    AGOLFCURL_dict[fc.id].append(URL)
    # Collecting all Feature Class Owners and appending them to FeatureClassOwner Variable
    AGOLFCOwner_dict[fc.id].append(fc.owner)
    # Finding Web Map IDs that use feature class
    matches = [m.id for m in webmaps if str(m.get_data()).find(URL) > -1]
    matchesName = [m.title for m in webmaps if str(m.get_data()).find(URL) > -1]
    matchesOwner = [m.owner for m in webmaps if str(m.get_data()).find(URL) > -1]

    # If matches is not empty append to dictionary.
    if len(matches) > 0:
        AGOLWMID_dict.update({fc.id: matches})
        AGOLWMName_dict.update({fc.id: matchesName})
        AGOLWMOwner_dict.update({fc.id: matchesOwner})
    else:
        pass

    criteria_matchesID = []
    criteria_matchesName = []
    criteria_matchesOwner = []
    # Finding Matching Web Applications
    for w in webapps:
        try:
            # Get the JSON as a string
            wdata = str(w.get_data())

            # Finding Matches
            criteria = [
                wdata.find(URL) > -1,  # Check if URL is directly referenced
                any([wdata.find(i) > -1 for i in matches])  # Check if any matching maps are in app
            ]

            # If there's a match append if not, do nothing.
            if any(criteria):
                criteria_matchesID.append(w.id)
                criteria_matchesName.append(w.title)
                criteria_matchesOwner.append(w.owner)

            # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

        if len(criteria_matchesID) > 0:
            print(set(criteria_matchesID))
            AGOLWAID_dict.update({fc.id: set(criteria_matchesID)})
            AGOLWAName_dict.update({fc.id: set(criteria_matchesName)})
            AGOLWAOwner_dict.update({fc.id: set(criteria_matchesOwner)})

    print('Finished ' + str(fc.title))


# Using dictionaries to create Data Frames
print('Appending Data to DF then Exporting to Excel')

# Variables
AGOLWMID_Count = []
AGOLWAID_Count = []

MasterDF['Feature Class ID'] = AGOLFCName_dict.keys()
MasterDF['Feature Class Name'] = AGOLFCName_dict.values()
MasterDF['Feature Class Url'] = AGOLFCURL_dict.values()
MasterDF['Feature Class Owner'] = AGOLFCOwner_dict.values()

# Getting Web Map and Application Counts
for k in AGOLWMID_dict:
    AGOLWMID_Count.append(len(AGOLWMID_dict[k]))

for k in AGOLWAID_dict:
    AGOLWAID_Count.append(len(AGOLWAID_dict[k]))

MasterDF['Number of Web Maps'] = AGOLWMID_Count
MasterDF['Web Map ID'] = AGOLWMID_dict.values()
MasterDF['Web Map Name'] = AGOLWMName_dict.values()
MasterDF['Web Map Owner'] = AGOLWMOwner_dict.values()
MasterDF['Number of Web Apps'] = AGOLWAID_Count
MasterDF['Web App IDs'] = AGOLWAID_dict.values()
MasterDF['Web App Names'] = AGOLWAName_dict.values()
MasterDF['Web App Owner'] = AGOLWAOwner_dict.values()

# Exporting DF to Excel
MasterDF.to_excel(ExcelOutput, index=False)

print('Script Complete')