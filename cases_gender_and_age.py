# coding=utf-8
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge

def cases_gender_and_age():
    covid_age_gender = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/sjukdomsfall-per-alder-kon.xlsx'

    cag = pd.read_excel(covid_age_gender, sheet_name='Antal', usecols=['Unnamed: 0', 'Män', 'Kvinnor'])
    cag.rename(columns={'Unnamed: 0': 'Ålder'}, inplace=True)
    cag = cag.dropna(subset=['Ålder'])
    cag['Ålder'] = cag['Ålder'].replace({'90 år eller äldre': '90 >'})
    cag = cag.replace({',': '.'})
    ages = cag['Ålder'].tolist()

    men = cag['Män'].tolist()
    men = [int(i) for i in men]
    women = cag['Kvinnor'].tolist()
    women = [int(i) for i in women]

    data = {'ages': ages,
            'men': men,
            'women': women, }

    source = ColumnDataSource(data=data)

    tooltips = [
        ("Ålder", "@ages"),
        ("Antal Män", "@men"),
        ("Antal Kvinnor", "@women"), ]

    p = figure(x_range=ages, plot_height=250, plot_width=670,
               title="Sjukdomsfall per ålder och kön. Uppdateras 1ggr/vecka",
               toolbar_location=None, tooltips=tooltips, tools="")

    p.vbar(x=dodge('ages', -0.15, range=p.x_range), top='men', width=0.3, source=source,
           color="#abb7ed", legend_label="Antal Män")

    p.vbar(x=dodge('ages', 0.15, range=p.x_range), top='women', width=0.3, source=source,
           color="#5069c8", legend_label="Antal Kvinnor")

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "vertical"
    return p


