
# Import packages
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, CDSView, GroupFilter, Title,
                          Legend, HoverTool)
from bokeh.models.annotations import Label, LabelSet

#Pull data from Excel Sheet "Mar21-Data-Underlying-Figures.xlsx"
deficit_dataframe = pd.read_excel('data\Mar21-Data-Underlying-Figures.xlsx',
                                  sheet_name=2,
                                  usecols="A:D",
                                  nrows=46,
                                  dtype={'A':np.int64, 'B':np.float64,'C':np.float64,'D':np.float64},
                                  skiprows=7)
deficit_dataframe.rename(columns={'Unnamed: 0':'Year'},inplace=True)
deficit_cds = ColumnDataSource(deficit_dataframe)

#Create Variables for min and max values
data_length = len(deficit_dataframe['Year'])
min_year = deficit_dataframe['Year'].min()
max_year = deficit_dataframe['Year'].max()
min_deficit = deficit_dataframe['Total Deficit'].min()
max_deficit = deficit_dataframe['Total Deficit'].max()

#Output to HTML file titled: "federal_debt_image.html"
fig_title = 'Total Deficits, Primary Deficits, and Net Interest'
output_file('images/deficit_interest_image.html', title=fig_title)

#Create a figure with '% of GDP' as Y-axis and year as X-axis
fig = figure(title=fig_title,
             plot_height=600,
             plot_width=1200,
             x_axis_label='Year',
             x_range=(min_year-0.5,max_year+0.5),
             y_axis_label='Percent of Gross Domestic Product',
             y_range=(min_deficit-5,max_deficit+5),
             toolbar_location=None)

#Plotting data
fig.segment(x0=-3000, y0=0, x1=3000, y1=0, color='gray', line_width=4)
bar_width=0.5
#Bar graph for Net Interest
fig.vbar(x='Year', top='Primary Deficit', bottom='Total Deficit',
         source=deficit_cds, width=bar_width, fill_color='#758CE0',
         legend_label='Net Interest')
#Bar Graph for Primary Deficit
fig.vbar(x='Year', top='Primary Deficit', source=deficit_cds, width=bar_width,
         fill_color='#8463BF', legend_label='Primary Deficit')
#Line for Total Deficit
fig.line(x='Year', y='Total Deficit', source=deficit_cds, color='#68417D',
         line_width=5, legend_label='Total Deficit')
fig.segment(x0=2020.5, y0=min_deficit-100, x1=2020.5, y1=max_deficit + 100,
            color='gray', line_dash='6 2', line_width=2)
label_temp = Label(x=2021, y=2.5, x_units='data', y_units='data',
                   text='Projected')
fig.add_layout(label_temp)

#Add legend
fig.legend.location = 'bottom_left'

#Add information on hover
tooltips = [ ('Year', '@Year'),
             ('Primary Deficit', '@{Primary Deficit}{0.0}'+'%'),
             ('Net Interest', '@{Net Interest}{0.0}'+'%'),
             ('Total Deficit', '@{Total Deficit}{0.0}'+'%')]
hover_glyph = fig.circle(x='Year', y='Total Deficit', source=deficit_cds,
                         size=10, alpha=0, hover_fill_color='gray',
                         hover_alpha=0.5)
fig.add_tools(HoverTool(tooltips=tooltips))

#Turn off scrolling
fig.toolbar.active_drag = None

#Add source text below image
fig.add_layout(Title(text='Source: Congressional Budget Office,' +
                          'Richard W. Evans (@RickEcon), ' +
                          'historical data from FRED FYFSGDA188S series. ' +
                          'CBO forecast values from CBO extended baseline ' +
                          'forecast of Revenues Minus Total Spending ' +
                          '(Sep. 2020).',
                     align='left',
                     text_font_size='3mm',
                     text_font_style='italic'),
               'below')

#Display the generated figure
show(fig)
