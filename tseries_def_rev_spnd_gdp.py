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

# Reading data from CVS (deficit_party_data.csv)
main_df = pd.read_csv(party_data_path,
                      dtype={'year': np.int64,
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
                             'dem_senate_maj': np.int64,
                             'total_senateseats': np.int64,
                             'dem_houseseats': np.int64,
                             'rep_houseseats': np.int64,
                             'other_houseseats': np.int64,
                             'dem_house_maj': np.int64,
                             'total_houseseats': np.int64},
                      skiprows=3)

def gen_tseries(yvar_str='deficit_gdp', start_year='min', main_df=main_df,
                recession_df=recession_df, note_text_list=[], fig_title_str='',
                fig_path=''):
    """
    This function creates a three-panel time-series plot--one panel for each
    definition of party control--for a particular variable as a percent of GDP.
    The particular variable is either deficits, receipts, or non-interest
    spending.

    Inputs:
        yvar_str (string): either ''deficit_gdp', 'receipts_gdp', or
            'spend_nonint_gdp'
    """
    # Create Variables for min and max values
    recession_data_length = len(recession_df['Peak'])
    if start_year == 'min':
        min_year = main_df['year'].min()
    else:
        min_year = int(start_year)
    main_df = main_df[main_df['year'] >= min_year]
    max_year = main_df['year'].max()
    min_yvar = main_df[yvar_str].min()
    max_yvar = main_df[yvar_str].max()

    # Create entire time series column data source for main and recession df's
    main_cds = ColumnDataSource(main_df)

    # Create Full control (WH + Sen + HouseRep) Republican control elements
    cntrl_all_rep_df = \
        main_df[(main_df['president_party'] == 'Republican') &
                (main_df['dem_senate_maj'] == 0) &
                (main_df['dem_house_maj'] == 0)]
    cntrl_all_rep_cds = ColumnDataSource(cntrl_all_rep_df)

    # Create Full control (WH + Sen + HouseRep) Democrat control elements
    cntrl_all_dem_df = \
        main_df[(main_df['president_party'] == 'Democrat') &
                (main_df['dem_senate_maj'] == 1) &
                (main_df['dem_house_maj'] == 1)]
    cntrl_all_dem_cds = ColumnDataSource(cntrl_all_dem_df)

    # Create Full control (WH + Sen + HouseRep) split control elements
    cntrl_all_split_df = \
        main_df[((main_df['president_party'] == 'Republican') &
                ((main_df['dem_senate_maj'] == 1) |
                (main_df['dem_house_maj'] == 1))) |
                ((main_df['president_party'] == 'Democrat') &
                ((main_df['dem_senate_maj'] == 0) |
                (main_df['dem_house_maj'] == 0)))]
    cntrl_all_split_cds = ColumnDataSource(cntrl_all_split_df)

    # Create Senate control (WH + Sen) Republican control elements
    cntrl_whsen_rep_df = \
        main_df[(main_df['president_party'] == 'Republican') &
                (main_df['dem_senate_maj'] == 0)]
    cntrl_whsen_rep_cds = ColumnDataSource(cntrl_whsen_rep_df)

    # Create Senate control (WH + Sen) Democrat control elements
    cntrl_whsen_dem_df = \
        main_df[(main_df['president_party'] == 'Democrat') &
                (main_df['dem_senate_maj'] == 1)]
    cntrl_whsen_dem_cds = ColumnDataSource(cntrl_whsen_dem_df)

    # Create Senate control (WH + Sen) split control elements
    cntrl_whsen_split_df = \
        main_df[((main_df['president_party'] == 'Republican') &
                (main_df['dem_senate_maj'] == 1)) |
                ((main_df['president_party'] == 'Democrat') &
                (main_df['dem_senate_maj'] == 0))]
    cntrl_whsen_split_cds = ColumnDataSource(cntrl_whsen_split_df)

    # Create House control (WH + HouseRep) Republican control elements
    cntrl_whhou_rep_df = \
        main_df[(main_df['president_party'] == 'Republican') &
                (main_df['dem_house_maj'] == 0)]
    cntrl_whhou_rep_cds = ColumnDataSource(cntrl_whhou_rep_df)

    # Create House control (WH + HouseRep) Democrat control elements
    cntrl_whhou_dem_df = \
        main_df[(main_df['president_party'] == 'Democrat') &
                (main_df['dem_house_maj'] == 1)]
    cntrl_whhou_dem_cds = ColumnDataSource(cntrl_whhou_dem_df)

    # Create House control (WH + HouseRep) split control elements
    cntrl_whhou_split_df = \
        main_df[((main_df['president_party'] == 'Republican') &
                (main_df['dem_house_maj'] == 1)) |
                ((main_df['president_party'] == 'Democrat') &
                (main_df['dem_house_maj'] == 0))]
    cntrl_whhou_split_cds = ColumnDataSource(cntrl_whhou_split_df)

    cntrl_cds_list = \
        [[cntrl_all_rep_cds, cntrl_all_dem_cds, cntrl_all_split_cds],
         [cntrl_whsen_rep_cds, cntrl_whsen_dem_cds, cntrl_whsen_split_cds],
         [cntrl_whhou_rep_cds, cntrl_whhou_dem_cds, cntrl_whhou_split_cds]]

    # Output to HTML file
    fig_title = fig_title_str
    fig_path = fig_path
    output_file(fig_path, title=fig_title)

    '''
    ---------------------------------------------------------------------------
    Create figure for each of the three party control definitions
    ---------------------------------------------------------------------------
    '''
    cntrl_str_list = ['all', 'whsen', 'whhou']
    panel_title_list = \
        ['Full control: (White House + Senate + House of Reps.)',
         'Senate control: (White House + Senate)',
         'House control: (White House + House of Reps.)']
    panel_list = []

    for k, v in enumerate(cntrl_str_list):
        # Create a figure with '% of GDP' as y-axis and year as x-axis
        fig = figure(title=fig_title,
                     plot_height=650,
                     plot_width=1100,
                     x_axis_label='Year',
                     x_range=(min_year - 1, max_year + 1),
                     y_axis_label='Percent of Gross Domestic Product',
                     y_range=(min_yvar - 3, max_yvar + 3),
                     toolbar_location=None)

        # Set title font size and axes font sizes
        fig.title.text_font_size = '15.5pt'
        fig.xaxis.axis_label_text_font_size = '12pt'
        fig.xaxis.major_label_text_font_size = '12pt'
        fig.yaxis.axis_label_text_font_size = '12pt'
        fig.yaxis.major_label_text_font_size = '12pt'

        # Modify tick intervals for X-axis and Y-axis
        fig.xaxis.ticker = SingleIntervalTicker(interval=10, num_minor_ticks=2)
        fig.xgrid.ticker = SingleIntervalTicker(interval=10)
        fig.yaxis.ticker = SingleIntervalTicker(interval=5, num_minor_ticks=5)
        fig.ygrid.ticker = SingleIntervalTicker(interval=5)

        # Create recession bars
        for x in range(0,recession_data_length):
            peak_year = recession_df['Peak'][x].year
            trough_year = recession_df['Trough'][x].year
            if(peak_year >= min_year and trough_year >= min_year):
                fig.patch(x=[peak_year, trough_year, trough_year,peak_year],
                          y=[-100, -100, max_yvar + 10, max_yvar + 10],
                          fill_color='gray',
                          fill_alpha=0.4,
                          line_width=0,
                          legend_label='Recession')
            if(peak_year == trough_year and peak_year >= min_year and
            trough_year >= min_year):
                fig.patch(x=[peak_year, trough_year + 1, trough_year + 1,
                             peak_year],
                          y=[-100, -100, max_yvar + 10, max_yvar + 10],
                          fill_color='gray',
                          fill_alpha=0.4,
                          line_width=0,
                          legend_label='Recession')

        # Plotting the line and scatter point circles
        fig.line(x='year', y=yvar_str, source=main_cds, color='#423D3C',
                 line_width=2)


        fig.circle(x='year', y=yvar_str, source=cntrl_cds_list[k][0], size=10,
                   line_width=1, line_color='black', fill_color='red',
                   alpha=0.7, muted_alpha=0.2,
                   legend_label='Republican control')

        fig.circle(x='year', y=yvar_str, source=cntrl_cds_list[k][1], size=10,
                   line_width=1, line_color='black', fill_color='blue',
                   alpha=0.7, muted_alpha=0.2, legend_label='Democrat control')

        fig.circle(x='year', y=yvar_str, source=cntrl_cds_list[k][2], size=10,
                   line_width=1, line_color='black', fill_color='green',
                   alpha=0.7, muted_alpha=0.2, legend_label='Split control')

        # Add information on hover
        if yvar_str == 'deficit_gdp':
            tool_str = 'Deficit / GDP'
        elif yvar_str == 'receipts_gdp':
            tool_str = 'Receipts / GDP'
        elif yvar_str == 'spend_nonint_gdp':
            tool_str = 'NonInt Spend / GDP'
        tooltips = [('Year', '@year'),
                    (tool_str, '@' + yvar_str +'{0.0}'+'%'),
                    ('President','@president'),
                    ('White House', '@president_party'),
                    ('Rep. House Seats', '@rep_houseseats'),
                    ('Dem. House Seats', '@dem_houseseats'),
                    ('Rep. Senate Seats', '@rep_senateseats'),
                    ('Dem. Senate Seats', '@dem_senateseats')]
        hover_glyph = fig.circle(x='year', y=yvar_str, source=main_cds,
                                 size=10, alpha=0, hover_fill_color='gray',
                                 hover_alpha=0.5)
        fig.add_tools(HoverTool(tooltips=tooltips))

        # Turn off scrolling
        fig.toolbar.active_drag = None

        # Add legend
        fig.legend.location = 'bottom_center'
        fig.legend.border_line_width = 2
        fig.legend.border_line_color = 'black'
        fig.legend.border_line_alpha = 1
        fig.legend.label_text_font_size = '4mm'

        # Set legend muting click policy
        fig.legend.click_policy = 'mute'

        # Add notes below image
        for note_text in note_text_list[k]:
            caption = Title(text=note_text, align='left', text_font_size='4mm',
                            text_font_style='italic')
            fig.add_layout(caption, 'below')

        panel = Panel(child=fig, title=panel_title_list[k])
        panel_list.append(panel)

    # Assign the panels to Tabs
    tabs = Tabs(tabs=panel_list)

    # Display the generated figure
    # show(tabs)

    return tabs


