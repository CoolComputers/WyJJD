
# coding: utf-8

# In[114]:


#File:getdata.ipynb
#Author: Rafer Cooley
#Desc:notebook for functions associated with loading raw data into pandas dataframes
#from IPython.display import HTML
import pandas as pd
import os, sys
import base64 #for createdownloadlink

#these years are used as the standard range to display for the report, based off given ORI juvenile arrest data
ORI_Begin_Year = '2010'
ORI_End_Year = '2017'

# translate these so we have a generic year to deal with elsewhere, while retaining the above variables for use in here
BEGIN_YEAR = ORI_Begin_Year
END_YEAR = ORI_End_Year

population_base_for_rates = 10000

##Files
data_folder = 'new-data/'
census_folder = data_folder+'census-info/'
population_data_file = census_folder+'census-factfinder/census-cleaned.csv'
population_agegroup_data_file = data_folder+'ojjdp/population-data/population_agegroup_ethnicity.csv'
demographic_data_file = data_folder+'ojjdp/population-data/combined.csv'#phasing out
dci_data_folder = data_folder+'DCI/all-combined/'
dci_index_crimes = dci_data_folder+'index-offenses/'
dfs_afcars_data_file = data_folder+'DFS/DFS_12-16-AFCARS-CLEAN.csv'
dfs_county_data_file = data_folder+'DFS/DFS_12-16-Placements-ByCounty-CLEAN.csv'
dfs_plc_data_file = data_folder+'DFS/DFS_12-16-Placements-ByPLC-CLEAN.csv'
school_discipline_data_file = data_folder+'school-discipline/SchoolDiscipline_2007-17_Combined-CSV2.csv'
ori_data_file = data_folder+'juvenile-arrests/ori_juvenile_arrest_{}-{}_CLEAN.csv'.format(ORI_Begin_Year,ORI_End_Year)
placements_folder = data_folder+'DFS/placements/'
placements_data_file = placements_folder+'combined1.csv'
case_count_data_file = data_folder+'case-counts/combined.csv'
##End Files

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

COUNTIES = ['Albany','Big Horn','Campbell','Carbon','Converse', 'Crook',
            'Fremont', 'Goshen', 'Hot Springs', 'Johnson', 'Laramie', 'Lincoln',
           'Natrona','Niobrara','Park','Platte','Sheridan','Sublette',
            'Sweetwater','Teton','Uinta','Washakie','Weston']


idx = pd.IndexSlice
class DataFunctions:
    #found:https://stackoverflow.com/questions/31893930/download-csv-from-an-ipython-notebook
    def create_download_link(self,df, title = "Download CSV file", filename = "data.csv"):
        csv1 = df.to_csv()
        b64 = base64.b64encode(csv1.encode())
        payload = b64.decode()
        html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
        html = html.format(payload=payload,title=title,filename=filename)
        return HTML(html)
    #end found

    ##Get Data Functs
    def getOverview(self):#DONE
        gather_overview_frames = []
        current_path = dci_data_folder+'overview/'
        year_files = next(os.walk(current_path))[2]
        for f in year_files:#process each file for this year
            file_path = current_path+'/'+f
            year = f.split('-')[0]
            try:
                df = pd.read_csv(file_path,sep=',',header='infer',index_col=0)
                df.assign(Year=year)
                gather_overview_frames.append(df)
            except Exception as e:
                print('cant load file: '+file_path)
                print('['+str(e)+']')
                print('*****************************************************************************************')
        return pd.concat(gather_overview_frames)

    ###################
    ## EDUCATION DATA FUNCTIONS
    def getSchool(self):
        #contains 'In School Suspensions'
#         df = pd.read_csv(school_discipline_data_file,sep=',',header='infer')
#         df['County'] = df['DISTRICT_NAME'].str.split('#').str[0]
#         df.set_index(['County','Beginning Year','End Year'],inplace=True)
#         df.sort_index(level=['County','Beginning Year','End Year'],ascending=[1,1,1],inplace=True)
#         dfii = [x.strip() for x in df.index.get_level_values(0).unique()]
#         df.index.set_levels(dfii, level='County', inplace=True)
#         df['Totals']=df.iloc[:,[2,3,4,5]].sum(axis=1)

        #Does NOT include 'In School Suspensions'
        df = pd.read_csv(school_discipline_data_file,sep=',',header='infer')
        df['County'] = df['DISTRICT_NAME'].str.split('#').str[0]
        df.drop('In school suspension',axis=1,inplace=True)
        df.set_index(['County','Beginning Year','End Year'],inplace=True)
        df.sort_index(level=['County','Beginning Year','End Year'],ascending=[1,1,1],inplace=True)
        dfii = [x.strip() for x in df.index.get_level_values(0).unique()]

        df.index.set_levels(dfii, level='County', inplace=True)

        df['Totals']=df.iloc[:,[2,3,4]].sum(axis=1)
        #df.sortlevel()
        return df.fillna(0)

    def getSchool_county_rates(self,edu,pop):
        school2 = edu.reset_index()
        school_rates = school2.groupby(['County','Beginning Year'])[['Totals']].sum().reset_index()
        school_rates.rename(columns={'Beginning Year':'Year'},inplace=True)
        pop = pop.reset_index()
        schl = []
        for year in range(int(ORI_Begin_Year),int(ORI_End_Year)):
            for county in COUNTIES:
                obj = {
                    'County':county,
                    'Year':year,
                    'Population 11-17':pop.loc[(pop['Age Range']=='11-17') & (pop['County']==county) & (pop['Year']==year)]['Total'].iloc[0],
                    'Total':school_rates.loc[(school_rates['County']==county) & (school_rates['Year']==year)]['Totals'].iloc[0]
                }
                schl.append(obj)
        df = pd.DataFrame(schl)
        df['Rate']=(df['Total']/df['Population 11-17'])*population_base_for_rates
        df['Rate']=df['Rate'].round(2)
