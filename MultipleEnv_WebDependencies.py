# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# WebGIS_Dependencies.py
# Created on: 2023-04-14
# Works in ArcGIS Pro
#
# Author: Andrew Parkin/GIS Manager
#
# Description:
# Will show Items (Feature Services, Map Services KML etc) and all their dependencies across your systems.
# It will show relationship between Enterprise and AGOL
#
#
#
# Need to look into adding the following applications: Dashboard, Form, Hub Page, Solution, StoryMap
# ---------------------------------------------------------------------------

from arcgis.gis import GIS
import pandas as pd
import os

# Setup Date/time variables
date = datetime.date.today().strftime("%Y%m%d")
Time = time.strftime("%H%M", time.localtime())

# Setup export path to user's documents folder
userprofile = os.environ['USERPROFILE']
ReportDirectory = userprofile+"\\Documents\\WebGISDependenciesReports"
reportdirExists = os.path.exists(ReportDirectory)
if not reportdirExists:
    os.makedirs(ReportDirectory)
    print(ReportDirectory+" was not found, so it was created")
ExcelOutput = os.path.join(ReportDirectory, 'Dependencies_report_'+str(date)+'.xlsx')

print("Logging in..")

# *** USER INPUT IS NEEDED HERE***
# This is where you add your url, Username and password to replace placeholders. You need to do this for both agol and portal!

# AGOL Connection
agol = GIS('Insert AGOL home URL', 'AGOL Username', 'AGOL Password')

# Portal Connection

portal = GIS('Insert Portal URL', 'Portal Username', 'Portal Password')

print('Logged in!')

# Variables
ItemList = ['Administrative Report', 'Apache Parquet', 'CAD Drawing', 'CSV', 'Color Set', 'Content Category Set',
            'Document Link', 'Earth Configuration', 'Esri Classifier Definition', 'Export Package',
            'Feature Collection', 'Feature Collection Template', 'Feature Service', 'File Geodatabase', 'GeoJson',
            'GML', 'GeoPackage', 'Geocoding Service', 'Geodata Service', 'Geometry Service', 'Geoprocessing Service',
            'Globe Service', 'Image', 'KML', 'KML CollectionMap Service', 'Microsoft Excel', 'Microsoft Powerpoint',
            'Microsoft Word', 'Network Analysis Service', 'OGCFeatureServer', 'Oriented Imagery Catalog', 'PDF',
            'Relational Database Connection', 'Relational Database Connection', 'Report Template', 'SQLite Geodatabase',
            'Scene Service', 'Shapefile', 'Statistical Data Collection', 'StoryMap Theme', 'Style',
            'Symbol SetImage Service', 'Vector Tile Service', 'Visio Document', 'WFS', 'WMS', 'WMTS',
            'Workflow Manager Service', 'iWork Keynote', 'iWork Numbers', 'iWork Pages']

AppList = ['360 VR Experience', 'AppBuilder Extension', 'AppBuilder Widget Package', 'CityEngine Web Scene',
           'Code Attachment', 'Dashboard', 'Deep Learning Studio Project', 'Esri Classification Schema',
           'Excalibur Imagery Project', 'Experience Builder Widget', 'Experience Builder Widget Package', 'Form',
           'GeoBIM Application', 'GeoBIM Project', 'Hub Event', 'Hub Initiative', 'Hub Initiative Template', 'Hub Page',
           'Hub Project', 'Hub Site Application', 'Insights Data Engineering Model',
           'Insights Data Engineering Workbook', 'Insights Model', 'Insights Page', 'Insights Theme',
           'Insights Workbook', 'Insights Workbook Package', 'Investigation', 'Mission', 'Mobile Application',
           'Native Application', 'Native Application Installer', 'Notebook', 'Notebook Code Snippet Library',
           'Operation View', 'Operations Dashboard Add In', 'Operations Dashboard Extension', 'Ortho Mapping Project',
           'Ortho Mapping Template', 'Pro Map', 'StoryMap', 'Web AppBuilder WidgetSolution', 'Web Experience',
           'Web Experience Template', 'Web Map', 'Web Mapping Application', 'Web Scene', 'Workforce Project']

# Agol Variables
Agol_Items = []
Agol_Apps = []
# Portal Variables
Portal_Items = []
Portal_Apps = []

# List to store all my Function Results
FuncResults = []


