#File:county_snapshot_tables.py
#Author: Rafer Cooley
#Desc:Generate County Snapshots tables for populating HTML page
# from ipywidgets import widgets
# from ipywidgets import interactive
# from IPython.display import display, HTML, clear_output
#from pivottablejs import pivot_ui
from GetDataFunctions import *

import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import os, sys
import subprocess
import base64 #for createdownloadlink

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

idx = pd.IndexSlice


def display_afcars_html(county,year_tup):
    try:
        return dfs[0].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()
    except Exception as e:
        return 'Error showing DFS afcars data.'+str(e)

def display_county_html(county,year_tup):
    try:
        return dfs[1].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()
    except Exception as e:
        return 'Error showing DFS county data.'+str(e)

def display_felony_html(county,year_tup):
    try:
        tmp_felony = juvenile_arrests.loc[idx[county,year_tup[0]:year_tup[1]], :][violent_felony]
        tmp_felony['Totals'] = tmp_felony.sum(axis=1)
        return tmp_felony.transpose().to_html()
    except Exception as e:
        return 'Error showing ORI data.'+str(e)

def display_lesser_html(county,year_tup):
    try:
        tmp_lesser = juvenile_arrests.loc[idx[county,year_tup[0]:year_tup[1]], :][lesser_offenses]
        tmp_lesser['Totals'] = tmp_lesser.sum(axis=1)
        return tmp_lesser.transpose().to_html()
    except Exception as e:
        return 'Error showing ORI lesser offenses data.'+str(e)

def display_school_html(county,year_tup):
    try:
        return school.loc[idx[county,year_tup[0]:year_tup[1],year_tup[0]:year_tup[1]], :].transpose().to_html()
    except Exception as e:
        return 'Error showing School data.'+str(e)

def display_school_rate_html(county,year_tup):
    try:
        return school_county_rates[['Total','Population 11-17','Rate']].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()
    except Exception as e:
        return 'Error showing School data.'+str(e)

def display_overview_html(county,year_tup):#NOT USED?
    try:
        return verview.loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()
    except Exception as e:
        return 'Error showing Overview data.'+str(e)

##PLACEMENTS
def display_placements_html(county,year_tup):
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

        return placement_data[placement_fields_to_show].loc[idx[year_tup[0]:year_tup[1],district_num+1], :].transpose().to_html()
    except Exception as e:
        return 'Error showing Placements data.'+str(e)

def display_county_placements_rates_html(county,year_tup):
    try:
        district_num = 0
        for county_arr_idx in range(1,len(placement_county_districts)):#search through county list to match county name with judicial district number
            if county in placement_county_districts[county_arr_idx]:
                district_num = county_arr_idx
                #return 'found county[{}:{}] in arr:{}'.format(county,district_num,str(placement_county_districts[district_num])))
        #return overview.loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()))
        return placement_rates_data.loc[idx[district_num+1,year_tup[0]:year_tup[1]], :].transpose().to_html()
    except Exception as e:
        return 'Error showing county placement rates data.'+str(e)

def display_state_placements_rates_html(county,year_tup):
    try:
        return state_placement_rates_data.loc[idx[year_tup[0]:year_tup[1]], :].transpose().to_html()
    except Exception as e:
        return 'Error showing state placement rate data.'+str(e)

##CASE COUNTS
def display_case_counts_html(county,year_tup):
    try:
        return court_case_counts.loc[idx[str(year_tup[0]):str(year_tup[1]),county], :].transpose().to_html()
    except Exception as e:
        return 'Error showing Case Counts data.'+str(e)

def display_demographic_html(county,year_tup):
    try:
        return demographic_data.loc[idx[county,:,year_tup[0]:year_tup[1]],:].transpose().to_html()
    except Exception as e:
        return 'Error showing demographic data.'+str(e)

# crime stats functions
#calculate crime rate per county
def county_crime_rate(county,year_tup):
    try:
        return juvenile_arrests[['Total Incidents','Population 11-17','Rate']].loc[idx[county,year_tup[0]:year_tup[1]], :].transpose().to_html()
    except Exception as e:
        return 'Error showing county crime rate data.'+str(e)

def state_crime_rate(county,year_tup):
    try:
        return arrest_totals[['Total Incidents','Population 11-17','Rate']].loc[idx[year_tup[0]:year_tup[1]],:].transpose().to_html()
    except Exception as e:
        return 'Error showing state crime rate data.'+str(e)

def agegroup_demographic(county,year_tup):
    try:
        return agegroup_demographic_data[agegroup_demographic_data['Age Range']=='11-17'].loc[idx[county,year_tup[0]:year_tup[1]],:].transpose().to_html()
    except Exception as e:
        return 'Error showing agegroup demographic data.'+str(e)


#