#         print(df.head(50))
        df.set_index(['County','Year'],inplace=True)
        df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
        return df

    def getSchool_state_rates(self,edu,pop):
        #pop = agegroup_demographic_data.reset_index()
#         pop = pop.reset_index()
#         total_arrests = {}
#         for row,new_df in edu.groupby(level=[0,1]):
#             if str(row[1]) not in total_arrests:
#                 edu[str(row[1])] = new_df['Total Incidents'][0]
#             else:
#                 edu[str(row[1])] = edu[str(row[1])]+new_df['Total Incidents'][0]
#         state_totals = []
#         for key in total_arrests:
#             #print("Year:{}-Totals:{}-StatePop:{}".format(key,state_totals[key],pop[key].sum()))
#             edu.append({'Year':int(key),'Total Incidents':edu[key],'Population 11-17':pop.loc[(pop['Age Range']=='11-17') & (pop['Year']==int(key))].groupby(['Year']).sum()['Total'].iloc[0]})
#         #print(str(state_totals))
#         df = pd.DataFrame(state_totals)
#         df['Rate']=(df['Total Incidents']/df['Population 11-17'])*population_base_for_rates
#         df['Rate']=df['Rate'].round(2)
#         df.set_index(['Year'],inplace=True)
#         df.sort_index(level='Year',ascending=[0],inplace=True)

#         #print(df.head(15))
#         return df
        return
    ####################
    #fix this to dynamically load files
    #replaced with ori data DO NOT USE!
    def getIndexCrimes(self):
        obj1 = pd.read_csv(dci_index_crimes+'2016-index-cp-after.csv',sep=',',header='infer')
        obj1['Year']='2016'
        obj2 = pd.read_csv(dci_index_crimes+'2015-index-cp-after.csv',sep=',',header='infer')
        obj2['Year']='2015'
        obj3 = pd.read_csv(dci_index_crimes+'2014-index-cp-after.csv',sep=',',header='infer')
        obj3['Year']='2014'
        #newobj = obj['2016']#+obj['2015']+obj['2014']
        newobj = pd.concat([obj1,obj2,obj3])
        return newobj
        #return pd.read_csv(dci_index_crimes+'2016-index-cp-after.csv',sep=',',header='infer')

    def getPopulationData(self):
        df = pd.read_csv(population_data_file,sep=',',header='infer',index_col=[0])
        #df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
        #df.sortlevel
        return df

    ######################################
    #DFS placement data
    def getDFS(self):#phasing out?
        afcars = pd.read_csv(dfs_afcars_data_file,sep=',',header='infer',index_col=[0,1])
        #afcars.set_index('COUNTY')
        county = pd.read_csv(dfs_county_data_file,sep=',',header='infer',index_col=[0,1])
        #county.set_index('COUNTY')
        plc = pd.read_csv(dfs_plc_data_file,sep=',',header='infer',index_col=0)
        return afcars, county, plc

    def getJudicialPlacementData(self):
        df = pd.read_csv(placements_data_file,sep=',',header='infer',index_col=['Year','district'])
        df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
        df=df.groupby(level=[0, 1]).sum()
