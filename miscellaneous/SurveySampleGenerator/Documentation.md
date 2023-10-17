```markdown
# SurveySampleGenerator
## Synopsis
Random sample generator tool in ArcGIS Pro.

## Author
Andrew Parkin

## Description
A tool designed for generating a random sample from an Excel spreadsheet in ArcGIS Pro.

### Usage
To use this tool, the user must provide inputs for the following parameters:

1. FileName : str
   - The file name of the Excel spreadsheet containing the data.

2. SampleNumber : int
   - The number of samples to be selected from the data.

3. OutputFolder : str
   - The location where the resulting sample will be exported.

The tool then performs the following steps:

1. Reads the input Excel spreadsheet into a pandas DataFrame.
2. Selects a random sample of the specified size from the DataFrame.
3. Adds a 'ControlNumber' column to the selected sample for sorting purposes.
4. Writes both the original data and the randomly selected sample to an Excel file.

### Date and Time Setup
The script initializes the current date and time to keep track of the processing time.

### Imported Modules
The script imports the following modules:

- `arcpy`: A module providing a Python interface for the ArcGIS Pro application.
- `pandas`: A powerful data analysis and manipulation library.
- `datetime`: A module for manipulating dates and times in Python.
- `time`: A module providing various time-related functions.
- `numpy`: A fundamental package for scientific computing with Python.

**Note**: This script is specifically designed to work in the ArcGIS Pro environment and is intended to be used as a geoprocessing tool.

### File Structure
The structure of the script is as follows:

1. Initial setup of the script including date and time.
2. User input for file name, sample number, and output folder.
3. Creation of pandas DataFrames and selection of a random sample.
4. Sorting the random sample by the 'ControlNumber' column.
5. Writing the original data and the random sample to an Excel file.

### Usage
If on county network.
1. Open ArcGIS Pro.
2. Add Custom GPTool Folder to Pro Project
   - R:\GIS\CustomGPTools\
2. Run the Random_Sample_Generator geoprocessing tool and provide the required
input:
   - Excel spreadsheet file to sample.
   - Number of samples to select.
   - Output location for the random sample.
3. The script will generate a new Excel file (`RandomSample.xlsx`) containing both the original data and the randomly selected sample.

If not you'll either have to create your own GP tool or run in pro and add input when asked.

### Limitations
This script is specifically designed for use within ArcGIS Pro and may not be compatible with other environments without modifications.
```
