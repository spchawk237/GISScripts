# ---------------------------------------------------------------------------
# SDE_Compress_Tools.py
#
# Description:
# This tool will first check for all database versions that contain "CCSDE.sde" in the name (excluding external database views), 
# retrieve a list of connected users, disconnect all users, then block new incoming connections to the database versions.
#
# It will then get a list of all public versions, then reconcile, post, then delete them.
#
# It will then, compress the SDE database, once that has completed. 
#
# It will then allow new database connections again.  Check R:\GIS\GIS_LOGS\GIS\Version_Log.log for the list of public versions that
# need rebuilt.
#
# It will finally check for a list of all datasets with each database connection, and rebuild the indexes and re-analyze them.
#
# Update: 
# After updating to SDE 11.2 it started failing at the reindexing so I took this oppertunity to fully reconfigure script with updated methods
# as I figured while I'm fixing a good chunk of code I can try and make it run more efficently.
#
# Orginally Authored: Phil Baranyai/Crawford County GIS Manager & 
# Reconfigured Author: Andrew Parkin/Crawford County GIS Manager
# Created on: 2019-05-16 
# Reconfigured on: 2024-02-06
# Updated on 2024-02-06
# Works in ArcGIS Pro
# ---------------------------------------------------------------------------

# Imports
import sys
import arcpy
import datetime
import os
import traceback
import logging
import time

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = r"\\skylab\\anybody\\GIS\\GIS_LOGS\\GIS\\SDE_Compress.log"
logging.basicConfig(filename=logfile, filemode='w', level=logging.DEBUG)

# Setup Version logging (configure version logging location, type, and filemode -- overwrite every run)
Version_logfile = r"\\skylab\\anybody\\GIS\\GIS_LOGS\\GIS\\Version_Log.log"
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
    print("\n Unable to write log file")
    sys.exit()

# Function to handle print and log statements
def print_log(message, log):
    print(message)
    write_log(message, log)


# Get list of database connections
def sdeConnections():
    appdata = os.getenv('APPDATA')
    arcgisVersion = arcpy.GetInstallInfo()['Version']
    arcCatalogPath = "E:\\ArcGIS_Pro\\Projects\\ArcServer"
    sdeConnections = []
    for file in os.listdir(arcCatalogPath):
        fileIsSdeConnection = file.lower().endswith("ccsde.sde")
        if fileIsSdeConnection:
            sdeConnections.append(os.path.join(arcCatalogPath, file))
          #  sdeConnections.append(os.path.join("{}\n".format(arcCatalogPath, file)))
    return sdeConnections

DB_LIST = sdeConnections()

start_time = time.time()

print_log("============================================================================", logfile)
print_log("Checking for Database Connections: " + str(Day) + " " + str(Time), logfile)
print_log("Works in ArcGIS Pro", logfile)
print_log("============================================================================", logfile)

DB_LIST.sort(reverse=False)
for DBConnection in DB_LIST:
    print(DBConnection)
    write_log(DBConnection, logfile)

# Set the connections folder 
DB_Connections = r"\\ccorbweaver\\Database_Connections"  

# Set the workspaces
arcpy.env.workspace = DB_Connections + '\\SDE@ccsde.sde'
workspace = arcpy.env.workspace
defaultVersion = "sde.DEFAULT"

# Set database connection variables
AGOL_EDIT_CONNECTION = DB_Connections + "\\agol_edit@ccsde.sde"
AGOL_EDIT_PUB_CONNECTION = DB_Connections + "\\agol_edit_pub@ccsde.sde"
AST_CONNECTION = DB_Connections + "\\AST@ccsde.sde"
AUTOWKSP_CONNECTION = DB_Connections + "\\auto_workspace@ccsde.sde"
CONSV_DIST_CONNECTION = DB_Connections + "\\CONSV_DIST@ccsde.sde"
CRAW_INTERNAL_CONNECTION = DB_Connections + "\\craw_internal@ccsde.sde"
GIS_CONNECTION = DB_Connections + "\\GIS@ccsde.sde"
PLAN_CONNECTION = DB_Connections + "\\PLANNING@ccsde.sde"
PUB_OD_CONNECTION = DB_Connections + "\\public_od@ccsde.sde"
PS_CONNECTION = DB_Connections + "\\PUBLIC_SAFETY@ccsde.sde"
PUBLIC_WEB_CONNECTION = DB_Connections + "\\public_web@ccsde.sde"
SDE_CONNECTION = DB_Connections + "\\SDE@ccsde.sde"
HS_CONNECTION = DB_Connections + "\\HUMAN_SERVICES@ccsde.sde"

