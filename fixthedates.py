#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def datetime(x):
    return np.array(x, dtype=np.datetime64)


def fix_dates(listin):
    listin = [d.replace(' januari ', '-01-') for d in listin]
    listin = [d.replace(' februari ', '-02-') for d in listin]
    listin = [d.replace(' mars ', '-03-') for d in listin]
    listin = [d.replace(' april ', '-04-') for d in listin]
    listin = [d.replace(' maj ', '-05-') for d in listin]
    listin = [d.replace(' juni ', '-06-') for d in listin]
    listin = [d.replace(' juli ', '-07-') for d in listin]
    listin = [d.replace(' augusti ', '-08-') for d in listin]
    listin = [d.replace(' september ', '-09-') for d in listin]
    listin = [d.replace(' oktober  ', '-10-') for d in listin]
    listin = [d.replace(' november ', '-11-') for d in listin]
    listin = [d.replace(' december ', '-12-') for d in listin]
    listin = [d.replace(' ', '') for d in listin]
    listin = pd.to_datetime(listin, format='%-d %m %Y', dayfirst=True, infer_datetime_format=True)
    return listin


def fix_mondays(listin):
    listin = listin[listin.weekday == 0]
    return listin
