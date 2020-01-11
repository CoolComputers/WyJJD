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
#census_folder = data_folder+'census-info/'
#population_data_file = census_folder+'census-factfinder/census-cleaned.csv'
population_agegroup_data_file = data_folder+'ojjdp/population-data/population_agegroup_ethnicity.csv'
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

    def getJudicialPlacementData(self):
        df = pd.read_csv(placements_data_file,sep=',',header='infer',index_col=['Year','district'])
        df.sort_index(level=[0,1],ascending=[1,1],inplace=True)
        df=df.groupby(level=[0, 1]).sum()

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
