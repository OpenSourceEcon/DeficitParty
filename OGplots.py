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
data_path1 = os.path.join(data_dir, 'cbo_ogusa_debt_forecasts.csv')
data_path2 = os.path.join(data_dir, 'ogusa_aggr_data.csv')
images_dir = os.path.join(cur_path, 'images')

# Read data from cbo_debt_forecasts.csv
df1 = pd.read_csv(data_path1, header=5,
                  dtype={'year': pd.Int64Dtype(),
                         'mar_2021': np.float64,
                         'mar_2021_frcst': pd.Int64Dtype(),
                         'ogusa': np.float64},
                  skiprows=0)

# Read data from ogusa_aggr_data.csv
df2 = pd.read_csv(data_path2, header=2,
                  dtype={'year': pd.Int64Dtype(),
                         'Y_base': np.float64,
                         'C_base': np.float64,
                         'K_base': np.float64,
                         'L_base': np.float64,
                         'D_base': np.float64,
                         'Y_ref_G033': np.float64,
                         'C_ref_G033': np.float64,
                         'K_ref_G033': np.float64,
                         'L_ref_G033': np.float64,
                         'D_ref_G033': np.float64,
                         'Y_ref_T340': np.float64,
                         'C_ref_T340': np.float64,
                         'K_ref_T340': np.float64,
                         'L_ref_T340': np.float64,
                         'D_ref_T340': np.float64},
                  skiprows=0)
df2['DebtGDP_base'] = (df2['D_base'] / df2['Y_base']) * 100
df2['DebtGDP_ref_G033'] = (df2['D_ref_G033'] / df2['Y_ref_G033']) * 100
df2['DebtGDP_ref_T340'] = (df2['D_ref_T340'] / df2['Y_ref_T340']) * 100


