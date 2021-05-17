'''
This graphs the federal debt held by the public as a percentage of GDP from
1900 to 2021, then adds the CBO extended baseline forecast from 2022 to 2050
from the most recent Long-Term Budget Outlook report.

This module defines the following function(s):
'''

'''
Steps:
    Read in data from the csv
    make sure data is printing to console
    graph data to simple line
    add in pretty lines and colors
    add annotations
    try to find data from web
'''
# Import packages
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Title, Legend, HoverTool

#Pull data from 
deficit_gdp = pd.read_csv('data\deficit_gdp.csv',
                            dtype = {'Year': 'int64', 'deficit_gdp': 'float64','cbo_forecast': 'int64'},
                            skiprows=3)
deficit_gdp_cds = ColumnDataSource(deficit_gdp)

data_length = len(deficit_gdp['Year'])
min_year = deficit_gdp['Year'].min()
max_year = deficit_gdp['Year'].max()
percent_gdp_list = []
for x in range(0,data_length):
    #print(deficit_gdp['deficit_gdp'][x])
    if deficit_gdp['deficit_gdp'][x] > 0:
        percent_gdp_list.append(deficit_gdp['deficit_gdp'][x]*10)
    else:
        percent_gdp_list.append(deficit_gdp['deficit_gdp'][x]*-10)
    print(percent_gdp_list[x])
deficit_gdp_cds.add(percent_gdp_list,"gdp_percent")

#Output to HTML file titled: "federal_debt_image.html"
fig_title = 'Federal Debt Held by the Public, 1900 to 2051'
output_file('images/federal_debt_image.html', title=fig_title)

#Create a figure with '% of GDP' as Y-axis and year as X-axis
fig = figure(title=fig_title,
             plot_height=600, 
             plot_width=1200,
             x_axis_label='Year', 
             x_range=(min_year,max_year),
             y_axis_label='Percent of Gross Domestic Product',
             y_range=(0,225),
             toolbar_location='right')
major_tick_labels = ['1930', '1945', '1960', '1980', '2000', '2008', '2020','2035', '2050']
major_tick_list = [1930, 1945, 1960, 1980, 2000, 2008, 2020, 2035, 2050]


#Plotting the line
fig.line(   x='Year',
            y='gdp_percent',
            source=deficit_gdp_cds,
            color='gray',
            line_width=1)
fig.segment(x0=2021, y0=0,x1=2021,y1=300,color='gray',line_width=3)

#Add source text below image
fig.add_layout(Title(text='Source: Richard W. Evans (@RickEcon), ' +
                          'historical data from FRED FYFSGDA188S series. ' +
                          'CBO forecast values from CBO extended baseline ' +
                          'forecast of Revenues Minus Total Spending ' +
                          '(Sep. 2020).',
                        align='left',
                        text_font_size='3mm',
                        text_font_style='italic'),
                'below')
#fig.legend.click_policy = 'mute'

#Display the generated figure
show(fig)