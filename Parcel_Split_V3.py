import arcpy
import os

arcpy.env.workspace = 'Y:\\GIS\\03_Data\\TaxParcel_Levels_Test.gdb'
arcpy.env.overwriteOutput = True

logfile = r"Y:\\GIS\\03_Data\\Parcel_Lvl_Log\\Parcel_Split.log"

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
    print("\n Unable to write log file")
    write_log("Unable to write log file", logfile)

write_log('Process Started:', logfile)

# Delete Existing taxparcel049, lvl1, lvl2, lvl3, PASDA

parcelList = ['taxparcel049', 'taxparcel049_lvl1', 'taxparcel049_lvl2', 'taxparcel049_lvl3', 'taxparcel049_PASDA']

write_log('Starting Delete Existing', logfile)

for parcels in parcelList:
    try:
        if arcpy.Exists(parcels):
            arcpy.Delete_management(parcels)
        else:
            print("Tax Parcel doesn't exist")
            write_log("Unable to delete existing tax parcel layer!", logfile)
    except:
        print("\n Unable to delete existing tax parcel lvl3 layer!")
        write_log("Unable to delete existing tax parcel lvl3 layer!", logfile)

write_log('Deleting Existing Parcels Finished!', logfile)

# Copy taxparcel049 from nightly update to Planning Shared update folder

write_log('Copying Tax Parcels to Planning Shared...', logfile)

for parcels in parcelList:
    try:
        arcpy.CopyFeatures_management('R:\\reassessment_gis_stack\\shapes_current\\taxparcel049.shp', parcels)
    except:
        print("\n Unable to copy taxparcel049 layer!")
        write_log("Unable to copy taxparcel049 layer!", logfile)

write_log('Copied Tax Parcels to Planning Shared!!', logfile)

# Delete unwanted fields

write_log('Deleting unnecessary fields...', logfile)

Delete_Lvl1 = ['DeededAc', 'GrossAc', 'Map', 'Block', 'Parcel', 'StreetNo', 'StrNoSuff', 'StreetDir', 'StreetName',
               'StrSuffix', 'StrSuff2', 'NbhdDesc', 'Class', 'LUC', 'LUCDesc', 'Str1Desc', 'Str2Desc', 'Topo1Desc',
               'Topo2Desc', 'Topo3Desc', 'Util1Desc', 'Util2Desc', 'Util3Desc', 'ZoningDesc', 'Owner1', 'Owner2',
               'OwnAddr1', 'OwnAddr2', 'OwnAddr3', 'OwnCity', 'OwnState', 'OwnZip1', 'OwnZip2', 'Book', 'Page',
               'LandValue', 'BldgVal', 'TotalValue', 'TaxLand', 'TaxBldg', 'TaxTotVal', 'SchoolDist', 'MuniDist',
               'CGStatus', 'CGAmount', 'HomeStat', 'FarmStat', 'LertaAmt', 'LertaEndYr', 'NbhdId', 'Photo']

Delete_Lvl2 = ['DeededAc', 'GrossAc', 'Map', 'Block', 'Parcel', 'StreetNo', 'StrNoSuff', 'StreetDir', 'StreetName',
               'StrSuffix', 'StrSuff2', 'NbhdDesc', 'Acres', 'Str1Desc', 'Str2Desc', 'Topo1Desc', 'Topo2Desc',
               'Topo3Desc', 'Util1Desc', 'Util2Desc', 'Util3Desc', 'ZoningDesc', 'OwnZip2', 'Book', 'Page', 'LandValue',
               'BldgVal', 'TotalValue', 'TaxLand', 'TaxBldg', 'TaxTotVal', 'SchoolDist', 'MuniDist', 'CGStatus',
               'CGAmount', 'HomeStat', 'FarmStat', 'LertaAmt', 'LertaEndYr', 'NbhdId', 'Photo']

Delete_Lvl3 = ['Map', 'Block', 'Parcel', 'StreetNo', 'StrNoSuff', 'StreetDir', 'StreetName', 'StrSuffix', 'StrSuff2',
               'NbhdDesc', 'Acres', 'Str1Desc', 'Str2Desc', 'Topo1Desc', 'Topo2Desc', 'Topo3Desc', 'Util1Desc',
               'Util2Desc', 'Util3Desc', 'ZoningDesc', 'OwnZip2', 'LandValue', 'BuildingValue', 'TotalValue',
               'SchoolDist', 'MuniDist', 'Photo']

Delete_PASDA = ['Muni', 'District', 'Acres', 'LegalDesc1', 'LegalDesc2', 'LegalDesc3', 'FullStreet', 'SqFt', 'Web',
                'DeededAc', 'GrossAc', 'Map', 'Block', 'Parcel', 'StreetNo', 'StrNoSuff', 'StreetDir', 'StreetName',
                'StrSuffix', 'StrSuff2', 'NbhdDesc', 'Class', 'LUC', 'LUCDesc', 'Str1Desc', 'Str2Desc', 'Topo1Desc',
                'Topo2Desc', 'Topo3Desc', 'Util1Desc', 'Util2Desc', 'Util3Desc', 'ZoningDesc', 'Owner1', 'Owner2',
                'OwnAddr1', 'OwnAddr2', 'OwnAddr3', 'OwnCity', 'OwnState', 'OwnZip1', 'OwnZip2', 'Book', 'Page',
                'LandValue', 'BldgVal', 'TotalValue', 'TaxLand', 'TaxBldg', 'TaxTotVal', 'SchoolDist', 'MuniDist',
                'CGStatus', 'CGAmount', 'HomeStat', 'FarmStat', 'LertaAmt', 'LertaEndYr', 'NbhdId', 'Photo']

arcpy.DeleteField_management('taxparcel049_lvl1', Delete_Lvl1)

arcpy.DeleteField_management('taxparcel049_lvl2', Delete_Lvl2)

arcpy.DeleteField_management('taxparcel049_lvl3', Delete_Lvl3)

arcpy.DeleteField_management('taxparcel049_PASDA', Delete_PASDA)

write_log('Fields Deleted!', logfile)
write_log('Process Complete!', logfile)
