'''
The deficit_plots.py module prints plots of deficit/GDP for United States
across years, by number of Democrat-held Senate seats and House seats, and by
three different measures of party control. If a user runs this module as a
script, it will create all six plots.
'''

# Import packages
from bokeh.core.property.numeric import Interval
from bokeh.io.output import reset_output
from bokeh.models.annotations import Label, LabelSet
from bokeh.models.glyphs import VArea
from bokeh.models.layouts import Panel
from bokeh.models.tickers import SingleIntervalTicker
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file, save
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, CDSView, GroupFilter, Title,
                          Legend, HoverTool, NumeralTickFormatter, Span, Tabs,
                          Panel)

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(cur_path, 'data')
party_data_path = os.path.join(data_dir, 'deficit_party_data.csv')
images_dir = os.path.join(cur_path, 'images')


# -------------------------------------------------------------------------------
#  Create pandas DataFrames and Column Data Source data objects
# -------------------------------------------------------------------------------

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
                     'congress_num': np.int64,
                     'congress_sess': np.int64,
                     'dem_whitehouse': np.int64,
                     'dem_senateseats': np.int64,
                     'rep_senateseats': np.int64,
                     'oth_senateseats': np.int64,
                     'tot_senateseats': np.int64,
                     'dem_houseseats': np.int64,
                     'rep_houseseats': np.int64,
                     'oth_houseseats': np.int64,
                     'tot_houseseats': np.int64},
                 skiprows=3)