# Database Index List
DB_index_list = [AGOL_EDIT_CONNECTION, AGOL_EDIT_PUB_CONNECTION, AST_CONNECTION, AUTOWKSP_CONNECTION, CONSV_DIST_CONNECTION, CRAW_INTERNAL_CONNECTION, GIS_CONNECTION, PLAN_CONNECTION,
                PUB_OD_CONNECTION, PS_CONNECTION, PUBLIC_WEB_CONNECTION, HS_CONNECTION]


print_log("\n============================================================================", logfile)
print_log("Checking for Connected users:", logfile)
print_log("============================================================================", logfile)

# Get a list of connected users.
try:
    userList = arcpy.ListUsers(SDE_CONNECTION)
    print("\n")
    userList.sort(reverse=False)
    for USERS in userList:
        print_log(USERS, logfile)
except:
    print_log("\n Unable to get list of connected users", logfile)
    logging.exception('Got exception on get list of connected users logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

print_log("\n============================================================================", logfile)
print_log("Preparing to compress SDE database", logfile)
print_log("Will compress the following:", logfile)

DB_LIST.sort(reverse=False)
for DBConnection in DB_LIST:
    print_log(DBConnection, logfile)
print_log("============================================================================", logfile)

print_log("\n Blocking new connections to database, then disconnecting all users", logfile)

try:
    # Block new connections to the database.
    arcpy.AcceptConnections(SDE_CONNECTION, False)
except:
    print_log("Unable to block new connections to the database", logfile)
    logging.exception('Got exception on block new connections to the database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

try:
    # Disconnect all users from the database.
    arcpy.DisconnectUser(SDE_CONNECTION, "ALL")
except:
    print_log("Unable to disconnect all users from the database", logfile)
    logging.exception('Got exception on disconnect all users from the database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDE_CONNECTION, True)
    raise
    sys.exit()

print_log("       Blocking new connections to database, then disconnecting all users completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print_log("\n Reconcile and Post all public database versions, then deletion of versions", logfile)

try:
    # Get a list of versions to pass into the ReconcileVersions tool.
    versionList = arcpy.ListVersions(SDE_CONNECTION)
    print("List of versions that will be reconciled and posted before compress: ")
    versionList.sort(reverse=False)
    for USERS in versionList:
        print_log(USERS, logfile)
except:
    print_log("Unable to obtain a list of versions from database", logfile)
    logging.exception('Got exception on obtain a list of versions from database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDE_CONNECTION, True)
    raise
    sys.exit()

try:
    # Execute the ReconcileVersions tool.
    arcpy.management.ReconcileVersions(SDE_CONNECTION, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", Version_logfile)
    print_log("\n  Log of reconcile and post written to "+ Version_logfile, logfile)
except:
    print_log("Unable to reconcile and post versions from database, then delete them", logfile)
    logging.exception('Got exception on reconcile and post versions from database, then delete them logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDE_CONNECTION, True)
    raise
    sys.exit()

print_log("       Reconcile and Post all public database versions, then deletion of versions completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print_log("\n Compression of SDE database", logfile)

try:
    # Run the compress tool.
    arcpy.management.Compress(SDE_CONNECTION)
except:
    print_log("Unable to compress SDE database", logfile)
    logging.exception('Got exception on compress SDE database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDE_CONNECTION, True)
    raise
    sys.exit()


print_log("       Compression of SDE database completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print_log("\n Allow incoming connections to database again", logfile)

try:
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDE_CONNECTION, True)
except:
    print_log("Unable to allow incoming connections to database again", logfile)
    logging.exception('Got exception on allow incoming connections to database again logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

print_log("       Allow incoming connections to database again completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print_log("\n Rebuild indexes and analyze datasets on AGOL_EDIT_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user

def rebuildindex(Database):
    try:
        print_log(f'Starting {Database}..', logfile)
        # set workspace
        workspace = Database
        
        # set the workspace environment
        arcpy.env.workspace = workspace
        # Get the user name for the workspace
        userName = arcpy.Describe(workspace).connectionProperties.user
        print(userName)

        # NOTE: Rebuild indexes can accept a Python list of datasets.

        # Get a list of all the datasets the user has access to.
        # First, get all the stand alone tables, feature classes and rasters.

        dataList= arcpy.ListTables(userName.upper() + '*') + arcpy.ListFeatureClasses(userName.upper() + '*')

        for dataset in arcpy.ListDatasets("", "Feature"):
            arcpy.env.workspace = os.path.join(workspace,dataset)
            dataList += arcpy.ListFeatureClasses(userName.upper() + '*') + arcpy.ListDatasets(userName.upper() + '*')

        print_log(dataList, logfile)
        print(len(dataList))
    
        # Pass in the list of datasets owned by the connected user to the rebuild indexes 
        # and update statistics on the data tables
        arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
        print_log("\n Rebuild index on AGOL_EDIT_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
        arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")

    except:
        print_log(f"Unable to rebuild indexes and analyze datasets on all datasets on {Database}", logfile)
        logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON {Database} logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
        raise
        sys.exit()

print_log("       Rebuild indexes and analyze datasets on all datasets on SDE CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

# Try and iterate through Database list to rebuild indexes

try:
    for db in DB_index_list:
        rebuildindex(db)

except:
    print_log(f"Unable to rebuild indexes and analyze datasets on all datasets", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON {Database} logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))

print("\n Rebuild versions that existed prior to SDE compress")
write_log("\n Rebuild versions that existed prior to SDE compress", logfile)

# Database Versions that are not currently used are commented out - as they were causing issues during the rebuild.  If they are used in the future, uncomment them out, also be sure to start the cursor with an "if", not an "elif"
try:
    for version in versionList:
##        if version.startswith("agol_edit"):
##            arcpy.management.CreateVersion(AGOL_EDIT_CONNECTION,defaultVersion, version[10:], "PUBLIC")
##            print ("Created version {0}".format(version))
##            write_log("Created version {0}".format(version),logfile)
##        elif version.startswith("agol_edit_pub"):
##            arcpy.management.CreateVersion(AGOL_EDIT_PUB_CONNECTION,defaultVersion, version[14:], "PUBLIC")
##            print ("Created version {0}".format(version))
##            write_log("Created version {0}".format(version),logfile)
##        elif version.startswith("CONSV_DIST"):
##            arcpy.management.CreateVersion(CONSV_DIST_CONNECTION,defaultVersion, version[11:], "PUBLIC")
##            print ("Created version {0}".format(version))
##            write_log("Created version {0}".format(version),logfile)
        if version.startswith("GIS"):
            arcpy.management.CreateVersion(GIS_CONNECTION, defaultVersion, version[4:], "PUBLIC")
            print("Created version {0}".format(version))
            write_log("Created version {0}".format(version), logfile)
        elif version.startswith("PUBLIC_SAFETY"):
            arcpy.management.CreateVersion(PS_CONNECTION, defaultVersion, version[14:], "PUBLIC")
            print("Created version {0}".format(version))
            write_log("Created version {0}".format(version), logfile)
        elif version.startswith("AST"):
            arcpy.management.CreateVersion(AST_CONNECTION, defaultVersion, version[4:], "PUBLIC")
            print("Created version {0}".format(version))
            write_log("Created version {0}".format(version), logfile)
        elif version.startswith("PLANNING"):
            arcpy.management.CreateVersion(PLAN_CONNECTION, defaultVersion, version[9:], "PUBLIC")
            print("Created version {0}".format(version))
            write_log("Created version {0}".format(version), logfile)
        elif version.startswith("HUMAN_SERVICES"):
            arcpy.management.CreateVersion(HS_CONNECTION, defaultVersion, version[15:], "PUBLIC")
            print("Created version {0}".format(version))
            write_log("Created version {0}".format(version), logfile)
        else:
            pass
        del version
except:
    print("\n Unable to rebuild versions")
    write_log("Unable to rebuild versions", logfile)
    logging.exception('Got exception on rebuild versions logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

print("       Rebuild versions completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild versions completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print_log("===========================================================", logfile)
print_log("\n ALL SDE COMPRESS PROCESSES HAVE COMPLETED: " + str(Day) + " " + str(end_time), logfile)
print_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print_log("===========================================================", logfile)
print_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
