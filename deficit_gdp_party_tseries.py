# Import packages
from bokeh.core.property.numeric import Interval
from bokeh.models.annotations import Label, LabelSet
from bokeh.models.glyphs import VArea
from bokeh.models.tickers import SingleIntervalTicker
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, Title, Legend, HoverTool,
                          NumeralTickFormatter)
from bokeh.models.widgets import Tabs, Panel

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(cur_path, 'data')
party_data_path = os.path.join(data_dir, 'deficit_party_data.csv')
recession_data_path = os.path.join(data_dir, 'recession_data.csv')
images_dir = os.path.join(cur_path, 'images')

'''
-------------------------------------------------------------------------------
Create pandas DataFrames and Column Data Source data objects
-------------------------------------------------------------------------------
'''
# Create recession data column data source object
recession_df = pd.read_csv(recession_data_path, parse_dates=['Peak','Trough'])
recession_cds = ColumnDataSource(recession_df)

# Reading data from CVS (deficit_party_data.csv)
main_df = pd.read_csv(party_data_path,
                      dtype={'Year': np.int64,
                             'deficit_gdp': np.float64,
                             'receipts_gdp': np.float64,
                             'spend_int_gdp': np.float64,
                             'spend_nonint_gdp': np.float64,
                             'spend_tot_gdp': np.float64,
                             'president': 'str',
                             'president_party': 'str',
                             'congress_number': np.int64,
                             'congress_session': np.int64,
                             'dem_whitehouse': np.int64,
                             'dem_senateseats': np.int64,
                             'rep_senateseats': np.int64,
                             'other_senateseats': np.int64,
                             'total_senateseats': np.int64,
                             'dem_houseseats': np.int64,
                             'rep_houseseats': np.int64,
                             'other_houseseats': np.int64,
                             'total_houseseats': np.int64},
                      skiprows=3)

# Create entire time series column data source
main_cds = ColumnDataSource(main_df)

# Create Full control (WH + Sen + HouseRep) Republican control elements
deficit_cntrl_all_rep_df = \
    main_df[(main_df['president_party'] == 'Republican') &
            (main_df['rep_senateseats'] >=
             0.5 * main_df['total_senateseats']) &
            (main_df['rep_houseseats'] >=
             0.5 * main_df['total_houseseats'])]
dfct_cntrl_all_rep_cds = ColumnDataSource(deficit_cntrl_all_rep_df)

# Create Full control (WH + Sen + HouseRep) Democrat control elements
deficit_cntrl_all_dem_df = \
    main_df[(main_df['president_party'] == 'Democrat') &
            (main_df['dem_senateseats'] >=
             0.5 * main_df['total_senateseats']) &
            (main_df['dem_houseseats'] >=
             0.5 * main_df['total_houseseats'])]
dfct_cntrl_all_dem_cds = ColumnDataSource(deficit_cntrl_all_dem_df)

# Create Full control (WH + Sen + HouseRep) split control elements
deficit_cntrl_all_split_df = \
    main_df[((main_df['president_party'] == 'Republican') &
             ((main_df['rep_senateseats'] <
               0.5 * main_df['total_senateseats']) |
              (main_df['rep_houseseats'] <
               0.5 * main_df['total_houseseats']))) |
            ((main_df['president_party'] == 'Democrat') &
             ((main_df['dem_senateseats'] <
               0.5 * main_df['total_senateseats']) |
              (main_df['dem_houseseats'] <
               0.5 * main_df['total_houseseats'])))]
dfct_cntrl_all_split_cds = ColumnDataSource(deficit_cntrl_all_split_df)

# Create Senate control (WH + Sen) Republican control elements
deficit_cntrl_whsen_rep_df = \
    main_df[(main_df['president_party'] == 'Republican') &
            (main_df['rep_senateseats'] >=
             0.5 * main_df['total_senateseats'])]
dfct_cntrl_whsen_rep_cds = ColumnDataSource(deficit_cntrl_whsen_rep_df)

# Create Senate control (WH + Sen) Democrat control elements
deficit_cntrl_whsen_dem_df = \
    main_df[(main_df['president_party'] == 'Democrat') &
            (main_df['dem_senateseats'] >=
             0.5 * main_df['total_senateseats'])]
