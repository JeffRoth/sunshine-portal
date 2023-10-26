# import libraries
import pandas as pd
from pandasql import sqldf
import unicodedata
import codecs
from datetime import datetime
import numpy as np
import os

# specify file locations
raw_dir = "data_downloads/"
formatted_dir = "formatted_monthly/"

# Prompt for name of new employee table
fname = input("Input file name for new employee table: ")
fdate = fname.split(".")[0][-8:]
form_date = datetime.strptime(fdate, "%Y%m%d").strftime("%m/%d/%Y")
input_file = os.path.join(raw_dir, fname)

# Create lambda function for easy queries
pysqldf = lambda q: sqldf(q, globals())

# read agencies csv
agencies = pd.read_csv('agencies.csv')
agencies.rename(columns={'Business Unit':'businessunit', 'BU Description':'budescription'}, inplace=True)

# read job_families csv
job_families = pd.read_csv('job_families.csv')
job_families.rename(columns={'Job Code':'jobcode', 'Position Descr':'positiondescr', 'Job Family':'jobfamily'}, inplace=True)

# read in employee csv
employee_table = pd.read_csv(input_file, encoding='latin_1')

# format column headers for SQL merge
employee_table.rename(columns={'Branch':'branch', 'Business Unit':'businessunit', 'BU Description':'budescription', 'Divsion':'division',
                               'Divsion Description':'divisiondescription', 'Position Nbr':'positionnumber', 'Position Descr':'positiondescription',
                               'Job Code':'jobcode', 'Name':'name', 'Classified/Exempt':'classified', 'Filled/Vacant':'filledvacant', 'Reg/Temp':'regtemp',
                               'Full/Part Time':'fullparttime', 'Position Start date':'positionstartdate', 'Hourly Rate':'hourlyrate',
                               'Annual Salary':'annualsalary', 'Fiscal YTD Paid':'fiscalytdpaid', 'Mid-Point Annual Salary': 'midsalary'}, inplace=True)

# Run SQL query
query = """
SELECT
	e.branch as "Branch",
	e.businessunit as "Business Unit",
	e.budescription as "BU Description",
	e.division as "Division",
	e.divisiondescription as "Division Description",
	e.positionnumber as "Position Nbr",
	CASE
		WHEN e.positiondescription IS NULL THEN 'none'
		ELSE e.positiondescription 
	END as "Position Descr",
    a.size as "Group",
	CASE
		WHEN jf.jobfamily IS NULL THEN 'non-IT'
		ELSE jf.jobfamily
	END as "Job Family",
	e.jobcode as "Job Code",
	e.name as "Name",
	e.classified as "Classified/Exempt",
	e.filledvacant as "Filled/Vacant",
	e.regtemp as "Reg/Temp",
	e.fullparttime as "Full/Part Time",
	e.positionstartdate as "Position Start date",
	e.hourlyrate as "Hourly Rate",
	e.annualsalary as "Annual Salary",
	e.fiscalytdpaid as "Fiscal YTD Paid",
	e.midsalary as "Mid-Point Annual Salary",
	CASE
		WHEN e.filledvacant = 'Vacant' THEN '0'
		ELSE e.midsalary
	END as "Mid-Point Annual Salary Filled"
FROM employee_table e
JOIN agencies a
  ON a.businessunit = e.businessunit AND a.branch = e.branch
FULL JOIN job_families jf
  ON jf.jobcode = e.jobcode
"""
employee_table_formatted = pysqldf(query)

# Add date column
employee_table_formatted['Date'] = form_date

# Remove false rows
employee_table_formatted['Branch'].replace('None', np.nan, inplace=True)
employee_table_formatted.dropna(subset=['Branch'], inplace=True)

# write to csv
output_file = os.path.join(formatted_dir, "emp" + str(fdate) + ".csv")
print(f"Outputting formatted table: {output_file}")
employee_table_formatted.to_csv(output_file, index=False)


# Concat to merged spreadsheet

q_merge = input("Do you wish to merge this month's report? (Y/N)")

if q_merge == "Y":
    
	# First check if merged file exists
	if os.path.isfile('merged.csv'): 
		merged_df = pd.read_csv('merged.csv', encoding='latin_1', low_memory=False)
		merged_df = merged_df.astype(dtype= {"Division":"object", "Position Start date":"object" })
		max_index = merged_df['Index'].max() + 1
		employee_table_formatted.insert(22, 'Index', range(max_index, max_index + len(employee_table_formatted)))
		new_merge = pd.concat([merged_df, employee_table_formatted], ignore_index=True)
		new_merge.to_csv('merged.csv', index=False)
	else:
		print("No merged file exists. Creating one for you now.")
		employee_table_formatted.insert(22, 'Index', range(0 + len(employee_table_formatted)))
		employee_table_formatted.to_csv('merged.csv', index=False)
