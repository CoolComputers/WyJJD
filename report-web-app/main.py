from GetDataFunctions import COUNTIES, BEGIN_YEAR, END_YEAR
from county_snapshot_tables import *

import flask
app = flask.Flask(__name__)

# from flask import Flask
# app = Flask(__name__)

#show county snapshot report
@app.route("/county_snapshot", methods=['GET', 'POST'])
def show_county_snapshot():
    if flask.request.method == 'GET':#show default page
        county = 'Albany'
        year_tup = (2014,2015)
    else:#show page based off user input
        #test if beginyear<endyear
        county = ''
        year_tup = ('','')

    return flask.render_template("county_snapshot_report.html",
                            counties=COUNTIES,
                            begin_year=BEGIN_YEAR,
                            end_year=END_YEAR,
                            ori_county_arrest_df=display_felony_html(county,year_tup))

#show state cloropleth graphs
@app.route("/state_graphical")
def show_state_graphical():
    return "Hello World!"
