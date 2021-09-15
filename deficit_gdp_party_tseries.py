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

#Reading data from CVS (deficit_party_data.csv)
deficit_df = pd.read_csv(party_data_path,
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
deficit_cds = ColumnDataSource(deficit_df)

# Create Full control (WH + Sen + HouseRep) Republican control elements
deficit_cntrl_all_rep_df = \
      deficit_df[(deficit_df['president_party'] == 'Republican') &
                 (deficit_df['rep_senateseats'] >=
                  0.5 * deficit_df['total_senateseats']) &
                 (deficit_df['rep_houseseats'] >=
                  0.5 * deficit_df['total_houseseats'])]
dfct_cntrl_all_rep_cds = ColumnDataSource(deficit_cntrl_all_rep_df)

# Create Full control (WH + Sen + HouseRep) Democrat control elements
deficit_cntrl_all_dem_df = \
      deficit_df[(deficit_df['president_party'] == 'Democrat') &
                 (deficit_df['dem_senateseats'] >=
                  0.5 * deficit_df['total_senateseats']) &
                 (deficit_df['dem_houseseats'] >=
                  0.5 * deficit_df['total_houseseats'])]
dfct_cntrl_all_dem_cds = ColumnDataSource(deficit_cntrl_all_dem_df)

# Create Full control (WH + Sen + HouseRep) split control elements
deficit_cntrl_all_split_df = \
      deficit_df[((deficit_df['president_party'] == 'Republican') &
                  ((deficit_df['dem_senateseats'] >=
                    0.5 * deficit_df['total_senateseats']) |
                   (deficit_df['dem_houseseats'] >=
                    0.5 * deficit_df['total_houseseats']))) |
                 ((deficit_df['president_party'] == 'Democrat') &
                  ((deficit_df['rep_senateseats'] >=
                    0.5 * deficit_df['total_senateseats']) |
                   (deficit_df['rep_houseseats'] >=
                    0.5 * deficit_df['total_houseseats'])))]
dfct_cntrl_all_split_cds = ColumnDataSource(deficit_cntrl_all_split_df)

# Create Senate control (WH + Sen) Republican control elements
deficit_cntrl_whsen_rep_df = \
      deficit_df[(deficit_df['president_party'] == 'Republican') &
                 (deficit_df['rep_senateseats'] >=
                  0.5 * deficit_df['total_senateseats'])]
dfct_cntrl_whsen_rep_cds = ColumnDataSource(deficit_cntrl_whsen_rep_df)

# Create Senate control (WH + Sen) Democrat control elements
deficit_cntrl_whsen_dem_df = \
      deficit_df[(deficit_df['president_party'] == 'Democrat') &
                 (deficit_df['dem_senateseats'] >=
                  0.5 * deficit_df['total_senateseats'])]
dfct_cntrl_whsen_dem_cds = ColumnDataSource(deficit_cntrl_whsen_dem_df)

# Create Senate control (WH + Sen) split control elements
deficit_cntrl_whsen_split_df = \
      deficit_df[((deficit_df['president_party'] == 'Republican') &
                  (deficit_df['dem_senateseats'] >=
                   0.5 * deficit_df['total_senateseats'])) |
                 ((deficit_df['president_party'] == 'Democrat') &
                  (deficit_df['rep_senateseats'] >=
                   0.5 * deficit_df['total_senateseats']))]
dfct_cntrl_whsen_split_cds = ColumnDataSource(deficit_cntrl_whsen_split_df)

# Create House control (WH + HouseRep) Republican control elements
deficit_cntrl_whhou_rep_df = \
      deficit_df[(deficit_df['president_party'] == 'Republican') &
                 (deficit_df['rep_houseseats'] >=
                  0.5 * deficit_df['total_houseseats'])]
dfct_cntrl_whhou_rep_cds = ColumnDataSource(deficit_cntrl_whhou_rep_df)

# Create House control (WH + HouseRep) Democrat control elements
deficit_cntrl_whhou_dem_df = \
      deficit_df[(deficit_df['president_party'] == 'Democrat') &
                 (deficit_df['dem_houseseats'] >=
                  0.5 * deficit_df['total_houseseats'])]
dfct_cntrl_whhou_dem_cds = ColumnDataSource(deficit_cntrl_whhou_dem_df)

# Create House control (WH + HouseRep) split control elements
deficit_cntrl_whhou_split_df = \
      deficit_df[((deficit_df['president_party'] == 'Republican') &
                  (deficit_df['dem_houseseats'] >=
                   0.5 * deficit_df['total_houseseats'])) |
                 ((deficit_df['president_party'] == 'Democrat') &
                  (deficit_df['rep_houseseats'] >=
                   0.5 * deficit_df['total_houseseats']))]
dfct_cntrl_whhou_split_cds = ColumnDataSource(deficit_cntrl_whhou_split_df)

recession_df = pd.read_csv(recession_data_path, parse_dates=['Peak','Trough'])
recession_cds = ColumnDataSource(recession_df)

# Create Variables for min and max values
data_length = len(deficit_df['Year'])
recession_data_length = len(recession_df['Peak'])
min_year = deficit_df['Year'].min()
max_year = deficit_df['Year'].max()
min_deficit = deficit_df['deficit_gdp'].min()
max_deficit = deficit_df['deficit_gdp'].max()

# Output to HTML file titled: "federal_debt_image.html"
fig_title = ('U.S. Federal Surplus (+) or Deficit (-) as Percent of Gross ' +
             'Domestic Product by Party Control: 1929-2020')
fig_path = os.path.join(images_dir, 'deficit_gdp_party_tseries.html')
output_file(fig_path, title=fig_title)

# Create a figure with '% of GDP' as Y-axis and year as X-axis
fig = figure(title=fig_title,
             plot_height=600,
             plot_width=1200,
             x_axis_label='Year',
             x_range=(min_year - 1, max_year + 1),
             y_axis_label='Percent of Gross Domestic Product',
             y_range=(min_deficit - 3, max_deficit + 3),
             toolbar_location=None)

# Set title font size and axes font sizes
fig.title.text_font_size = '17pt'
fig.xaxis.axis_label_text_font_size = '12pt'
fig.xaxis.major_label_text_font_size = '12pt'
fig.yaxis.axis_label_text_font_size = '12pt'
fig.yaxis.major_label_text_font_size = '12pt'

# Modify tick intervals for X-axis and Y-axis
fig.xaxis.ticker=SingleIntervalTicker(interval=10, num_minor_ticks=2)
fig.xgrid.ticker=SingleIntervalTicker(interval=10)
fig.yaxis.ticker=SingleIntervalTicker(interval=5, num_minor_ticks=5)
fig.ygrid.ticker=SingleIntervalTicker(interval=5)

# Create recession bars
for x in range(0,recession_data_length):
      peak_year = recession_df['Peak'][x].year
      trough_year = recession_df['Trough'][x].year
      if(peak_year >= min_year and trough_year >= min_year):
            fig.patch(  x=[peak_year, trough_year, trough_year,peak_year],
                        y=[-100, -100, max_deficit + 10, max_deficit + 10],
                        fill_color='gray',
                        fill_alpha=0.4,
                        line_width=0,
                        legend_label='Recession')
      if(peak_year == trough_year and peak_year >= min_year and
         trough_year >= min_year):
            fig.patch(x=[peak_year, trough_year + 1, trough_year + 1,
                         peak_year],
                      y=[-100, -100, max_deficit + 10, max_deficit + 10],
                      fill_color='gray',
                      fill_alpha=0.4,
                      line_width=0,
                      legend_label='Recession')

# Plotting the line and scatter point circles
fig.line(x='Year', y='deficit_gdp', source=deficit_cds, color='#423D3C',
         line_width=2)

fig.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_all_rep_cds, size=10,
           line_width=1, line_color='black', fill_color='red', alpha=0.7,
           muted_alpha=0.2, legend_label='Republican control')

