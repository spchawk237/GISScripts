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

# Item Dictionaries
ItemName_dict = {}
ItemURL_dict = {}
ItemOwner_dict = {}
ItemType_dict = {}
# Web Map Dictionaries
WMID_dict = {}
WMName_dict = {}
WMOwner_dict = {}
# Web Mapping Application Dictionaries
WMAID_dict = {}
WMAName_dict = {}
WMAOwner_dict = {}
# Dashboard Dictionaries
DBID_dict = {}
DBName_dict = {}
DBOwner_dict = {}
# Hub Site Application Dictionaries
HSAID_dict = {}
HSAName_dict = {}
HSAOwner_dict = {}
# Form Dictionaries
FormID_dict = {}
FormName_dict = {}
FormOwner_dict = {}
# Hub Page Dictionaries
HPID_dict = {}
HPName_dict = {}
HPOwner_dict = {}
# Solutions Dictionaries
SID_dict = {}
SName_dict = {}
SOwner_dict = {}
# Story Map Dictionaries
SMID_dict = {}
SMName_dict = {}
SMOwner_dict = {}

# Find Url IDs for all feature Classes
print('Collecting Item Data...')

# Grabbing feature class, Image service, Map Service, WFS, WMS Information

ItemList = ['Feature Service', 'Image Service', 'Map Service', 'WFS', 'WMS']

# Combining all Items into a single list
Items = []

for i in ItemList:
    Temp = gis.content.search('', item_type=i, max_items=-1)
    if len(Temp) > 0:
        for t in Temp:
            Items.append(t)

print('Collected Item Data!')
print('Collecting Application Data..')
# Gathering Application Information

webmaps = gis.content.search('', item_type='Web Map', max_items=-1)
webapp = gis.content.search('', item_type='Web Mapping Application', max_items=-1)
hubsiteapp = gis.content.search('', item_type='Hub Site Application', max_items=-1)
dashboard = gis.content.search('', item_type='Dashboard', max_items=-1)
form = gis.content.search('', item_type='Form', max_items=-1)
hubpage = gis.content.search('', item_type='Hub Page', max_items=-1)
solution = gis.content.search('', item_type='Solution', max_items=-1)
storymap = gis.content.search('', item_type='StoryMap', max_items=-1)
AppList = ['Web Map', 'Web Mapping Application', 'Hub Site Application', 'Dashboard', 'Form', 'Hub Page', 'Solution',
           'StoryMap']

# Combining all Apps into a single list
WebApps = []
for w in AppList:
    Temp = gis.content.search('', item_type=w, max_items=-1)
    if len(Temp) > 0:
        for t in Temp:
            Items.append(t)

print('Collected Application Data!')
print('Finding Relationships...')

