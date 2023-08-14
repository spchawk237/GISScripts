# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Prebuilt_Map_Export.py
# Created on: 2021-12-08
# Updated on 2022-11-14
# Works in ArcGIS Pro
#
# Author: Andrew Parkin/GIS Manager
#
# Description:
#  Export Prebuilt Maps from ArcGIS Pro Map Series Layouts to individual PDFs
#
#
# ---------------------------------------------------------------------------

import sys
import arcpy
import datetime
import os
import logging
import time

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\skylab\\anybody\\GIS\\GIS_LOGS\\GIS\\Prebuilt_Map_Export.log"
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

# Variables
map_path_letter = 'R:\\GIS\\Data - Map sales\\Pre-designed GIS maps - PDF\\Letter\\'
map_path_Tabloid = 'R:\\GIS\\Data - Map sales\\Pre-designed GIS maps - PDF\\Tabloid\\'
map_path_ArchD = 'R:\\GIS\\Data - Map sales\\Pre-designed GIS maps - PDF\\Arch D\\'
map_path_ArchE = 'R:\\GIS\\Data - Map sales\\Pre-designed GIS maps - PDF\\Arch E\\'
Pro_project = r'C:\Users\aparkin\Documents\ArcGIS\Projects\CountyWideMaps_ForSale_Local.aprx'
aprx = arcpy.mp.ArcGISProject(Pro_project)
layouts = [0, 1, 2, 3, 6, 7, 8, 9, 10]
# Next two just used for reference only
# mapseries_layouts = [9, 10]
# other_layouts = [0, 1, 2, 6, 7, 8]


start_time = time.time()

print("============================================================================")
print("Exporting Predesigned Maps: " + str(Day) + " " + str(Time))
print("Located at: R:\\GIS\\GIS_LOGS\\GIS\\Prebuilt_Map_Export.log")
print("Works in ArcGIS Pro")
print("============================================================================")
write_log("============================================================================", logfile)
write_log("Exporting Predesigned Maps: " + str(Day) + " " + str(Time), logfile)
write_log("Located at: R:\\GIS\\GIS_LOGS\\GIS\\Prebuilt_Map_Export.log", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

# Getting Layout Name and appending it to empty Variable layoutNames

#for lyt in aprx.listLayouts():
    #print(f"  {lyt.name} ({lyt.pageHeight} x {lyt.pageWidth} {lyt.pageUnits})")

try:
    p = arcpy.mp.ArcGISProject(Pro_project)

    for lyt in layouts:
        l = aprx.listLayouts()[lyt]
        lname = f"{l.name}"

        #Arch E (6,7,9) Arch D (1,2, 10)
        if lyt in (1, 2, 10):
            print(f'Starting {lname}...')
            l.exportToPDF(os.path.join(map_path_ArchD, f"{lname}.pdf"))
            print(f'Finished {lname}!')

        elif lyt in (6, 7, 9):
            print(f'Starting {lname}...')
            l.exportToPDF(os.path.join(map_path_ArchE, f"{lname}.pdf"))
            print(f'Finished {lname}!')

        elif lyt in (0, 8):
            print(f'Starting {lname}...')
            if not l.mapSeries is None:
                ms = l.mapSeries
                indexLyr = ms.indexLayer

            # Loops through all the layouts and puts files in correct folders. 14-16 City of Meadville, 27-30 City of Titusville.
            # For everything else it uses the dictionary above to place file in correct folder passed on the first 2 numbers of map name.

            if ms.enabled:
                for pageNum in range(1, ms.pageCount + 1):
                    ms.currentPageNumber = pageNum
                    print("Exporting {0}".format(ms.pageRow.MUNI_NAME))
                    pageName = ms.pageRow.MUNI_NAME
                    if lyt in (0):
                        ms.exportToPDF(os.path.join(map_path_ArchD, f"{pageName}.pdf"), 'CURRENT')
                    else:
                        ms.exportToPDF(os.path.join(map_path_ArchE, f"{pageName}.pdf"), 'CURRENT')


            print(f'Finished {lname}!')

        else:
            print(lname + " didn't get exported")

except:
    print("\n Unable to export Predeisgned Maps to PDF")
    write_log("\n Unable to export Predeisgned Maps to PDF", logfile)
    logging.exception(
        'Got exception on export Tax Maps Inserts & Sections to PDF logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print("==============================================================")
print("\n PREDESIGNED Maps ARE EXPORTED: " + str(Day) + " " + str(end_time))
write_log("\n PREDESIGNED MAPS ARE EXPORTED: " + str(Day) + " " + str(end_time), logfile)

print("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time)) + " // Program completed: " + str(
    Day) + " " + str(end_time))
write_log("Elapsed time: " + str(
    time.strftime(" %H:%M:%S", time.gmtime(elapsed_time)) + " // Program completed: " + str(Day) + " " + str(end_time)),
          logfile)
print("==============================================================")

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
