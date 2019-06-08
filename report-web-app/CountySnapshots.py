
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n} ')


# In[2]:


#File:CountySnapshots.ipynb
#Author: Rafer Cooley
#Desc:Generate County Snapshots of Juvenile Data
from ipywidgets import widgets
from ipywidgets import interactive
from IPython.display import display, HTML, clear_output
#from pivottablejs import pivot_ui
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import os, sys
import subprocess
import base64 #for createdownloadlink
#import data_functions as dfunct
get_ipython().run_line_magic('run', 'getdata.ipynb')
#%run crimestats.ipynb


# In[3]:


my_styles = """
<style>
@media screen{
.container { width:90% !important; }
.page-break {page-break-after:always;}
}
@media print{
.container { width:100% !important; }
.page-break {page-break-after:always;}
}
</style>
"""
display(HTML(my_styles))


# In[4]:


dfunct = DataFunctions()
overview = dfunct.getOverview()#not used
dfs = dfunct.getDFS()#afcars, county, plc

agegroup_demographic_data = dfunct.getDemographic_By_AgeGroup()
population_data = dfunct.getPopulationData()#phasing out?
#arrest_totals = dfunct.getStateTotalArrests(juvenile_arrests,population_data)

school = dfunct.getSchool()
school_county_rates = dfunct.getSchool_county_rates(school,agegroup_demographic_data)
school_state_rates = dfunct.getSchool_state_rates(school,agegroup_demographic_data)

juvenile_arrests = dfunct.getORIData(agegroup_demographic_data)
arrest_totals = dfunct.getStateTotalArrests(juvenile_arrests,agegroup_demographic_data)

judicial_district_population_data = dfunct.getJudicialDistrictJuvenilePopulations(agegroup_demographic_data)
placement_data = dfunct.getJudicialPlacementData()
placement_rates_data,state_placement_rates_data = dfunct.getJudicialPlacementRates(placement_data,judicial_district_population_data)

demographic_data = dfunct.getDemographicData()
court_case_counts = dfunct.getCourtCaseNumbersData()

data_sources_for_citation = [

]

#qualifiers for ORI data
violent_felony = ['Manslaughter','Rape','Robbery','Aggravated-Assault']
lesser_offenses = ['Burglary','Larceny-Theft','Motor-Vehicle-Theft','Arson',
    'Other-Assaults','Forgery-Counterfeiting','Fraud','Embezzlement','Stolen-Property','Vandalism','Weapons',
    'Prostitution','Sex-Offenses','Drug-Abuse-Violations','Drug-Abuse-Violations-Possession','Gambling-Offenses',
    'Offenses-Against-Family-Children','Driving-Under-the-Influence','Liquor-Laws','Drunkenness',
    'Disorderly-Conduct','All-Other-Offenses-Except-Traffic','Suspicion','Curfew-Loitering-Law-Violations',
    'Run-a-ways','Vagrancy']

#qualifiers for placements data
placement_county_districts = []
placement_county_districts.append(['Laramie'])
placement_county_districts.append(['Albany','Carbon'])
placement_county_districts.append(['Uinta','Sweetwater','Lincoln'])
placement_county_districts.append(['Johnson','Sheridan'])
placement_county_districts.append(['Big Horn','Park','Hot Springs','Washakie'])
placement_county_districts.append(['Campbell','Weston','Crook'])
placement_county_districts.append(['Natrona'])
placement_county_districts.append(['Converse','Niobrara','Goshen','Platte'])
placement_county_districts.append(['Teton','Fremont','Sublette'])


# In[5]:


def display_header():
    display(HTML('<h1>Juvenile Justice County Snapshots</h1>'))
    display(HTML('Use the county dropdown to select which county to observe, and then adjust the year slider range to view different time frames of data.<hr>'))


# In[6]:


#Show html table functions
idx = pd.IndexSlice

def display_afcars_html(county,year_tup):
    sources = []
    try:
        display(HTML('<h3>Afcars Data</h3>'))
        display(HTML(dfs[0].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()))
    except Exception as e:
        print('Error showing DFS afcars data.'+str(e))

def display_county_html(county,year_tup):
    try:
        display(HTML('<h3>DFS By County</h3>'))
        display(HTML(dfs[1].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()))
    except Exception as e:
        print('Error showing DFS county data.'+str(e))

