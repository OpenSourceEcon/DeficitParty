# Import packages
from bokeh.core.property.numeric import Interval
from bokeh.models.annotations import Label, LabelSet
from bokeh.models.glyphs import VArea
from bokeh.models.tickers import SingleIntervalTicker
import numpy as np
import pandas as pd
from scipy.stats import t as tdist
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, Title, Legend, HoverTool,
                          NumeralTickFormatter)
from bokeh.models.widgets import Tabs, Panel

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
images_dir = os.path.join(cur_path, 'images')

'''
-------------------------------------------------------------------------------
Create pandas DataFrame and Column Data Source data object
-------------------------------------------------------------------------------
'''
N = 1000
deg_fr = 20
x_min = -4.0
x_max = 4.0
y_min = 0.0
y_max = 1.1 * tdist.pdf(0, deg_fr)
t_stat_vals = np.linspace(x_min, x_max, N)
t_dist_vals = tdist.pdf(t_stat_vals, deg_fr)
t_i = tdist.ppf(0.95, deg_fr)  # test statistic value

t_df = pd.DataFrame(data=np.hstack((t_stat_vals.reshape((N, 1)),
                                    t_dist_vals.reshape((N, 1)))),
                    columns=['t_stat_vals', 't_dist_vals'])
shade_df = t_df[t_df['t_stat_vals'] >= t_i]
t_cds = ColumnDataSource(t_df)
shade_cds = ColumnDataSource(shade_df)

'''
-------------------------------------------------------------------------------
Create figure
-------------------------------------------------------------------------------
'''

fig_title = 't Distribution and p-value'
fig_path = os.path.join(images_dir, 'tdist.html')
fig = figure(title=fig_title,
             plot_height=600,
             plot_width=1000,
             x_axis_label='t-statistic',
             x_range=(x_min, x_max),
             y_axis_label='pdf f(t|df)',
             y_range=(y_min, y_max),
             toolbar_location=None)

# Output to HTML file
output_file(fig_path, title=fig_title)

# Set title font size and axes font sizes
fig.title.text_font_size = '15.5pt'
fig.xaxis.axis_label_text_font_size = '12pt'
fig.xaxis.major_label_text_font_size = '12pt'
fig.yaxis.axis_label_text_font_size = '12pt'
fig.yaxis.major_label_text_font_size = '12pt'

# Modify tick intervals for X-axis and Y-axis
fig.xaxis.ticker = SingleIntervalTicker(interval=10, num_minor_ticks=1)
# fig.xgrid.ticker = SingleIntervalTicker(interval=10)
# fig.xaxis.major_label_overrides = dict(zip([0, t_i], ['0', '|t_i|']))
fig.yaxis.ticker = SingleIntervalTicker(interval=0.1, num_minor_ticks=2)
fig.ygrid.ticker = SingleIntervalTicker(interval=10)

# Plotting the line
fig.line(x='t_stat_vals', y='t_dist_vals', source=t_cds, color='black',
            line_width=3)

# Create vertical dotted line at 0
fig.segment(x0=0, y0=0, x1=0, y1=tdist.pdf(0, deg_fr), color='black',
            line_dash='3 3', line_width=1)

# Create vertical dotted line at |t_i| such that 1-F(t_i|deg_fr) = 0.05
fig.segment(x0=t_i, y0=0, x1=t_i, y1=tdist.pdf(t_i, deg_fr), color='black',
            line_dash='6 2', line_width=3)

# Shade in the area under the curve to the right of the test statistic
fig.varea(x='t_stat_vals', y1='t_dist_vals', y2=0, source=shade_cds,
          color='#C584DB')

# Create describing the p-value
label_pv = Label(x=t_i + 0.5, y=0.07, x_units='data', y_units='data',
                 text='p-value = P[t > abs(t_i)]')
fig.add_layout(label_pv)

# Turn off scrolling
fig.toolbar.active_drag = None

# Display the generated figure
show(fig)