#         df1=df.groupby(level=[0, 1]).sum()
#         df2=df.groupby(level=[0,1]).sum()/12
#         df2 = df2.round(decimals=0)

        df['Total'] = df.sum(axis=1)
        df['Total']=(df['Total']-df['Total Children in Care']-df['Total Family-like setting']-df['Total Group Care'])
        return df



    def getJudicialPlacementRates(self,placements,pop):
        year_range = range(int(ORI_Begin_Year),int(ORI_End_Year)+1)
        cnty_plc = placements.reset_index()
        cnty_plc = cnty_plc[['Year','district',"Total"]]
        for year in year_range:
            for county in range(9):
                if not cnty_plc.loc[(cnty_plc['Year']==year) & (cnty_plc['district']==county+1)].empty:
                    cnty_plc.loc[(cnty_plc['Year']==year) & (cnty_plc['district']==county+1),'Population 11-17']=pop.loc[idx[str(year):str(year)],:].iloc[:,county][0]
        cnty_plc['Rate']=(cnty_plc['Total']/cnty_plc['Population 11-17'])*population_base_for_rates
        cnty_plc['Rate']=cnty_plc['Rate'].round(2)
        cnty_plc.set_index(['district','Year'],inplace=True)
        cnty_plc.sort_index(level=[0,1],ascending=[1,1],inplace=True)

        state_plc = cnty_plc.reset_index().groupby(['Year'])[['Total','Population 11-17']].sum()
        state_plc['Rate']=(state_plc['Total']/state_plc['Population 11-17'])*population_base_for_rates
        state_plc['Rate']=state_plc['Rate'].round(2)
        #cnty_plc.set_index(['Year'],inplace=True)
        #cnty_plc.sort_index(level=[1],ascending=[1],inplace=True)
        #state_placement_rates_data['Rate'] =
        return cnty_plc,state_plc

    ######################################
    ##JUVENILE ARRESTS
    def getORIData(self,pops):#juvyarrests
        #population_data = pd.read_csv(population_data_file,sep=',',header='infer',index_col=[0])

        df = pd.read_csv(ori_data_file,sep=',',header='infer',index_col=[1,0])
        df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
        df['Total Incidents'] = df.sum(axis=1)
        #df['Population 11-20'] = (pops[pops['Age Range']=='18-20']['Total']+pops[pops['Age Range']=='11-17']['Total'])
        df['Population 11-17'] = (pops[pops['Age Range']=='11-17']['Total'])
        df['Rate'] = (df['Total Incidents']/df['Population 11-17'])*population_base_for_rates
        df['Rate']=df['Rate'].round(2)
        #df['Total Incidents']=df['Total Incidents'].round(0)
        #df.sortlevel
        return df

    def getStateTotalArrests(self,juvenile_arrests,pop):#arrest_totals
        #pop = agegroup_demographic_data.reset_index()
        pop = pop.reset_index()
        total_arrests = {}
        for row,new_df in juvenile_arrests.groupby(level=[0,1]):
            if str(row[1]) not in total_arrests:
                total_arrests[str(row[1])] = new_df['Total Incidents'][0]
            else:
                total_arrests[str(row[1])] = total_arrests[str(row[1])]+new_df['Total Incidents'][0]
        state_totals = []
        for key in total_arrests:
            #print("Year:{}-Totals:{}-StatePop:{}".format(key,state_totals[key],pop[key].sum()))
            state_totals.append({'Year':int(key),'Total Incidents':total_arrests[key],'Population 11-17':pop.loc[(pop['Age Range']=='11-17') & (pop['Year']==int(key))].groupby(['Year']).sum()['Total'].iloc[0]})
        #print(str(state_totals))
        df = pd.DataFrame(state_totals)
        df['Rate']=(df['Total Incidents']/df['Population 11-17'])*population_base_for_rates
        df['Rate']=df['Rate'].round(2)
        df.set_index(['Year'],inplace=True)
        df.sort_index(level='Year',ascending=[0],inplace=True)

        #print(df.head(15))
        return df

    #####################################
    def getCourtCaseNumbersData(self):
        df = pd.read_csv(case_count_data_file,sep=',',header='infer',index_col=[0,1])
        df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
        #df['total'] = df.sum(axis=1)
        #df=df.groupby(level=[0, 1]).sum()
        return df[['Delinquency Petition','Status Petition','Dependency Petition']]
        #return df

    #phase out
    def getDemographicData(self):
        df = pd.read_csv(demographic_data_file,sep=',',header='infer',index_col=[0,2,1])
        #df.sort_index(level=[1,1,1],ascending=[1,1,1],inplace=True)
        df.sort_index(level=['County','Age Range','Year'],ascending=[1,1,1],inplace=True)
        #df.sortlevel()
        return df

    #copied from above to prevent breaking something
    #REMOVE!
    def getDemographicData2(self):
        df = pd.read_csv(demographic_data_file,sep=',',header='infer')
        #df.sort_index(level=[1,1,1],ascending=[1,1,1],inplace=True)
        #df.sort_index(level=['County','Year'],ascending=[1,1],inplace=True)
        #df.sortlevel()
        return df

    def getDemographic_By_AgeGroup(self):
        df = pd.read_csv(population_agegroup_data_file,sep=',',header='infer')
        df['County'] = df['County'].str.replace(' County','')
        df.set_index(['County','Year'],inplace=True)
        #df.sort_index(level=[1,1,1],ascending=[1,1,1],inplace=True)
        df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
        #df.sortlevel()
        return df

    def getJudicialDistrictJuvenilePopulations(self,pop):
        county_juvy_populations = pop[pop['Age Range']=='11-17']['Total']
        county_juvy_populations = pd.DataFrame(county_juvy_populations)
        #print(county_juvy_populations.head(1))
        #county_juvy_populations.set_index(['County','Year'],inplace=True)
        #print(county_juvy_populations.head(1))
        year_range = range(int(ORI_Begin_Year),int(ORI_End_Year)+1)
        district_num = 0
        districts = {}
        for county_arr_idx in range(0,len(placement_county_districts)):#search through county list to match county name with judicial district number
            #print('{}-{}'.format(county_arr_idx+1,placement_county_districts[county_arr_idx]))
            if county_arr_idx not in districts:
                districts[str(county_arr_idx)] = {}
                for year in year_range:
                    #print(county_juvy_populations.loc[idx[placement_county_districts[county_arr_idx],year:year]])
                    if year not in districts[str(county_arr_idx)]:
                        districts[str(county_arr_idx)][str(year)] = 0
            #print('district format=={}'.format(districts[str(county_arr_idx)]))
            for cnty in placement_county_districts[county_arr_idx]:
                for year in year_range:
                    try:
                        districts[str(county_arr_idx)][str(year)] += county_juvy_populations.loc[idx[cnty,year],:]['Total']
                        #print(county_juvy_populations.loc[idx[cnty,year],:]['Total'])
                    except:
                        xx=0#blorp
        df = pd.DataFrame(districts)
        return df

