# Import packages
from bokeh.core.property.numeric import Interval
from bokeh.models.annotations import Label, LabelSet
from bokeh.models.tickers import SingleIntervalTicker
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, CDSView, GroupFilter, Title,
                          Legend, HoverTool, NumeralTickFormatter)

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(cur_path, 'data')
debt_data_path = os.path.join(data_dir, '56977-Data-Underlying-Figures.xlsx')
images_dir = os.path.join(cur_path, 'images')


# Pull data from Excel Sheet "Mar21-Data-Underlying-Figures.xlsx"
debt_df = pd.read_excel(debt_data_path,
                        sheet_name=1,
                        usecols="A,B",
                        nrows=152,
                        dtype={'A': np.int64, 'B': np.float64},
                        skiprows=7)
debt_df.rename(columns={'Unnamed: 0':'year','Unnamed: 1':'debt'}, inplace=True)
debt_cds = ColumnDataSource(debt_df)

# Create Variables for min and max values
data_length = len(debt_df['year'])
min_year = debt_df['year'].min()
max_year = debt_df['year'].max()
min_debt = debt_df['debt'].min()
max_debt = debt_df['debt'].max()

# Output to HTML file titled: "federal_debt_image.html"
fig_title = 'U.S. Federal Debt Held by the Public, 1900 to 2051'
fig_path = os.path.join(images_dir, 'tseries_pubdebt_gdp.html')
output_file(fig_path, title=fig_title)

# Create a figure with '% of GDP' as Y-axis and year as X-axis
fig = figure(title=fig_title,
             plot_height=600,
             plot_width=1200,
             x_axis_label='Year',
             x_range=(min_year, max_year),
             y_axis_label='Percent of Gross Domestic Product',
             y_range=(0, max_debt + 20),
             toolbar_location=None)

# Set title font size and axes font sizes
fig.title.text_font_size = '18pt'
fig.xaxis.axis_label_text_font_size = '12pt'
fig.xaxis.major_label_text_font_size = '12pt'
fig.yaxis.axis_label_text_font_size = '12pt'
fig.yaxis.major_label_text_font_size = '12pt'

# Modify tick intervals for X-axis and Y-axis
fig.xaxis.ticker=SingleIntervalTicker(interval=10, num_minor_ticks=0)
fig.xgrid.ticker=SingleIntervalTicker(interval=20)
fig.yaxis.ticker=SingleIntervalTicker(interval=25, num_minor_ticks=0)
fig.ygrid.ticker=SingleIntervalTicker(interval=50)

# Plotting the data line
fig.varea(x='year', y1='debt', y2=0, source=debt_cds, color='#C584DB')
# Vertical line showing start of forecast data
fig.segment(x0=2021, y0=0, x1=2021, y1=300, color='gray', line_dash='6 2',
            line_width=2)

# Labels of significant events
label_temp = Label(x=1915, y=38, x_units='data', y_units='data',
                   text='World War I')
fig.add_layout(label_temp)
label_temp = Label(x=1931.5, y=55, x_units='data', y_units='data', text='Great')
fig.add_layout(label_temp)
label_temp = Label(x=1929, y=48, x_units='data', y_units='data',
                   text='Depression')
fig.add_layout(label_temp)
label_temp = Label(x=1939, y=108, x_units='data', y_units='data',
                   text='World War II')
fig.add_layout(label_temp)
label_temp = Label(x=2005.5, y=78, x_units='data', y_units='data', text='Great')
fig.add_layout(label_temp)
label_temp = Label(x=2003, y=71, x_units='data', y_units='data',
                   text='Recession')
fig.add_layout(label_temp)
label_temp = Label(x=2015.9, y=105, x_units='data', y_units='data',
                   text='Pandemic')
fig.add_layout(label_temp)
label_temp = Label(x=2021.7, y=190, x_units='data', y_units='data',
                   text='Projected')
fig.add_layout(label_temp)

# Add information on hover
tooltips = [ ('Year', '@year'), ('Debt', '@debt{0.0}'+'%')]
hover_glyph = fig.circle(x='year', y='debt', source=debt_cds,size=10, alpha=0,
                         hover_fill_color='gray', hover_alpha=0.5)
fig.add_tools(HoverTool(tooltips=tooltips))

# Turn off scrolling
fig.toolbar.active_drag = None

# Add source text below image
note_text_1 = ('Source: Recreation of Figure 1 from CBO "The 2021 Long-term ' +
               'Budget Outlook", Mar. 4, 2021, using dat from '+
               '56977-Data-Underlying-Figures.xlsx, Richard W. Evans')
caption1 = Title(text=note_text_1, align='left', text_font_size='4mm',
                 text_font_style='italic')
fig.add_layout(caption1, 'below')
note_text_2 = ('   (@RickEcon).')
caption2 = Title(text=note_text_2, align='left', text_font_size='4mm',
                 text_font_style='italic')
fig.add_layout(caption2, 'below')

# Display the generated figure
show(fig)
