#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import maxent as m
import stopwordremoval as s
import removetag as r
import dbmodel as d
import func as f
from datetime import datetime
import calendar as c


def execute(month, year):
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Bedakan data yang digunakan untuk training iis dan proses ner, karena prosesnya juga berbeda
	# misal pada training IIS Yogyakarta/LOC masih tetap di pertahankan, 
	# akan tetapi pada NER menjadi Yogyakarta LOC (atau dihilangkan simbol /)
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	#create object class maxent
	classify = m.Maxent()

	#create object class stopword removal
	stopword = s.StopwordRemoval()

	#create object class remove tag
	tag = r.RemoveTag()

	#create object class independent function
	func = f.Func()

	#create object class database model
	dbmodel = d.DBModel()

	now = datetime.now()

	now_date_day = now.day
	# [0:3] mencetak char 0 sampai 3
	date_month = (now.strftime("%B"))[0:3]

	#+++++++++++++++++++++++++++++++++++++
	#CUSTOM
	month_of_get_data = "%s_ner"%month

	db_insert_ner = "%s_ner"%year

	collection_insert_ner = month.replace("_" + year, "")
	#+++++++++++++++++++++++++++++++++++++

	#print date_month
	for date_day in range(1, 32):
		#documents = dbmodel.get_data(date_month, date_day)
		day = ""
		day_str = str(date_day)
		if len(day_str) == 1:
			day = "0"+day_str
		else:
			day = day_str

		documents = dbmodel.get_data_unique_ner(month_of_get_data, day)

		
		if documents:
			#datas = documents["result"]
			for result in documents:
				#print result
				#ambil data index 0 atau ambil satu data dari group
				arr_url = []
				for arr in result["data"]:
					arr_url.append(arr["url"])
				#ambil salah satu tweet
				data = result["data"][0]
				#=======================================================
				#masukan url tweet yang sama kedalam array url_duplicate
				data["url_duplicate"] = arr_url
				#=======================================================
				time = data["time"]
				print "time in data", time
				date = time.split(" ")
				date_in_int = 0
				result_month = month
				if len(date[0]) == 3:
					date_in_int = int(date[1])
					result_month = date[0].title()
				else:
					date_in_int = int(date[0])
					result_month = date[1].title()
				#fill date in int
				data["day"] = date_in_int
				abbr_to_num = {name: num for num, name in enumerate(c.month_abbr) if num}
				data["month"] = abbr_to_num[result_month]

				if len(date) == 3:
					data["year"] = date[2]
				else:
					data['year'] = year
				insert_document = dbmodel.bulk_insert(db_insert_ner, collection_insert_ner, data)
				print "%s inserted to ner"%insert_document

	return True