fig.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_all_dem_cds, size=10,
           line_width=1, line_color='black', fill_color='blue', alpha=0.7,
           muted_alpha=0.2, legend_label='Democrat control')

fig.circle(x='Year', y='deficit_gdp', source=dfct_cntrl_all_split_cds, size=10,
           line_width=1, line_color='black', fill_color='green', alpha=0.7,
           muted_alpha=0.2, legend_label='Split control')

# Add information on hover
tooltips = [('Year', '@Year'),
            ('Deficit over GDP', '@deficit_gdp{0.0}'+'%'),
            ('President','@president'),
            ('White House', '@president_party'),
            ('Rep. House Seats', '@rep_houseseats'),
            ('Dem. House Seats', '@dem_houseseats'),
            ('Rep. Senate Seats', '@rep_senateseats'),
            ('Dem. Senate Seats', '@dem_senateseats')]
hover_glyph = fig.circle(x='Year', y='deficit_gdp', source=deficit_cds,
                         size=10, alpha=0, hover_fill_color='gray',
                         hover_alpha=0.5)
fig.add_tools(HoverTool(tooltips=tooltips))

#Turn off scrolling
fig.toolbar.active_drag = None

#Add legend
fig.legend.location = 'bottom_center'
fig.legend.border_line_width = 2
fig.legend.border_line_color = 'black'
fig.legend.border_line_alpha = 1
fig.legend.label_text_font_size = '4mm'

#Set legend muting click policy
fig.legend.click_policy = 'mute'

#Add notes below image
note_text_1 = ('Note: Republican control in a given year is defined as the ' +
               'President being Republican and Republicans holding more ' +
               'than 217 House seats for the majority of that year.')
caption1 = Title(text=note_text_1, align='left', text_font_size='4mm',
                 text_font_style='italic')
fig.add_layout(caption1, 'below')
note_text_2 = ('   Democrat control is defined as the President being ' +
               'Democrat and Democrats holding more than 217 House seats ' +
               'for the majority of that year. Split government is')
caption2 = Title(text=note_text_2, align='left', text_font_size='4mm',
                 text_font_style='italic')
fig.add_layout(caption2, 'below')
note_text_3 = ('   defined as one party holding the White ' +
               'House while the other party holds a majority of House seats.')
caption3 = Title(text=note_text_3, align='left', text_font_size='4mm',
                 text_font_style='italic')
fig.add_layout(caption3, 'below')
note_text_4 = ('Source: Federal Reserve Economic Data (FRED, FYFRGDA188S), ' +
               'United States House of Representatives History, Art, & ' +
               'Archives, "Party Divisions of the House of')
caption4 = Title(text=note_text_4, align='left', text_font_size='4mm',
                 text_font_style='italic')
fig.add_layout(caption4, 'below')
note_text_5 = ('   Representatives, 1789 to present", ' +
               'https://history.house.gov/Institution/Party-Divisions/' +
               'Party-Divisions/, Richard W. Evans (@rickecon).')
caption5 = Title(text=note_text_5, align='left', text_font_size='4mm',
                 text_font_style='italic')
fig.add_layout(caption5, 'below')

#Display the generated figure
show(fig)