for i in Items:
    print('Starting ' + str(i.title))
    URL = gis.content.get(i.id).url
    # Adding Keys to Item Dictionaries
    ItemName_dict[i.id] = []
    ItemOwner_dict[i.id] = []
    ItemURL_dict[i.id] = []
    ItemType_dict[i.id] = []
    # Adding Keys to Web Map Dictionaries
    WMID_dict[i.id] = []
    WMName_dict[i.id] = []
    WMOwner_dict[i.id] = []
    # Adding Keys to Web Mapping Application Dictionaries
    WMAID_dict[i.id] = []
    WMAName_dict[i.id] = []
    WMAOwner_dict[i.id] = []
    # Adding Keys to Hub Site Application Dictionaries
    HSAID_dict[i.id] = []
    HSAName_dict[i.id] = []
    HSAOwner_dict[i.id] = []
    # Adding Keys to Form Dictionaries
    FormID_dict[i.id] = []
    FormName_dict[i.id] = []
    FormOwner_dict[i.id] = []
    # Adding Keys to Hub Page Dictionaries
    HPID_dict[i.id] = []
    HPName_dict[i.id] = []
    HPOwner_dict[i.id] = []
    # Adding Keys to Solutions Dictionaries
    SID_dict[i.id] = []
    SName_dict[i.id] = []
    SOwner_dict[i.id] = []
    # Adding Keys to Story Map Dictionaries
    SMID_dict[i.id] = []
    SMName_dict[i.id] = []
    SMOwner_dict[i.id] = []
    # Collecting all Item Names and appending them
    ItemName_dict[i.id].append(i.title)
    # Collecting all Item URLs and appending them
    ItemURL_dict[i.id].append(URL)
    # Collecting all Items Owners and appending them
    ItemOwner_dict[i.id].append(i.owner)
    # Collecting all Item Types and appending them
    ItemType_dict[i.id].append(i.type)
    # Finding Web Map IDs that use feature class
    matches = [m.id for m in webmaps if str(m.get_data()).find(URL) > -1]
    matchesName = [m.title for m in webmaps if str(m.get_data()).find(URL) > -1]
    matchesOwner = [m.owner for m in webmaps if str(m.get_data()).find(URL) > -1]

    # If matches is not empty append to dictionary.
    if len(matches) > 0:
        WMID_dict.update({i.id: matches})
        WMName_dict.update({i.id: matchesName})
        WMOwner_dict.update({i.id: matchesOwner})
    else:
        pass

    # Web Mapping Application Matches
    WMA_matchesID = []
    WMA_matchesName = []
    WMA_matchesOwner = []
    # Hub Site Application Matches
    HSA_matchesID = []
    HSA_matchesName = []
    HSA_matchesOwner = []
    # Dashboard Matches
    DB_matchesID = []
    DB_matchesName = []
    DB_matchesOwner = []
    # Form Matches
    Form_matchesID = []
    Form_matchesName = []
    Form_matchesOwner = []
    # Hub Page Matches
    HP_matchesID = []
    HP_matchesName = []
    HP_matchesOwner = []
    # Solution Matches
    S_matchesID = []
    S_matchesName = []
    S_matchesOwner = []
    # Story Maps
    SM_matchesID = []
    SM_matchesName = []
    SM_matchesOwner = []

    # Finding Matching Web Applications
    for w in WebApps:
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
                if w.type == 'Web Mapping Application':
                    WMA_matchesID.append(w.id)
                    WMA_matchesName.append(w.title)
                    WMA_matchesOwner.append(w.owner)
                if w.type == 'Hub Site Application':
                    HSA_matchesID.append(w.id)
                    HSA_matchesName.append(w.title)
                    HSA_matchesOwner.append(w.owner)
                if w.type == 'Dashboard':
                    DB_matchesID.append(w.id)
                    DB_matchesName.append(w.title)
                    DB_matchesOwner.append(w.owner)
                if w.type == 'Form':
                    Form_matchesID.append(w.id)
                    Form_matchesName.append(w.title)
                    Form_matchesOwner.append(w.owner)
                if w.type == 'Hub Page':
                    HP_matchesID.append(w.id)
                    HP_matchesName.append(w.title)
                    Form_matchesOwner.append(w.owner)
                if w.type == 'Solution':
                    S_matchesID.append(w.id)
                    S_matchesName.append(w.title)
                    S_matchesOwner.append(w.owner)
                if w.type == 'Story Map':
                    SM_matchesID.append(w.id)
                    SM_matchesName.append(w.title)
                    SM_matchesOwner.append(w.owner)

            # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

        if len(WMA_matchesID) > 0:
            WMAID_dict.update({i.id: set(WMA_matchesID)})
            WMAName_dict.update({i.id: set(WMA_matchesName)})
            WMAOwner_dict.update({i.id: set(WMA_matchesOwner)})

        if len(HSA_matchesID) > 0:
            HSAID_dict.update({i.id: set(HSA_matchesID)})
            HSAName_dict.update({i.id: set(HSA_matchesName)})
            HSAOwner_dict.update({i.id: set(HSA_matchesOwner)})

        if len(DB_matchesID) > 0:
            DBID_dict.update({i.id: set(DB_matchesID)})
            DBName_dict.update({i.id: set(DB_matchesName)})
            DBOwner_dict.update({i.id: set(DB_matchesOwner)})

        if len(Form_matchesID) > 0:
            FormID_dict.update({i.id: set(DB_matchesID)})
            FormName_dict.update({i.id: set(DB_matchesName)})
            FormOwner_dict.update({i.id: set(DB_matchesOwner)})

        if len(HP_matchesID) > 0:
            HPID_dict.update({i.id: set(HP_matchesID)})
            HPName_dict.update({i.id: set(HP_matchesName)})
            HPOwner_dict.update({i.id: set(HP_matchesOwner)})

        if len(S_matchesID) > 0:
            SID_dict.update({i.id: set(S_matchesID)})
            SName_dict.update({i.id: set(S_matchesName)})
            SOwner_dict.update({i.id: set(S_matchesOwner)})

        if len(SM_matchesID) > 0:
            SMID_dict.update({i.id: set(SM_matchesID)})
            SMName_dict.update({i.id: set(SM_matchesName)})
            SMOwner_dict.update({i.id: set(SM_matchesOwner)})

    print('Finished ' + str(i.title))

