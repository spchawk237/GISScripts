# Coding Document: TaxMaps_MapSeriesExport.py

## Overview
The script is designed to export Tax Maps from ArcGIS Pro Map Series Layouts to individual PDFs, followed by sorting the PDFs into their respective folders. The script sets up error logging, deletes existing tax map folders if found, and then creates new folders. It also creates subfolders within the tax map folder for various municipalities. The script exports tax map indexes, inserts, and sections to PDF format based on the provided parameters. Additionally, it logs the start and completion time, along with the elapsed time for the script execution.

## Metadata
- **Author:** Phil Baranyai
- **Completed by:** Andrew Parkin
- **Created on:** 2021-12-08
- **Finished on:** 2022-11-14
- **Works in:** ArcGIS Pro

## Description
The primary purpose of this script is to create a random sample from an Excel spreadsheet. The user is prompted to provide the following information through the ArcGIS Pro interface:
1. The Excel spreadsheet file that contains the data to sample.
2. The number of samples to select.
3. The output location for the random sample.

## Dependencies
This script relies on several Python libraries, which are imported at the beginning of the script:
- `arcpy`: The ArcPy library for geospatial data processing.
- `datetime`: To work with date and time information.
- `time`: To retrieve the current time.
- `os`: Operating System dependent functionality.
- `sys`: System-specific parameters and functions.
- `logging`: Logging facility for Python.

## Code Breakdown

### Disabling Geoprocessing Log History
```python
arcpy.SetLogHistory(False)
```
This line disables the geoprocessing log history in metadata, preventing the program from filling up the geoprocessing history in metadata with every run.

### Setting up Error Logging
```python
logfile = r"\\skylab\\anybody\\GIS\\GIS_LOGS\\Assessment\\TaxMap_MapSeriesExport.log"
logging.basicConfig(filename=logfile, filemode='w', level=logging.DEBUG)
```
This code segment sets up the error logging mechanism. It specifies the file path for the log file where log messages will be stored. The `filemode='w'` parameter ensures that the log file is overwritten every time the script runs. The `level=logging.DEBUG` parameter sets the logging level to `DEBUG`, enabling detailed logging.

### Setting up Date and Time
```python
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())
```
These lines set up the current date and time. The `date` variable stores the current date in the "YYYYMMDD" format. The `Day` variable stores the current date in the "MM-DD-YYYY" format, and the `Time` variable stores the current time in the "HH:MM:SS AM/PM" format.

### Defining the Write Log Function
```python
try:
    def write_log(text, file):
        f = open(file, 'a')
        f.write("{}\n".format(text))
        return
except:
    print("\n Unable to write log file")
    write_log("Unable to write log file", logfile)
    sys.exit()
```
This segment defines the `write_log` function for writing log messages to the log file. The function opens the specified log file in append mode ('a'), writes the provided text along with a new line character, and then returns. The `try-except` block is used to catch any exceptions that may occur during the file writing process. If an exception occurs, it prints an error message, writes the error message to the log file, and exits the script.

This section sets up the necessary logging infrastructure for the script, ensuring that errors and important information are logged to the specified file for monitoring and debugging purposes.

### Variable and Directory Setup
```python
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
```

This part of the script initializes various variables and directories. 
- `Tax_Map_Year` stores the current year. 
- `directory` is the name of the directory for the tax maps, which includes the current year. 
- `parent_dir` is the path to the parent directory for the tax map exports. 
- `path` is the complete path for the directory where the tax maps will be exported. 
- `Tax_Map_Export_Project` is the path to the project file containing the tax maps. 
- `Tax_Map_Export_Folder` is the final path for exporting the tax maps. 
- `aprx` represents the ArcGIS project file. 
- `layoutList` is a list of layout numbers. 
- `intLayoutList` is a list of layout numbers converted to integers.

### Logging Start of the Process
```python
start_time = time.time()

print("============================================================================")
print("Exporting Tax Maps: " + str(Day) + " " + str(Time))
print("Located at: R:\\GIS\\Assessment\\TaxMap_MapSeriesExport.log")
print("Works in ArcGIS Pro")
print("============================================================================")
write_log("============================================================================", logfile)
write_log("Exporting Tax Maps: " + str(Day) + " " + str(Time), logfile)
write_log("Located at: R:\\GIS\\Assessment\\TaxMap_MapSeriesExport.log", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)
```

This part of the script logs the start of the process. It prints and writes a series of messages indicating the start of the tax map export process. The `start_time` variable stores the current time for performance tracking.

