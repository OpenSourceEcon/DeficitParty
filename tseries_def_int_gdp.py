
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
from bokeh.models.tickers import SingleIntervalTicker

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(cur_path, 'data')
deficit_data_path = os.path.join(data_dir,
                                 'Mar21-Data-Underlying-Figures.xlsx')
images_dir = os.path.join(cur_path, 'images')

#Pull data from Excel Sheet "Mar21-Data-Underlying-Figures.xlsx"
deficit_dataframe = pd.read_excel(deficit_data_path,
                                  sheet_name=2,
                                  usecols="A:D",
                                  nrows=46,
                                  dtype={'A': np.int64, 'B': np.float64,
                                         'C': np.float64, 'D': np.float64},
                                  skiprows=7)
deficit_dataframe.rename(columns={'Unnamed: 0':'Year'}, inplace=True)
deficit_cds = ColumnDataSource(deficit_dataframe)

#Create Variables for min and max values
data_length = len(deficit_dataframe['Year'])
min_year = deficit_dataframe['Year'].min()
max_year = deficit_dataframe['Year'].max()
min_deficit = deficit_dataframe['Total Deficit'].min()
max_deficit = deficit_dataframe['Total Deficit'].max()

#Output to HTML file titled: "federal_debt_image.html"
fig_title = 'Total Deficits, Primary Deficits, and Net Interest: 2006-2051'
fig_path = os.path.join(images_dir, 'tseries_def_int_gdp.html')
output_file(fig_path, title=fig_title)

#Create a figure with '% of GDP' as Y-axis and year as X-axis
fig = figure(title=fig_title,
             plot_height=600,
             plot_width=1200,
             x_axis_label='Year',
             x_range=(min_year - 0.5, max_year + 0.5),
             y_axis_label='Percent of Gross Domestic Product',
             y_range=(min_deficit - 2, max_deficit + 5),
             toolbar_location=None)

# Set title font size
fig.title.text_font_size = '20pt'

#Modify tick intervals for X-axis and Y-axis
fig.xaxis.ticker=SingleIntervalTicker(interval=5, num_minor_ticks=5)
fig.xgrid.ticker=SingleIntervalTicker(interval=5)
fig.yaxis.ticker=SingleIntervalTicker(interval=3, num_minor_ticks=3)
fig.ygrid.ticker=SingleIntervalTicker(interval=3)

#Plotting data
fig.segment(x0=-3000, y0=0, x1=3000, y1=0, color='gray', line_width=4)
bar_width=0.5
#Bar graph for Net Interest
fig.vbar(x='Year', top='Primary Deficit', bottom='Total Deficit',
         source=deficit_cds, width=bar_width, fill_color='#6C9CB2',
         legend_label='Net Interest')
#Bar Graph for Primary Deficit
fig.vbar(x='Year', top='Primary Deficit', source=deficit_cds, width=bar_width,
         fill_color='#7D386E', legend_label='Primary Deficit')
#Line for Total Deficit
fig.line(x='Year', y='Total Deficit', source=deficit_cds, color='#5D1950',
         line_width=5, legend_label='Total Deficit')
fig.segment(x0=2020.5, y0=min_deficit-100, x1=2020.5, y1=max_deficit + 100,
            color='gray', line_dash='6 2', line_width=2)
label_temp = Label(x=2021, y=1.5, x_units='data', y_units='data',
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
fig.add_layout(Title(text='Source: Congressional Budget Office, ' +
                          'Richard W. Evans (@RickEcon), ' +
                          'historical data from FRED FYFSGDA188S series. ' +
                          'CBO forecast values from CBO extended baseline ' +
                          'forecast of Revenues Minus Total Spending ' +
                          '(Mar. 2021).',
                     align='center',
                     text_font_size='3mm',
                     text_font_style='italic'),
               'below')

#Display the generated figure
show(fig)