def deficitPartyPlots(yvar_str='deficit_gdp', xvar_str='dem_senateseats', main_df=main_df, note_text_list=[], fig_title_str='',fig_path=''):
    '''
    Generates one of six different plot types of U.S. deficit/GDP by year, by
    Democrat held Senate seats or House seats, and by three different measures
    of political control

    Args:
        deficit_component (string): either "deficit", "spending", or "revenues"
        seat_type (string): either "house" or "senate"
        df (DataFrame): input data
        show (boolean): =True shows figure by opening browser page

    Returns:
        Y (array_like): aggregate output

    '''
    # Output to HTML file
    fig_title = fig_title_str
    fig_path = fig_path
    output_file(fig_path, title=fig_title)

    # Create variables
    min_seat = main_df[xvar_str].min()
    max_seat = main_df[xvar_str].max()
    min_yvar = main_df[yvar_str].min()
    max_yvar = main_df[yvar_str].max()
    if(xvar_str == 'dem_senateseats'):
        seat_type = 'Senate'
    else:
        seat_type = 'House'
    if(yvar_str == 'deficit_gdp'):
        legend_location = 'bottom_right'
    elif(yvar_str == 'spend_nonint_gdp'):
        legend_location = 'bottom_right'
    else:
        legend_location = 'top_right'

    #------------------------------------------------------------------
    # Create Column Data Sources for each definition of party control
    #------------------------------------------------------------------

    # Create entire time series column data source for main and recession df's
    main_cds = ColumnDataSource(main_df)

    # Create Full control (WH + Sen + HouseRep) Republican control elements
    cntrl_all_rep_df = \
        main_df[(main_df['president_party'] == 'Republican') &
                (main_df['rep_senateseats'] >=
                0.5 * main_df['total_senateseats']) &
                (main_df['rep_houseseats'] >=
                0.5 * main_df['total_houseseats'])]
    cntrl_all_rep_cds = ColumnDataSource(cntrl_all_rep_df)

    # Create Full control (WH + Sen + HouseRep) Democrat control elements
    cntrl_all_dem_df = \
        main_df[(main_df['president_party'] == 'Democrat') &
                (main_df['dem_senateseats'] >=
                0.5 * main_df['total_senateseats']) &
                (main_df['dem_houseseats'] >=
                0.5 * main_df['total_houseseats'])]
    cntrl_all_dem_cds = ColumnDataSource(cntrl_all_dem_df)

    # Create Full control (WH + Sen + HouseRep) split control elements
    cntrl_all_split_df = \
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
    cntrl_all_split_cds = ColumnDataSource(cntrl_all_split_df)

    # Create Senate control (WH + Sen) Republican control elements
    cntrl_whsen_rep_df = \
        main_df[(main_df['president_party'] == 'Republican') &
                (main_df['rep_senateseats'] >=
                0.5 * main_df['total_senateseats'])]
    cntrl_whsen_rep_cds = ColumnDataSource(cntrl_whsen_rep_df)

    # Create Senate control (WH + Sen) Democrat control elements
    cntrl_whsen_dem_df = \
        main_df[(main_df['president_party'] == 'Democrat') &
                (main_df['dem_senateseats'] >=
                0.5 * main_df['total_senateseats'])]
    cntrl_whsen_dem_cds = ColumnDataSource(cntrl_whsen_dem_df)

    # Create Senate control (WH + Sen) split control elements
    cntrl_whsen_split_df = \
        main_df[((main_df['president_party'] == 'Republican') &
                (main_df['rep_senateseats'] <
                0.5 * main_df['total_senateseats'])) |
                ((main_df['president_party'] == 'Democrat') &
                (main_df['dem_senateseats'] <
                0.5 * main_df['total_senateseats']))]
    cntrl_whsen_split_cds = ColumnDataSource(cntrl_whsen_split_df)

    # Create House control (WH + HouseRep) Republican control elements
    cntrl_whhou_rep_df = \
        main_df[(main_df['president_party'] == 'Republican') &
                (main_df['rep_houseseats'] >=
                0.5 * main_df['total_houseseats'])]
    cntrl_whhou_rep_cds = ColumnDataSource(cntrl_whhou_rep_df)

    # Create House control (WH + HouseRep) Democrat control elements
    cntrl_whhou_dem_df = \
        main_df[(main_df['president_party'] == 'Democrat') &
                (main_df['dem_houseseats'] >=
                0.5 * main_df['total_houseseats'])]
    cntrl_whhou_dem_cds = ColumnDataSource(cntrl_whhou_dem_df)

    # Create House control (WH + HouseRep) split control elements
    cntrl_whhou_split_df = \
        main_df[((main_df['president_party'] == 'Republican') &
                (main_df['rep_houseseats'] <
                0.5 * main_df['total_houseseats'])) |
                ((main_df['president_party'] == 'Democrat') &
                (main_df['dem_houseseats'] <
                0.5 * main_df['total_houseseats']))]
    cntrl_whhou_split_cds = ColumnDataSource(cntrl_whhou_split_df)

    cntrl_cds_list = \
        [[cntrl_all_rep_cds, cntrl_all_dem_cds, cntrl_all_split_cds],
         [cntrl_whsen_rep_cds, cntrl_whsen_dem_cds, cntrl_whsen_split_cds],
         [cntrl_whhou_rep_cds, cntrl_whhou_dem_cds, cntrl_whhou_split_cds]]

    #-----------------------------------------------------------------
    # Create figure for each of the three party control definitions
    #-----------------------------------------------------------------
    cntrl_str_list = ['all', 'whsen', 'whhou']
    panel_title_list = \
        ['Full control: (White House + Senate + House of Reps.)',
         'Senate control: (White House + Senate)',
         'House control: (White House + House of Reps.)']
    panel_list = []

    # Create buffers for data on both axis
    x_buffer = (max_seat - min_seat) * .1
    y_buffer = (max_yvar - min_yvar) * .1

    for k, v in enumerate(cntrl_str_list):
        # Create a figure with '% of GDP' as Y-axis and year as X-axis
        fig = figure(title=fig_title,
                     plot_height=600,
                     plot_width=1200,
                     x_axis_label='Democrat '+seat_type+' seats',
                     x_range=(min_seat - x_buffer, max_seat + x_buffer),
                     y_axis_label='Percent of Gross Domestic Product',
                     y_range=(min_yvar - y_buffer, max_yvar + y_buffer),
                     toolbar_location=None)

        # Set title font size and axes font sizes
        fig.title.text_font_size = '17pt'
        fig.xaxis.axis_label_text_font_size = '12pt'
        fig.xaxis.major_label_text_font_size = '12pt'
        fig.yaxis.axis_label_text_font_size = '12pt'
        fig.yaxis.major_label_text_font_size = '12pt'

        # Modify tick intervals for X-axis and Y-axis
        fig.yaxis.ticker = SingleIntervalTicker(interval=5, num_minor_ticks=5)
        fig.ygrid.ticker = SingleIntervalTicker(interval=5)
        if(seat_type == 'Senate'):
            fig.xaxis.ticker = SingleIntervalTicker(interval=10, num_minor_ticks=2)
            fig.xgrid.ticker = SingleIntervalTicker(interval=10)
        else:
            fig.xaxis.ticker = SingleIntervalTicker(interval=20, num_minor_ticks=4)
            fig.xgrid.ticker = SingleIntervalTicker(interval=20)

        # Plotting the scatter point circles
        fig.circle(x=xvar_str, y=yvar_str, source=cntrl_cds_list[k][0], size=10,
                   line_width=1, line_color='black', fill_color='red',
                   alpha=0.7, muted_alpha=0.2,
                   legend_label='Republican control')

        fig.circle(x=xvar_str, y=yvar_str, source=cntrl_cds_list[k][1], size=10,
                   line_width=1, line_color='black', fill_color='blue',
                   alpha=0.7, muted_alpha=0.2, legend_label='Democrat control')

        fig.circle(x=xvar_str, y=yvar_str, source=cntrl_cds_list[k][2], size=10,
                   line_width=1, line_color='black', fill_color='green',
                   alpha=0.7, muted_alpha=0.2, legend_label='Split control')

        # Add information on hover
        if yvar_str == 'deficit_gdp':
            tool_str = 'Deficit / GDP'
        elif yvar_str == 'receipts_gdp':
            tool_str = 'Receipts / GDP'
        elif yvar_str == 'spend_nonint_gdp':
            tool_str = 'NonInt Spend / GDP'
        tooltips = [('Year', '@Year'),
                    (tool_str, '@' + yvar_str +'{0.0}'+'%'),
                    ('President','@president'),
                    ('White House', '@president_party'),
                    ('Rep. House Seats', '@rep_houseseats'),
                    ('Dem. House Seats', '@dem_houseseats'),
                    ('Rep. Senate Seats', '@rep_senateseats'),
                    ('Dem. Senate Seats', '@dem_senateseats')]
        hover_glyph = fig.circle(x='Year', y=yvar_str, source=main_cds,
                                 size=10, alpha=0, hover_fill_color='gray',
                                 hover_alpha=0.5)
        fig.add_tools(HoverTool(tooltips=tooltips))

        # Turn off scrolling
        fig.toolbar.active_drag = None

        # Add legend
        fig.legend.location = legend_location
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
    #---------------------------------------------------------------------------
    # Create time series for deficit_gdp by party control
    #---------------------------------------------------------------------------
    
    note_text_list = \
        [
            [
                ('Note: Republican control in a given year is defined as ' +
                'the President being Republican and Republicans holding at ' +
                'least half of Senate seats (50 or more) and at least'),
                ('   half of House seats (usually 217 or more) for the ' +
                'majority of that year. Democrat control is defined as the ' +
                'President being Democrat and Democrats holding at least'),
                ('   half of the Senate seats and at least half of the ' +
                'House seats for the majority of that year. Split ' +
                'government is defined as one party holding the White House ' +
                'while'),
                ('   either not holding a majority of Senate seates or not ' +
                'holding a majority of House seats.'),
                ('Source: Federal Reserve Economic Data (FRED, ' +
                 'FYFRGDA188S), United States House of Representatives ' +
                 'History, Art, & Archives, "Party Divisions of the House of'),
                ('   Representatives, 1789 to present", ' +
                 'https://history.house.gov/Institution/Party-Divisions/' +
                 'Party-Divisions/, Richard W. Evans (@rickecon).')
            ],
            [
                ('Note: Republican control in a given year is defined as ' +
                'the President being Republican and Republicans holding at ' +
                'least half of the Senate seats (50 or more) for the'),
                ('   majority of that year. Democrat control is defined as ' +
                'the President being Democrat and Democrats holding at ' +
                'least half of the Senate seats for the majority of that'),
                ('   year. Split government is defined as one party holding ' +
                 'the White House while not holding a majority of Senate ' +
                 'seats.'),
                ('Source: Federal Reserve Economic Data (FRED, ' +
                 'FYFRGDA188S), United States House of Representatives ' +
                 'History, Art, & Archives, "Party Divisions of the House of'),
                ('   Representatives, 1789 to present", ' +
                 'https://history.house.gov/Institution/Party-Divisions/' +
                 'Party-Divisions/, Richard W. Evans (@rickecon).')
            ],
            [
                ('Note: Republican control in a given year is defined as ' +
                'the President being Republican and Republicans holding at ' +
                'least half of the House seats (usually 217 or more)'),
                ('   for the majority of that year. Democrat control is ' +
                'defined as the President being Democrat and Democrats ' +
                'holding at least half of the House seats for the majority ' +
                'of'),
                ('   that year. Split government is defined as one party ' +
                'holding the White House while not holding a majority of ' +
                'House seats.'),
                ('Source: Federal Reserve Economic Data (FRED, ' +
                 'FYFRGDA188S), United States House of Representatives ' +
                 'History, Art, & Archives, "Party Divisions of the House of'),
                ('   Representatives, 1789 to present", ' +
                 'https://history.house.gov/Institution/Party-Divisions/' +
                 'Party-Divisions/, Richard W. Evans (@rickecon).')
            ]
        ]

    #------------------------
    # Function Calls
    #------------------------

    # Create deficits-to-GDP by Democrat Senate seats scatterplot
    fig_title_deficit = ('U.S. Federal Deficits as Percent of GDP by ' +
                         'Democrat Senate Seats: 1929-2020')
    fig_path_deficit = os.path.join(images_dir,
                                    'deficitGDP_SenateSeats.html')
    deficit_gdp_party_tseries = \
        deficitPartyPlots(yvar_str='deficit_gdp', xvar_str='dem_senateseats',
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_deficit, fig_path=fig_path_deficit)
    show(deficit_gdp_party_tseries)

    # Create deficits-to-GDP by Democrat House seats scatterplot
    fig_title_deficit = ('U.S. Federal Deficits as Percent of GDP by ' +
                         'Democrat House Seats: 1929-2020')
    fig_path_deficit = os.path.join(images_dir,
                                    'deficitGDP_HouseSeats.html')
    deficit_gdp_party_tseries = \
        deficitPartyPlots(yvar_str='deficit_gdp', xvar_str='dem_houseseats',
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_deficit, fig_path=fig_path_deficit)
    show(deficit_gdp_party_tseries)

    # Create non-interest spending-to-GDP by Democrat Senate seats scatterplot
    fig_title_deficit = ('U.S. Federal Non-interest Spending as Percent of GDP by ' +
                         'Democrat Senate Seats: 1929-2020')
    fig_path_deficit = os.path.join(images_dir,
                                    'spendingGDP_SenateSeats.html')
    deficit_gdp_party_tseries = \
        deficitPartyPlots(yvar_str='spend_nonint_gdp', xvar_str='dem_senateseats',
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_deficit, fig_path=fig_path_deficit)
    show(deficit_gdp_party_tseries)

    # Create non-interest spending-to-GDP by Democrat House seats scatterplot
    fig_title_deficit = ('U.S. Federal Non-interest Spending as Percent of GDP by ' +
                         'Democrat House Seats: 1929-2020')
    fig_path_deficit = os.path.join(images_dir,
                                    'spendingGDP_HouseSeats.html')
    deficit_gdp_party_tseries = \
        deficitPartyPlots(yvar_str='spend_nonint_gdp', xvar_str='dem_houseseats',
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_deficit, fig_path=fig_path_deficit)
    show(deficit_gdp_party_tseries)

    # Create revenues-to-GDP by Democrat Senate seats scatterplot
    fig_title_deficit = ('U.S. Federal Revenues as Percent of GDP by ' +
                         'Democrat Senate Seats: 1929-2020')
    fig_path_deficit = os.path.join(images_dir,
                                    'revenuesGDP_SenateSeats.html')
    deficit_gdp_party_tseries = \
        deficitPartyPlots(yvar_str='receipts_gdp', xvar_str='dem_senateseats',
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_deficit, fig_path=fig_path_deficit)
    show(deficit_gdp_party_tseries)

    # Create revenues-to-GDP by Democrat House seats scatterplot
    fig_title_deficit = ('U.S. Federal Revenues as Percent of GDP by ' +
                         'Democrat House Seats: 1929-2020')
    fig_path_deficit = os.path.join(images_dir,
                                    'revenuesGDP_HouseSeats.html')
    deficit_gdp_party_tseries = \
        deficitPartyPlots(yvar_str='receipts_gdp', xvar_str='dem_houseseats',
                    note_text_list=note_text_list,
                    fig_title_str=fig_title_deficit, fig_path=fig_path_deficit)
    show(deficit_gdp_party_tseries)