if __name__ == "__main__":
    '''
    ---------------------------------------------------------------------------
    Create time series for deficit_gdp by party control
    ---------------------------------------------------------------------------
    '''
    note_text_list = \
        [
            [
                ('Note: Republican control in a given year is defined as ' +
                 'the President being Republican and Republicans holding ' +
                 'the majority of the Senate (either the most'),
                ('   caucus seats or a tiebreaker majority with the Vice ' +
                 'President) and a majority of House seats (usually 217 or ' +
                 'more) for the majority of that year. Democrat'),
                ('   control is defined similarly in the White House, ' +
                 'Senate, and House of Representatives. Split government is ' +
                 'defined as one party holding the White House'),
                ('   while either not holding the majority in the Sentate ' +
                 'or not holding the majority in the House of ' +
                 'Representatives.'),
                ('Source: Federal Reserve Economic Data (FRED, ' +
                 'FYFRGDA188S); United States House of Representatives ' +
                 'History, Art, & Archives, "Party Divisions of'),
                ('   the House of Representatives, 1789 to present", ' +
                 'https://history.house.gov/Institution/Party-Divisions/' +
                 'Party-Divisions/; United States Senate, Art & History,'),
                ('   Party Division, ' +
                 'https://www.cop.senate.gov/history/partydiv.htm; ' +
                 'Richard W. Evans (@rickecon).')
            ],
            [
                ('Note: Republican control in a given year is defined as ' +
                 'the President being Republican and Republicans holding ' +
                 'the majority of the Senate (either the most'),
                ('   caucus seats or a tiebreaker majority with the Vice ' +
                 'President) for the majority of that year. Democrat ' +
                 'control is defined similarly in the White House and'),
                ('   Senate. Split government is defined as one party ' +
                 'holding the White House while not holding the majority in ' +
                 'the Senate.'),
                ('Source: Federal Reserve Economic Data (FRED, ' +
                 'FYFRGDA188S); United States House of Representatives ' +
                 'History, Art, & Archives, "Party Divisions of'),
                ('   the House of Representatives, 1789 to present", ' +
                 'https://history.house.gov/Institution/Party-Divisions/' +
                 'Party-Divisions/; United States Senate, Art & History,'),
                ('   Party Division, ' +
                 'https://www.cop.senate.gov/history/partydiv.htm; ' +
                 'Richard W. Evans (@rickecon).')
            ],
            [
                ('Note: Republican control in a given year is defined as ' +
                 'the President being Republican and Republicans holding a ' +
                 'majority of House seats (usually 217 or'),
                ('   more) for the majority of that year. Democrat control ' +
                 'is defined similarly in the White House and House of ' +
                 'Representatives. Split government is defined'),
                ('   as one party holding the White House while not holding ' +
                 'a majority of House seats.'),
                ('Source: Federal Reserve Economic Data (FRED, ' +
                 'FYFRGDA188S); United States House of Representatives ' +
                 'History, Art, & Archives, "Party Divisions of'),
                ('   the House of Representatives, 1789 to present", ' +
                 'https://history.house.gov/Institution/Party-Divisions/' +
                 'Party-Divisions/; United States Senate, Art & History,'),
                ('   Party Division, ' +
                 'https://www.cop.senate.gov/history/partydiv.htm; ' +
                 'Richard W. Evans (@rickecon).')
            ]
        ]

    # Create deficits-to-GDP time series by party control figure
    fig_title_deficit = ('U.S. Federal Surplus (+) or Deficit (-) as ' +
                        'Percent of Gross Domestic Product by Party ' +
                        'Control: 1947-2020')
    fig_path_deficit = os.path.join(images_dir,
                                    'tseries_deficit_gdp_party.html')
    tseries_deficit_gdp_party = \
        gen_tseries(yvar_str='deficit_gdp', start_year=1947,
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_deficit, fig_path=fig_path_deficit)
    show(tseries_deficit_gdp_party)

    # Create receipts-to-GDP time series by party control figure
    fig_title_receipts = ('U.S. Federal Receipts as Percent of Gross ' +
                          'Domestic Product by Party Control: 1947-2020')
    fig_path_receipts = os.path.join(images_dir,
                                     'tseries_receipts_gdp_party.html')
    tseries_receipts_gdp_party = \
        gen_tseries(yvar_str='receipts_gdp', start_year=1947,
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_receipts,
                    fig_path=fig_path_receipts)
    show(tseries_receipts_gdp_party)

    # Create noninterest speinding-to-GDP time series by party control figure
    fig_title_nonintspend = ('U.S. Federal Noninterest Spending as Percent ' +
                             'of Gross Domestic Product by Party Control: ' +
                             '1947-2020')
    fig_path_nonintspend = os.path.join(images_dir,
                                        'tseries_nonintspend_gdp_party.html')
    tseries_nonintspend_gdp_party = \
        gen_tseries(yvar_str='spend_nonint_gdp', start_year=1947,
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_nonintspend,
                    fig_path=fig_path_nonintspend)
    show(tseries_nonintspend_gdp_party)