dfct_cntrl_whsen_dem_cds = ColumnDataSource(deficit_cntrl_whsen_dem_df)

# Create Senate control (WH + Sen) split control elements
deficit_cntrl_whsen_split_df = \
    main_df[((main_df['president_party'] == 'Republican') &
             (main_df['rep_senateseats'] <
              0.5 * main_df['total_senateseats'])) |
            ((main_df['president_party'] == 'Democrat') &
             (main_df['dem_senateseats'] <
              0.5 * main_df['total_senateseats']))]
dfct_cntrl_whsen_split_cds = ColumnDataSource(deficit_cntrl_whsen_split_df)

# Create House control (WH + HouseRep) Republican control elements
deficit_cntrl_whhou_rep_df = \
    main_df[(main_df['president_party'] == 'Republican') &
            (main_df['rep_houseseats'] >=
             0.5 * main_df['total_houseseats'])]
dfct_cntrl_whhou_rep_cds = ColumnDataSource(deficit_cntrl_whhou_rep_df)

# Create House control (WH + HouseRep) Democrat control elements
deficit_cntrl_whhou_dem_df = \
    main_df[(main_df['president_party'] == 'Democrat') &
            (main_df['dem_houseseats'] >=
             0.5 * main_df['total_houseseats'])]
dfct_cntrl_whhou_dem_cds = ColumnDataSource(deficit_cntrl_whhou_dem_df)

# Create House control (WH + HouseRep) split control elements
deficit_cntrl_whhou_split_df = \
    main_df[((main_df['president_party'] == 'Republican') &
             (main_df['rep_houseseats'] <
              0.5 * main_df['total_houseseats'])) |
            ((main_df['president_party'] == 'Democrat') &
             (main_df['dem_houseseats'] <
              0.5 * main_df['total_houseseats']))]
dfct_cntrl_whhou_split_cds = ColumnDataSource(deficit_cntrl_whhou_split_df)

# Create Variables for min and max values
data_length = len(main_df['Year'])
recession_data_length = len(recession_df['Peak'])
min_year = main_df['Year'].min()
max_year = main_df['Year'].max()
min_deficit = main_df['deficit_gdp'].min()
max_deficit = main_df['deficit_gdp'].max()

# Output to HTML file titled: "federal_debt_image.html"
fig_title = ('U.S. Federal Surplus (+) or Deficit (-) as Percent of Gross ' +
             'Domestic Product by Party Control: 1929-2020')
fig_path = os.path.join(images_dir, 'deficit_gdp_party_tseries.html')
output_file(fig_path, title=fig_title)

'''
-------------------------------------------------------------------------------
Create full control party control definition figure
-------------------------------------------------------------------------------
'''

# Create a figure with '% of GDP' as Y-axis and year as X-axis
fig_all = figure(title=fig_title,
                 plot_height=600,
                 plot_width=1200,
                 x_axis_label='Year',
                 x_range=(min_year - 1, max_year + 1),
                 y_axis_label='Percent of Gross Domestic Product',
                 y_range=(min_deficit - 3, max_deficit + 3),
                 toolbar_location=None)

# Set title font size and axes font sizes
fig_all.title.text_font_size = '17pt'
fig_all.xaxis.axis_label_text_font_size = '12pt'
fig_all.xaxis.major_label_text_font_size = '12pt'
fig_all.yaxis.axis_label_text_font_size = '12pt'
fig_all.yaxis.major_label_text_font_size = '12pt'

# Modify tick intervals for X-axis and Y-axis
fig_all.xaxis.ticker=SingleIntervalTicker(interval=10, num_minor_ticks=2)
fig_all.xgrid.ticker=SingleIntervalTicker(interval=10)
fig_all.yaxis.ticker=SingleIntervalTicker(interval=5, num_minor_ticks=5)
fig_all.ygrid.ticker=SingleIntervalTicker(interval=5)

