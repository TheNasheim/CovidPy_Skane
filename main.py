# coding=utf-8
#!/usr/bin/env python

from tot_reported_cases import *
from municipalities_cases import *
from cases_gender_and_age import *

from bokeh.layouts import layout
from bokeh.plotting import output_file, show

output_file('index.html', 'Lägesbild COVID-19 i Skåne', mode="cdn")

p1 = tot_reported_cases()
p2 = municipalities_cases()
p3 = cases_gender_and_age()
lay = layout([p1], [p2])
lay.spacing = 0
show(lay)