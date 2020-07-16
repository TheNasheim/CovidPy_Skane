import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, LinearAxis


def tests_pr_week():
    excelfile = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/prover-och-fall-per-vecka.xlsx'

    pofpv = pd.read_excel(excelfile, sheet_name='Blad1',
                          usecols=['Unnamed: 0', 'Antal provtagna', 'Antal personer med konstaterad covid-19'])

    pofpv.rename(columns={'Unnamed: 0': 'Vecka'}, inplace=True)
    vecka = pofpv['Vecka'].tolist()
    prov = pofpv['Antal provtagna'].tolist()
    prov = [int(i) for i in prov]
    konstaterade = pofpv['Antal personer med konstaterad covid-19'].tolist()
    konstaterade = [int(i) for i in konstaterade]

    data = {'vecka': vecka,
            'prover': prov,
            'konstaterade': konstaterade,
            }

    source = ColumnDataSource(data=data)

    tooltips = [
        ("Vecka", "@vecka"),
        ("--------------Prover--------------", ""),
        ("Antal provtagna", "@prover"),
        ("-----------Konstaterade-----------", ""),
        ("Antal personer med konstaterad covid-19", "@konstaterade"),
    ]

    p = figure(y_range=(0, max(prov) * 1.15), x_range=vecka, plot_height=300, plot_width=950,
               title="Prover tagna och konstaterade. Uppdateras 1ggr/vecka",
               tooltips=tooltips,
               toolbar_location=None, tools="")

    p.vbar(x='vecka', width=0.7, top='prover', color="#bfc8f6", source=source,
           legend_label="Antal provtagna")
    p.yaxis.axis_label = 'Prover vecka'
    p.legend.background_fill_alpha = 0.2
    p.legend.border_line_alpha = 0.0

    p.extra_y_ranges["weekcase"] = Range1d(start=0, end=max(konstaterade) * 1.15)
    p.line(y='konstaterade', x='vecka', color="red", y_range_name="weekcase",
           legend_label="Totalt antal personer med konstaterad covid-19", source=source)

    p.add_layout(LinearAxis(y_range_name="weekcase", axis_label="Konstaterad med covid-19"), 'right')

    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1
    p.legend.location = "top_left"
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None

    return p
