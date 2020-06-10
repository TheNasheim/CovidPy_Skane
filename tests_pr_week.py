# coding=utf-8
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis
from bokeh.transform import dodge


def tests_pr_week():
    excel_file = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/prover-per-vecka.xlsx'
    excel_file2 = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/konstaterade-per-vecka.xlsx'

    ppv = pd.read_excel(excel_file, sheet_name='Blad1',
                        usecols=['Unnamed: 0', 'Vård- och omsorgspersonal', 'Patienter och boende'])
    kpv = pd.read_excel(excel_file2, sheet_name='Blad1', usecols=['Unnamed: 0', 'Konstaterad vård- och omsorgspersonal',
                                                                  'Konstaterade patienter och övriga'])

    ppv.rename(columns={'Unnamed: 0': 'Vecka'}, inplace=True)
    kpv.rename(columns={'Unnamed: 0': 'Vecka'}, inplace=True)
    vecka = ppv['Vecka'].tolist()
    vard = ppv['Vård- och omsorgspersonal'].tolist()
    vard = [int(i) for i in vard]
    patient = ppv['Patienter och boende'].tolist()
    patient = [int(i) for i in patient]
    konstvard = kpv['Konstaterad vård- och omsorgspersonal'].tolist()
    konstvard = [int(i) for i in konstvard]
    konstpatient = kpv['Konstaterade patienter och övriga'].tolist()
    konstpatient = [int(i) for i in konstpatient]

    totweek = np.array(vard) + np.array(patient)
    totprov = []
    total = 0
    for i in range(len(totweek)):
        total += totweek[i]
        totprov.append(total)

    totweek2 = np.array(konstvard) + np.array(konstpatient)
    totkonst = []
    total = 0
    for i in range(len(totweek2)):
        total += totweek2[i]
        totkonst.append(total)

    prov_omraden = ['vardprov', 'patientprov']
    konst_omraden = ['konstvard', 'konstpatient']
    prov_legend_avdel = ['Vård- och omsorgspersonal', 'Patienter och boende']
    konst_legend_avdel = ['Konstaterad vård- och omsorgspersonal', 'Konstaterade patienter och övriga']
    colors = ["#5069c8", "#bfc8f6"]

    colors2 = ["#c75650", "#f5c2bf"]

    data = {'vecka': vecka,
            'vardprov': vard,
            'patientprov': patient,
            'totweekprov': totweek,
            'totprov': totprov,
            'konstvard': konstvard,
            'totweekkonst': totweek2,
            'konstpatient': konstpatient,
            'totkonst': totkonst
            }

    tooltips = [
        ("Vecka", "@vecka"),
        ("--------------Prover--------------", ""),
        ("Patienter och boende", "@patientprov"),
        ("Vård- och omsorgspersonal", "@vardprov"),
        ("Totalt antal tagna prover", "@totweekprov"),
        ("-----------Konstaterade-----------", ""),
        ("Konstaterade patienter och övriga", "@konstpatient"),
        ("Konstaterad vård- och omsorgspersonal", "@konstvard"),
        ("Totalt antal konstaterade", "@totweekkonst")
    ]

    p = figure(y_range=(0, max(totweek) * 1.2), x_range=vecka, plot_height=300, plot_width=670,
               title="Prover tagna och konstaterade. Uppdateras varje onsdag",
               tooltips=tooltips,
               toolbar_location=None, tools="")

    p.vbar_stack(prov_omraden, x=dodge('vecka', -0.22, range=p.x_range), width=0.4, color=colors, source=data,
                 legend_label=["%s" % x for x in prov_legend_avdel])
    p.yaxis.axis_label = 'Prover vecka'
    p.legend.background_fill_alpha = 0.2
    p.legend.border_line_alpha = 0.0
    p.extra_y_ranges["dtot"] = Range1d(start=0, end=max(totweek) * 1.2)
    p.add_layout(LinearAxis(y_range_name="dtot", axis_label="Konstaterade vecka"), 'right')
    p.vbar_stack(konst_omraden, x=dodge('vecka', 0.22, range=p.x_range), width=0.4, color=colors2, source=data,
                 legend_label=["%s" % x for x in konst_legend_avdel])

    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1
    p.legend.location = "top_left"
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    return p
