# import libraries
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
import bisect
import pandas as pd

# Get list of months available from directory
formatted_dir = "formatted_monthly/"
files = sorted([f for f in listdir(formatted_dir) if isfile(join(formatted_dir, f))])

# grab list of file dates
file_dates = []
for file in files:
    file_date = datetime.strptime(file.split(".")[0][-8:], "%Y%m%d")
    file_dates.append(file_date)

most_recent_date = max(file_dates)

# prompt user for start and end date
start_input = input("Please provide start date for merge (mm/yyyy): ")
start_date = datetime.strptime(start_input, "%m/%Y")
end_input = input("Please provide end date for merge (mm/yyyy) or press 'enter' to get most current: ")
if end_input == "":
    end_input = most_recent_date.strftime("%m/%Y")
end_date = datetime.strptime(end_input, "%m/%Y")

print("Start Date: ", start_date.strftime("%m/%Y"))
print("End Date: ", end_date.strftime("%m/%Y"))

# filter file dates for selected date range
lower = bisect.bisect_right(file_dates, start_date)
upper = bisect.bisect_left(file_dates, end_date)+1

# Merge files
merged_df = pd.DataFrame()
for file in files[lower:upper]:
    file_path = os.path.join(formatted_dir, file)
    file_df = pd.read_csv(file_path, encoding='latin_1', low_memory=False)
    merged_df = pd.concat([merged_df, file_df], ignore_index=True)
merged_df.insert(22, 'Index', range(0 + len(merged_df)))

# Write file to disk
merged_df.to_csv('merged.csv', index=False)
print("merge.csv file created.")