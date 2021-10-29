# Import packages
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, Title, Legend, HoverTool,
                          NumeralTickFormatter)
from bokeh.models.annotations import Label, LabelSet
from bokeh.models.tickers import SingleIntervalTicker
from bokeh.core.property.numeric import Interval
from bokeh.palettes import Reds

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(cur_path, 'data')
data_path = os.path.join(data_dir, 'outlays.csv')
images_dir = os.path.join(cur_path, 'images')

# Read data from cbo_debt_forecasts.csv
main_df = pd.read_csv(data_path,
                      dtype={'year': pd.Int64Dtype(),
                             'mand_outlays_lev': np.float64,
                             'discr_outlays_lev': np.float64,
                             'net_int_lev': np.float64,
                             'tot_nonint_outlays_lev': np.float64,
                             'tot_outlays_lev': np.float64,
                             'mand_outlays_pct_tot_nonint': np.float64,
                             'mand_outlays_pct_tot': np.float64,
                             'mand_outlays_gdp': np.float64,
                             'discr_outlays_gdp': np.float64,
                             'net_int_gdp': np.float64,
                             'tot_nonint_outlays_gdp': np.float64,
                             'tot_outlays_gdp': np.float64},
                      skiprows=12)
main_df = main_df.drop(['Unnamed: 8'], axis=1)


def gen_tseries(tseries_var, hover_descr='yvar', df=main_df, start_year='min',
                end_year='max', note_text_list=[], fig_title_str='',
                fig_path=''):
    """
    This function creates a plot of a single time series from the set of
    variables from the outlays.csv dataset.
    """
    # Create Variables for min and max values
    if start_year == 'min':
        min_year = df['year'].min()
    else:
        min_year = int(start_year)
    if end_year == 'max':
        max_year = df['year'].max()
    else:
        max_year = int(end_year)
    df_main = df[(df['year'] >= min_year) & (df['year'] <= max_year)]
    min_yvar = df_main[tseries_var].min()
    max_yvar = df_main[tseries_var].max()
    buffer_pct_yvar = 0.1
    buffer_yvar = buffer_pct_yvar * (max_yvar - min_yvar)


    # Create column data source for visualization
    cds = ColumnDataSource(df_main)

    # Output to HTML file
    fig_title = fig_title_str
    fig_path = fig_path
    output_file(fig_path, title=fig_title)

    fig = figure(title=fig_title,
                 plot_height=600,
                 plot_width=1100,
                 x_axis_label='Year',
                 x_range=(min_year - 1, max_year + 1),
                 y_axis_label='Percent of Gross Domestic Product',
                 y_range=(min_yvar - buffer_yvar, max_yvar + buffer_yvar),
                 toolbar_location=None)

    # Set title font size and axes font sizes
    fig.title.text_font_size = '15pt'
    fig.xaxis.axis_label_text_font_size = '12pt'
    fig.xaxis.major_label_text_font_size = '12pt'
    fig.yaxis.axis_label_text_font_size = '12pt'
    fig.yaxis.major_label_text_font_size = '12pt'

    # Modify tick intervals for X-axis and Y-axis
    fig.xaxis.ticker = SingleIntervalTicker(interval=5, num_minor_ticks=5)
    fig.xgrid.ticker = SingleIntervalTicker(interval=5)
    fig.yaxis.ticker = SingleIntervalTicker(interval=2, num_minor_ticks=2)
    fig.ygrid.ticker = SingleIntervalTicker(interval=2)

    fig.line(x='year', y=tseries_var, source=cds, color='blue', line_width=4,
             alpha=0.7)

    # Add information on hover
    tooltips = [('Year', '@year'),
                (hover_descr, '@' + tseries_var + '{0.0}'+'%')]
    fig.add_tools(HoverTool(tooltips=tooltips))

    # Turn off scrolling
    fig.toolbar.active_drag = None

    # Add notes below image
    for note_text in note_text_list:
        caption = Title(text=note_text, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig.add_layout(caption, 'below')

    return fig


if __name__ == "__main__":
    """
    Script that runs if the module is called and executed directly
    """
    note_text_list = \
        [
            ('Source: Historical data associated with CBO February ' +
             '2021 "The Budget and Economic Outlook: 2021 to 2031. ' +
             'Richard W. Evans (@rickecon).')
        ]

    # Create time series plot of total non-interest outlays as percent of GDP
    fig_title = ('Total Non-interest Outlays as Percent of GDP: 1962-2020')
    fig_path = os.path.join(images_dir, 'tseries_nonintoutlays_gdp.html')
    nonintoutlays_gdp_tseries = \
        gen_tseries('tot_nonint_outlays_gdp', hover_descr='Nonint Outlays/GDP',
                    start_year='min', end_year=2020,
                    note_text_list=note_text_list,
                    fig_title_str=fig_title, fig_path=fig_path)
    show(nonintoutlays_gdp_tseries)