#dfu = DataFunctions()
#print(dfu.getPopulationData())


# In[113]:


# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# #import seaborn as sns
# from IPython.display import HTML
#
# dfunct = DataFunctions()
# df = dfu.getCourtCaseNumbersData()
# idx = pd.IndexSlice
#
# agegroup_demographic_data = dfunct.getDemographic_By_AgeGroup()
# population_data = dfunct.getPopulationData()#phasing out?
# #arrest_totals = dfunct.getStateTotalArrests(juvenile_arrests,population_data)
#
# school = dfunct.getSchool()
# school_county_rates = dfunct.getSchool_county_rates(school,agegroup_demographic_data)
# school_state_rates = dfunct.getSchool_state_rates(school,agegroup_demographic_data)
#
# juvenile_arrests = dfunct.getORIData(agegroup_demographic_data)
# arrest_totals = dfunct.getStateTotalArrests(juvenile_arrests,agegroup_demographic_data)
#
# judicial_district_population_data = dfunct.getJudicialDistrictJuvenilePopulations(agegroup_demographic_data)
# placement_data = dfunct.getJudicialPlacementData()
# placement_rates_data,state_placement_rates_data = dfunct.getJudicialPlacementRates(placement_data,judicial_district_population_data)
#
# demographic_data = dfunct.getDemographicData()
# court_case_counts = dfunct.getCourtCaseNumbersData()
#
# ############################################
# county = 'Albany'
# year_tup = (2014,2017)
# years = [x for x in range(year_tup[0],year_tup[1]+1)]

#print(school_state_rates)

#print(school_county_rates.head(5))
#display(HTML(school_county_rates.loc[idx[:,year_tup[0]:year_tup[1]]].to_html()))
#display(HTML(school_county_rates.loc[idx[:,:]].groupby(level=[0, 1]).sum().transpose().to_html()))
#display(HTML(school_county_rates[['Total','Population 11-17','Rate']].loc[idx['Albany',year_tup[0]:year_tup[1]], :].reset_index(level=0,drop=True).transpose().to_html()))
#print(school_county_rates['Population 11-17'].loc[idx[:,'2015':'2015'], :])
# objs = []
# for year in years:
#     #print(school_county_rates['Population 11-17'].loc[idx[:,year:year], :])
#     objs.append({
#         'year':year,
#         'Population 11-17':school_county_rates['Population 11-17'].loc[idx[:,year:year], :]
#     })

#data.groupby(level=[0, 1]).sum()
#display(HTML(school_county_rates.loc[idx[:,str(year_tup[0]):str(year_tup[1])]].transpose().to_html()))
# print(school_county_rates.head(1))
# state_placement_rates_data['pct'] = state_placement_rates_data['Rate'].pct_change()
# #juvenile_arrests['pct'] = juvenile_arrests['Rate'].pct_change()
# print(state_placement_rates_data['pct'].head(5))
# print(state_placement_rates_data['Rate'].loc[idx[year_tup[0]:year_tup[1]]].values.flatten().tolist())
# print(school_county_rates.head(2))
# #print(school_county_rates[['Rate']].loc[idx[begin_year:end_year],:].values.flatten().tolist())
# print(school_county_rates[['pct']].loc[idx[:,year_tup[0]:year_tup[0]], :].values.flatten().tolist())

# year_average = []
# for year in years:
#     print(juvenile_arrests.loc[idx[:,year:year],:]['pct'].values.flatten().tolist())
#     year_average.append(np.mean(juvenile_arrests.loc[idx[:,year:year],:]['pct'].values.flatten().tolist()))
# print(year_average)