#Table Columns
#Manslaughter,Rape,Robbery,Aggravated-Assault,Burglary,Larceny-Theft,Motor-Vehicle-Theft,Arson
#Other-Assaults,Forgery-Counterfeiting,Fraud,Embezzlement,Stolen-Property,Vandalism,Weapons
#Prostitution,Sex-Offenses,Drug-Abuse-Violations,Drug-Abuse-Violations-Possession,Gambling-Offenses
#Offenses-Against-Family-Children,Driving-Under-the-Influence,Liquor-Laws,Drunkenness
#Disorderly-Conduct,All-Other-Offenses-Except-Traffic,Suspicion,Curfew-Loitering-Law-Violations
#Run-a-ways,Vagrancy
def display_felony_html(county,year_tup):
    try:
        tmp_felony = juvenile_arrests.loc[idx[county,year_tup[0]:year_tup[1]], :][violent_felony]
        tmp_felony['Totals'] = tmp_felony.sum(axis=1)
        display(HTML('<center><h3>Violent Felony</h3></center>'))
        display(HTML(tmp_felony.transpose().to_html()))
    except Exception as e:
        print('Error showing ORI data.'+str(e))

def display_lesser_html(county,year_tup):
    try:
        tmp_lesser = juvenile_arrests.loc[idx[county,year_tup[0]:year_tup[1]], :][lesser_offenses]
        tmp_lesser['Totals'] = tmp_lesser.sum(axis=1)
        display(HTML('<center><h3>Lesser Offenses</h3></center>'))
        display(HTML(tmp_lesser.transpose().to_html()))
    except Exception as e:
        print('Error showing ORI data.'+str(e))

def display_school_html(county,year_tup):
    try:
        display(HTML(school.loc[idx[county,year_tup[0]:year_tup[1],year_tup[0]:year_tup[1]], :].transpose().to_html()))
    except Exception as e:
        print('Error showing School data.'+str(e))

def display_school_rate_html(county,year_tup):
    try:
        display(HTML(school_county_rates[['Total','Population 11-17','Rate']].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()))
    except Exception as e:
        print('Error showing School data.'+str(e))

def display_overview_html(county,year_tup):#NOT USED?
    try:
        display(HTML(overview.loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()))
    except Exception as e:
        print('Error showing Overview data.'+str(e))

##PLACEMENTS
def display_placements_html(county,year_tup):
    #'period,Total Children in Care,Psychiatric RTC,Relative foster home,Supervised Independent Living,
    #Long Term FC Non Relative,Long Term FC Relative,Interim,Boys School,State Hospital,Girls School,
    #Hospital,Total Family-like setting,Therapeutic FC Non Relative,Specialized FC Relative,Jail,
    #Pre-adoptive home,Crisis Center,Detention,district,Therapeutic FC Relative,Trial Home Visit,
    #Runaway,Total Group Care,Non-relative foster home,Residential Treatment,Group Home,Specialized FC Non Relative,Unknown
    #     Supervised Independent Living <<---????
    #GROUP CATEGORIES(NON RELATIVE)
#     Psychiatric RTC
#     Long Term FC Non Relative
#     Interim,Boys School,State Hospital,Girls School
#     Hospital
#     Therapeutic FC Non Relative,Jail
#     Pre-adoptive home,Crisis Center,Detention,Trial Home Visit
#     Runaway,Total Group Care,Non-relative foster home,Residential Treatment
#     Group Home,Specialized FC Non Relative,Unknown
    #RELATIVE CATEGORIES
    #Long Term FC Relative,Total Family-like setting,Specialized FC Relative,Therapeutic FC Relative
    placement_fields_to_show=['Psychiatric RTC',
    'Long Term FC Non Relative',
    'Interim','Boys School','State Hospital','Girls School',
    'Hospital',
    'Therapeutic FC Non Relative','Jail',
    'Pre-adoptive home','Crisis Center','Detention','Trial Home Visit',
    'Runaway','Non-relative foster home','Residential Treatment',
    'Group Home','Specialized FC Non Relative','Total Group Care','Total Family-like setting','Unknown','Total Children in Care']
    try:
        district_num = 0
        for county_arr_idx in range(len(placement_county_districts)):#search through county list to match county name with judicial district number
            if county in placement_county_districts[county_arr_idx]:
                district_num = county_arr_idx
                #print('found county[{}:{}] in arr:{}'.format(county,district_num,str(placement_county_districts[district_num])))

        display(HTML(placement_data[placement_fields_to_show].loc[idx[year_tup[0]:year_tup[1],district_num+1], :].transpose().to_html()))
    except Exception as e:
        print('Error showing Placements data.'+str(e))

