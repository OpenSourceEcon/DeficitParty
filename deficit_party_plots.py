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
from bokeh.models.filters import BooleanFilter
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

# Reading data from CVS (deficit_party_data.csv)
df = pd.read_csv(party_data_path,
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

# Create list of three tabs of political control definitions
control_type_list = ['wh_sen_hou', 'wh_sen', 'wh_hou']
control_type_labels = ['Full control: White House + Senate + House',
                       'White House and Senate control',
                       'White House and House control']
footnotes1_list = \
    ['217 seats in the House and more than 50 seats in the Senate',
     '50 seats in the Senate', '217 seats in the House']
footnotes2_list = ['Senate and House', 'Senate', 'House']

def output(title, file_name):
    fig_path = os.path.join(images_dir, file_name)
    output_file(fig_path, title=title)


def generateFigures(title, x_label, y_label, min_seats, max_seats, min_y,
                    max_y):
    r'''
    Returns a list of three empty figures for a given plot type with property
    values to be used as the figures are filled in. This figures will become
    the three tabs for the unified three-tab unified figure.

    Args:
        title (string): title text for figures
        x_label (string): x-axis label for figures
        y_label (string): y-axis label for figures
        min_seats (scalar): minimum number of Senate or House seats in the data
        max_seats (scalar): maximum number of Senate or House seats in the data
        min_y (scalar): minimum y-data value
        max_y (scalar): maximum y-data value

    Returns:
        fig_list (list): three-element list of blank Bokeh figures

    '''
    fig_list=[]
    for i in range(3):
        x_spread = max_seats - min_seats
        x_buffer = 0.1
        y_spread = max_y - min_y
        y_buffer = 0.1
        fig = figure(title=title,
                     plot_height=600,
                     plot_width=1000,
                     x_axis_label=x_label,
                     x_range=(min_seats - (x_buffer * min_seats),
                              max_seats + (x_buffer * max_seats)),
                     y_axis_label=y_label,
                     y_range=(min_y - (y_buffer * y_spread),
                              max_y + (y_buffer * y_spread)),
                     tools=['zoom_in', 'zoom_out', 'box_zoom', 'pan', 'undo',
                            'redo', 'reset'],
                     toolbar_location='right')

        # Set title font size and axes font sizes
        fig.title.text_font_size = '16pt'
        fig.xaxis.axis_label_text_font_size = '12pt'
        fig.xaxis.major_label_text_font_size = '12pt'
        fig.yaxis.axis_label_text_font_size = '12pt'
        fig.yaxis.major_label_text_font_size = '12pt'
        # Modify tick intervals for X-axis and Y-axis
        fig.xaxis.ticker=SingleIntervalTicker(interval=10, num_minor_ticks=0)
        fig.xgrid.ticker=SingleIntervalTicker(interval=10)
        fig.yaxis.ticker=SingleIntervalTicker(interval=5, num_minor_ticks=0)
        fig.ygrid.ticker=SingleIntervalTicker(interval=10)
        # Remove Logo from toolbar
        fig.toolbar.logo = None

        fig_list.append(fig)

    return fig_list


def plotCircle(i, x_value, y_value, fig, color, df):
    if(color == 'red'):
        LEGEND_LABEL = 'Republican Control'
    elif(color == 'blue'):
        LEGEND_LABEL = 'Democrat Control'
    else:
        LEGEND_LABEL = 'Split Control'

    fig.circle(x=df[x_value][i],
               y=df[y_value][i],
               size=10,
               line_width=1,
               line_color='black',
               fill_color=color,
               alpha=0.7,
               muted_alpha=0.1,
               legend_label=LEGEND_LABEL)


def deficitPartyPlots(deficit_component, seat_type, df=df,
                      control_type_list=control_type_list,
                      control_type_labels=control_type_labels, show_fig=False):
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
    # Create ColumnDataSource and filters to be used for plot
    cds = ColumnDataSource(df)
    '''
    r = ([True if x == 0 else False for x in cds.data['DemWhitehouse']] and 
            [True if y < 217 else False for y in cds.data['DemHouseSeats']] and
            [True if z < 50 else False for z in cds.data['DemSenateSeats']])
    b = ([True if x == 1 else False for x in cds.data['DemWhitehouse']] and 
            [True if y > 217 else False for y in cds.data['DemHouseSeats']] and
            [True if z > 50 else False for z in cds.data['DemSenateSeats']])      
    g = ([True if x == 0 else False for x in cds.data['DemWhitehouse']] and 
            [True if y > 217 else False for y in cds.data['DemHouseSeats']] and
            [True if z < 50 else False for z in cds.data['DemSenateSeats']])
    '''
    color_list=['black']*92
    cds.data['color'] = color_list
    red_filter = CDSView(source=cds, filters=[GroupFilter(column_name='color', group='red')])
    blue_filter = CDSView(source=cds, filters=[GroupFilter(column_name='color', group='blue')])
    green_filter = CDSView(source=cds, filters=[GroupFilter(column_name='color', group='green')])
    #red_filter = CDSView(source=cds, filters=[BooleanFilter(r)])
    #blue_filter = CDSView(source=cds, filters=[BooleanFilter(b)])
    #green_filter = CDSView(source=cds, filters=[BooleanFilter(g)])
    

    # Check input
    if (not (deficit_component == 'deficit' or
             deficit_component == 'spending' or
             deficit_component == 'revenues')):
        raise ValueError('deficit_component input invalid')

    if (not (seat_type == 'house' or seat_type == 'senate')):
        raise ValueError('seat_type input invalid')

    # Define variables for plot
    data_length = len(df['Year'])
    starting_index = 0
    footnote1_list=['217 seats in the House and more than 50 seats in the Senate',
                  '50 seats in the Senate',
                  '217 seats in the House']
    footnote2_list=['House and Senate',
                    'Senate',
                    'House']
    if seat_type == 'house':
        half_line = 217
        x_label='Number of Democratic House Seats (out of 435)'
        x_value = 'DemHouseSeats'
        min_seats = df[x_value].min()
        max_seats = df[x_value].max()
        if deficit_component == 'deficit':
            fig_title = ('U.S. Federal Deficits as Percent of GDP by ' +
                         'Democrat House Seats: 1929-2020')
            file_name = 'deficitGDP_HouseSeats.html'
            y_label = 'Deficit / GDP'
            y_value = 'deficit_gdp'
            min_y = df[y_value].min()
            max_y = df[y_value].max()
            legend_location = 'bottom_right'
        elif deficit_component == 'spending':
            fig_title = ('U.S. Federal Noninterest Spending as Percent of ' +
                         'GDP by Democrat House Seats: 1929-2020')
            file_name = 'spendingGDP_HouseSeats.html'
            y_label = 'Noninterest Spending / GDP'
            y_value = 'spend_nonint_gdp'
            min_y = df[y_value].min()
            max_y = df[y_value].max()
            starting_index = 11
            legend_location = 'top_right'
        elif deficit_component == 'revenues':
            fig_title = ('U.S. Federal Receipts as Percent of GDP by ' +
                         'Democrat House Seats: 1929-2020')
            file_name = 'revenuesGDP_HouseSeats.html'
            y_label = 'Receipts / GDP'
            y_value = 'receipts_gdp'
            min_y = df[y_value].min()
            max_y = df[y_value].max()
            legend_location = 'top_right'
    elif seat_type == 'senate':
        half_line=50
        x_label = 'Number of Democratic Senate Seats (out of 100)'
        x_value = 'DemSenateSeats'
        min_seats = df[x_value].min()
        max_seats = df[x_value].max()
        if deficit_component == 'deficit':
            fig_title = ('U.S. Federal Deficits as Percent of GDP by ' +
                         'Democrat Senate Seats: 1929-2020')
            file_name = 'deficitGDP_SenateSeats.html'
            y_label = 'Deficit / GDP'
            y_value = 'deficit_gdp'
            min_y = df[y_value].min()
            max_y = df[y_value].max()
            legend_location = 'bottom_right'
        elif deficit_component=='spending':
            fig_title = ('U.S. Federal Noninterest Spending as Percent of ' +
                         'GDP by Democrat Senate Seats: 1929-2020')
            file_name = 'spendingGDP_SenateSeats.html'
            y_label = 'Noninterest Spending / GDP'
            y_value = 'spend_nonint_gdp'
            min_y = df[y_value].min()
            max_y = df[y_value].max()
            starting_index = 11
            legend_location = 'top_right'
        elif deficit_component=='revenues':
            fig_title = ('U.S. Federal Receipts as Percent of GDP by ' +
                         'Democrat Senate Seats: 1929-2020')
            file_name = 'revenuesGDP_SenateSeats.html'
            y_label = 'Receipts / GDP'
            y_value = 'receipts_gdp'
            min_y = df[y_value].min()
            max_y = df[y_value].max()
            legend_location = 'top_right'

    # Set up tool tip text
    TOOLTIPS = [('Year', '@Year'),
                ('Deficit over GDP', '@deficit_gdp{0.0}'+'%'),
                ('President','@President'),
                ('White House', '@PresidentParty'),
                ('Rep. House Seats', '@RepHouseSeats'),
                ('Dem. House Seats', '@DemHouseSeats'),
                ('Rep. Senate Seats', '@RepSenateSeats'),
                ('Dem. Senate Seats', '@DemSenateSeats')]

    # Console start notification
    print('Generating ' + file_name)

    # Generate Figures
    fig_list = []
    fig_list = generateFigures(fig_title, x_label, y_label, min_seats,
                               max_seats, min_y, max_y)

    # Vertical black line noting half of senate seats
    halfLine = Span(location=half_line, dimension='height', line_color='black',
                    line_width=2)

    # Run loop for each tab of plot
    for i in range(3):
        #Add vertical black line at half number of seats
        fig_list[i].add_layout(halfLine)

        # Determine color for each data point
        for x in range(starting_index, data_length):
            if i == 0:
                if(df['DemHouseSeats'][x] < 217 and
                   df['DemSenateSeats'][x] < 50 and
                   df['DemWhitehouse'][x] == 0):
                    #plotCircle(i, x_value, y_value, fig_list[i], 'red', df)
                    cds.data['color'][x] = 'red'
                elif (df['DemHouseSeats'][x] > 217 and
                      df['DemSenateSeats'][x] > 50 and
                      df['DemWhitehouse'][x] == 1):
                    #plotCircle(i, x_value, y_value, fig_list[i], 'blue', df)
                    cds.data['color'][x] = 'blue'
                else:
                    #plotCircle(i,x_value, y_value, fig_list[i], 'green', df)
                    cds.data['color'][x] = 'green'
            elif i == 1:
                if (df['DemSenateSeats'][x] < 50 and
                    df['DemWhitehouse'][x] == 0):
                    #plotCircle(i, x_value, y_value, fig_list[i], 'red', df)
                    cds.data['color'][x] = 'red'
                elif (df['DemSenateSeats'][x] > 50 and
                      df['DemWhitehouse'][x] == 1):
                    #plotCircle(i, x_value, y_value, fig_list[i], 'blue', df)
                    cds.data['color'][x] = 'blue'
                else:
                    #plotCircle(i, x_value, y_value, fig_list[i], 'green', df)
                    cds.data['color'][x] = 'green'
            elif i == 2:
                if (df['DemHouseSeats'][x] < 217 and
                    df['DemWhitehouse'][x] == 0):
                    #plotCircle(i, x_value, y_value, fig_list[i], 'red', df)
                    cds.data['color'][x] = 'red'
                elif (df['DemHouseSeats'][x] > 217 and
                      df['DemWhitehouse'][x] == 1):
                    #plotCircle(i, x_value, y_value, fig_list[i], 'blue', df)
                    cds.data['color'][x] = 'blue'
                else:
                    #plotCircle(i, x_value, y_value, fig_list[i], 'green', df)
                    cds.data['color'][x] = 'green'

        # Plot points
        fig_list[i].scatter(x=x_value, y=y_value, 
                            source=cds, 
                            view=red_filter,
                            size=10, 
                            line_width=1,
                            alpha=.8, 
                            muted_alpha=0.1,
                            fill_color='red', 
                            legend_label='Republican Control')
        fig_list[i].scatter(x=x_value, y=y_value, 
                            source=cds, 
                            view=blue_filter,
                            size=10, 
                            line_width=1,
                            alpha=.8, 
                            muted_alpha=0.1,
                            fill_color='blue', 
                            legend_label='Democrat Control')
        fig_list[i].scatter(x=x_value, y=y_value, 
                            source=cds, 
                            view=green_filter,
                            size=10, 
                            line_width=1,
                            alpha=.8, 
                            muted_alpha=0.1,
                            fill_color='green', 
                            legend_label='Split Control')

        # Set up points to tigger the hover tool
        #fig_list[i].scatter(x=x_value, y=y_value, source=cds, size=20, alpha=0,
        #                    name='hover_trigger')
        #fig_list[i].add_tools(HoverTool(tooltips=TOOLTIPS,
        #                                names=['hover_trigger']))

        # Set up legend for each figure
        fig_list[i].legend.location = legend_location
        fig_list[i].legend.border_line_width = 2
        fig_list[i].legend.border_line_color = 'black'
        fig_list[i].legend.border_line_alpha = 1
        fig_list[i].legend.label_text_font_size = '4mm'
        # Set legend muting click policy
        fig_list[i].legend.click_policy = 'mute'

        # Add notes below plot
        note_text_1 = ('Note: Republican control in a given year is defined as the President '+ 
                      'being Republican and Republicans holding more than ')
        caption1 = Title(text=note_text_1, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption1, 'below')
        if(i==0):
            note_text_2 = ('   '+footnote1_list[i]+' for the majority of that year. Split '+
                            'government is defined as')
            caption2 = Title(text=note_text_2, align='left', text_font_size='4mm',
                            text_font_style='italic')
            fig_list[i].add_layout(caption2, 'below')
            note_text_3 = ('   one party holding the White House while the other party holds'+
                            ' a majority of '+footnote2_list[i] + ' seats.')
            caption3 = Title(text=note_text_3, align='left', text_font_size='4mm',
                            text_font_style='italic')
            fig_list[i].add_layout(caption3, 'below')
        else:
            note_text_2 = ('   ' + footnote1_list[i]+' for the majority of that year. Split '+
                            'government is defined as one party '+'holding the White House while')
            caption2 = Title(text=note_text_2, align='left', text_font_size='4mm',
                        text_font_style='italic')
            fig_list[i].add_layout(caption2, 'below')
            note_text_3 = ('   while the other party holds a majority of '+
                            footnote2_list[i] + ' seats.')
            caption3 = Title(text=note_text_3, align='left', text_font_size='4mm',
                        text_font_style='italic')
            fig_list[i].add_layout(caption3, 'below')
        note_text_4 = ('Source: Federal Reserve Economic Data (FRED, FYFRGDA188S), ' +
                    'United States House of Representatives History, Art, & ')
        caption4 = Title(text=note_text_4, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption4, 'below')
        note_text_5 = ('   Archives, "Party Divisions of the House of Representatives, 1789 to present", ')
        caption5 = Title(text=note_text_5, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption5, 'below')
        note_text_6 = ('   https://history.house.gov/Institution/Party-Divisions/Party-Divisions/, '+
                    'Richard W. Evans (@rickecon).')
        caption6 = Title(text=note_text_6, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption6, 'below')

    # Output figures to an HTML file
    output(fig_title, file_name)

    panel_list=[]
    title_str_full = 'Full control: White House + Senate + House'
    title_str_senate = 'White House and Senate control'
    title_str_house = 'White House and House control'
    panel_list.append(Panel(child=fig_list[0], title=title_str_full))
    panel_list.append(Panel(child=fig_list[1], title=title_str_senate))
    panel_list.append(Panel(child=fig_list[2], title=title_str_house))

    tabs = Tabs(tabs=panel_list)
    save(tabs)
    # Console start notification
    print(file_name + ' Complete')

    if show_fig:  # Show figure by opening browser page
        show(tabs)

    return tabs


if __name__ == "__main__":
    '''
    Execute all six plots if user runs the module as a script
    '''
    deficitPartyPlots('deficit', 'senate')
    #deficitPartyPlots('revenues', 'senate')
    #deficitPartyPlots('spending', 'senate')
    #deficitPartyPlots('deficit', 'house')
    #deficitPartyPlots('revenues', 'house')
    #deficitPartyPlots('spending', 'house')