#print(school_state_rates)
# print(juvenile_arrests.loc[idx[:,year:year],:]['pct'].values.flatten().tolist())
# year_average = []
# for year in years:
#     year_average.append(np.mean(juvenile_arrests.loc[idx[:,year:year],:]['pct'].values.flatten().tolist()))

# print(['{},{}'.format(x,y) for x,y in zip(years,year_average)])
#for year in range(2014,2018):
    #print(juvenile_arrests[['pct']].loc[idx[county,year:year], :].values.flatten()[0])

#juvenile_arrests[['Rate']].loc[idx[county,year_tup[0]:year_tup[1]], :].values.flatten()
#print(arrest_totals[['Rate']].loc[idx[year_tup[0]:year_tup[1]],:].values.flatten())
        #pct_change_vals=df[['Rate']].loc[idx[county,year:year], :].pct_change().values.flatten().tolist()
#         objs.append({'county':county,'pct_change':pct_change_vals})
#         cnt=0
#         pos_years = []
#         pos_data = []
#         neg_years = []
#         neg_data = []
#         for year in years:
#             if pct_change_vals[cnt]<0:
#                 neg_years.append(year)
#                 neg_data.append(pct_change_vals[cnt])
#             else:
#                 pos_years.append(year)
#                 pos_data.append(pct_change_vals[cnt])
#             cnt+=1
#schl = dfunct.getSchool_county_rates(school,agegroup_demographic_data)
#print(school_county_rates.head(3))


# In[ ]:


# df = pd.read_csv(school_discipline_data_file,sep=',',header='infer')
# df['County'] = df['DISTRICT_NAME'].str.split('#').str[0]
# df.drop('In school suspension',axis=1,inplace=True)
# df.set_index(['County','Beginning Year','End Year'],inplace=True)
# df.sort_index(level=['County','Beginning Year','End Year'],ascending=[1,1,1],inplace=True)
# dfii = [x.strip() for x in df.index.get_level_values(0).unique()]

# df.index.set_levels(dfii, level='County', inplace=True)

# df['Totals']=df.iloc[:,[2,3,4]].sum(axis=1)

# print(df.head(5))


# In[ ]:


#calculating education rates
# school2 = school.reset_index()
# #print(school2.head(1))
# #print(school2.groupby(['County','Beginning Year']).head(5))
# school_rates = school2.groupby(['County','Beginning Year'])[['Totals']].sum().reset_index()
# school_rates.rename(columns={'Beginning Year':'Year'},inplace=True)
# #print(school_rates.head(1))
# #school_rates['Year'] = school_rates['Beginning Year']
# print(school_rates.head(2))
# #print(school2[['County','Beginning Year','End Year','Totals']].sum())
# pop = agegroup_demographic_data

# pop = pop.reset_index()
# print(pop.head(2))
# #print(pop.loc[(pop['Age Range']=='11-17')][['County','Year','Total']].head(20))
# # school_rates['Population'] = pop.loc[(pop['Age Range']=='11-17')]['Total']
# # print(school_rates.head(20))
# schl = []
# for year in range(int(ORI_Begin_Year),int(ORI_End_Year)):
#     for county in COUNTIES:
#         #print(pop.loc[(pop['Age Range']=='11-17') & (pop['County']==county) & (pop['Year']==year)]['Total'].iloc[0])
#         #print(school_rates.loc[(school_rates['County']==county) & (school_rates['Year']==year)]['Totals'].iloc[0])
#         obj = {
#             'County':county,
#             'Year':year,
#             'Population':pop.loc[(pop['Age Range']=='11-17') & (pop['County']==county) & (pop['Year']==year)]['Total'].iloc[0],
#             'Total':school_rates.loc[(school_rates['County']==county) & (school_rates['Year']==year)]['Totals'].iloc[0]
#         }
# #         print('county:{}--year:{}--pop:{}--eduTotal:{}'.format(
# #             county,
# #             str(year),
# #             pop.loc[(pop['Age Range']=='11-17') & (pop['County']==county) & (pop['Year']==year)]['Total'].iloc[0],
# #             school_rates.loc[(school_rates['County']==county) & (school_rates['Year']==year)]['Totals'].iloc[0]
# #         ))
#         #print(obj)
#         schl.append(obj)
# df = pd.DataFrame(schl)
# df['Rate']=(df['Total']/df['Population'])*population_base_for_rates
# print(df.head(50))


# In[ ]:


# total_arrests = {}
# for row,new_df in juvenile_arrests.groupby(level=[0,1]):
#     if str(row[1]) not in total_arrests:
#         total_arrests[str(row[1])] = new_df['Total Incidents'][0]
#     else:
#         total_arrests[str(row[1])] = total_arrests[str(row[1])]+new_df['Total Incidents'][0]
# state_totals = []
# for key in total_arrests:
#     #print("Year:{}-Totals:{}-StatePop:{}".format(key,state_totals[key],pop[key].sum()))
#     state_totals.append({'Year':int(key),'Total Incidents':total_arrests[key],'Population 11-17':pop.loc[(pop['Age Range']=='11-17') & (pop['Year']==int(key))].groupby(['Year']).sum()['Total'].iloc[0]})
# #print(str(state_totals))
# df = pd.DataFrame(state_totals)


# total_edu_points = {}
# for row,new_df in school.groupby(level=[0,1]):
#     print('row:{}'.format(row))
#     print('df:{}'.format(new_df))
#     if str(row[0]) not in total_edu_points:
#         total_edu_points[str(row[0])] = new_df['Totals'][0]
#     total_edu_points[str(row[0])] = total_edu_points[str(row[0])]+new_df['Totals'][0]

# state_totals = []
# for key in total_arrests:
#     #print("Year:{}-Totals:{}-StatePop:{}".format(key,state_totals[key],pop[key].sum()))
#     state_totals.append({'Year':int(key),'Total Incidents':total_arrests[key],'Population 11-17':pop.loc[(pop['Age Range']=='11-17') & (pop['Year']==int(key))].groupby(['Year']).sum()['Total'].iloc[0]})
# #print(str(state_totals))
# df = pd.DataFrame(state_totals)


# df['Rate']=(df['Total Incidents']/df['Population 11-17'])*population_base_for_rates
# df['Rate']=df['Rate'].round(2)
# df.set_index(['Year'],inplace=True)
# df.sort_index(level='Year',ascending=[0],inplace=True)


# In[ ]:


# print(placement_data.head(4))
# print(placement_rates_data.head(6))

# agegroup_demographic_data = agegroup_demographic_data.reset_index()
# school = dfunct.getSchool()
# # school_county_rates = dfunct.getSchool_county_rates(school,agegroup_demographic_data)
# # school_state_rates = dfunct.getSchool_state_rates(school,agegroup_demographic_data)
# school_county_rates = school.reset_index()[['County','Beginning Year','Totals']]
# school_county_rates['Year'] = school_county_rates['Beginning Year']
# school_county_rates = school_county_rates[['County','Year','Totals']]
# school_county_rates['Population 11-17'] = agegroup_demographic_data[(agegroup_demographic_data['Age Range']=='11-17')]['Total']
# # f['Population 11-17'] = (pops[pops['Age Range']=='11-17']['Total'])
# # df['Rate'] = (df['Total Incidents']/df['Population 11-17'])*population_base_for_rates
# print(school_county_rates.head(10))
# print(agegroup_demographic_data.head(4))


# In[ ]:


# county_juvy_populations = agegroup_demographic_data[agegroup_demographic_data['Age Range']=='18-20']['Total']+agegroup_demographic_data[agegroup_demographic_data['Age Range']=='11-17']['Total']
# county_juvy_populations = pd.DataFrame(county_juvy_populations)
#print(county_juvy_populations.head(1))
#county_juvy_populations.set_index(['County','Year'],inplace=True)
#print(county_juvy_populations.head(1))
#print(placement_data.head(1))

#print(placement_rates_data.head(5))
# state_rates = placement_rates_data.reset_index()
# state_rates['Rate']=0
# print(state_rates.head(5))
# #x=state_rates[state_rates['Year']==2018].sum()
# #print(x.to_frame().transpose())
# #df.groupby(['Country', 'Item_Code'])[["Y1961", "Y1962", "Y1963"]]
# print(state_rates.groupby(['Year'])[['Total','Population 11-20']].sum())


# In[ ]:


# df = pd.read_csv(placements_data_file,sep=',',header='infer',index_col=['Year','district'])
# df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
# df1=df.groupby(level=[0, 1]).sum()
# df2=df.groupby(level=[0,1]).sum()/12
# df2 = df2.round(decimals=0)
# print(df1.head(3))
# print('**********')
# print(df2.head(3))
# df['Total'] = df.sum(axis=1)
# df['Total']=(df['Total']-df['Total Children in Care']-df['Total Family-like setting']-df['Total Group Care'])


# In[ ]:


# district_num = 0
# districts = {}
# distArr = []
#print(placement_rates_data.head(15))
# for county_arr_idx in range(0,len(placement_county_districts)):#search through county list to match county name with judicial district number

#     print('{}-{}'.format(county_arr_idx+1,placement_county_districts[county_arr_idx]))
#     if county_arr_idx not in districts:
#         districts[str(county_arr_idx)] = {}
#         for year in year_range:
#             #print(county_juvy_populations.loc[idx[placement_county_districts[county_arr_idx],year:year]])
#             if year not in districts[str(county_arr_idx)]:
#                 districts[str(county_arr_idx)][str(year)] = 0
#     print('district format=={}'.format(districts[str(county_arr_idx)]))
#     for cnty in placement_county_districts[county_arr_idx]:
#         for year in year_range:
#             try:
#                 districts[str(county_arr_idx)][str(year)] += county_juvy_populations.loc[idx[cnty,year],:]['Total']
#                 print(county_juvy_populations.loc[idx[cnty,year],:]['Total'])
#             except:
#                 xx=0#blorp

