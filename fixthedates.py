#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def datetime(x):
    return np.array(x, dtype=np.datetime64)

def fix_dates(listIn):
    listIn = [d.replace(' januari ', '-01-') for d in listIn]
    listIn = [d.replace(' februari ', '-02-') for d in listIn]
    listIn = [d.replace(' mars ', '-03-') for d in listIn]
    listIn = [d.replace(' april ', '-04-') for d in listIn]
    listIn = [d.replace(' maj ', '-05-') for d in listIn]
    listIn = [d.replace(' juni ', '-06-') for d in listIn]
    listIn = [d.replace(' juli ', '-07-') for d in listIn]
    listIn = [d.replace(' augusti ', '-08-') for d in listIn]
    listIn = [d.replace(' september ', '-09-') for d in listIn]
    listIn = [d.replace(' oktober  ', '-10-') for d in listIn]
    listIn = [d.replace(' november ', '-11-') for d in listIn]
    listIn = [d.replace(' december ', '-12-') for d in listIn]
    listIn = [d.replace(' ', '') for d in listIn]
    listIn = pd.to_datetime(listIn, format='%-d %m %Y', dayfirst=True, infer_datetime_format=True)
    return listIn


def fix_mondays(listIn):
    listIn = listIn[listIn.weekday==0]
    return listIn