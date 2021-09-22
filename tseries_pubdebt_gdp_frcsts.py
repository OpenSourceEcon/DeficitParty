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
data_path = os.path.join(data_dir, 'cbo_debt_forecasts.csv')
images_dir = os.path.join(cur_path, 'images')

# Read data from cbo_debt_forecasts.csv
main_df = pd.read_csv(data_path, header=5,
                      dtype={'year': pd.Int64Dtype(),
                             'jun_2009': np.float64,
                             'jun_2009_frcst': pd.Int64Dtype(),
                             'jun_2010': np.float64,
                             'jun_2010_frcst': pd.Int64Dtype(),
                             'jun_2011': np.float64,
                             'jun_2011_frcst': pd.Int64Dtype(),
                             'jun_2012': np.float64,
                             'jun_2012_frcst': pd.Int64Dtype(),
                             'sep_2013': np.float64,
                             'sep_2013_frcst': pd.Int64Dtype(),
                             'jul_2014': np.float64,
                             'jul_2014_frcst': pd.Int64Dtype(),
                             'jun_2015': np.float64,
                             'jun_2015_frcst': pd.Int64Dtype(),
                             'jul_2016': np.float64,
                             'jul_2016_frcst': pd.Int64Dtype(),
                             'jan_2017': np.float64,
                             'jan_2017_frcst': pd.Int64Dtype(),
                             'mar_2017': np.float64,
                             'mar_2017_frcst': pd.Int64Dtype(),
                             'jun_2018': np.float64,
                             'jun_2018_frcst': pd.Int64Dtype(),
                             'jan_2019': np.float64,
                             'jan_2019_frcst': pd.Int64Dtype(),
                             'jun_2019': np.float64,
                             'jun_2019_frcst': pd.Int64Dtype(),
                             'jan_2020': np.float64,
                             'jan_2020_frcst': pd.Int64Dtype(),
                             'sep_2020': np.float64,
                             'sep_2020_frcst': pd.Int64Dtype(),
                             'mar_2021': np.float64,
                             'mar_2021_frcst': pd.Int64Dtype()},
                      skiprows=0)