#         tmpobj = districts[str(county_arr_idx)]
#         tmpobj['County']=county_arr_idx
#         print(districts[str(county_arr_idx)])
#         distArr.append(tmpobj)
# print(districts)
# df = pd.DataFrame(distArr)

# print(df.head(3))


# In[ ]:


# year_range = range(int(ORI_Begin_Year),int(ORI_End_Year)+1)

# x = dfunct.getJudicialDistrictJuvenilePopulations()
# #print(x.head(1))
# #print(x.loc[idx['2012':'2013'],:])

# #print(county_juvy_populations.loc[idx['Albany','2012':'2013'],:])
# #print(placement_data.sum(axis=1))
# #print(placement_data.head(15))
# print('<<<<<<<<<<<')
# pmt = placement_data.reset_index()
# pmt['Total']=(pmt['Total']-pmt['Total Children in Care']-pmt['Total Family-like setting']-pmt['Total Group Care'])
# pmt = pmt[['Year','district',"Total"]]
# # pmt.set_index(['Year'],inplace=True)
# # pmt.sort_index(level=[1],ascending=[0],inplace=True)
# #z = placement_totals.reset_index()
# #pmt = pmt.drop(['Total Children in Care'],axis=1)
# print(pmt.head(25))
# #placement_totals['Population'] = 0
# #print(placement_totals.loc[idx['2012',3],1].head(3))
# print('#####')
# #print(pmt.loc[(pmt['Year']==2012) & (pmt['district']==1)])
# #print(pmt.loc[idx['2012':'2012']])
# #print(placement_totals.loc[idx['2012':'2013',:],:].head(3))
# print('###')
# #print(x.loc[idx['2012':'2013'],:].iloc[:,1])

# for year in year_range:
#     for county in range(9):
#         #print('>>>>')
#         #print(x.loc[idx[str(year):str(year)],:].iloc[:,county][0])
#         #print('****')
#         #print(pmt.loc[idx['2012':'2012']].loc[pmt['district']==district])
#         #print(pmt.loc[(pmt['Year']==year) & (pmt['district']==county)])
#         if not pmt.loc[(pmt['Year']==year) & (pmt['district']==county+1)].empty:
#             pmt.loc[(pmt['Year']==year) & (pmt['district']==county+1),'Population 11-20']=x.loc[idx[str(year):str(year)],:].iloc[:,county][0]
#         #print(placement_data['Total'].loc[idx[str(year):str(year),str(county)],:])
# pmt['Rate']=(pmt['Total']/pmt['Population 11-20'])*10000
# print(pmt.head(30))
#turdz =
#placement_rates = placement_totals + x

#print(placement_rates.head(3))
# print('*******************')
# district_populations = {}
# for i in range(10):
#     print(i)
#     if str(i) not in district_populations:
#         district_populations[str(i)] = 0
# print(district_populations)
# for district in district_populations:
#     print(district)

#print(placement_data.loc[idx[:,'2012':'2013'],:].head(1))


# In[ ]:


#df2 = dfunct.getJudicialPlacementRates(df,pop)
#print(agegroup_demographic_data.head(1))
#print(placement_data.head(1))
#print(juvenile_arrests.head(1))
# placement_county_districts = []
# placement_county_districts.append(['Laramie'])
# placement_county_districts.append(['Albany','Carbon'])
# placement_county_districts.append(['Uinta','Sweetwater','Lincoln'])
# placement_county_districts.append(['Johnson','Sheridan'])
# placement_county_districts.append(['Big Horn','Park','Hot Springs','Washakie'])
# placement_county_districts.append(['Campbell','Weston','Crook'])
# placement_county_districts.append(['Natrona'])
# placement_county_districts.append(['Converse','Niobrara','Goshen','Platte'])
# placement_county_districts.append(['Teton','Fremont','Sublette'])

# year_range = range(2012,2020)
# county = 'Albany'
# year_tup = ('2014','2015')
# district_num = 0
# districts = {}
# for county_arr_idx in range(0,len(placement_county_districts)):#search through county list to match county name with judicial district number
#     print('{}-{}'.format(county_arr_idx+1,placement_county_districts[county_arr_idx]))
#     if county_arr_idx not in districts:
#         districts[str(county_arr_idx)] = {}
#         for year in year_range:
#             #print(county_juvy_populations.loc[idx[placement_county_districts[county_arr_idx],year:year]])
#             if year not in districts[str(county_arr_idx)]:
#                 districts[str(county_arr_idx)][str(year)] = 0
#     print('district format=={}'.format(districts[str(county_arr_idx)]))
#     for cnty in placement_county_districts[county_arr_idx]:
#         for year in year_range:
#             try:
#                 districts[str(county_arr_idx)][str(year)] += county_juvy_populations.loc[idx[cnty,year],:]['Total']
#                 print(county_juvy_populations.loc[idx[cnty,year],:]['Total'])
#             except:
#                 xx=0#blorp
# df = pd.DataFrame(districts)
# print(df.head(1))
# print(df)
        #print('found county[{}:{}] in arr:{}'.format(county,district_num,str(placement_county_districts[district_num])))
