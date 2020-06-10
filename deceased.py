# coding=utf-8

import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models import Range1d, LinearAxis, RangeTool, HoverTool, FixedTicker
from bokeh.layouts import column
from datetime import timedelta
from fixthedates import *


def deceased_cases():
    dec_cases_excel = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/avlidna-per-dag.xlsx'

    apd = pd.read_excel(dec_cases_excel, sheet_name='Blad1', usecols="A:F")
    apd.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
    apd.dropna()
    date = apd['Date'].copy().tolist()
    date = fix_dates(date)
    tickers = fix_mondays(date).astype(int) / 10 ** 6
    tot = apd['Totalt antal avlidna i Skåne'].tolist()
    tot = [int(i) for i in tot]

    totps = apd['Totalt antal avlidna på sjukhus'].tolist()
    totps = [int(i) for i in totps]
    dagps = apd['Dagligt antal avlidna på sjukhus'].tolist()
    dagps = [int(i) for i in dagps]

    totus = apd['Totalt antal avlidna utanför sjukhus'].tolist()
    totus = [int(i) for i in totus]
    dagus = apd['Dagligt antal avlidna utanför sjukhus'].tolist()
    dagus = [int(i) for i in dagus]

    legend_cases = ['Dagligt antal avlidna på sjukhus', 'Dagligt antal avlidna utanför sjukhus']
    vart = ['Daps', 'Daus']
    colors = ["#5069c8", "#bfc8f6"]

    data = {
        'Date': datetime(date),
        'Tot': tot,
        'Totps': totps,
        'Daps': dagps,
        'Totus': totus,
        'Daus': dagus}

    min_x_range = max(date) - timedelta(days=30)
    max_x_range = max(date) + timedelta(days=1)

    p = figure(y_range=(0, max(max(totps), max(totus)) * 1.1), title="Avlidna per dag", x_axis_type='datetime',
               x_range=(min_x_range, max_x_range),
               plot_width=950, tools="xpan", plot_height=300, x_axis_location="above")

    p.add_tools(HoverTool(
        tooltips=[
            ('Datum', '@Date{%F}'),
            ('Totalt antal avlidna i Skåne', '@Tot'),
            ('Totalt antal avlidna på sjukhus', '@Totps'),
            ('Totalt antal avlidna utanför sjukhus', '@Totus'),
            ('Dagligt antal avlidna på sjukhus', '@Daps'),
            ('Dagligt antal avlidna utanför sjukhus', '@Daus'),
        ],
        formatters={
            '@Date': 'datetime'
        }))

    p.xaxis.axis_label = 'Datum'
    p.xaxis.ticker = FixedTicker(ticks=list(tickers))
    p.yaxis.axis_label = 'Totala Fall'
    p.toolbar_location = None
    p.grid.grid_line_alpha = 0.3

    p.extra_y_ranges["dfall"] = Range1d(start=0, end=max(data['Daps']) + max(data['Daus']))
    p.vbar_stack(vart, x='Date', y_range_name="dfall", width=60000000, color=colors, source=data,
                 legend_label=["%s" % x for x in legend_cases])
    p.add_layout(LinearAxis(y_range_name="dfall", axis_label="Dagliga Fall"), 'right')

    p.line(y='Totps', x='Date', color="#5069c8", legend_label="Totalt antal avlidna på sjukhus", source=data)
    p.line(y='Totus', x='Date', color="#c75650", legend_label="Totalt antal avlidna utanför sjukhus", source=data)

    p.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"])
    p.legend.location = "top_left"
    p.legend.background_fill_alpha = 0.2
    p.legend.border_line_alpha = 0.0

    select = figure(title="Dra i mitten eller kanterna av rutan för att ändra ovan",
                    plot_height=130, plot_width=950, y_range=p.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line('Date', 'Totps', color="#5069c8", source=data)
    select.line('Date', 'Totus', color="#c75650", source=data)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool
    select.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"])

    return column(p, select)

