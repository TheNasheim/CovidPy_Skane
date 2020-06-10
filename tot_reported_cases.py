# -*- coding: utf-8 -*-

import pandas as pd
from bokeh.plotting import figure
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models import Range1d, LinearAxis, RangeTool, HoverTool, FixedTicker
from bokeh.layouts import column
from datetime import timedelta
from fixthedates import *


def tot_reported_cases():
    tot_rep_cases = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/totalt-antal-konstaterade-covid-fall.xlsx'

    trc = pd.read_excel(tot_rep_cases, sheet_name='Blad1',
                        usecols=['Unnamed: 0', 'Totalt antal personer med konstaterad covid-19',
                                 'Nya konstaterade personer'])
    trc.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
    trc.dropna()
    date = trc['Date'].copy().tolist()
    date = fix_dates(date)
    tickers = fix_mondays(date).astype(int) / 10 ** 6
    tot = trc['Totalt antal personer med konstaterad covid-19'].tolist()
    tot = [int(i) for i in tot]
    newtoday = trc['Nya konstaterade personer'].tolist()
    newtoday = [int(i) for i in newtoday]

    data = {'Date': datetime(date),
            'Newtoday': newtoday,
            'Tot': tot,
            'Datum': date}

    min_x_range = max(date) - timedelta(days=30)
    max_x_range = max(date) + timedelta(days=1)

    p = figure(y_range=(0, max(tot) * 1.05), title='Totalt antal konstaterade covid fall', x_axis_type='datetime',
               x_range=(min_x_range, max_x_range),
               plot_width=950, tools="xpan", plot_height=300, x_axis_location="above")

    p.add_tools(HoverTool(
        tooltips=[
            ('Datum', '@Date{%F}'),
            ("Nya konstaterade personer", "@Newtoday"),
            ("Totala Fall", "@Tot"),
        ],
        formatters={
            '@Date': 'datetime'
        }))

    p.xaxis.axis_label = 'Datum'
    p.yaxis.axis_label = 'Totala Fall'
    p.toolbar_location = None
    p.grid.grid_line_alpha = 0.3

    p.extra_y_ranges["dailycase"] = Range1d(start=0, end=max(newtoday) * 1.1)
    p.vbar(x='Date', width=60000000, top='Newtoday', y_range_name="dailycase", source=data,
           color="#94a2e3", legend_label="Nya konstaterade personer")
    p.add_layout(LinearAxis(y_range_name="dailycase", axis_label="Dagliga Fall"), 'right')

    p.line(y='Tot', x='Date', color="red", legend_label="Totalt antal personer med konstaterad covid-19", source=data)

    p.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"])

    p.xaxis.minor_tick_line_color = "orange"
    p.xaxis.ticker = FixedTicker(ticks=list(tickers))
    #p.xaxis.ticker = DaysTicker(days=np.arange(1, 32,7))

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

    select.line('Date', 'Tot', source=data)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool
    select.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"])

    return column(p, select)