#print('{} county num = {}'.format(county,district_num))
#print(placement_data.loc[idx[year_tup[0]:year_tup[1],district_num+1], :].head(2))

# for row,new_df in placement_data.groupby(level=[0,1]):
#     #print(row,new_df.head(1))
#     print('row='.format(row))
#     if str(row[1]) not in district_populations:
#         district_populations[str(row[1])] = 0
#     else:
#         #district_populations[str(row[1])] = total_arrests[str(row[1])]+new_df['Total Incidents'][0]
#         #district_populations[str(row[1])] = 0
#         print(placement_county_districts[row[1]])
#         for cnty2 in placement_county_districts[row[1]]:
#             print(cnty2)
#     print(district_populations)
# total_arrests = {}
# for row,new_df in juvenile_arrests.groupby(level=[0,1]):
#     if str(row[1]) not in total_arrests:
#         total_arrests[str(row[1])] = new_df['Total Incidents'][0]
#     else:
#         total_arrests[str(row[1])] = total_arrests[str(row[1])]+new_df['Total Incidents'][0]
# state_totals = []
# for key in total_arrests:
#     #print("Year:{}-Totals:{}-StatePop:{}".format(key,state_totals[key],pop[key].sum()))
#     state_totals.append({'Year':int(key),'Total Incidents':total_arrests[key],'Population 11-20':pop[key].sum()})
# #print(str(state_totals))
# df = pd.DataFrame(state_totals)
# df['Rate']=(df['Total Incidents']/df['Population 11-20'])*10000
# df['Rate']=df['Rate'].round(2)



# In[ ]:


#sch = dfu.getSchool()
#print(sch['Expulsion - Services not provided'])
# print(sch.head())
# demo = dfu.getDemographic_By_AgeGroup()
# print(demo.head())
# print(demo[demo['Age Range']=='11-17'].head())
# demo.loc[idx['Albany','2014':'2016'],:].transpose()
# demo[demo['Age Range']=='11-17'].loc[idx['Albany','2014':'2016'],:].transpose()
# #print(demo[demo['Age Range']=='18-20']['Total'])
# juvy_arrest = dfu.getORIData(demo)
# juvy_arrest[['Population','Rate']].head()


# In[ ]:


#print(df.head(1))
#display(HTML(demographic_data.loc[idx[county,year_tup[0]:year_tup[1]]].to_html()))
#county = 'Albany'
#year_tup = (2012,2013)
#df.loc[idx[county,:,year_tup[0]:year_tup[1]],:].transpose()

# overview = dfunct.getOverview()
# dfs = dfunct.getDFS()#afcars, county, plc
# school = dfunct.getSchool()
# #school['County'] = school['DISTRICT_NAME'].str.split('#').str[0]
# index_crimes = dfunct.getIndexCrimes()#DO NOT USE THIS! replaced by ori data
# juvenile_arrests = dfunct.getORIData()


# In[ ]:


#set(school.index.levels[0])


# In[ ]:


#pd.core.strings.str_strip(school[0])
# school_indx = [x.strip() for x in school.index.get_level_values(0).unique()]
# school.index.set_levels(school_indx, level='county', inplace=True)
# school


# In[ ]:


# dfunct = DataFunctions()
# idx = pd.IndexSlice
# import numpy as np

# juvenile_arrests = dfunct.getORIData()
# pop = dfunct.getPopulationData()
# print(pop.head(3))

# print('*************')
# county = 'Albany'
# year_tup = (2014,2016)
# county_population = pop.loc[idx[county],:]
# print(juvenile_arrests.head(3))
# county_arrests = juvenile_arrests.loc[idx[county,year_tup[0]:year_tup[1]], :]
# print('*************')
# juvenile_arrests['total'] = juvenile_arrests.sum(axis=1)

# print('*************COUNTY ARRESTS')
# print(county_arrests)

# pops = []
# for row,new_df in juvenile_arrests.groupby(level=[0,1]):
#     #print(new_df)
#     print(type(row))
#     print(row[0])
#     #print(pop[row[0]][pop.get_loc(row[1])])
#     print(pop.loc[row[0],str(row[1])])
#     pops.append(pop.loc[row[0],str(row[1])])
# juvenile_arrests['population']=pops
# juvenile_arrests['rate'] = juvenile_arrests['total']/juvenile_arrests['population']
# print(juvenile_arrests.head(3))
