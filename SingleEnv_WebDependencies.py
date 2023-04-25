# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# WebGIS_Dependencies.py
# Created on: 2023-03-23
# Works in ArcGIS Pro
#
# Author: Andrew Parkin/GIS Manager with a lot of help and support of Phil Baranyai #SpatialAF
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

# Logging in works with Enterprise and AGOL

print('Logged in...')

# *** USER INPUT IS NEEDED HERE***
# This is where you add your url, Username and password to replace placeholders.

gis = GIS('Insert url to AGOL OR ENTERPRISE HERE', 'Username', 'Password')

print('Logged in!')

# Grabbing Item Information
print('Collecting Item Data...')

ItemList = ['Administrative Report', 'Apache Parquet', 'CAD Drawing', 'CSV', 'Color Set', 'Content Category Set',
            'Document Link', 'Esri Classifier Definition', 'Export Package', 'Feature Collection',
            'Feature Collection Template', 'Feature Service', 'File Geodatabase', 'GeoJson', 'GML', 'GeoPackage',
            'Geocoding Service', 'Geodata Service', 'Geometry Service', 'Geoprocessing Service', 'Globe Service',
            'Image', 'KML', 'KML CollectionMap Service', 'Microsoft Excel', 'Microsoft Powerpoint',
            'Microsoft Word', 'Network Analysis Service', 'OGCFeatureServer', 'Oriented Imagery Catalog', 'PDF',
            'Relational Database Connection', 'Relational Database Connection', 'Report Template', 'SQLite Geodatabase',
            'Scene Service', 'Service Definition', 'Shapefile', 'Statistical Data Collection', 'StoryMap Theme',
            'Style', 'Symbol SetImage Service', 'Vector Tile Service', 'Visio Document', 'WFS', 'WMS', 'WMTS',
            'Workflow Manager Service', 'iWork Keynote', 'iWork Numbers', 'iWork Pages']

# Combining all Item types into a single list
Items = []

for i in ItemList:
    Temp = gis.content.search('', item_type=i, max_items=-1)
    if len(Temp) > 0:
        for t in Temp:
            Items.append(t)

print('Collected Item Data!')
print('Collecting Webmaps...')

webmaps = gis.content.search('', item_type='Web Map', max_items=-1)

print('Collected Webmaps!')
print('Collecting Application Data..')
# Gathering Application Information

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
    # Item info
    item_info = item
    find_id = item_info.id
    find_url = gis.content.get(find_id).url
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
                                'Item Url': find_url, 'Item Owner': item_owner, 'Application Name': a.title,
                                'Application Type': a.type, 'Application ID': a.id, 'Application Owner': a.owner})

    if len(app_list) == 0:
        FuncResults.append({'Item Name': item_title, 'Item Type': item_type, 'Item ID': find_id, 'Item Url': find_url,
                            'Item Owner': item_owner, 'Application Name': 'N/A', 'Application Type': 'N/A',
                            'Application ID': 'N/A', 'Application Owner': 'N/A'})


# Running function through a loop
for i in Items:
    print("Starting " + str(i.title))
    my_func(i)
    print("Finished " + str(i.title))

df = pd.DataFrame(FuncResults)

print(df)
df.to_excel(ExcelOutput, index=False)
print('Finished')
