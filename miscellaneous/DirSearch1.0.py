import os
import collections
import pandas as pd

# Using this format chose the directory of your choosing
dirName = r"Z:\\"

print('starting process..')

fileList = []
FilePath = []
fileSize = []
filetype = ['.txt', '.docx', '.pdf', '.shp', '.xlsx', '.csv', '.mdb', '.jpg', '.psd', '.tif', '.tiff', '.svg', '.pps',
            '.ppt', '.pptx', '.xls', '.xlsm', '.doc', '.rft']

print('Gathering raw data...')

for (dirpath, dirnames, filenames) in os.walk(dirName):
    for file in filenames:
        for type in filetype:
            if file.endswith(type):
                fileList.append(file)  # Finding File Name
                FilePath.append(os.path.join(dirpath, file))  # Finding File Path
                fileSize.append(os.stat(os.path.join(dirpath, file)).st_size)  # Finding File Size

# Create Dictionary joining file name to file size.

print('Getting File Size Dictonary..')
sizeDict = dict(zip(fileList, fileSize))
PathSizeDict = dict(zip(FilePath, fileSize))

# Finding Files with the same file name

print('Finding Files With duplicate Names...')
dupFiles = [item for item, count in collections.Counter(fileList).items() if count > 1]

# Finding Dup Count

print('Getting count of duplicates...')
DupCount = []

for dup in dupFiles:
    dupDict = {dup: fileList.count(dup)}
    DupCount.append(dupDict)

df = pd.DataFrame(DupCount)

df.T.to_excel(r'D:\\Projects\\dir\\dir_FileCount.xlsx', index=[0])

# Getting file size Need to shirk size Dict based on duplicate name.

print('Getting dup file size...')

DupSize = []

for dup in dupFiles:
    size = sizeDict.get(dup)
    DupSize.append(size)

df1 = pd.DataFrame(DupSize)

df1.to_excel(r'D:\\Projects\\dir\\dir_FileSize.xlsx', index=[0])

# FilePath based on dup name and file size.

print('Getting File Paths....')

FPDict = {}

for dup in dupFiles:
    FPDict.update({dup: []})


for (dirpath, dirnames, filenames) in os.walk(dirName):
    for file in filenames:
        for dup in dupFiles:
            if file == dup:
                FPDict[dup].append(os.path.join(dirpath, dup))


df2 = pd.DataFrame.from_dict(FPDict, orient='index')

df2.to_excel(r'D:\\Projects\\dir\\dir_FilePath.xlsx', index=[0])

print('Complete')

