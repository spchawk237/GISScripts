# Coding Document: SurveySampleGenerator.py

## Overview
The `SurveySampleGenerator.py` script is designed to work within ArcGIS Pro. It is a geoprocessing tool that generates a random sample from an Excel spreadsheet and exports the selected data to a location specified by the user. The script uses Python and several libraries, including ArcPy and pandas, to accomplish this task.

## Metadata
- **Author:** Andrew Parkin
- **Created on:** 2023-04-10
- **Works in:** ArcGIS Pro

## Description
The primary purpose of this script is to create a random sample from an Excel spreadsheet. The user is prompted to provide the following information through the ArcGIS Pro interface:
1. The Excel spreadsheet file that contains the data to sample.
2. The number of samples to select.
3. The output location for the random sample.

## Dependencies
This script relies on several Python libraries, which are imported at the beginning of the script:
- `arcpy`: The ArcPy library for geospatial data processing.
- `pandas`: A popular data manipulation library.
- `datetime`: To work with date and time information.
- `time`: To retrieve the current time.
- `numpy`: For generating a sequence of numbers.

## Code Breakdown

### Setting Up Date and Time
```python
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())
```
These lines retrieve the current date, day, and time, which are used later for logging and as part of the output file name.

### User Input
```python
FileName = arcpy.GetParameterAsText(0)
SampleNumber = arcpy.GetParameterAsText(1)
OutputFolder = arcpy.GetParameterAsText(2)
```
These variables store the user inputs received through ArcGIS Pro. They include the path to the Excel file (`FileName`), the number of samples to select (`SampleNumber`), and the output folder for the random sample (`OutputFolder`).

### Data Manipulation with Pandas
```python
df = pd.read_excel(FileName)
```
The script reads the Excel file specified by the user into a Pandas DataFrame (`df`). This DataFrame is used for further data manipulation.

```python
df1 = df.sample(int(SampleNumber))
```
A random sample of the specified size (`SampleNumber`) is selected from the original DataFrame (`df`) using the Pandas `sample` function. The resulting DataFrame is stored in `df1`.

### Sorting the Random Sample
```python
df1['ControlNumber'] = np.arange(1, len(df1) + 1)
```
This line adds a 'ControlNumber' column to the `df1` DataFrame, which assigns sequential numbers starting from 1 to the rows in the random sample. This is done to provide order to the selected data.

### Exporting Data to Excel
```python
with pd.ExcelWriter(OutputFolder + '\\RandomSample.xlsx') as writer:
    df.to_excel(writer, sheet_name="Original", index=False)
    df1.to_excel(writer, sheet_name="RandomSample", index=False)
```
The script uses Pandas to write both the original data and the random sample to an Excel file named 'RandomSample.xlsx' in the specified output folder. Two sheets are created within the Excel file: "Original" and "RandomSample," each containing their respective data.

## Usage
1. Open ArcGIS Pro.
2. Add Custom GPTool Folder to Pro Project
   - R:\GIS\CustomGPTools\
2. Run the Random_Sample_Generator geoprocessing tool and provide the required
input:
   - Excel spreadsheet file to sample.
   - Number of samples to select.
   - Output location for the random sample.
3. The script will generate a new Excel file (`RandomSample.xlsx`) containing both the original data and the randomly selected sample.

This script provides a practical and automated way to create random samples from Excel data, which can be valuable in various research and analysis scenarios.