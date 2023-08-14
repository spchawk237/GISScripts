import arcpy
import os

arcpy.env.workspace = 'Y:\\GIS\\03_Data\\ErieCountyBaseMap.gdb'
arcpy.env.overwriteOutput = True
logfile = r"Y:\\GIS\\03_Data\\Python_Logs\\DataTransfer.log"
timestr = time.strftime('%Y%m%d')

if os.path.exists(logfile):
    os.remove(logfile)
else:
    print('File doesnt exist')
try:
    # Write Logfile (define logfile write process, each step will append to the log, if program is started over)
    def write_log(text, file):
        f = open(file, 'a')
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    write_log("Unable to write log file", logfile)

# Transfer.gdb  fcs list

write_log('Process Started... ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)

# Getting File Paths

write_log('Getting File Paths...', logfile)
write_log('Getting Transfer Filepath...', logfile)

transFPList = []


def TransferFP_List():
    arcpy.env.workspace = 'Y:\\GIS\\03_Data\\TransferDatabase.gdb'

    # Filters through TransferDatabase to see what needs to be added to the basemap and creates a list file paths.
    for dataset in arcpy.ListDatasets():
        for fc in arcpy.ListFeatureClasses('*', 'ALL', dataset):
            transFPList.append('\\' + dataset + '\\' + fc)
    for fc in arcpy.ListFeatureClasses():
        transFPList.append('\\' + dataset + '\\' + fc)
    write_log(transFPList, logfile)


TransferFP_List()

write_log('Finished Transfer Filepath!', logfile)

# Basemap.gdb fcs list

write_log('Creating Basemap File Path...', logfile)

baseFPlist = []


def ECBMFP_List():
    arcpy.env.workspace = 'Y:\\GIS\\03_Data\\ErieCountyBaseMap.gdb'

    # Creates a list of file paths for all feature classes in basemap.
    for dataset in arcpy.ListDatasets():
        for fc in arcpy.ListFeatureClasses('*', 'ALL', dataset):
            baseFPlist.append('\\' + dataset + '\\' + fc)
    for fc in arcpy.ListFeatureClasses():
        baseFPlist.append('\\' + dataset + '\\' + fc)
    write_log(baseFPlist, logfile)


ECBMFP_List()

write_log('Finished Basemap File Path!', logfile)

# Look for Duplicates between transfcList and basefclist

write_log('Finding Duplicates between databases...', logfile)

# Searches for any feature classes that are in both the basemap and transfer databases.
fpboth = set(transFPList).intersection(baseFPlist)

write_log(fpboth, logfile)
write_log('Finding Duplicates between databases Complete!', logfile)

# Archiving features from fpboth

write_log('Archiving Old fcs..', logfile)

try:
    for fp in fpboth:
        write_log('Archiving..' + ' ' + fp, logfile)
        arcpy.CopyFeatures_management(fp, 'W:\\Basemap Backup\\ErieCountyBaseMap.gdb' + fp + '_' + timestr)
        write_log('Archive Completed' + ' ' + fp, logfile)
except:
    try:
        write_log(arcpy.GetMessages(), logfile)
    except:
        write_log('Unable to log Error Message', logfile)

write_log('Archiving old fcs Finished', logfile)

# Check to make sure everything got transferred ok before deleting.

write_log('Gathering Archive File Paths...', logfile)

# Creating List of Archive Drive.

AC_list = []


def archiveCheck():
    arcpy.env.workspace = 'W:\\Basemap Backup\\ErieCountyBaseMap.gdb'

    for dataset in arcpy.ListDatasets():
        for fc in arcpy.ListFeatureClasses('*', 'ALL', dataset):
            AC_list.append('\\' + dataset + '\\' + fc)
    for fc in arcpy.ListFeatureClasses():
        AC_list.append('\\' + dataset + '\\' + fc)
    write_log(AC_list, logfile)


archiveCheck()

write_log('Finished gathering Archive File Paths!', logfile)

# Comparing fpboth to AC_list

write_log('Comparing fpboth to AC_list...', logfile)

BMAC_Check = []


def BMAC():
    arcpy.env.workspace = 'Y:\\GIS\\03_Data\\ErieCountyBaseMap.gdb'

    for dataset in arcpy.ListDatasets():
        for fc in arcpy.ListFeatureClasses('*', 'ALL', dataset):
            BMAC_Check.append('\\' + dataset + '\\' + fc + '_' + timestr)
    for fc in arcpy.ListFeatureClasses():
        baseFPlist.append('\\' + dataset + '\\' + fc + '_' + timestr)
    write_log(BMAC_Check, logfile)


BMAC()

AC_Check = set(BMAC_Check).intersection(AC_list)
write_log(AC_Check, logfile)

write_log('Completed Comparison!', logfile)
write_log('Deleting Archived fcs from basemap..', logfile)

BM_Del = [x[:-9] for x in AC_Check]

try:
    for fp in BM_Del:
        write_log("Currently Deleting" + ' ' + fp, logfile)
        arcpy.Delete_management(fp)
        write_log('Deleted' + ' ' + fp, logfile)
except:
    try:
        write_log(arcpy.GetMessages(), logfile)
    except:
        write_log('Unable to log Error Message', logfile)


write_log('Deleted Archived fcs from basemap', logfile)

# Adding fcs from Transfer Database to basemap

write_log('Transfer FCs from transfer to Basemap..', logfile)

try:
    for fp in transFPList:
        write_log('Transferring' + ' ' + fp + ' ' + 'to base map', logfile)
        arcpy.CopyFeatures_management('Y:\\GIS\\03_Data\\TransferDatabase.gdb' + fp, fp)
        write_log('Transferred' + ' ' + fp + ' ' + 'to base map', logfile)
except:
    try:
        write_log(arcpy.GetMessages(), logfile)
    except:
        write_log('Unable to log Error Message', logfile)


write_log('Transfer FCs from transfer to Basemap Completed!', logfile)

# Delete fcs from Transfer Database

write_log('Delete FCs from Transfer.gdb..', logfile)


def transdel():
    arcpy.env.workspace = 'Y:\\GIS\\03_Data\\TransferDatabase.gdb'

    try:
        for fc in transFPList:
            write_log('Deleting' + ' ' + fc, logfile)
            arcpy.Delete_management(fc)
            write_log('Deleted' + ' ' + fc, logfile)
    except:
        try:
            write_log(arcpy.GetMessages(), logfile)
        except:
            write_log('Unable to log Error Message', logfile)


transdel()

write_log('FCs Deleted from Transfer.gdb!', logfile)
write_log('Process Completed! ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
