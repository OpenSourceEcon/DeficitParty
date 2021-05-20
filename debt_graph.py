# Import packages
from bokeh.models.annotations import Label, LabelSet
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Title, Legend, HoverTool, NumeralTickFormatter

#Pull data from Excel Sheet "Mar21-Data-Underlying-Figures.xlsx"
debt_df = pd.read_excel('data\Mar21-Data-Underlying-Figures.xlsx',
                                sheet_name=1,
                                usecols="A,B",
                                nrows=152,
                                dtype={'A':np.int64, 'B':np.float64},
                                skiprows=7)
debt_df.rename(columns={'Unnamed: 0':'year','Unnamed: 1':'debt'},inplace=True)
debt_cds = ColumnDataSource(debt_df)

#Create Variables for min and max values
data_length = len(debt_df['year'])
min_year = debt_df['year'].min()
max_year = debt_df['year'].max()
min_debt = debt_df['debt'].min()
max_debt = debt_df['debt'].max()

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
             y_range=(0,max_debt+20),
             toolbar_location=None)

#Plotting the data line
fig.varea(x='year',y1='debt',y2=0,source=debt_cds,color='#C584DB')
#Vertical line showing start of forecast data
fig.segment(x0=2021, y0=0,x1=2021,y1=300,color='gray',line_dash = '6 2',line_width=2)

#Labels of significant events
label_temp = Label(x=1915, y=38,
                    x_units='data', y_units='data',
                    text='World War I')
fig.add_layout(label_temp)
label_temp = Label(x=1933, y=55,
                    x_units='data', y_units='data',
                    text='Great')
fig.add_layout(label_temp)
label_temp = Label(x=1929, y=48,
                    x_units='data', y_units='data',
                    text='Depression')
fig.add_layout(label_temp)
label_temp = Label(x=1939, y=108,
                    x_units='data', y_units='data',
                    text='World War II')
fig.add_layout(label_temp)
label_temp = Label(x=2005, y=78,
                    x_units='data', y_units='data',
                    text='Great')
fig.add_layout(label_temp)
label_temp = Label(x=2003, y=71,
                    x_units='data', y_units='data',
                    text='Recession')
fig.add_layout(label_temp)
label_temp = Label(x=2018, y=105,
                    x_units='data', y_units='data',
                    text='Pandemic')
fig.add_layout(label_temp)
label_temp = Label(x=2022, y=190,
                    x_units='data', y_units='data',
                    text='Projected')
fig.add_layout(label_temp)

#Add information on hover
tooltips = [ ('Year', '@year'), ('Debt', '@debt{0.0}'+'%')]
hover_glyph = fig.circle(x='year',y='debt', source=debt_cds,size=10, alpha=0,hover_fill_color='gray', hover_alpha=0.5)
fig.add_tools(HoverTool(tooltips=tooltips))

#Turn off scrolling
fig.toolbar.active_drag = None

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

#Display the generated figure
show(fig)