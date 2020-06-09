# coding=utf-8
import pandas as pd
from bokeh.plotting import figure

def hospitalized():
    excelFile = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/inlagda-per-sjukhus.xlsx'

    ips = pd.read_excel(excelFile, sheet_name='Blad1', usecols="B:E")
    ips = ips.dropna(subset=['Sjukhusort', 'Vårdavdelning'])
    ips.drop(ips.loc[ips['Sjukhusort'] == 'TOTALT'].index, inplace=True)
    ips['Intensivvårdsavdelning'] = ips['Intensivvårdsavdelning'].fillna(0)
    ips.sort_values(by=['Sjukhusort'], inplace=True)
    ips = ips.iloc[::-1]
    sjukhus = ips['Sjukhusort'].tolist()
    vard = ips['Vårdavdelning'].tolist()
    vard = [int(i) for i in vard]
    intensiv = ips['Intensivvårdsavdelning'].tolist()
    intensiv = [int(i) for i in intensiv]
    totala = ips['TOTALT'].tolist()
    totala = [int(i) for i in totala]

    kommuner = ips['Sjukhusort']
    avdelningar = ['vard', 'intensiv']
    legend_avdel = ['Vårdavdelning', 'Intensivvårdsavdelning']
    colors = ["#abb7ed", "#5069c8"]

    data = {'Sjukhusort': sjukhus,
            'vard': vard,
            'intensiv': intensiv,
            'TOTALT': totala, }

    tooltips = [
        ("Sjukhusort", "@Sjukhusort"),
        ("Vårdavdelning", "@vard"),
        ("Intensivvårdsavdelning", "@intensiv"),
        ("Total", "@TOTALT"),
    ]

    p = figure(y_range=kommuner, plot_height=300, plot_width=670, title="Inlagda per sjukhus",
               tooltips=tooltips,
               toolbar_location=None, tools="")

    p.hbar_stack(avdelningar, y='Sjukhusort', height=0.9, color=colors, source=data,
                 legend_label=["%s" % x for x in legend_avdel])

    p.y_range.range_padding = 0.1
    p.ygrid.grid_line_color = None
    p.legend.location = "bottom_right"
    p.legend.orientation = "horizontal"
    p.axis.minor_tick_line_color = None
    p.legend.background_fill_alpha = 0.2
    p.outline_line_color = None
    return p