# Create recession bars
for x in range(0,recession_data_length):
    peak_year = recession_df['Peak'][x].year
    trough_year = recession_df['Trough'][x].year
    if(peak_year >= min_year and trough_year >= min_year):
        fig_all.patch(x=[peak_year, trough_year, trough_year,peak_year],
                      y=[-100, -100, max_deficit + 10, max_deficit + 10],
                      fill_color='gray',
                      fill_alpha=0.4,
                      line_width=0,
                      legend_label='Recession')
    if(peak_year == trough_year and peak_year >= min_year and
       trough_year >= min_year):
        fig_all.patch(x=[peak_year, trough_year + 1, trough_year + 1,
                         peak_year],
                      y=[-100, -100, max_deficit + 10, max_deficit + 10],
                      fill_color='gray',
                      fill_alpha=0.4,
                      line_width=0,
                      legend_label='Recession')

# Plotting the line and scatter point circles
fig_all.line(x='Year', y='deficit_gdp', source=main_cds, color='#423D3C',
             line_width=2)

fig_all.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_all_rep_cds,
               size=10, line_width=1, line_color='black', fill_color='red',
               alpha=0.7, muted_alpha=0.2, legend_label='Republican control')

fig_all.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_all_dem_cds,
               size=10, line_width=1, line_color='black', fill_color='blue',
               alpha=0.7, muted_alpha=0.2, legend_label='Democrat control')

fig_all.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_all_split_cds,
               size=10, line_width=1, line_color='black', fill_color='green',
               alpha=0.7, muted_alpha=0.2, legend_label='Split control')

# Add information on hover
tooltips = [('Year', '@Year'),
            ('Deficit over GDP', '@deficit_gdp{0.0}'+'%'),
            ('President','@president'),
            ('White House', '@president_party'),
            ('Rep. House Seats', '@rep_houseseats'),
            ('Dem. House Seats', '@dem_houseseats'),
            ('Rep. Senate Seats', '@rep_senateseats'),
            ('Dem. Senate Seats', '@dem_senateseats')]
hover_glyph = fig_all.circle(x='Year', y='deficit_gdp', source=main_cds,
                             size=10, alpha=0, hover_fill_color='gray',
                             hover_alpha=0.5)
fig_all.add_tools(HoverTool(tooltips=tooltips))

#Turn off scrolling
fig_all.toolbar.active_drag = None

#Add legend
fig_all.legend.location = 'bottom_center'
fig_all.legend.border_line_width = 2
fig_all.legend.border_line_color = 'black'
fig_all.legend.border_line_alpha = 1
fig_all.legend.label_text_font_size = '4mm'

#Set legend muting click policy
fig_all.legend.click_policy = 'mute'

#Add notes below image
note_text_all_1 = \
    ('Note: Republican control in a given year is defined as the President ' +
     'being Republican and Republicans holding at least half of Senate ' +
     'seats (50 or more) and at least')
caption_all_1 = Title(text=note_text_all_1, align='left', text_font_size='4mm',
                      text_font_style='italic')
fig_all.add_layout(caption_all_1, 'below')
note_text_all_2 = \
    ('   half of House seats (usually 217 or more) for the majority of that ' +
     'year. Democrat control is defined as the President being Democrat and ' +
     'Democrats holding at least')
caption_all_2 = Title(text=note_text_all_2, align='left', text_font_size='4mm',
                      text_font_style='italic')
fig_all.add_layout(caption_all_2, 'below')
note_text_all_3 = \
    ('   half of the Senate seats and at least half of the House seats for ' +
     'the majority of that year. Split government is defined as one party ' +
     'holding the White House while')
caption_all_3 = Title(text=note_text_all_3, align='left', text_font_size='4mm',
                      text_font_style='italic')
fig_all.add_layout(caption_all_3, 'below')
note_text_all_4 = \
    ('   either not holding a majority of Senate seates or not holding a ' +
     'majority of House seats.')
caption_all_4 = Title(text=note_text_all_4, align='left', text_font_size='4mm',
                      text_font_style='italic')
fig_all.add_layout(caption_all_4, 'below')
note_text_all_5 = \
    ('Source: Federal Reserve Economic Data (FRED, FYFRGDA188S), United ' +
     'States House of Representatives History, Art, & Archives, "Party ' +
     'Divisions of the House of')
caption_all_5 = Title(text=note_text_all_5, align='left', text_font_size='4mm',
                      text_font_style='italic')
fig_all.add_layout(caption_all_5, 'below')
note_text_all_6 = \
    ('   Representatives, 1789 to present", ' +
     'https://history.house.gov/Institution/Party-Divisions/' +
     'Party-Divisions/, Richard W. Evans (@rickecon).')
