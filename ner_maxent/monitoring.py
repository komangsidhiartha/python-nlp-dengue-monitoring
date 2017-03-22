#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import preprocessor
import ner
import ner_pasing_to_month as npm
import fwc_data_preparation as fwc

def execute(month, year):
	preprocessor_process = preprocessor.execute(month, year, "ner")
	ner_process = ner.execute(month)
	npm_process = npm.execute(month, year)
	fwc_process = fwc.execute(month, year)

	if preprocessor_process:
		print "preprocessor success"
	else:
		print "preprocessor failed"

	if ner_process:
		print "ner success"
	else:
		print "ner failed"

	if npm_process:
		print "data parse to month success"
	else:
		print "data parse to month failed"

	if fwc_process :
		print "unique data success"
	else:
		print "unique data failed"

	if preprocessor_process and ner_process and npm_process and fwc_process:
		print "Monitoring DBD Bulan %s Tahun %s Success"%(month,year)
	else:
		print "Monitoring DBD Bulan %s Tahun %s FAILED"%(month,year)
