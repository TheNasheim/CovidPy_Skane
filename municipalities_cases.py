# coding=utf-8

import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

def municipalities_cases():
    excelFile = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/antal-fall-per-kommun.xlsx'

    afpk = pd.read_excel(excelFile, sheet_name='Blad1', usecols=['Kommun', 'Antal fall'])
    afpk = afpk.iloc[::-1]
    afpk = afpk.dropna(subset=['Kommun', 'Antal fall'])
    af = afpk['Antal fall'].copy()
    symbols = '<'
    af = [str(item).translate(symbols).strip() for item in af]
    af = fix_values(af)
    source = ColumnDataSource(data={
        'Kommun': afpk['Kommun'],
        'Antalfall': af,
        'AntalfallDesc': afpk['Antal fall']
    })

    tooltips = [
        ("Kommun", "@Kommun"),
        ("Antal fall", "@AntalfallDesc"),
    ]

    p = figure(y_range=afpk['Kommun'], plot_width=310, plot_height=850, title="Antal rapporterade fall per kommun", tooltips=tooltips, tools="")

    p.hbar(y='Kommun', left=0, right='Antalfall', height=0.9, color='#94a2e3', source=source)

    p.toolbar_location = None
    p.ygrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1
    return p

def fix_values(listIn):
    for n, i in enumerate(listIn):
        if i == '<10':
            listIn[n] = '5'

    return listIn