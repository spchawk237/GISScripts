# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# WebGIS_Dependencies.py
# Created on: 2023-03-23
# Works in ArcGIS Pro
#
# Author: Andrew Parkin/GIS Manager
#
# Description:
# Will show FCs and all their dependencies across your enterprise or AGOL enviroments
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
AGOLWAID_dict = {}

# Find Url IDs for all feature Classes
print('Collecting Data...')

# Grabbing all Feature Classes, Webmaps, and Web apps in Portal or AGOL

FeatureClasses = gis.content.search('', item_type='Feature Service', max_items=-1)
webmaps = gis.content.search('', item_type='Web Map', max_items=-1)
webapps = gis.content.search('', item_type='Application', max_items=-1)

for fc in FeatureClasses:
    print('Starting ' + str(fc.title))
    URL = gis.content.get(fc.id).url
    # Adding Key to Dictionaries
    AGOLFCName_dict[fc.id] = []
    AGOLFCURL_dict[fc.id] = []
    AGOLFCOwner_dict[fc.id] = []
    AGOLWMID_dict[fc.id] = []
    AGOLWAID_dict[fc.id] = []
    # Collecting all Feature Class Names and appending them to FeatureClassName Variable
    # AGOLFeatureClassName.append(fc.title)
    AGOLFCName_dict[fc.id].append(fc.title)
    # Collecting all Feature Class IDs and appending them to FeatureClassID Variable
    # AGOLFeatureClassID.append(fc.id)
    # Collecting all Feature Class URLs and appending them to FeatureClassURL Variable
    # AGOLFeatureClassURL.append(URL)
    AGOLFCURL_dict[fc.id].append(URL)
    # Collecting all Feature Class Owners and appending them to FeatureClassOwner Variable
    # AGOLFeatureClassOwner.append(fc.owner)
    AGOLFCOwner_dict[fc.id].append(fc.owner)
    # Finding Web Map IDs that use feature class
    matches = [m.id for m in webmaps if str(m.get_data()).find(URL) > -1]

    # If matches is not empty append to dictionary.
    if len(matches) > 0:
        AGOLWMID_dict.update({fc.id: matches})
    else:
        pass

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

            # If there's a match append to Dictionary if not, do nothing.
            if len(criteria) > 0:
                AGOLWAID_dict[fc.id].append(w.id)
            else:
                pass

        # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

    print('Finished ' + str(fc.title))

# Using dictionaries to create Data Frames
print('Appending Data to DF then Exporting to Excel')

MasterDF['Feature Class ID'] = AGOLFCName_dict.keys()
MasterDF['Feature Class Name'] = AGOLFCName_dict.values()
MasterDF['Feature Class Url'] = AGOLFCURL_dict.values()
MasterDF['Feature Class Owner'] = AGOLFCOwner_dict.values()
MasterDF['Number of Web Maps'] = len(AGOLWMID_dict.values())
MasterDF['Number of Web Apps'] = len(AGOLWAID_dict.values())

# Exporting DF to Excel
MasterDF.to_excel(ExcelOutput)
print('Test Complete')