caption_all_6 = Title(text=note_text_all_6, align='left', text_font_size='4mm',
                      text_font_style='italic')
fig_all.add_layout(caption_all_6, 'below')

'''
-------------------------------------------------------------------------------
Create Senate control party control definition figure
-------------------------------------------------------------------------------
'''

# Create a figure with '% of GDP' as Y-axis and year as X-axis
fig_whsen = figure(title=fig_title,
                   plot_height=600,
                   plot_width=1200,
                   x_axis_label='Year',
                   x_range=(min_year - 1, max_year + 1),
                   y_axis_label='Percent of Gross Domestic Product',
                   y_range=(min_deficit - 3, max_deficit + 3),
                   toolbar_location=None)

# Set title font size and axes font sizes
fig_whsen.title.text_font_size = '17pt'
fig_whsen.xaxis.axis_label_text_font_size = '12pt'
fig_whsen.xaxis.major_label_text_font_size = '12pt'
fig_whsen.yaxis.axis_label_text_font_size = '12pt'
fig_whsen.yaxis.major_label_text_font_size = '12pt'

# Modify tick intervals for X-axis and Y-axis
fig_whsen.xaxis.ticker=SingleIntervalTicker(interval=10, num_minor_ticks=2)
fig_whsen.xgrid.ticker=SingleIntervalTicker(interval=10)
fig_whsen.yaxis.ticker=SingleIntervalTicker(interval=5, num_minor_ticks=5)
fig_whsen.ygrid.ticker=SingleIntervalTicker(interval=5)

# Create recession bars
for x in range(0,recession_data_length):
    peak_year = recession_df['Peak'][x].year
    trough_year = recession_df['Trough'][x].year
    if(peak_year >= min_year and trough_year >= min_year):
        fig_whsen.patch(x=[peak_year, trough_year, trough_year,peak_year],
                        y=[-100, -100, max_deficit + 10, max_deficit + 10],
                        fill_color='gray',
                        fill_alpha=0.4,
                        line_width=0,
                        legend_label='Recession')
    if(peak_year == trough_year and peak_year >= min_year and
       trough_year >= min_year):
        fig_whsen.patch(x=[peak_year, trough_year + 1, trough_year + 1,
                           peak_year],
                        y=[-100, -100, max_deficit + 10, max_deficit + 10],
                        fill_color='gray',
                        fill_alpha=0.4,
                        line_width=0,
                        legend_label='Recession')

# Plotting the line and scatter point circles
fig_whsen.line(x='Year', y='deficit_gdp', source=main_cds, color='#423D3C',
               line_width=2)

fig_whsen.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_whsen_rep_cds,
                 size=10, line_width=1, line_color='black', fill_color='red',
                 alpha=0.7, muted_alpha=0.2, legend_label='Republican control')

fig_whsen.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_whsen_dem_cds,
                 size=10, line_width=1, line_color='black', fill_color='blue',
                 alpha=0.7, muted_alpha=0.2, legend_label='Democrat control')

fig_whsen.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_whsen_split_cds,
                 size=10, line_width=1, line_color='black', fill_color='green',
                 alpha=0.7, muted_alpha=0.2, legend_label='Split control')

# Add information on hover
tooltips = [('Year', '@Year'),
            ('Deficit over GDP', '@deficit_gdp{0.0}'+'%'),
            ('President','@president'),
            ('White House', '@president_party'),
            ('Rep. House Seats', '@rep_houseseats'),
            ('Dem. House Seats', '@dem_houseseats'),
            ('Rep. Senate Seats', '@rep_senateseats'),
            ('Dem. Senate Seats', '@dem_senateseats')]
hover_glyph = fig_whsen.circle(x='Year', y='deficit_gdp', source=main_cds,
                               size=10, alpha=0, hover_fill_color='gray',
                               hover_alpha=0.5)
fig_whsen.add_tools(HoverTool(tooltips=tooltips))

#Turn off scrolling
fig_whsen.toolbar.active_drag = None

#Add legend
fig_whsen.legend.location = 'bottom_center'
fig_whsen.legend.border_line_width = 2
fig_whsen.legend.border_line_color = 'black'
fig_whsen.legend.border_line_alpha = 1
fig_whsen.legend.label_text_font_size = '4mm'

