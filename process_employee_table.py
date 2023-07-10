# import libraries
import pandas as pd
from pandasql import sqldf
import unicodedata
import codecs

# Create lambda function for easy queries
pysqldf = lambda q: sqldf(q, globals())

# read agencies csv
agencies = pd.read_csv('agencies.csv')
agencies.rename(columns={'Business Unit':'businessunit', 'BU Description':'budescription'}, inplace=True)

# read job_families csv
job_families = pd.read_csv('job_families.csv')
job_families.rename(columns={'Job Code':'jobcode', 'Position Descr':'positiondescr', 'Job Family':'jobfamily'}, inplace=True)

# read in employee csv
employee_table = pd.read_csv('employees20230114.csv')

employee_table.rename(columns={'Branch':'branch', 'Business Unit':'businessunit', 'BU Description':'budescription', 'Divsion':'division',
                               'Divsion Description':'divisiondescription', 'Position Nbr':'positionnumber', 'Position Descr':'positiondescription',
                               'Job Code':'jobcode', 'Name':'name', 'Classified/Exempt':'classified', 'Filled/Vacant':'filledvacant', 'Reg/Temp':'regtemp',
                               'Full/Part Time':'fullparttime', 'Position Start date':'positionstartdate', 'Hourly Rate':'hourlyrate',
                               'Annual Salary':'annualsalary', 'Fiscal YTD Paid':'fiscalytdpaid', 'Mid-Point Annual Salary': 'midsalary'}, inplace=True)

# Create it_positions table
employess_20230114 = pd.read_csv('employees20230114.csv')
employess_20230114.rename(columns={'Job Code': 'jobcode', 'Position Descr': 'positiondescription', 'Classified/Exempt': 'classified'}, inplace=True)

query = """
SELECT
	jobcode,
	positiondescription,
	classified
FROM employess_20230114
WHERE (
	UPPER(positiondescription) LIKE UPPER('% IT %')
	or UPPER(positiondescription) LIKE UPPER('IT%')
	or UPPER(positiondescription) LIKE UPPER('Chief Information Officer')
	or UPPER(positiondescription) LIKE UPPER('DATA ANALYST%')
	or UPPER(positiondescription) LIKE UPPER('Information%')
	or UPPER(positiondescription) LIKE UPPER('Network%')
	or UPPER(positiondescription) LIKE UPPER('Chief Technology Officer')
	or UPPER(positiondescription) LIKE UPPER('%Software%')
	or UPPER(positiondescription) LIKE UPPER('%Systems%')
	or UPPER(positiondescription) LIKE UPPER('%Odyssey%')
	or UPPER(positiondescription) LIKE UPPER('%DATA SCIENTIST%')
	or UPPER(positiondescription) LIKE UPPER('Database Admin%')
	or UPPER(positiondescription) LIKE UPPER('AOC Chief Tech%')
	or UPPER(positiondescription) LIKE UPPER('Broadband%')
	or UPPER(positiondescription) LIKE UPPER('Computer%')
)
GROUP BY jobcode, positiondescription, classified
ORDER BY jobcode;
"""
it_positions = pysqldf(query)

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
	END as "Mid-Point Annual Salary Filled",
	'Jan 2023' as "Date"
FROM employee_table e
JOIN agencies a
  ON a.businessunit = e.businessunit AND a.branch = e.branch
FULL JOIN job_families jf
  ON jf.jobcode = e.jobcode
"""
employee_table_formatted = pysqldf(query)

# write to csv
employee_table_formatted.to_csv('emp20230114.csv', index=False)