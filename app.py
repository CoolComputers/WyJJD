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
        selected_begin = 2014
        selected_end = 2016
        year_tup = (selected_begin,selected_end)
    else:#show page based off user input
        #test if beginyear<endyear
        post_data = flask.request.form
        county = str(post_data['select_county'])
        selected_begin = int(post_data['select_year_begin'])
        selected_end = int(post_data['select_year_end'])
        year_tup = (selected_begin,selected_end)

    return flask.render_template("county_snapshot_report.html",
                            selected_begin_year=selected_begin,
                            selected_end_year=selected_end,
                            option_counties=COUNTIES,
                            option_begin_year=int(BEGIN_YEAR),
                            option_end_year=int(END_YEAR),
                            ori_county_arrest_df=display_felony_html(county,year_tup),
                            lesser_offenses_df=display_lesser_html(county,year_tup),
                            crime_rate_df=county_crime_rate(county,year_tup),
                            case_counts_df=display_case_counts_html(county,year_tup),
                            state_crime_rate_df=state_crime_rate(county,year_tup),
                            age_group_demographic_df=agegroup_demographic(county,year_tup),
                            placements_df=display_placements_html(county,year_tup),
                            county_placement_rates_df=display_county_placements_rates_html(county,year_tup),
                            state_placement_rates_df=display_state_placements_rates_html(county,year_tup),
                            county_df=display_county_html(county,year_tup),
                            school_discipline_df=display_school_html(county,year_tup))

#show state cloropleth graphs
@app.route("/state_graphical")
def show_state_graphical():
    return "Hello World!"


if __name__ == '__main__':
   app.run(debug = False)
