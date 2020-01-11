# Data Sources
All data can be found within the new-data/ folder of the project repository. Feel free to download and use this data for your own use cases but please carry through to your project the data source citations and references described below.

1. Demographic Information by Age Group. File: 'ojjdp/population-data/population_agegroup_ethnicity.csv'. Source: [Office of Juvenile Justice and Delinquency Prevention](https://www.ojjdp.gov/ojstatbb/ezapop/asp/source.asp)  
2. Wyoming Education Discipline Data. File: 'school-discipline/SchoolDiscipline_2007-17_Combined-CSV2.csv'. Source: [Wyoming Dept. of Education](https://edu.wyoming.gov/)    
3. Juvenile Arrest Data by Agency ORI. File: 'juvenile-arrests/ori_juvenile_arrest_2010-2017_CLEAN.csv'. Source: [Wyoming Division of Criminal Investigation](wyomingdci.wyo.gov)  
4. Juvenile Placement Rates by Judicial District. File: 'DFS/placements/combined1.csv'. Source: [Wyoming Dept. of Family Services](http://dfsweb.wyo.gov/)  
5. Juvenile Court Case Counts. File: 'case-counts/combined.csv'. Source: [Office of Juvenile Justice and Delinquency Prevention](https://www.ojjdp.gov/ojstatbb/ezaco/asp/method.asp)  


## Data Preparation
- Demographic Information by Age Group. File: 'ojjdp/population-data/population_agegroup_ethnicity.csv'.
  - Population data is pulled from the OJJDP website using Selenium web automation
  - leaned into a single file using [this notebook](ojjdp/population-data/method2-cleaning/Cleaning.ipynb).
- Wyoming Education Discipline Data. File: 'school-discipline/SchoolDiscipline_2007-17_Combined-CSV2.csv'.
  - file provided as is
- Juvenile Arrest Data by Agency ORI. File: 'juvenile-arrests/ori_juvenile_arrest_2010-2017_CLEAN.csv'.
  - See [this notebook](juvenile-arrests/Add_ORI_Year.ipynb) for the steps taken to clean report data into the usable datasheet.
- Juvenile Placement Rates by Judicial District. File: 'DFS/placements/combined1.csv'.
  - See the [legend guide](DFS/placements/guide.md) for a description of the cleaning process as well as report datafield explanations.
- Juvenile Court Case Counts. File: 'case-counts/combined.csv'.
  - Original reports stored in [case-counts/original-reports/](case-counts/original-reports/) with file naming format report-<2-digit year>.csv
  - [This notebook](case-counts/cleaner.ipynb) is then used to combine all the separate yearly reports into one combined csv file.