print('Found Relationships!')
# Using dictionaries to create Data Frames
print('Appending Data to DF then Exporting to Excel')

# Creating Item Dataframes
MasterDF['Item ID'] = ItemName_dict.keys()
MasterDF['Item Name'] = ItemName_dict.values()
MasterDF['Item Type'] = ItemType_dict.values()
MasterDF['Item Url'] = ItemURL_dict.values()
MasterDF['Item Owner'] = ItemOwner_dict.values()
# Creating Web Map Dataframes
MasterDF['Web Map ID'] = WMID_dict.values()
MasterDF['Web Map Name'] = WMName_dict.values()
MasterDF['Web Map Owner'] = WMOwner_dict.values()
# Creating Web Mapping Application Dataframes
MasterDF['Web Mapping App IDs'] = WMAID_dict.values()
MasterDF['Web Mapping App Names'] = WMAName_dict.values()
MasterDF['Web Mapping App Owner'] = WMAOwner_dict.values()
# Creating Hube Site Application Dataframes
MasterDF['Hub Site App IDs'] = HSAID_dict.values()
MasterDF['Hub Site App Names'] = HSAName_dict.values()
MasterDF['Hub Site App Owner'] = HSAOwner_dict.values()
# Creating Dashboard Dataframes
MasterDF['Dashboard IDs'] = DBID_dict.values()
MasterDF['Dashboard Names'] = DBName_dict.values()
MasterDF['Dashboard Owner'] = DBOwner_dict.values()
# Creating Form Dataframes
MasterDF['Form IDs'] = HSAID_dict.values()
MasterDF['Form Names'] = HSAName_dict.values()
MasterDF['Form Owner'] = HSAOwner_dict.values()
# Creating Hub Page Dataframes
MasterDF['Hub Page App IDs'] = HPID_dict.values()
MasterDF['Hub Page App Names'] = HPName_dict.values()
MasterDF['Hub Page App Owner'] = HPOwner_dict.values()
# Creating Solutions Dataframes
MasterDF['Solution IDs'] = SID_dict.values()
MasterDF['Solution Names'] = SName_dict.values()
MasterDF['Solution Owner'] = SOwner_dict.values()
# Creating Story Map Dataframes
MasterDF['Hub Story Map IDs'] = SMID_dict.values()
MasterDF['Hub Story Map Names'] = SMName_dict.values()
MasterDF['Hub Story Map Owner'] = SMOwner_dict.values()

# Exporting DF to Excel
MasterDF.to_excel(ExcelOutput, index=False)

print('Script Complete')