#Set legend muting click policy
fig_whsen.legend.click_policy = 'mute'

#Add notes below image
note_text_whsen_1 = \
    ('Note: Republican control in a given year is defined as the President ' +
     'being Republican and Republicans holding at least half of the Senate ' +
     'seats (50 or more) for the')
caption_whsen_1 = Title(text=note_text_whsen_1, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whsen.add_layout(caption_whsen_1, 'below')
note_text_whsen_2 = \
    ('   majority of that year. Democrat control is defined as the ' +
     'President being Democrat and Democrats holding at least half of the ' +
     'Senate seats for the majority of that')
caption_whsen_2 = Title(text=note_text_whsen_2, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whsen.add_layout(caption_whsen_2, 'below')
note_text_whsen_3 = \
    ('   year. Split government is defined as one party holding the White ' +
     'House while not holding a majority of Senate seats.')
caption_whsen_3 = Title(text=note_text_whsen_3, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whsen.add_layout(caption_whsen_3, 'below')
note_text_whsen_4 = \
    ('Source: Federal Reserve Economic Data (FRED, FYFRGDA188S), United ' +
     'States House of Representatives History, Art, & Archives, "Party ' +
     'Divisions of the House of')
caption_whsen_4 = Title(text=note_text_whsen_4, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whsen.add_layout(caption_whsen_4, 'below')
note_text_whsen_5 = \
    ('   Representatives, 1789 to present", ' +
     'https://history.house.gov/Institution/Party-Divisions/' +
     'Party-Divisions/, Richard W. Evans (@rickecon).')
caption_whsen_5 = Title(text=note_text_whsen_5, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whsen.add_layout(caption_whsen_5, 'below')

'''
-------------------------------------------------------------------------------
Create House of Represenatives control party control definition figure
-------------------------------------------------------------------------------
'''

# Create a figure with '% of GDP' as Y-axis and year as X-axis
fig_whhou = figure(title=fig_title,
                   plot_height=600,
                   plot_width=1200,
                   x_axis_label='Year',
                   x_range=(min_year - 1, max_year + 1),
                   y_axis_label='Percent of Gross Domestic Product',
                   y_range=(min_deficit - 3, max_deficit + 3),
                   toolbar_location=None)

# Set title font size and axes font sizes
fig_whhou.title.text_font_size = '17pt'
fig_whhou.xaxis.axis_label_text_font_size = '12pt'
fig_whhou.xaxis.major_label_text_font_size = '12pt'
fig_whhou.yaxis.axis_label_text_font_size = '12pt'
fig_whhou.yaxis.major_label_text_font_size = '12pt'

# Modify tick intervals for X-axis and Y-axis
fig_whhou.xaxis.ticker=SingleIntervalTicker(interval=10, num_minor_ticks=2)
fig_whhou.xgrid.ticker=SingleIntervalTicker(interval=10)
fig_whhou.yaxis.ticker=SingleIntervalTicker(interval=5, num_minor_ticks=5)
fig_whhou.ygrid.ticker=SingleIntervalTicker(interval=5)

# Create recession bars
for x in range(0,recession_data_length):
    peak_year = recession_df['Peak'][x].year
    trough_year = recession_df['Trough'][x].year
    if(peak_year >= min_year and trough_year >= min_year):
        fig_whhou.patch(x=[peak_year, trough_year, trough_year,peak_year],
                        y=[-100, -100, max_deficit + 10, max_deficit + 10],
                        fill_color='gray',
                        fill_alpha=0.4,
                        line_width=0,
                        legend_label='Recession')
    if(peak_year == trough_year and peak_year >= min_year and
       trough_year >= min_year):
        fig_whhou.patch(x=[peak_year, trough_year + 1, trough_year + 1,
                           peak_year],
                        y=[-100, -100, max_deficit + 10, max_deficit + 10],
                        fill_color='gray',
                        fill_alpha=0.4,
                        line_width=0,
                        legend_label='Recession')

# Plotting the line and scatter point circles
fig_whhou.line(x='Year', y='deficit_gdp', source=main_cds, color='#423D3C',
               line_width=2)

fig_whhou.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_whhou_rep_cds,
                 size=10, line_width=1, line_color='black', fill_color='red',
                 alpha=0.7, muted_alpha=0.2, legend_label='Republican control')

fig_whhou.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_whhou_dem_cds,
                 size=10, line_width=1, line_color='black', fill_color='blue',
                 alpha=0.7, muted_alpha=0.2, legend_label='Democrat control')

fig_whhou.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_whhou_split_cds,
                 size=10, line_width=1, line_color='black', fill_color='green',
                 alpha=0.7, muted_alpha=0.2, legend_label='Split control')

# Add information on hover
tooltips = [('Year', '@Year'),
            ('Deficit over GDP', '@deficit_gdp{0.0}'+'%'),
            ('President','@president'),
            ('White House', '@president_party'),
            ('Rep. House Seats', '@rep_houseseats'),
            ('Dem. House Seats', '@dem_houseseats'),
            ('Rep. Senate Seats', '@rep_senateseats'),
            ('Dem. Senate Seats', '@dem_senateseats')]
hover_glyph = fig_whhou.circle(x='Year', y='deficit_gdp', source=main_cds,
                               size=10, alpha=0, hover_fill_color='gray',
                               hover_alpha=0.5)
fig_whhou.add_tools(HoverTool(tooltips=tooltips))

#Turn off scrolling
fig_whhou.toolbar.active_drag = None

#Add legend
fig_whhou.legend.location = 'bottom_center'
fig_whhou.legend.border_line_width = 2
fig_whhou.legend.border_line_color = 'black'
fig_whhou.legend.border_line_alpha = 1
fig_whhou.legend.label_text_font_size = '4mm'

#Set legend muting click policy
fig_whhou.legend.click_policy = 'mute'

#Add notes below image
note_text_whhou_1 = \
    ('Note: Republican control in a given year is defined as the President ' +
     'being Republican and Republicans holding at least half of the House ' +
     'seats (usually 217 or more)')
caption_whhou_1 = Title(text=note_text_whhou_1, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whhou.add_layout(caption_whhou_1, 'below')
note_text_whhou_2 = \
    ('   for the majority of that year. Democrat control is defined as the ' +
     'President being Democrat and Democrats holding at least half of the ' +
     'House seats for the majority of')
caption_whhou_2 = Title(text=note_text_whhou_2, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whhou.add_layout(caption_whhou_2, 'below')
note_text_whhou_3 = \
    ('   that year. Split government is defined as one party holding the ' +
     'White House while not holding a majority of House seats.')
caption_whhou_3 = Title(text=note_text_whhou_3, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whhou.add_layout(caption_whhou_3, 'below')
note_text_whhou_4 = \
    ('Source: Federal Reserve Economic Data (FRED, FYFRGDA188S), United ' +
     'States House of Representatives History, Art, & Archives, "Party ' +
     'Divisions of the House of')
caption_whhou_4 = Title(text=note_text_whhou_4, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whhou.add_layout(caption_whhou_4, 'below')
note_text_whhou_5 = \
    ('   Representatives, 1789 to present", ' +
     'https://history.house.gov/Institution/Party-Divisions/' +
     'Party-Divisions/, Richard W. Evans (@rickecon).')
caption_whhou_5 = Title(text=note_text_whhou_5, align='left',
                        text_font_size='4mm', text_font_style='italic')
fig_whhou.add_layout(caption_whhou_5, 'below')

'''
-------------------------------------------------------------------------------
Create panels for figure
-------------------------------------------------------------------------------
'''

# Create three panels, one for each definition of party control
cntrl_all_panel_title = 'Full control: (White House + Senate + House of Reps.)'
cntrl_all_panel = Panel(child=fig_all, title=cntrl_all_panel_title)

cntrl_whsen_panel_title = 'Senate control: (White House + Senate)'
cntrl_whsen_panel = Panel(child=fig_whsen, title=cntrl_whsen_panel_title)

cntrl_whhou_panel_title = 'House control: (White House + House of Reps.)'
cntrl_whhou_panel = Panel(child=fig_whhou, title=cntrl_whhou_panel_title)

# Assign the panels to Tabs
tabs = Tabs(tabs=[cntrl_all_panel, cntrl_whsen_panel, cntrl_whhou_panel])

# Display the generated figure
show(tabs)