### Handling Directory Creation
```python
try:
    if arcpy.Exists(Tax_Map_Export_Folder):
        arcpy.Delete_management(Tax_Map_Export_Folder, "Workspace")
        print("Tax Map folder found & deleted")
        write_log("Tax Map folder found & deleted", logfile)
    os.mkdir(path) 
except:
    print("\n Unable to recreate Tax Map folder")
    write_log("\n Unable to recreate Tax Map folder", logfile)
    logging.exception('Got exception on recreate Tax Map folder logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()
```

This segment tries to handle the creation of the tax map folder. It checks if the folder already exists using `arcpy.Exists` and then deletes it using `arcpy.Delete_management`. If it doesn't exist, it attempts to create the folder using `os.mkdir`. If any exception occurs, it prints an error message, writes it to the log, logs the exception with the date and time, raises the exception, and exits the script.

This part of the script deals with the setup and initialization of necessary variables and directories, as well as logging the start of the tax map export process. Additionally, it handles the creation and deletion of the tax map folder, ensuring proper folder management during the script execution.

### Creating Subfolders for Municipalities
```python
try:
    subfolder_names = ['Athens Twp', 'Beaver Twp', 'Bloomfield Twp', 'Blooming Valley Boro',Cambridge Twp', 'Cambridge Springs Boro', 'Centerville Boro', 'Cochranton Boro', 'Conneaut Twp', 'Conneautville Boro', 'Conneaut Lake Boro', 'Cussewago Twp', 'Fairfield Twp', 'East Fairfield Twp', 'East Fallowfield Twp', 'West Fallowfield Twp', 'Greenwood Twp', 'Hayfield Twp', 'Hydetown Boro', 'Linesville Boro', 'East Mead Twp', 'West Mead Twp', 'Oil Creek Twp', 'Pine Twp', 'Randolph Twp', 'Richmond Twp', 'Rockdale Twp', 'Rome Twp', 'Sadsbury Twp ', 'Saegertown Boro', 'North Shenango Twp', 'South Shenango Twp', 'West Shenango Twp', 'Sparta Twp', 'Spartansburg Boro', 'Spring Twp', 'Springboro Boro', 'Steuben Twp', 'Summerhill Twp', 'Summit Twp', 'Townville Boro', 'Troy Twp', 'Union Twp', 'Venango Twp', 'Venango Boro', 'Vernon Twp', 'Wayne Twp', 'Woodcock Twp', 'Woodcock Boro', 'Meadville City', 'Titusville City']

    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(Tax_Map_Export_Folder, subfolder_name))
    print("Municipal subfolders created within Tax Map folder")
    write_log("Municipal subfolders created within Tax Map folder", logfile)
except:
    print("\n Unable to create subfolders within Tax Map folder")
    write_log("\n Unable to create subfolders within Tax Map folder", logfile)
    logging.exception('Got exception on create subfolders within Tax Map folder logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()
```

This section attempts to create subfolders within the Tax Map folder for each municipality. It uses a list named `subfolder_names` containing the names of the municipalities. The script then iterates through each name in the list and creates a corresponding subfolder using the `os.makedirs` function.

If any exception occurs during the subfolder creation process, it prints an error message, writes it to the log, logs the exception with the date and time, raises the exception, and exits the script.

This section ensures that subfolders for each municipality are created within the Tax Map folder, facilitating the organized export of tax maps based on their respective municipalities.

### Exporting Tax Map Indexes to PDF
```python
print("\n Export Tax Maps Indexes to PDF")
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
    print("\n Unable to export Tax Maps Indexes to PDF")
    write_log("\n Unable to export Tax Maps Indexes to PDF", logfile)
    logging.exception('Got exception on export Tax Maps Indexes to PDF logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()
```

This section of the code is responsible for exporting tax map indexes to PDF. It first prints and logs a message indicating the start of the export process. It then attempts to open the ArcGIS project, access the layout, and check if a map series exists. If the map series is enabled, it iterates through each page and exports the corresponding tax map index to a PDF file, naming the file after the municipality.

If any exception occurs during the export process, it prints an error message, writes it to the log, logs the exception with the date and time, raises the exception, and exits the script.

This section handles the export of tax map indexes to PDF files, ensuring that each municipality's tax map index is exported to the appropriate directory.

## Usage
1. Manually run at the request of Assessment. 
   - Usually around Feburary after closeouts.
   - But can be run at any point during the year if need arises.
