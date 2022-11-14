# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# TaxMaps_MapSeriesExport.py
# Created on: 2021-12-08
# Updated on 2022-11-14
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
# Completed by: Andrew Parkin/GIS Manager
#
# Description: 
#  Export Tax Maps from ArcGIS Pro Map Series Layouts to individual PDFs
#  Then sort into correct folders
#
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import traceback
import logging
import shutil
from pathlib import Path
import re

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\skylab\\anybody\\GIS\\GIS_LOGS\\Assessment\\TaxMap_MapSeriesExport.log"
logging.basicConfig(filename=logfile, filemode='w', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

try:
    # Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    write_log("Unable to write log file", logfile)
    sys.exit()

#Variables
Tax_Map_Year = datetime.datetime.today().year
directory = "TaxMaps_" + str(Tax_Map_Year)
parent_dir = r"\\skylab\\anybody\\GIS\\County office projects\\Assessment\\TaxMapDocuments_ArcPro\\TaxMaps_PDFExport"
path = os.path.join(parent_dir, directory)
Tax_Map_Export_Project = r"\\skylab\\anybody\\GIS\\County office projects\\Assessment\\TaxMapDocuments_ArcPro\\TaxMapAutomation\\TaxMapAutomation.aprx"
Tax_Map_Export_Folder = path
aprx = arcpy.mp.ArcGISProject(Tax_Map_Export_Project)
layoutList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
              '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
intLayoutList = [int(i) for i in layoutList]

start_time = time.time()

print ("============================================================================")
print ("Exporting Tax Maps: " + str(Day) + " " + str(Time))
print ("Located at: R:\\GIS\\Assessment\\TaxMap_MapSeriesExport.log")
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Exporting Tax Maps: " + str(Day) + " " + str(Time), logfile)
write_log("Located at: R:\\GIS\\Assessment\\TaxMap_MapSeriesExport.log", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

aprx = arcpy.mp.ArcGISProject(Tax_Map_Export_Project)

# Check to see if Tax Map folder exists, delete if so, then create new folder
try:
    if arcpy.Exists(Tax_Map_Export_Folder):
        arcpy.Delete_management(Tax_Map_Export_Folder, "Workspace")
        print ("Tax Map folder found & deleted")
        write_log("Tax Map folder found & deleted", logfile)
    os.mkdir(path) 
except:
    print ("\n Unable to recreate Tax Map folder")
    write_log("\n Unable to recreate Tax Map folder", logfile)
    logging.exception('Got exception on recreate Tax Map folder logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

# Create subfolders within Tax Map folder

try:
    subfolder_names = ['Athens Twp', 'Beaver Twp', 'Bloomfield Twp', 'Blooming Valley Boro', 'Cambridge Twp',
                       'Cambridge Springs Boro', 'Centerville Boro', 'Cochranton Boro', 'Conneaut Twp',
                       'Conneautville Boro', 'Conneaut Lake Boro', 'Cussewago Twp', 'Fairfield Twp',
                       'East Fairfield Twp', 'East Fallowfield Twp', 'West Fallowfield Twp', 'Greenwood Twp', 'Hayfield Twp',
                       'Hydetown Boro', 'Linesville Boro', 'East Mead Twp', 'West Mead Twp', 'Oil Creek Twp',
                       'Pine Twp', 'Randolph Twp', 'Richmond Twp', 'Rockdale Twp', 'Rome Twp', 'Sadsbury Twp ',
                       'Saegertown Boro', 'North Shenango Twp', 'South Shenango Twp', 'West Shenango Twp', 'Sparta Twp',
                       'Spartansburg Boro', 'Spring Twp', 'Springboro Boro', 'Steuben Twp', 'Summerhill Twp',
                       'Summit Twp', 'Townville Boro', 'Troy Twp', 'Union Twp', 'Venango Twp', 'Venango Boro',
                       'Vernon Twp', 'Wayne Twp', 'Woodcock Twp', 'Woodcock Boro', 'Meadville City', 'Titusville City']

    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(Tax_Map_Export_Folder, subfolder_name))
    print ("Municipal subfolders created within Tax Map folder")
    write_log("Municipal subfolders created within Tax Map folder", logfile)
except:
    print ("\n Unable to create subfolders within Tax Map folder")
    write_log("\n Unable to create subfolders within Tax Map folder", logfile)
    logging.exception('Got exception on create subfolders within Tax Map folder logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

print ("\n Export Tax Maps Indexes to PDF")
write_log("\n Export Tax Maps Indexes to PDF", logfile)

try:
    p = arcpy.mp.ArcGISProject(Tax_Map_Export_Project)
    l = aprx.listLayouts()[0]
    if not l.mapSeries is None:
      ms = l.mapSeries
      indexLyr = ms.indexLayer

      if ms.enabled:
        for pageNum in range(1, ms.pageCount + 1):
          ms.currentPageNumber = pageNum
          print("Exporting {0}".format(ms.pageRow.Municipality))
          pageName = ms.pageRow.Municipality.title()
          ms.exportToPDF(Tax_Map_Export_Folder + "\\" + pageName + "\\" + pageName + ".pdf", "CURRENT")
except:
    print ("\n Unable to export Tax Maps Indexes to PDF")
    write_log("\n Unable to export Tax Maps Indexes to PDF", logfile)
    logging.exception('Got exception on export Tax Maps Indexes to PDF logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

print ("\n   Tax Maps Indexes exported to PDF successfully")
write_log("\n   Tax Maps Indexes exported to PDF successfully", logfile)

print ("\n Export Tax Maps Inserts & Sections to PDF")
write_log("\n Export Tax Maps Inserts & Sections to PDF", logfile)

subfolder_dict = {'Athens Twp': 11, 'Beaver Twp': 12, 'Bloomfield Twp': 13, 'Blooming Valley Boro': 14,
                  'Cambridge Twp': 15, 'Cambridge Springs Boro': 16, 'Centerville Boro': 17,
                  'Cochranton Boro': 18, 'Conneaut Twp': 19, 'Conneautville Boro': 20, 'Conneaut Lake Boro': 21,
                  'Cussewago Twp': 22, 'Fairfield Twp': 23, 'East Fairfield Twp': 24, 'East Fallowfield Twp': 25,
                  'West Fallowfield Twp': 26, 'Greenwood Twp': 27, 'Hayfield Twp': 28, 'Hydetown Boro': 29,
                  'Linesville Boro': 30, 'East Mead Twp': 31, 'West Mead Twp': 32, 'Oil Creek Twp': 38,
                  'Pine Twp': 39, 'Randolph Twp': 40, 'Richmond Twp': 41, 'Rockdale Twp': 42, 'Rome Twp': 43,
                  'Sadsbury Twp': 44, 'Saegertown Boro': 45, 'North Shenango Twp': 46, 'South Shenango Twp': 47,
                  'West Shenango Twp': 48, 'Sparta Twp': 49, 'Spartansburg Boro': 50, 'Spring Twp': 51,
                  'Springboro Boro': 52, 'Steuben Twp': 53, 'Summerhill Twp': 54, 'Summit Twp': 55,
                  'Townville Boro': 60, 'Troy Twp': 61, 'Union Twp': 62, 'Venango Twp': 63,
                  'Venango Boro': 64, 'Vernon Twp': 65, 'Wayne Twp': 66, 'Woodcock Twp': 67,
                  'Woodcock Boro': 68}

try:
    p = arcpy.mp.ArcGISProject(Tax_Map_Export_Project)

    for layout in intLayoutList:
        l = aprx.listLayouts()[layout]

        if not l.mapSeries is None:
            ms = l.mapSeries
            indexLyr = ms.indexLayer

        # Loops through all the layouts and puts files in correct folders. 14-16 City of Meadville, 27-30 City of Titusville.
        # For everything else it uses the dictionary above to place file in correct folder passed on the first 2 numbers of map name.

        if ms.enabled:
            for pageNum in range(1, ms.pageCount + 1):
                ms.currentPageNumber = pageNum
                print("Exporting {0}".format(ms.pageRow.MAP))
                pageName = ms.pageRow.MAP
                if layout in (14, 15, 16):
                    ms.exportToPDF(Tax_Map_Export_Folder + "\\" + 'Meadville City' + '\\' + pageName + ".pdf",
                                   "CURRENT")
                elif layout in (27, 28, 29, 30):
                    ms.exportToPDF(Tax_Map_Export_Folder + "\\" + 'Titusville City' + '\\' + pageName + ".pdf",
                                   "CURRENT")
                else:
                    for value in subfolder_dict.values():
                        if pageName.startswith(str(value)):
                            keylist = list(subfolder_dict.keys())
                            val_list = list(subfolder_dict.values())
                            position = val_list.index(value)
                            ms.exportToPDF(Tax_Map_Export_Folder + "\\" + keylist[position] + '\\' + pageName + ".pdf", "CURRENT")

except:
    print ("\n Unable to export Tax Maps Inserts & Sections to PDF")
    write_log("\n Unable to export Tax Maps Inserts & Sections to PDF", logfile)
    logging.exception('Got exception on export Tax Maps Inserts & Sections to PDF logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()
    
print ("\n   Tax Maps Inserts & Sections exported to PDF successfully")
write_log("\n   Tax Maps Inserts & Sections exported to PDF successfully", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n TAX MAPS ARE EXPORTED: " + str(Day) + " " + str(end_time))
write_log("\n TAX MAPS ARE EXPORTED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str(time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
