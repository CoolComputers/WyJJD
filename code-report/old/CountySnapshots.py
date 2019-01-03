
# coding: utf-8
<script>
  function code_toggle() {
    if (code_shown){
      $('div.input').hide('500');
      $('#toggleButton').val('Show Code')
    } else {
      $('div.input').show('500');
      $('#toggleButton').val('Hide Code')
    }
    code_shown = !code_shown
  }

  $( document ).ready(function(){
    code_shown=false;
    $('div.input').hide()
  });
</script>
<form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Code"></form>
# In[1]:


#File:CountySnapshots.ipynb
#Author: Rafer Cooley
#Desc:Generate County Snapshots of Juvenile Data
from ipywidgets import widgets
from ipywidgets import interactive
from IPython.display import display, HTML, clear_output
from pivottablejs import pivot_ui
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import os, sys
import subprocess
import base64 #for createdownloadlink
#import data_functions as dfunct
get_ipython().magic(u'run getdata.ipynb')


# In[2]:


dfunct = DataFunctions()
overview = dfunct.getOverview()
dfs = dfunct.getDFS()#afcars, county, plc
school = dfunct.getSchool()
#school['County'] = school['DISTRICT_NAME'].str.split('#').str[0]
index_crimes = dfunct.getIndexCrimes()#DO NOT USE THIS! replaced by ori data
juvenile_arrests = dfunct.getORIData()
#display(index_crimes.loc[index_crimes['county'].str.upper()=='ALBANY COUNTY TOTALS'])
#new = school[school['DISTRICT_NAME']]
#display(school)
#display(HTML(overview.to_html()))

#violent felony list
violent_felony = ['Manslaughter','Rape','Robbery','Aggravated Assault']


# In[3]:


# print('overview')
# print(overview.head(3))
# print('**********************************')
# print('dfs[0]')
# print(dfs[0].head(3))
# print('**********************************')
# print('dfs[1]')
# print(dfs[1].head(3))
# print('**********************************')
# print('dfs[2]')
# print(dfs[2].head(3))
# print('**********************************')
# print('school')
# print(school.head(3))
# # print('**********************************')
# # print('index_crimes')
# # print(index_crimes.head(3))
# print('**********************************')
# print('juvy arrests')
# print(juvenile_arrests.head(3))


# In[4]:


#Show Data Functions
idx = pd.IndexSlice
def display_dfs_html(county,year_tup):
    try:
        print('Afcars Data')
        #display(HTML(dfs[0].loc[(county,slice(year_tup[0],year_tup[1]))].to_frame().to_html()))
        display(HTML(dfs[0].loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()))
        print('By County')
        display(HTML(dfs[1].loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()))
        #print('PLC Data')
        #display(HTML(dfs[2].loc[dfs[0]['county'].str.upper().contains(county.upper())].to_html()))
    except Exception as e:
        print('Error showing DFS data.'+str(e))
    
def display_arrests_html(county,year_tup):
    try:
        display(HTML(juvenile_arrests.loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()))  
    except Exception as e:
        print('Error showing ORI data.'+str(e))

def display_school_html(county,year_tup):
    try:
        display(HTML(school.loc[idx[county,year_tup[0]:year_tup[1],year_tup[0]:year_tup[1]], :].to_html()))
    except Exception as e:
        print('Error showing School data.'+str(e))

def display_overview_html(county,year_tup):
    try:
        display(HTML(overview.loc[idx[county,year_tup[0]:year_tup[1]], :].to_html()))
    except Exception as e:
        print('Error showing Overview data.'+str(e))


# In[5]:


##Widget Objects
county_drop = widgets.Dropdown(
    options=set(school.index.levels[0].str.strip()),
    description='County:',
    disabled=False,
)

year_slide = widgets.IntRangeSlider(min=2012,max=2017,step=1)
    
##Widget Update Functions
#these have been replaced by interactive_output
#def county_changed(change):
    #plt.close('all')
    #print('county changed to:'+str(change['new'])+'--'+str(county_drop.value))
    #print('year is'+str(year_slide.value[0]))
    #refresh_tables()

#def year_changed(change):
    #plt.close('all')
    #print('changed year'+str(change['new']))
    #refresh_tables()
    
# county_drop.observe(county_changed, names='value')
# year_slide.observe(year_changed,names='value')
##End Update Functs

#Show Widgets
# display(county_drop)
# display(year_slide)

dfs_out = widgets.interactive_output(display_dfs_html,{'county':county_drop,'year_tup':year_slide})
arrests_out = widgets.interactive_output(display_arrests_html,{'county':county_drop,'year_tup':year_slide})
school_out = widgets.interactive_output(display_school_html,{'county':county_drop,'year_tup':year_slide})
#dfs_out = widgets.interactive_output(display_dfs_html,{'county':county_drop,'year_tup':year_slide})

display(widgets.VBox([widgets.HBox([county_drop,year_slide]),dfs_out,arrests_out,school_out]))


# In[6]:


# print('overview')
# print(overview.head(3))
# print('**********************************')
# print('dfs[0]')
# print(dfs[0].head(3))
# print('**********************************')
# print('dfs[1]')
# print(dfs[1].head(3))
# print('**********************************')
# print('dfs[2]')
# print(dfs[2].head(3))
# print('**********************************')
# print('school')
# print(school.head(3))
# print('**********************************')
# print('index_crimes')
# print(index_crimes.head(3))
# print('**********************************')
# print('juvy arrests')
# print(juvenile_arrests.head(3))


# In[7]:


# df = pd.DataFrame({'month': [1, 4, 7, 10],
#                     'year': [2012, 2014, 2013, 2014],
#                     'sale':[55, 40, 84, 31]})
# df.set_index('month')
# #df['4']
# #df.loc(['4','1'])

# df1 = pd.DataFrame(np.random.randn(6,4),
#                     index=list('abcdef'),
#                     columns=list('ABCD'))
# print(df1)
# print(df1.loc['a'][0])

