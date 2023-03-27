# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# WebGIS_Dependencies.py
# Created on: 2023-03-23
# Works in ArcGIS Pro
#
# Author: Andrew Parkin/GIS Manager
#
# Description:
# Will collect an inventory of Feature classes, web maps, and web apps.
# Will then find which Web Maps and Apps that each feature service is used in. *Work in Progess*
#
# Works with Enterprise GIS & ArcGIS Online
#
# Works with:
# Map Image/Feature Layers
# Tables
# GP Tools
# Locators
# Tile Layers
#
# ---------------------------------------------------------------------------

from arcgis.gis import GIS
import pandas as pd

#Variables
# File Location you want the excel output
ExcelOutput = r'R:\GIS\GIS_LOGS\ExcelOutputs\WebGISDependencies.xlsx'

# Logging in works with Enterprise and AGOL

print("Logging into AGOL..")

gis = GIS('Insert url to AGOL OR ENTERPRISE HERE', Username, Password)

print('Logged into AGOL!')



# Feature Class Variables
FeatureClassName = []
FeatureClassID = []
FeatureClassURL = []
FeatureClassOwner = []
FeatureClassDF = pd.DataFrame()

# Find Url IDs for all feature Classes
print('Collecting all Feature Class Data...')

# Grabbing all Feature Classes in Portal or AGOL

FeatureClasses = gis.content.search('', item_type='Feature Service', max_items=-1)

for fc in FeatureClasses:
    Name = fc.title
    ID = fc.id
    Owner = fc.owner
    # Collecting all Feature Class Names and appending them to FeatureClassName Variable
    FeatureClassName.append(Name)
    # Collecting all Feature Class IDs and appending them to FeatureClassID Variable
    FeatureClassID.append(ID)
    # Collecting all Feature Class URLs and appending them to FeatureClassURL Variable
    FeatureClassURL.append(gis.content.get(ID).url)
    # Collecting all Feature Class Owners and appending them to FeatureClassOwner Variable
    FeatureClassOwner.append(Owner)

# Creating Rows in FeatureClassDF for each of the lists we iterated through the for loop
FeatureClassDF['Feature Class Name'] = FeatureClassName
FeatureClassDF['Feature Class ID'] = FeatureClassID
FeatureClassDF['Feature Class URL'] = FeatureClassURL
FeatureClassDF['Feature Class Owner'] = FeatureClassOwner

print('Collected all Feature Class Data!')
print('Collecting all webmap Data..')

# WebMap Class Variables
WebMapName = []
WebMapID = []
WebMapOwner = []
WebMapDF = pd.DataFrame()

# Grabbing all Web Maps in Portal or AGOL

webmaps = gis.content.search('', item_type='Web Map', max_items=-1)

for wm in webmaps:
    Name = wm.title
    ID = wm.id
    Owner = wm.owner
    # Collecting all Web Map Names and appending them to WebMapName Variable
    WebMapName.append(Name)
    # Collecting all Web map IDs and appending them to WebMapID Variable
    WebMapID.append(ID)
    # Collecting all Web Map Owners and appending them to WebMapOwner Variable
    WebMapOwner.append(Owner)

# Creating Rows in WebMapDF for each of the lists we iterated through the for loop

WebMapDF['Wep Map Name'] = WebMapName
WebMapDF['Wep Map ID'] = WebMapID
WebMapDF['Wep Map Owner'] = WebMapOwner

print('Collected all webmap Data!')
print('Collecting all webapp Data..')

# WebApp Class Variables
WebAppName = []
WebAppID = []
WebAppURL = []
WebAppOwner = []
WebAppDF = pd.DataFrame()

# Grabbing all Web Apps in Portal or AGOL

webapps = gis.content.search('', item_type='Application', max_items=-1)

for wa in webapps:
    Name = wa.title
    ID = wa.id
    Owner = wa.owner
    # Collecting all Web App Names and appending them to WebAppName Variable
    WebAppName.append(Name)
    # Collecting all Web App Ids and appending them to WebAppID Variable
    WebAppID.append(ID)
    # Collecting all Web App Urls and appending them to WebAppURL Variable
    WebAppURL.append(gis.content.get(ID).url)
    # Collecting all Web App Owners and appending them to WebAppOwner Variable
    WebAppOwner.append(Owner)

# Creating Rows in WebAppDF for each of the lists we iterated through the for loop

WebAppDF['Wep App Name'] = WebAppName
WebAppDF['Wep App ID'] = WebAppID
WebAppDF['Wep App URL'] = WebAppURL
WebAppDF['Wep App Owner'] = WebAppOwner

print('Collected all webapp Data!')

# Combining all 3 Full Inventory DataFrames into Excel
print('Combining Full Inventory DataFrames to xlsx..')

with pd.ExcelWriter(ExcelOutput) as writer:
    FeatureClassDF.to_excel(writer, sheet_name='Feature Classes')
    WebMapDF.to_excel(writer, sheet_name='Web Maps')
    WebAppDF.to_excel(writer, sheet_name='Web Apps')

print('Combined Full Inventory DataFrames to xlsx!')



# Return subset of map IDs which contain the service URL we're looking for *** TWEAK TO FIT LIKE ABOVE WHERE IT APPENDS TO TWO TABLES TO GET WEB MAP ID AND URL

print('Finding Webmaps matching ID..')
matches = [m.id for m in webmaps if str(m.get_data()).find(find_url) > -1]
print('Found Webmaps matching ID!')

# Pull list of all web apps in portal
print('Finding all Webapps...')
webapps = gis.content.search('', item_type='Application', max_items=-1)
print('Found all Webapps!')

# Create empty list to populate with results
app_list = []

# Check each web app for matches
for fc in FeatureClassURL:
    for w in webapps:

        try:
            # Get the JSON as a string
            wdata = str(w.get_data())

            criteria = [
                wdata.find(fc) > -1,  # Check if URL is directly referenced
                any([wdata.find(i) > -1 for i in matches])  # Check if any matching maps are in app
            ]

            # If layer is referenced directly or indirectly, append app to list
            if any(criteria):
                app_list.append(w)

        # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

output = pd.DataFrame([{'title': a.title, 'id': a.id, 'type': a.type} for a in app_list])

print(output)