def gen_tseries_frcst(frcst_var_list, legend_label_list, df=main_df,
                      main_start_year='min', main_end_year='max',
                      full_start_year='min', full_end_year='max',
                      note_text_list=[], fig_title_str='', fig_path=''):
    """
    This function creates a plot of multiple time series of CBO forecasts of
    U.S. publicly held national debt.
    """
    # Create Variables for min and max values
    if main_start_year == 'min':
        main_min_year = df['year'].min()
    else:
        main_min_year = int(main_start_year)
    if full_start_year == 'min':
        full_min_year = df['year'].min()
    else:
        full_min_year = int(full_start_year)
    if main_end_year == 'max':
        main_max_year = df['year'].max()
    else:
        main_max_year = int(main_end_year)
    if full_end_year == 'max':
        full_max_year = df['year'].max()
    else:
        full_max_year = int(full_end_year)
    df_full = df[(df['year'] >= full_min_year) & (df['year'] <= full_max_year)]
    df_main = df[(df['year'] >= main_min_year) & (df['year'] <= main_max_year)]
    # Find the min and max yvar values across the list of yvars and create
    # separate ColumnDataSource objects for each forecast series (this helps
    # with the hovertools)
    main_min_yvar = 100
    main_max_yvar = 0
    cds_list = []
    for k, yvar in enumerate(frcst_var_list):
        main_min_yvar = np.minimum(main_min_yvar, df_main[yvar].min())
        main_max_yvar = np.maximum(main_max_yvar, df_main[yvar].max())
        frcst_df = df_full[['year', yvar, yvar + '_frcst']].dropna()
        frcst_df['frcst'] = frcst_df[yvar + '_frcst'] = 1
        frcst_df['frcst_label'] = legend_label_list[k]
        frcst_df.rename(columns={yvar: 'debt_gdp'}, inplace=True)
        frcst_df = frcst_df[['year', 'debt_gdp', 'frcst', 'frcst_label']]
        cds_list.append(ColumnDataSource(frcst_df))

    # Output to HTML file
    fig_title = fig_title_str
    fig_path = fig_path
    output_file(fig_path, title=fig_title)

    fig = figure(title=fig_title,
                 plot_height=600,
                 plot_width=1100,
                 x_axis_label='Year',
                 x_range=(main_min_year - 1, main_max_year + 1),
                 y_axis_label='Percent of Gross Domestic Product',
                 y_range=(main_min_yvar - 5, main_max_yvar + 5),
                 tools=['save', 'zoom_in', 'zoom_out', 'box_zoom',
                        'pan', 'undo', 'redo', 'reset', 'help'],
                 toolbar_location='left')
    fig.toolbar.logo = None

    # Set title font size and axes font sizes
    fig.title.text_font_size = '15pt'
    fig.xaxis.axis_label_text_font_size = '12pt'
    fig.xaxis.major_label_text_font_size = '12pt'
    fig.yaxis.axis_label_text_font_size = '12pt'
    fig.yaxis.major_label_text_font_size = '12pt'

    # Modify tick intervals for X-axis and Y-axis
    fig.xaxis.ticker = SingleIntervalTicker(interval=10, num_minor_ticks=2)
    fig.xgrid.ticker = SingleIntervalTicker(interval=10)
    fig.yaxis.ticker = SingleIntervalTicker(interval=20, num_minor_ticks=2)
    fig.ygrid.ticker = SingleIntervalTicker(interval=20)

    min_256_color_ind = 0
    max_256_color_ind = 200
    intercept = max_256_color_ind
    slope = (min_256_color_ind - intercept) / (len(frcst_var_list) - 1)

    legend_item_list = []
    for k, v in enumerate(frcst_var_list):
        color_ind = int(np.round(slope * k + intercept))
        line = fig.line(x='year', y='debt_gdp', source=cds_list[k],
                        color=Reds[256][color_ind], line_width=3, alpha=0.7,
                        muted_alpha=0.15)
        legend_item_list.append((legend_label_list[k], [line]))

    # Add information on hover
    tooltips = [('Year', '@year'),
                ('Debt/GDP','@debt_gdp'),
                ('Forecast', '@frcst'),
                ('Forecast date', '@frcst_label')]
    fig.add_tools(HoverTool(tooltips=tooltips, toggleable=False))

    # Add legend
    legend = Legend(items=legend_item_list, location='center')
    fig.add_layout(legend, 'right')
    fig.legend.border_line_width = 1
    fig.legend.border_line_color = 'black'
    fig.legend.border_line_alpha = 1
    fig.legend.label_text_font_size = '4mm'

    # Set legend muting click policy
    fig.legend.click_policy = 'mute'

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
    frcst_var_list = [
        'jun_2009', 'jun_2010', 'jun_2011', 'jun_2012', 'sep_2013', 'jul_2014',
        'jun_2015', 'jul_2016', 'jan_2017', 'mar_2017', 'jun_2018', 'jan_2019',
        'jun_2019', 'jan_2020', 'sep_2020', 'mar_2021']
    legend_label_list = [
        'Jun. 2009', 'Jun. 2010', 'Jun. 2011', 'Jun. 2012', 'Sep. 2013',
        'Jul. 2014', 'Jun. 2015', 'Jul. 2016', 'Jan. 2017', 'Mar. 2017',
        'Jun. 2018', 'Jan. 2019', 'Jun. 2019', 'Jan. 2020', 'Sep. 2020',
        'Mar. 2021']
    note_text_list = \
        [
            ('Source: U.S. publicly held debt-to-GDP forecasts (extended ' +
             'baseline) from Congressional Budget Office Long-term Budget ' +
             'Outlook reports in'),
            ('   data associated with underlying figures, Long-term Budget ' +
             'Projections Data (https://www.cbo.gov/data/budget-economic-' +
             'data#1), and'),
            ('   Historical Budget Data (https://www.cbo.gov/data/budget-' +
             'economic-data#2). Richard W. Evans (@rickecon).')
        ]

    # Create publicly held debt forecasts figure
    fig_title = ('Comparison of 16 CBO Forecasts of U.S. Publicly Held Debt ' +
                 'as Percent of GDP: 2009-2021 forecasts')
    fig_path = os.path.join(images_dir, 'tseries_pubdebt_gdp_frcsts.html')
    pubdebt_gdp_frcsts_tseries = \
        gen_tseries_frcst(frcst_var_list, legend_label_list,
                          main_start_year=1915, main_end_year=2050,
                          full_start_year='min', full_end_year='max',
                          note_text_list=note_text_list,
                          fig_title_str=fig_title, fig_path=fig_path)
    show(pubdebt_gdp_frcsts_tseries)
