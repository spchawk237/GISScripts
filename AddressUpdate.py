# Address Monthly update 02-11-2022
import arcpy
import os
import time

# Creating Logfile and setting workspace

logfile = r"Y:\GIS\03_Data\Python_Logs\AddressTransfer.log"
timestr = time.strftime('%Y%m%d %H:%M:%S')

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

arcpy.env.workspace = r'Y:\GIS\03_Data\TransferDatabase.gdb\PublicSafety'
arcpy.env.overwriteOutput = True

logfile = r"Y:\GIS\03_Data\Python_Logs\AddressTransfer.log"
timestr = time.strftime('%Y%m%d %H:%M:%S')

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

# Pull Address from Public Safety monthly update to Transfer GDB

write_log('Process Started... ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Process Started... ' + time.strftime('%Y%m%d %H:%M:%S'))

write_log('Copying Addresses to Transfer.gdb: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Copying Addresses to Transfer.gdb: ' + time.strftime('%Y%m%d %H:%M:%S'))

arcpy.CopyFeatures_management(r'R:\03 Public Safety\Sites\20220207\Sites.shp', 'Addresses_Raw')

write_log('Copied Addresses to Transfer.gdb: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Copied Addresses to Transfer.gdb: ' + time.strftime('%Y%m%d %H:%M:%S'))

# Adding Muni Field

table = r'Y:\GIS\03_Data\ErieCountyBaseMap.gdb\MCAddressTable'
Address = r'Y:\GIS\03_Data\TransferDatabase.gdb\PublicSafety\Addresses_Raw'
AddressOutput = r'Y:\GIS\03_Data\TransferDatabase.gdb\PublicSafety\Addresses'
AddressJoinField = 'MCODE'
TableJoinField = 'mcode'

write_log('Adding Muni Field: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Adding Muni Field')

arcpy.AddField_management(Address, 'Muni', "TEXT", field_length=255)

write_log('Add Muni Field Complete: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Add Muni Field Complete')

write_log('Starting Join: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Starting Join')

addressjoin = arcpy.AddJoin_management(Address, AddressJoinField, table, TableJoinField)

write_log('Join Complete: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Join Complete')

# field Calc Muni field

write_log('Starting Field Calc: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Starting Field Calc')

arcpy.CalculateField_management(addressjoin, 'Addresses_Raw.Muni', '!MCAddressTable.MCN!', 'PYTHON3')

write_log('Field Calc Complete: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Field Calc Complete')

# Remove Join

write_log('Removing Join: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Removing Join')

arcpy.RemoveJoin_management(addressjoin, 'MCAddressTable')

write_log('Join Removed: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Join Removed')

write_log('Starting copy to permanent fc: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Starting copy to permanent fc')

arcpy.CopyFeatures_management(Address, AddressOutput)

write_log('Copied to permanent fc: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Copied to permanent fc')

# Delete Addresses_Raw

write_log('Deleting Addresses_Raw: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Deleting Addresses_Raw')

arcpy.Delete_management(Address)

write_log('Deleted Addresses_Raw: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Deleted Addresses_Raw')

# Export Table to update Address Vlookup Table

write_log('Starting Vlookup Table Export: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Starting Vlookup Table Export')

ExcelOutput = r"Y:\GIS\03_Data\Python_Logs\AddressVlookup.xlsx"

arcpy.conversion.TableToExcel(AddressOutput, ExcelOutput)

write_log('Vlookup Table Exported: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Vlookup Table Exported')


# Delete Unwanted fields in Excel sheet

write_log('Exporting VLookup Table: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Exporting VLookup Table...')

ColumnDelete = ['OBJECTID_12', 'OBJECTID_1', 'OBJECTID', 'NEWSTREX', 'NEWCITST', 'NEWZIP', 'Address', 'RDNAME', 'MCODE',
                'ESN', 'COM', 'TYPE', 'SiteID', 'GPSFLG', 'HSNUM', 'ALISTR', 'PICTNUM', 'PICTYPE', 'AT_ID', 'LR',
                'GFAddress', 'PrimaryNa', 'Street', 'UpdateSour', 'UpdateDate', 'GPSUPDT', 'StreetID', 'JBoundID',
                'ALIName', 'PD', 'PT', 'SN', 'ST', 'SD', 'Alias1', 'Alias2', 'Alias3', 'ADDRESSTEM', 'DiscrpAgID',
                'COUNTRY', 'STATE', 'COUNTY', 'ADD_NUMBER', 'DateUpdate',    'St_PosTyp', 'Unit', 'MSAGComm', 'JOIN_ID',
                'Post_Comm', 'Lat', 'Long', 'Post_Code', 'Effective', 'Expire', 'Site_NGUID', 'AddCode', 'AddDataURI',
                'Inc_Muni', 'Nbrhd_Comm', 'AddNum_Pre', 'AddNum_Suf', 'St_PreMod', 'St_PreDir', 'St_PreTyp',
                'St_PreSep', 'St_Name', 'St_PosDir', 'St_PosMod', 'LSt_PreDir', 'LSt_Name', 'LSt_Type', 'LStPosDir',
                'ESN25', 'Post_Code4', 'Building', 'Floor', 'Room', 'Seat', 'Addtl_Loc', 'LandmkName', 'Mile_Post',
                'Place_Type', 'Placement', 'Elev', 'FullName', 'HouseNumbe']

df = pd.read_excel(ExcelOutput)

for col in ColumnDelete:
    try:
        df.drop(col, axis=1, inplace=True)
    except:
        print('Couldnt Delete!')

df.to_excel(r'Y:\GIS\03_Data\Python_Logs\AddressVlookup.xlsx')

write_log('VLookup Table Exported: ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('VLookup Table Exported')

write_log('Process Completed! ' + time.strftime('%Y%m%d %H:%M:%S'), logfile)
print('Process Completed! ' + time.strftime('%Y%m%d %H:%M:%S'))