def gen_tseries2(frcst_var_list, legend_label_list, df, color_list,
                start_year='min', end_year='max', note_text_list=[],
                fig_title_str='', fig_path=''):
    """
    This function creates a plot of multiple time series of CBO forecasts of
    U.S. publicly held national debt.
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
    # Find the min and max yvar values across the list of yvars and create
    # separate ColumnDataSource objects for each forecast series (this helps
    # with the hovertools)
    min_yvar = 100
    max_yvar = 0
    cds_list = []
    for k, yvar in enumerate(frcst_var_list):
        min_yvar = np.minimum(min_yvar, df_main[yvar].min())
        max_yvar = np.maximum(max_yvar, df_main[yvar].max())
        frcst_df = df_main[['year', yvar]].dropna()
        frcst_df['frcst_label'] = legend_label_list[k]
        frcst_df.rename(columns={yvar: 'debt_gdp'}, inplace=True)
        frcst_df = frcst_df[['year', 'debt_gdp', 'frcst_label']]
        cds_list.append(ColumnDataSource(frcst_df))

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
                 y_range=(min_yvar - 5, max_yvar + 5),
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
    fig.yaxis.ticker = SingleIntervalTicker(interval=10, num_minor_ticks=2)
    fig.ygrid.ticker = SingleIntervalTicker(interval=10)

    # Create lines and markers for two time series
    fig.line(x='year', y='debt_gdp', source=cds_list[0], color=color_list[0],
             line_width=3, alpha=0.7, muted_alpha=0.15)
    fig.triangle(x='year', y='debt_gdp', source=cds_list[0], size=9,
                 line_width=1, line_color='black', fill_color=color_list[0],
                 alpha=0.7, muted_alpha=0.2, legend_label=legend_label_list[0])
    fig.line(x='year', y='debt_gdp', source=cds_list[1], color=color_list[1],
             line_width=3, alpha=0.7, muted_alpha=0.15)
    fig.circle(x='year', y='debt_gdp', source=cds_list[1], size=8,
                 line_width=1, line_color='black', fill_color=color_list[1],
                 alpha=0.7, muted_alpha=0.2, legend_label=legend_label_list[1])

    # Add vertical dashed line at 2050
    fig.segment(x0=2050, y0=90, x1=2050, y1=215, color='black',
                line_dash='6 4', line_width=2)

    # Add information on hover
    tooltips = [('Year', '@year'),
                ('Debt/GDP','@debt_gdp'),
                ('Forecast date', '@frcst_label')]
    fig.add_tools(HoverTool(tooltips=tooltips, toggleable=False))

    # Add legend
    fig.legend.location = 'top_center'
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


def gen_tseries3(frcst_var_list, legend_label_list, df, color_list,
                 start_year='min', end_year='max', note_text_list=[],
                 fig_title_str='', fig_path=''):
    """
    This function creates a plot of multiple time series of CBO forecasts of
    U.S. publicly held national debt.
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
    # Find the min and max yvar values across the list of yvars and create
    # separate ColumnDataSource objects for each forecast series (this helps
    # with the hovertools)
    min_yvar = 100
    max_yvar = 0
    cds_list = []
    for k, yvar in enumerate(frcst_var_list):
        min_yvar = np.minimum(min_yvar, df_main[yvar].min())
        max_yvar = np.maximum(max_yvar, df_main[yvar].max())
        frcst_df = df_main[['year', yvar]].dropna()
        frcst_df['frcst_label'] = legend_label_list[k]
        frcst_df.rename(columns={yvar: 'debt_gdp'}, inplace=True)
        frcst_df = frcst_df[['year', 'debt_gdp', 'frcst_label']]
        cds_list.append(ColumnDataSource(frcst_df))

    y_buffer_pct = 0.1
    y_range = max_yvar - min_yvar
    y_buffer_amt = y_buffer_pct * y_range

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
                 y_range=(min_yvar - y_buffer_amt, max_yvar + y_buffer_amt),
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
    fig.yaxis.ticker = SingleIntervalTicker(interval=10, num_minor_ticks=2)
    fig.ygrid.ticker = SingleIntervalTicker(interval=10)

    # Create lines and markers for two time series
    fig.line(x='year', y='debt_gdp', source=cds_list[0], color=color_list[0],
             line_width=3, alpha=0.7, muted_alpha=0.15)
    fig.circle(x='year', y='debt_gdp', source=cds_list[0], size=8,
                 line_width=1, line_color='black', fill_color=color_list[0],
                 alpha=0.7, muted_alpha=0.2, legend_label=legend_label_list[0])
    fig.line(x='year', y='debt_gdp', source=cds_list[1], color=color_list[1],
             line_width=3, alpha=0.7, muted_alpha=0.15)
    fig.triangle(x='year', y='debt_gdp', source=cds_list[1], size=9,
                 line_width=1, line_color='black', fill_color=color_list[1],
                 alpha=0.7, muted_alpha=0.2, legend_label=legend_label_list[1])
    fig.line(x='year', y='debt_gdp', source=cds_list[2], color=color_list[2],
             line_width=3, alpha=0.7, muted_alpha=0.15)
    fig.square(x='year', y='debt_gdp', source=cds_list[2], size=8,
                 line_width=1, line_color='black', fill_color=color_list[2],
                 alpha=0.7, muted_alpha=0.2, legend_label=legend_label_list[2])

    # Add vertical dashed line at 2050
    fig.segment(x0=2050, y0=90, x1=2050, y1=215, color='black',
                line_dash='6 4', line_width=2)

    # Add information on hover
    tooltips = [('Year', '@year'),
                ('Debt/GDP','@debt_gdp'),
                ('Forecast date', '@frcst_label')]
    fig.add_tools(HoverTool(tooltips=tooltips, toggleable=False))

    # Add legend
    fig.legend.location = 'top_center'
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
    # Create publicly held debt forecasts figure
    frcst_var_list1 = ['mar_2021', 'ogusa']
    color_list1 = ['red', 'blue']
    legend_label_list1 = [
        'CBO forecast (Mar. 2021)', 'OG-USA baseline forecast']
    note_text_list1 = \
        [
            ('Source: U.S. publicly held debt-to-GDP forecasts (extended ' +
             'baseline) from Congressional Budget Office Long-term Budget ' +
             'Outlook March 4, 2021 report.'),
            ('   OG-USA forecast from baseline simulation in Appendix D.')
        ]

    fig_title1 = ('Baseline Forecasts of U.S. Federal Debt Held by the ' +
                  'Public, CBO March 2021 versus OG-USA, 2021 to 2051')
    fig_path1 = os.path.join(images_dir,
                             'tseries_pubdebt_gdp_cbo_ogusa_frcsts.html')
    pubdebt_gdp_frcsts_cbo_ogusa_tseries = \
        gen_tseries2(frcst_var_list1, legend_label_list1, df1, color_list1,
                     start_year=2021, end_year=2051,
                     note_text_list=note_text_list1,
                     fig_title_str=fig_title1, fig_path=fig_path1)
    show(pubdebt_gdp_frcsts_cbo_ogusa_tseries)

    # Create figure of baseline and reform debt-to-GDP time paths
    frcst_var_list2 = ['DebtGDP_base', 'DebtGDP_ref_G033', 'DebtGDP_ref_T340']
    color_list2 = ['blue', 'green', '#C584DB']
    legend_label_list2 = [
        'Current law baseline', 'Gov\'t discretionary spending cut',
        'Per. income and corporate tax increase']
    note_text_list2 = \
        [
            ('Source: OG-USA baseline and reform forecasts from simulations ' +
             'in Appendix D.'),
        ]

    fig_title2 = ('Debt-to-GDP in Two Reforms Forecasts versus Baseline ' +
                  'Forecast, 2021 to 2055')
    fig_path2 = os.path.join(images_dir,
                             'tseries_pubdebt_gdp_G033_T340.html')
    pubdebt_gdp_G033_T340_tseries = \
        gen_tseries3(frcst_var_list2, legend_label_list2, df2, color_list2,
                     start_year=2021, end_year=2055,
                     note_text_list=note_text_list2,
                     fig_title_str=fig_title2, fig_path=fig_path2)
    show(pubdebt_gdp_G033_T340_tseries)