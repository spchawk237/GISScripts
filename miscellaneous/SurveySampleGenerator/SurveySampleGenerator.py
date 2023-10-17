# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# SurveySampleGenerator.py
# Created on: 2023-04-10
# Works in ArcPro
#
# Author: Andrew Parkin
#
# Description:
#  Random sample generator tool in ArcGIS Pro
# Takes an Excel spreadsheet and selects a random selected number selected by the user. Then exports sample to a
# destination of the users choice.
#
# Used as a Geoprocessing Tool in ArcGIS Pro
# ---------------------------------------------------------------------------

# Importing required modules
import arcpy
import pandas as pd
import datetime
import time
import numpy as np

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

# File name of spreadsheet for random sample. Requires user input in the tool
FileName = arcpy.GetParameterAsText(0)

# Number of Samples needed. Requires user input in the tool
SampleNumber = arcpy.GetParameterAsText(1)

# Output Location Requires user input in the tool
OutputFolder = arcpy.GetParameterAsText(2)

# Creating Dataframes and getting random sample

# Creates a dataframe that python can read and manipulate.
df = pd.read_excel(FileName)

# Using Sample function on existing dataframe
df1 = df.sample(int(SampleNumber))

# Sorts random sample by Control Number Column
df1['ControlNumber'] = np.arange(1, len(df1) + 1)

# Create a Pandas Excel writer using XlsxWriter as the engine.
with pd.ExcelWriter(OutputFolder + '\\RandomSample.xlsx') as writer:
    df.to_excel(writer, sheet_name="Original", index=False)
    df1.to_excel(writer, sheet_name="RandomSample", index=False)
