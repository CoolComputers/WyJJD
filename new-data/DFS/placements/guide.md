# Filter Guide for DFS Placement files
Report Title: Placement Type (of those in care)  
Report Description: The number/percent of children on the caseload on the last day of each report period, by the level of care they were in on that day  
Report Time Period: January 1, 2012 - May 31, 2018 (Monthly)  
Level: Statewide  
Reporting Time Period: January 1,2012 - May 31, 2018(Monthly)  

MNELSO3   -Type=Probation/judicial district=Judicial District 1  
MNELSO3-1 -Type=Probation/judicial district=Judicial District 2  
MNELSO3-2 -Type=Probation/judicial district=Judicial District 3  
MNELSO3-3 -Type=Probation/judicial district=Judicial District 4  
MNELSO3-4 -Type=Probation/judicial district=Judicial District 5  
MNELSO3-5 -Type=Probation/judicial district=Judicial District 6  
MNELSO3-6 -Type=Probation/judicial district=Judicial District 7  
MNELSO3-7 -Type=Probation/judicial district=Judicial District 8  
MNELSO3-8 -Type=Probation/judicial district=Judicial District 9  

## Cleaning Process
Report PDF -> Adobe Acrobat -> Export PDF to Excel .xlsx -> Excel export .xlsx as .csv(text) -> cleaner.ipynb -> combined.csv

## Legend
|Data Field|Field Description|
|-|-|						
|Total Children in Care			|			Total children on caseload anytime on the last day of the Report Period
|Total Family-like setting	|					(of Total) Children placed in a family-like setting
|Relative foster home				|		Relative foster home (sub category of Substitute Care)
|Non-relative foster home		|				Non-relative foster home (sub category of Substitute Care)
|Pre-adoptive home					|	Pre-adoptive home (sub category of Substitute Care)
|Trial Home Visit						|Trial Home Visit (sub category of Family Like setting)
|Supervised Independent Living|						Supervised Independent Living (sub category of Family Like setting)
|Long Term FC Non Relative	|					Long Term FC Non Relative (sub category of Family Like setting)
|Long Term FC Relative			|			Long Term FC Relative (sub category of Family Like setting)
|Specialized FC Non Relative|						Specialized FC Non Relative (sub category of Family Like setting)
|Specialized FC Relative		|				Specialized FC Relative (sub category of Family Like setting)
|Therapuetic FC Non Relative|						Therapuetic FC Non Relative (sub category of Family Like setting)
|Therapuetic FC Relative|						Therapuetic FC Relative (sub category of Family Like setting)
|Total Group Care	|					(of Total) Children placed in group care setting
|Group Home				|		Group home or residential placement setting (sub-category of Total Group Care)
|Residental Treatment	|					Children in an Residental Treatment setting (sub-category of Total Group Care)
|Psychiatric RTC	|					Children in a Psychiatric RTC setting (sub-category of Total Group Care)
|Boys School	|					Children in a Boys School setting (sub-category of Total Group Care)
|Girls School	|					Children in a Girls School setting (sub-category of Total Group Care)
|Detention		|				Children in a Detention setting (sub-category of Total Group Care)
|Crisis Center|						Children in a Crisis Center setting (sub-category of Total Group Care)
|Hosptial						|Children in a Hospital setting (sub-category of Total Group Care)
|State Hosptial			|			Children in a State Hospital setting (sub-category of Total Group Care)
|Jail						|Children in a Jail setting (sub-category of Total Group Care)
|Runaway				|		(of Total) Child in runaway status on last day of the Report Period
|Interim				|		(of Total) Child in runaway status on last day of the Report Period
|Unknown				|		(of Total) Children whose placement setting is unknown
|Date data are based|						The point in time date on which the level of care data are reported
