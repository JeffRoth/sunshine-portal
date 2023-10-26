# sunshine-portal

Python codes for analyzing data from the Sunshine Portal

merge_tables.py is a python script for merging processed monthly employee data tables.

process_employee_table.py is a python script for processing a single employee data table and optionally merging it with the existing merge.csv file.

purchases_nb.ipynb is a python jupyter notebook for searching purchase data

## Requirements:
* pandas
* pandasql
* numpy

## To Install
* Install Python on your machine.
* Install libraries by running `pip install -r requirements.txt`

## To Process a new employee spreadsheet
* Go to sunshine portal website and select "Employees" (https://ssp3.sunshineportalnm.com/#employees)
* Select "Data Download" button at the top of the screen.
* Select the month data file you wish to process.
* After downloading, move the .csv file to ./data_downloads/ folder
* open a windows terminal in the ./Sunshine_portal/ folder
* run `python process_employee_table.py` in the terminal window
* you will be prompted for the name of the .csv file.  Type in the name of the file (don't forget to add .csv)
* After processing, you will be asked whether you want to add the new month to the existing 'merge.csv' file (if there is one).

## To Merge processed employee spreadhseets
* In the event that the 'merge.csv' file becomes corrupted, goes missing, or you simply wish to merge a different range of dates, follow these steps
* open a windows terminal in the ./Sunshine_portal/ folder
* run `python merge_tables.py`
* you will be prompted for a start date for the merge. Please enter the date using the format: mm/yyyy
* you will be prompted for an end date for the merge.  Please enter the date using the format: mm/yyyy
* alternatively, you may press enter without entering a date, and the script will merge everything from your start date to the most recent file found.

## Excel Directions:
* after running one or both of the above scripts, open the 'State IT employees pivot.xlsx' file
* Select the 'Data' tab
* Select 'Refresh All' under 'Queries & Connections'.  You may need to select 'Refresh All' twice to get the pivot table to update.




