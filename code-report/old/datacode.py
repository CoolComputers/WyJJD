#basic functions for retrieving data, to be imported into the notebooks
import csv
import numpy as np
import pandas as pd
import os, sys
import subprocess
import base64 #for createdownloadlink

data_folder = '../new-data/'
dci_data_folder = data_folder+'DCI/all-combined/'
dfs_afcars_data_file = data_folder+'DFS/DFS_12-16-AFCARS-CLEAN.csv'
dfs_county_data_file = data_folder+'DFS/DFS_12-16-Placements-ByCounty-CLEAN.csv'
dfs_plc_data_file = data_folder+'DFS/DFS_12-16-Placements-ByPLC-CLEAN.csv'
school_discipline_data_file = data_folder+'school-discipline/SchoolDiscipline_2007-17_Combined-CSV.csv'

#found:https://stackoverflow.com/questions/31893930/download-csv-from-an-ipython-notebook
def create_download_link( df, title = "Download CSV file", filename = "data.csv"):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)
#end found

#Functions to get data frames
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
    return pd.read_csv(school_discipline_data_file,sep=',',header='infer',index_col=0)
