from IPython.display import HTML
import pandas as pd
import os, sys
import base64 #for createdownloadlink

##Files
data_folder = '../new-data/'
dci_data_folder = data_folder+'DCI/all-combined/'
dci_index_crimes = dci_data_folder+'index-offenses/'
dfs_afcars_data_file = data_folder+'DFS/DFS_12-16-AFCARS-CLEAN.csv'
dfs_county_data_file = data_folder+'DFS/DFS_12-16-Placements-ByCounty-CLEAN.csv'
dfs_plc_data_file = data_folder+'DFS/DFS_12-16-Placements-ByPLC-CLEAN.csv'
school_discipline_data_file = data_folder+'school-discipline/SchoolDiscipline_2007-17_Combined-CSV2.csv'
ori_data_file = data_folder+'juvenile-arrests/ori_juvenile_arrest_2010-2016_CLEAN.csv'
##End Files

#found:https://stackoverflow.com/questions/31893930/download-csv-from-an-ipython-notebook
def create_download_link( df, title = "Download CSV file", filename = "data.csv"):
    csv1 = df.to_csv()
    b64 = base64.b64encode(csv1.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)
#end found

##Get Data Functs
def getOverview():#DONE
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

def getDFS():
    afcars = pd.read_csv(dfs_afcars_data_file,sep=',',header='infer',index_col=0)
    county = pd.read_csv(dfs_county_data_file,sep=',',header='infer',index_col=0)
    plc = pd.read_csv(dfs_plc_data_file,sep=',',header='infer',index_col=0)
    return afcars, county, plc

def getSchool():
    return pd.read_csv(school_discipline_data_file,sep=',',header='infer')

#fix this to dynamically load files
def getIndexCrimes():
    obj1 = pd.read_csv(dci_index_crimes+'2016-index-cp-after.csv',sep=',',header='infer')
    obj1['year']='2016'
    obj2 = pd.read_csv(dci_index_crimes+'2015-index-cp-after.csv',sep=',',header='infer')
    obj2['year']='2015'
    obj3 = pd.read_csv(dci_index_crimes+'2014-index-cp-after.csv',sep=',',header='infer')
    obj3['year']='2014'
    #newobj = obj['2016']#+obj['2015']+obj['2014']
    newobj = pd.concat([obj1,obj2,obj3])
    return newobj
    #return pd.read_csv(dci_index_crimes+'2016-index-cp-after.csv',sep=',',header='infer')

def getORIData():
    return pd.read_csv(ori_data_file,sep=',',header='infer')
