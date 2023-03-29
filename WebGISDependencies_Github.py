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

# AGOL Feature Class Variable
AGOLFeatureClassName = []
AGOLFeatureClassID = []
AGOLFeatureClassURL = []
AGOLFeatureClassOwner = []
AGOLWebMapMatchesID = []
AGOLWebAppMatchesID = []

# Find Url IDs for all feature Classes
print('Collecting Data...')

# Grabbing all Feature Classes, Webmaps, and Web apps in Portal or AGOL

FeatureClasses = gis.content.search('', item_type='Feature Service', max_items=-1)
print(len(FeatureClasses))
webmaps = gis.content.search('', item_type='Web Map', max_items=-1)
print(len(webmaps))
webapps = gis.content.search('', item_type='Application', max_items=-1)
print(len(webapps))

for fc in FeatureClasses:
    print('Starting ' + str(fc.title))
    URL = gis.content.get(fc.id).url
    # Collecting all Feature Class Names and appending them to FeatureClassName Variable
    AGOLFeatureClassName.append(fc.title)
    # Collecting all Feature Class IDs and appending them to FeatureClassID Variable
    AGOLFeatureClassID.append(fc.id)
    # Collecting all Feature Class URLs and appending them to FeatureClassURL Variable
    AGOLFeatureClassURL.append(URL)
    # Collecting all Feature Class Owners and appending them to FeatureClassOwner Variable
    AGOLFeatureClassOwner.append(fc.owner)

    print('Finding matches for ' + str(fc.title))
    # Finding Web Map IDs that use feature class
    matches = [m.id for m in webmaps if str(m.get_data()).find(URL) > -1]
    print('Found matches for ' + str(fc.title))
    AGOLWebMapMatchesID.append(matches)
    # Finding Matching Web Applications
    for w in webapps:
        try:
            print('Finding Webapp Matches' + str(fc.title))
            # Get the JSON as a string
            wdata = str(w.get_data())

            criteria = [
                wdata.find(URL) > -1,  # Check if URL is directly referenced
                any([wdata.find(i) > -1 for i in matches])  # Check if any matching maps are in app
            ]

            # If layer is referenced directly or indirectly, append app to list
            if any(criteria):
                print('Found Webapp Matches' + str(fc.title))
                AGOLWebAppMatchesID.append(w)
            else:
                pass

        # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

print('Appending Data to DF then Exporting to Excel')
# Creating Rows in FeatureClassDF for each of the lists we iterated through the for loop
MasterDF['Feature Class Name'] = AGOLFeatureClassName
MasterDF['Feature Class ID'] = AGOLFeatureClassID
MasterDF['Feature Class URL'] = AGOLFeatureClassURL
MasterDF['Feature Class Owner'] = AGOLFeatureClassOwner
MasterDF['Web Map Matches'] = AGOLWebMapMatchesID
MasterDF['Web App Matches'] = AGOLWebAppMatchesID

MasterDF.to_excel(ExcelOutput)
print('Script Complete')
