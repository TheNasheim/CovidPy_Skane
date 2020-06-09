import pandas as pd
import datetime

from bokeh.models.widgets import Div
from bokeh.layouts import row, layout

def info_head():
    reported_cases_excel = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/totalt-antal-konstaterade-covid-fall.xlsx'
    hospitalized_excel = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/inlagda-per-sjukhus.xlsx'
    deceaced_excel = 'https://www.skane.se/globalassets/lagesbild-covid-19-i-skane/avlidna-per-dag.xlsx'

    takcf = pd.read_excel(reported_cases_excel, sheet_name='Blad1',
                        usecols=['Totalt antal personer med konstaterad covid-19', 'Nya konstaterade personer'])
    totrc = takcf['Totalt antal personer med konstaterad covid-19'].tolist()
    totrc = [int(i) for i in totrc]
    totrep = totrc[-1]
    totrep = "{:,}".format(totrep)
    newrc = takcf['Nya konstaterade personer'].tolist()
    newrc = [int(i) for i in newrc]
    newrep = newrc[-1]
    avgrep = sum(newrc[-7:])
    avgrep = round(avgrep / 7, 1)

    ips = pd.read_excel(hospitalized_excel, sheet_name='Blad1',
                        usecols=['Sjukhusort', 'Vårdavdelning', 'Intensivvårdsavdelning', 'TOTALT'])
    ips = ips.dropna(subset=['Sjukhusort', 'Vårdavdelning'])
    ips.drop(ips.loc[ips['Sjukhusort'] == 'TOTALT'].index, inplace=True)
    ips['Intensivvårdsavdelning'] = ips['Intensivvårdsavdelning'].fillna(0)
    vard = ips['Vårdavdelning'].tolist()
    vard = [int(i) for i in vard]
    varden = sum(vard)
    intensiv = ips['Intensivvårdsavdelning'].tolist()
    intensiv = [int(i) for i in intensiv]
    intensiven = sum(intensiv)
    total_hos = ips['TOTALT'].tolist()
    total_hos = [int(i) for i in total_hos]
    tot_hosp = sum(total_hos)

    apd = pd.read_excel(deceaced_excel, sheet_name='Blad1',
                        usecols=['Totalt antal avlidna i Skåne', 'Totalt antal avlidna på sjukhus',
                                 'Totalt antal avlidna utanför sjukhus'])

    dec_tot = apd['Totalt antal avlidna i Skåne'].tolist()
    dec_tot = [int(i) for i in dec_tot]
    totdec = dec_tot[-1]
    dec_totps = apd['Totalt antal avlidna på sjukhus'].tolist()
    dec_totps = [int(i) for i in dec_totps]
    totps = dec_totps[-1]
    dec_totus = apd['Totalt antal avlidna utanför sjukhus'].tolist()
    dec_totus = [int(i) for i in dec_totus]
    totus = dec_totus[-1]

    # initial html text
    template1 = ("""
          <div class='content' style='margin:auto;width:930px;padding:0px;'>
           <p style='text-align:left;margin:0px'><b>Antal fall av covid-19 i Skåne</b> - data hämtas 3 gånger om dagen ifrån <a href="https://www.skane.se/">Region Skåne</a>.
           <span style='float:right;margin:0px'>Senaste data hämtades: {downloadtime}</span></p>
           <hr>
          </div>
          """)
    now = datetime.datetime.now()
    text = template1.format(downloadtime=now.strftime("%Y-%m-%d %H:%M"))
    div_info = Div(text=text, height=25, width=930)

    # initial html text
    template2 = ("""
          <div class='content' style='text-align:center;margin:auto;width:300px;border:0px solid black;padding-left:10px;padding-right:10px;padding-top:0px;'>
           <p class='name' style='text-align:center;margin:auto;width:100%;padding:0px;'><big>Sjukdomsfall</big><br />
           <h2 style='line-height: 20%'>{total_reported}</h2>
           Nya fall: <b>{reported_today}</b> | Genomsnitt på 7 dagar: <b>{reported_avg}</b></p>
          </div>
          """)

    text = template2.format(total_reported=totrep, reported_today=newrep, reported_avg=avgrep)
    tot_cases_info = Div(text=text, height=70, width=305)

    # initial html text
    template3 = ("""
          <div class='content' style='text-align:center;margin:auto;width:300px;border:0px solid black;padding-left:10px;padding-right:10px;padding-top:0px;'>
           <p class='name' style='text-align:center;margin:auto;width:100%;padding:0px;'><big>Inlagda på sjukhus</big><br />
           <h2 style='line-height: 20%'><b>{total_reported}</b></h2>
           Vårdavdelning: <b>{hosp_varden}</b> | Intensivvården: <b>{hosp_intensiven}</b> </p>
          </div>
          """)

    text = template3.format(total_reported=tot_hosp, hosp_varden=varden, hosp_intensiven=intensiven)
    hospitalized_info = Div(text=text, height=70, width=305)

    # initial html text
    template4 = ("""
          <div class='content' style='text-align:center;margin:auto;width:300px;border:0px solid black;padding-left:10px;padding-right:10px;padding-top:0px;'>
           <p class='name' style='text-align:center;margin:auto;width:100%;padding:0px;'><big>Avlidna</big><br />
           <h2 style='line-height: 20%'><b>{total_reported}</b></h2>
           På sjukhus: <b>{hosp_varden}</b> | Utanför sjukhus: <b>{hosp_intensiven}</b> </p>
          </div>
          """)
    # initial text
    text = template4.format(total_reported=totdec, hosp_varden=totps, hosp_intensiven=totus)
    deceased_info = Div(text=text, height=70, width=305)

    # initial html text
    template5 = ("""
          <div class='content' style='margin:auto;width:930px;padding:0px;'>
           <hr>
          </div>
          """)
    # initial text
    text = template5.format()
    spacer = Div(text=text, height=10, width=930)

    ro = row(tot_cases_info, hospitalized_info, deceased_info)
    lay = layout(div_info, ro, spacer)
    return lay


