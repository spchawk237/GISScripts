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

# Grabbing feature class, Image service, Map Service, WFS, WMS Information
print('Collecting Item Data...')

ItemList = ['Feature Service', 'Image Service', 'Map Service', 'WFS', 'WMS']

# Combining all Item types into a single list
Items = []

for i in ItemList:
    Temp = gis.content.search('', item_type=i, max_items=-1)
    if len(Temp) > 0:
        for t in Temp:
            Items.append(t)

ItemsTest = Items[:10]
print('Collected Item Data!')
print('Collecting Webmaps...')

webmaps = gis.content.search('', item_type='Web Map', max_items=-1)

print('Collected Webmaps!')
print('Collecting Application Data..')
# Gathering Application Information

AppList = ['Web Map', 'Web Mapping Application', 'Hub Site Application', 'Dashboard', 'Form', 'Hub Page', 'Solution',
           'StoryMap']

# Combining all Apps into a single list
WebApps = []
for al in AppList:
    Temp = gis.content.search('', item_type=al, max_items=-1)
    if len(Temp) > 0:
        for t in Temp:
            WebApps.append(t)

print('Collected Application Data!')


# List to store all my Function Results

FuncResults = []


# ***Defining function that will gather the information we need. ***
def my_func(item):
    # Layer ID to search for and its URL
    item_info = item
    find_id = item_info.id
    find_url = gis.content.get(find_id).url

    # Additional Item Variables
    item_title = item_info.title
    item_owner = item_info.owner
    item_type = item_info.type

    # Return subset of map IDs which contain the service URL we're looking for
    matches = [m.id for m in webmaps if str(m.get_data()).find(find_url) > -1]

    # Create empty list to populate with results
    app_list = []

    # Check each web app for matches
    for w in WebApps:

        try:
            # Get the JSON as a string
            wdata = str(w.get_data())

            criteria = [
                wdata.find(find_url) > -1,  # Check if URL is directly referenced
                any([wdata.find(m) > -1 for m in matches])  # Check if any matching maps are in app
            ]

            # If layer is referenced directly or indirectly, append app to list
            if any(criteria):
                app_list.append(w)

        # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

    if len(app_list) > 0:
        for a in app_list:
            FuncResults.append({'Item Name': item_title, 'Item Type': item_type, 'Item ID': find_id,
                                'Item Owner': item_owner, 'Application Name': a.title, 'Application Type': a.type,
                                'Application ID': a.id, 'Application Owner': a.owner})

    if len(app_list) == 0:
        FuncResults.append({'Item Name': item_title, 'Item Type': item_type, 'Item ID': find_id,
                            'Item Owner': item_owner, 'Application Name': 'N/A', 'Application Type': 'N/A',
                            'Application ID': 'N/A', 'Application Owner': 'N/A'})


# Running function through a loop
for i in ItemsTest:
    print("Starting " + str(i.title))
    my_func(i)
    print("Finished " + str(i.title))

df = pd.DataFrame(FuncResults)

print(df)
df.to_excel(ExcelOutput, index=False)
print('Finished')
