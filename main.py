# coding=utf-8
# !/usr/bin/env python

from header import *
from tot_reported_cases import *
from municipalities_cases import *
from cases_gender_and_age import *
from hospitalized import *
from tests_pr_week import *
from deceased import *

from bokeh.layouts import layout
from bokeh.plotting import output_file, show

output_file('index.html', 'Lägesbild COVID-19 i Skåne', mode="cdn")

i1 = info_head()
p1 = tot_reported_cases()
p2 = municipalities_cases()
p3 = cases_gender_and_age()
p4 = hospitalized()
p5 = tests_pr_week()
p6 = deceased_cases()
lay = layout([i1], [p1], [p2, [p4, p3, p5]], [p6])
lay.spacing = 0
show(lay)