def display_county_placements_rates_html(county,year_tup):
    try:
        district_num = 0
        for county_arr_idx in range(1,len(placement_county_districts)):#search through county list to match county name with judicial district number
            if county in placement_county_districts[county_arr_idx]:
                district_num = county_arr_idx
                #print('found county[{}:{}] in arr:{}'.format(county,district_num,str(placement_county_districts[district_num])))
        #display(HTML(overview.loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()))
        display(HTML(placement_rates_data.loc[idx[district_num+1,year_tup[0]:year_tup[1]], :].transpose().to_html()))
    except Exception as e:
        print('Error showing county placement rates data.'+str(e))

def display_state_placements_rates_html(county,year_tup):
    try:
        display(HTML(state_placement_rates_data.loc[idx[year_tup[0]:year_tup[1]], :].transpose().to_html()))
    except Exception as e:
        print('Error showing state placement rate data.'+str(e))

##CASE COUNTS
def display_case_counts_html(county,year_tup):
    try:
        display(HTML(court_case_counts.loc[idx[str(year_tup[0]):str(year_tup[1]),county], :].transpose().to_html()))
    except Exception as e:
        print('Error showing Case Counts data.'+str(e))

def display_demographic_html(county,year_tup):
    try:
        display(HTML(demographic_data.loc[idx[county,:,year_tup[0]:year_tup[1]],:].transpose().to_html()))
    except Exception as e:
        print('Error showing demographic data.'+str(e))


# In[7]:


# crime stats functions
#calculate crime rate per county
def county_crime_rate(county,year_tup,estimate_per):
    #df = juvenile_arrests.round({'Total Incidents':0,'Population 11-20':0,'Rate':2})
    display(HTML(juvenile_arrests[['Total Incidents','Population 11-17','Rate']].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()))
    #display(HTML(df.loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()))
    return

def state_crime_rate(county,year_tup,estimate_per):
    year_tup=(year_tup[0],year_tup[1])
    display(HTML(arrest_totals[['Total Incidents','Population 11-17','Rate']].loc[idx[year_tup[0]:year_tup[1]],:].transpose().to_html()))
    return

def agegroup_demographic(county,year_tup):
    display(HTML(agegroup_demographic_data[agegroup_demographic_data['Age Range']=='11-17'].loc[idx[county,year_tup[0]:year_tup[1]],:].transpose().to_html()))
    #display(HTML(agegroup_demographic_data[agegroup_demographic_data['Age Range']=='18-20'].loc[idx[county,year_tup[0]:year_tup[1]],:].transpose().to_html()))
    return


# In[8]:


# tests = school.index.levels[0].str.strip()
# print(tests)
# x = [x for x in tests]
# print(x)
# print(x.sort())


# In[9]:


##Widget Objects
county_drop = widgets.Dropdown(
    options=[x for x in school.index.levels[0].str.strip()],
    description='County:',
    disabled=False,
)
year_slide = widgets.IntRangeSlider(
    description='Year range:',
    min=2012,
    max=2017,
    value=(2014,2017),
    step=1
)
estimates_slide = widgets.Select(
    options=[10000],
    value=10000,
    description='Estimate per',
    disabled=False,
    continuous_update=True,
    orientation='horizontal',
    readout=True
)


# In[10]:



#tables widgets
afcars_out = widgets.interactive_output(display_afcars_html,{'county':county_drop,'year_tup':year_slide})
county_out = widgets.interactive_output(display_county_html,{'county':county_drop,'year_tup':year_slide})
felony_out = widgets.interactive_output(display_felony_html,{'county':county_drop,'year_tup':year_slide})
lesser_out = widgets.interactive_output(display_lesser_html,{'county':county_drop,'year_tup':year_slide})
school_out = widgets.interactive_output(display_school_html,{'county':county_drop,'year_tup':year_slide})
school_rate_out = widgets.interactive_output(display_school_rate_html,{'county':county_drop,'year_tup':year_slide})
placements_out = widgets.interactive_output(display_placements_html,{'county':county_drop,'year_tup':year_slide})
placements_rates_out = widgets.interactive_output(display_county_placements_rates_html,{'county':county_drop,'year_tup':year_slide})
state_placements_rates_out = widgets.interactive_output(display_state_placements_rates_html,{'county':county_drop,'year_tup':year_slide})
demographics_out = widgets.interactive_output(display_demographic_html,{'county':county_drop,'year_tup':year_slide})
case_counts_out = widgets.interactive_output(display_case_counts_html,{'county':county_drop,'year_tup':year_slide})
agegroup_demographic_out = widgets.interactive_output(agegroup_demographic,{'county':county_drop,'year_tup':year_slide})
#estimates widgets
crime_rate_out = widgets.interactive_output(county_crime_rate,{'county':county_drop,'year_tup':year_slide,'estimate_per':estimates_slide})
state_crime_rate_out = widgets.interactive_output(state_crime_rate,{'county':county_drop,'year_tup':year_slide,'estimate_per':estimates_slide})