# ***Defining function that will gather the information we need. ***
def my_func(connection, connection_type, item, webapps):
    # For some reason script won't pull in certain Urls so try and except added to prevent script breaking.
    # If url cant be pulled it will still collect as much as the item info added.
    try:
        # Item info
        item_info = item
        find_id = item_info.id
        find_url = connection.content.get(find_id).url
        item_title = item_info.title
        item_owner = item_info.owner
        item_type = item_info.type

        # Collects Web maps then Return subset of map IDs which contain the service URL we're looking for
        webmaps = connection.content.search('', item_type='Web Map', max_items=-1)
        matches = [m.id for m in webmaps if str(m.get_data()).find(find_url) > -1]

        # Create empty list to populate with results
        app_list = []

        # Check each web app for matches
        for w in webapps:

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
                FuncResults.append({'Environment': connection_type, 'Item Name': item_title, 'Item Type': item_type,
                                    'Item ID': find_id, 'Item Url': find_url, 'Item Owner': item_owner,
                                    'Application Name': a.title, 'Application Type': a.type, 'Application ID': a.id,
                                    'Application Owner': a.owner})

        if len(app_list) == 0:
            FuncResults.append({'Environment': connection_type, 'Item Name': item_title, 'Item Type': item_type,
                                'Item ID': find_id, 'Item Url': find_url, 'Item Owner': item_owner,
                                'Application Name': 'N/A', 'Application Type': 'N/A', 'Application ID': 'N/A',
                                'Application Owner': 'N/A'})

    except:
        print("Exception found gathering baseline item info.")
        item_info = item
        find_id = item_info.id
        item_title = item_info.title
        item_owner = item_info.owner
        item_type = item_info.type

        FuncResults.append({'Environment': connection_type, 'Item Name': item_title, 'Item Type': item_type,
                            'Item ID': find_id, 'Item Url': 'Cant find Url', 'Item Owner': item_owner,
                            'Application Name': 'N/A', 'Application Type': 'N/A', 'Application ID': 'N/A',
                            'Application Owner': 'N/A'})


# Grabbing feature class, Image service, Map Service, WFS, WMS Information
print('Collecting Item Data...')

# Combining all Item types into a single list

for i in ItemList:
    ATemp = agol.content.search('', item_type=i, max_items=-1)
    PTemp = portal.content.search('', item_type=i, max_items=-1)
    if len(ATemp) > 0:
        for at in ATemp:
            Agol_Items.append(at)
    if len(PTemp) > 0:
        for pt in PTemp:
            Portal_Items.append(pt)

print('Collected Item Data!')

print('Collecting Application Data..')

# Combining all Apps into a single list

for al in AppList:
    ATemp = agol.content.search('', item_type=al, max_items=-1)
    PTemp = portal.content.search('', item_type=al, max_items=-1)
    if len(ATemp) > 0:
        for at in ATemp:
            Agol_Apps.append(at)
    if len(PTemp) > 0:
        for pt in PTemp:
            Portal_Apps.append(pt)

print('Collected Application Data!')

# Running function through a loop for AGOL
print('Starting AGOL Items')
for i in Agol_Items:
    print(str(i.title))
    my_func(agol, 'Agol', i, Agol_Apps)
print('Finished AGOL Items')

# Running function through a loop for Portal
print('Starting Portal Items')
for i in Portal_Items:
    print(str(i.title))
    my_func(portal, 'Portal', i, Portal_Apps)
print('Finished Portal Items')

# Creating dataframe
print('Creating Data Frame')

df = pd.DataFrame(FuncResults)

# Sorting by Url with Portal items on top of AGOL
df1 = df.sort_values(by=['Item Url', 'Environment'], ascending=[True, False])
# Reindexing
df2 = df1.reset_index(drop=True)

# Creating Mask that will put a line of separation between each Item
mask = df2['Item Url'].ne(df2['Item Url'].shift(-1))
df3 = pd.DataFrame('', index=mask.index[mask] + .5, columns=df.columns)

# Creating the Final Dataframe.
new_df = pd.concat([df2, df3]).sort_index().reset_index(drop=True).iloc[:-1]
print(new_df)
print('Finished Data Frame')
# Exporting Dataframe to excel
print('Exporting to Excel')
new_df.to_excel(ExcelOutput, index=False)
print('Finished')