#show everything
##################################### Header stuff
display_header()
display(widgets.HBox([
    widgets.VBox([county_drop,year_slide]),
    estimates_slide,
    widgets.HTML(value="people")
]))
##################################### Arrests Data
display(
    widgets.VBox([
        widgets.HTML(value='<hr><center><h1>ORI Arrests Data</h1></center>'),
        #widgets.HTML(value="Wyoming Juvenile Arrests reported from agency ORI numbers. Split between violent felony offenses and non-violent offenses.")
        widgets.HTML(value="Data depicted represents Juvenile Arrests as reported by Wyoming Department of Criminal Investigations(DataSource[3]). The data is split into two tables \
                     with the table on the left showing violent felony offenses and the table on the right showing the lesser offenses reported.")
    ]),
        widgets.HBox([
        felony_out,
        lesser_out
    ]),
    #widgets.HTML(value="SOURCE: Wyoming DCI UCR arrests by ORI"),
    widgets.HTML(value="<p class=\"page-break\"></p>")
)

display(
    widgets.HTML(value="<center><h1>Arrest Rate Comparisons</h1></center>"),
    widgets.HTML(value="""
        Depicts county arrest rates calculated from the above ORI Arrests Data. Rate is calculated from
        the 'Estimate per {} people' field at the top of the form. County arrest rates are calculated
        using the sum of all arrests for each year, for the selected county portrayed in the ORI Arrests Data above. Then for
        comparison, the state arrest rates are calculated from all counties for the selected years. Population data is
        then added from the OJJDP source containing only population values for ages 11-17 within the county. (DataSources[1,3,5])
                 """.format(estimates_slide.value)),
    widgets.HBox([

        widgets.VBox([
            widgets.VBox([
                widgets.HTML(value="<h2>County Arrest Rates</h2>"),
                widgets.HBox([crime_rate_out]),
                #widgets.HTML(value="SOURCE: Wyoming DCI UCR arrests by ORI")
            ]),
            widgets.VBox([
                widgets.HTML(value="<h2>Juvenile Court Case Counts</h2>"),
                widgets.HTML(value="* denotes case counts greater than zero and less than five."),
                widgets.HBox([case_counts_out]),
                #widgets.HTML(value="SOURCE: OOJDP Easy Access to State and County Juvenile Court Case Counts")
            ])
        ]),
        widgets.VBox([
            widgets.HTML(value="<h2>State Arrest Rates</h2><br>"),
            widgets.HBox([state_crime_rate_out]),
            #widgets.HTML(value="SOURCE: Wyoming DCI UCR arrests by ORI"),
            widgets.HTML(value="<h2>Juvenile Population Demographics by Age Group</h2>"),
            widgets.HBox([agegroup_demographic_out])
        ])
    ]),
    widgets.HTML(value="<p class=\"page-break\"></p>")
)
#display(widgets.HBox([county_comparisons]))
##################################### Placement Info
display(
    widgets.HTML(value="<hr><h1>DFS Placements</h1>"),
    widgets.HTML(value="The left table depicts placement type (of those in care) for probation/delinquency cases only,\
                 by Judicial District. The yearly numbers depicted are calculated from the 12-month average of the \
                 number of juveniles in a placement scenario, as reported at the end of every month. \
                 Data shown is for the judicial district to which the current selected \
                 county belongs to. The table on the right shows DFS placements by county as provided by \
                 the DFS prior to 2017(see note below). Placement rates are calculated using the same method \
                 as the arrest rates above.(DataSources[1,4])"),
    widgets.HBox([
        widgets.VBox([
            placements_out,
            #widgets.HTML(value="SOURCE: placements footer"),
        ]),
        widgets.VBox([
            widgets.HTML(value="<h2>District Placement Rates</h2>"),
            placements_rates_out,
            widgets.HTML(value="<h2>State Placement Rates</h2>"),
            state_placements_rates_out,
            widgets.VBox([
                county_out,
                #widgets.HTML(value="SOURCE: by county footer"),
                widgets.HTML(value="Prior to 2017 all DFS reports were reported on a per county basis. After 2017, DFS data collection systems no longer classified data per county.")
            ])
    #         widgets.HBox([crime_rate_out])
        ]),
    ]),
    widgets.HTML(value="<p class=\"page-break\"></p>")
)
##################################### School info
display(
    widgets.VBox([
        widgets.HTML(value='<hr><h2>Educational Discipline Data</h2>'),
        widgets.HTML(value="""
                    The table below depicts Educational discipline data as reported by the Wyoming
                    Department of Education. The left table represents the raw data portrayed
                    by school district within the selected county. The right table portrays the
                    educational discipline rates of the selected county. The rates do not include in school suspensions,
                    and are calculated in a similar fashion to the above two tables,
                    using the sum of the total incidents for each school district contained within a county as
                    the total value per year. (DataSources[1,2])
                """),
    ]),
    widgets.HBox([
        school_out,
        #school_rate_out ##NEEDS WORK!!
    ])
)


# In[11]:


## Download Data
# dfunct = DataFunctions()
# overview = dfunct.getOverview()
# dfs = dfunct.getDFS()#afcars, county, plc
# school = dfunct.getSchool()
# agegroup_demographic_data = dfunct.getDemographic_By_AgeGroup()
# juvenile_arrests = dfunct.getORIData(agegroup_demographic_data)
# population_data = dfunct.getPopulationData()#phasing out?
# arrest_totals = dfunct.getStateTotalArrests(juvenile_arrests,population_data)
# judicial_district_population_data = dfunct.getJudicialDistrictJuvenilePopulations()
# placement_data = dfunct.getJudicialPlacementData()
# placement_rates_data,state_placement_rates_data = dfunct.getJudicialPlacementRates(placement_data,judicial_district_population_data)
# demographic_data = dfunct.getDemographicData()
# court_case_counts = dfunct.getCourtCaseNumbersData()
from IPython.display import Javascript

def downloadCSV_python(name):
    print('pycsv:{}'.format(name))
    csv_string = ''
    if name is 'Education':
        csv_string = school.to_csv(index=False).replace('\n','\\n').replace("'","\'")
    elif name is 'Demographic':
        csv_string = agegroup_demographic_data.to_csv(index=False).replace('\n','\\n').replace("'","\'")
    elif name is 'JuvyArrest':
        csv_string = arrest_totals.to_csv(index=False).replace('\n','\\n').replace("'","\'")
    elif name is 'JuvyCourtCase':
        csv_string = court_case_counts.to_csv(index=False).replace('\n','\\n').replace("'","\'")

    js_download = """
    var csv = '%s';

    var filename = 'results.csv';
    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            link.innerHTML = 'link';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
    """ % csv_string

    Javascript(js_download)

js_download_funct = """
<script>
function downloadCSV_js(name){
    console.log('clicked')
    var kernel = IPython.notebook.kernel;
    kernel.execute(downloadCSV_python(name));
}
</script>
"""
display(HTML(js_download_funct))
display(HTML('<h3>Download the Data</h3> Click on the links below to download the CSV files being used in the above report.'))
display(HTML("""To view Data Citations please visit <a href="https://github.com/coolcomputers/WyJJD/new-data/DataGuide.md">this page</a>"""))

display(HTML('<a onclick="downloadCSV_js(\'Education\')">Download Educational Discipline Data</a>'))
display(HTML('<a onclick="downloadCSV_js(\'Demographic\')">Download Population and Demographic Information by Age Group Data</a>'))
display(HTML('<a onclick="downloadCSV_js(\'JuvyArrest\')">Download Juvenile Arrest Data Data</a>'))
display(HTML('<a onclick="downloadCSV_js(\'JuvyCourtCase\')">Download Juvenile Court Case Counts Data</a>'))

display(HTML('<h3>Data Citations</h3>'))
display(HTML("""To view references and sources of data, please visit <a href="https://github.com/coolcomputers/WyJJD/new-data/DataGuide.md">this page</a>"""))


# In[12]:


display(HTML('<p>Please visit <a href="https://github.com/coolcomputers/WyJJD/new-data/DataGuide.md" target="_blank">the Data Guide page</a> for data source citations.</p>'))
display(HTML('<p>Project created by Cool Computers for the Wyoming Children\'s Law Center, funded partially by grants provided by the <a href="https://www.aecf.org/where-we-work/location/wy/" target="_blank">Annie E. Casey Foundation</a></p>'))


# In[13]:


#arrest_totals[['Total Incidents','Population 11-17','Rate']]
