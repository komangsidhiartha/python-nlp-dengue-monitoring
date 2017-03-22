#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import maxent as m
import stopwordremoval as s
import removetag as r
import regexp as regx
import dbmodel as d
import func as f


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Bedakan data yang digunakan untuk training iis dan proses ner, karena prosesnya juga berbeda
# misal pada training IIS Yogyakarta/LOC masih tetap di pertahankan, 
# akan tetapi pada NER menjadi Yogyakarta LOC (atau dihilangkan simbol /)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#create object class maxent
classify = m.Maxent()

#create object class independent function
func = f.Func()

#create object class database model
dbmodel = d.DBModel()

#--------------------------------------------------------------------------
# open hasil training iis
#--------------------------------------------------------------------------
classifier = func.open_file('train.pickle')
# classifier.show_most_informative_features()
# print classifier

def execute(month):

	# define month clean
	month_data_preprocessor = "%s_clean"%month

	# define month ner
	month_data_ner = "%s_ner"%month

	db_location = "indo_db"
	location_collection = "location"

	#setting combination str match
	combination_match_string = True

	# --------------------------------------------------------------------------
	# NER
	# --------------------------------------------------------------------------
	for date_day in range(1,32):
		day = ""
		day_str = str(date_day)
		if len(day_str) == 1:
			day = "0"+day_str
		else:
			day = day_str

		cursor_get_data_preprocessor = dbmodel.get_data_preprocessor(month_data_preprocessor,day)
		for document in cursor_get_data_preprocessor:
			data = document["data"]

			for sentences in data :
				sentence = sentences["text_tweet"]
				if sentence :
					print sentences["id"]
					ner = classify.training_ner(sentence.encode("utf8"), classifier)

					if combination_match_string == True:
						sentence_ne = ner["text_tweet"]
						entity_position = ner["entity_position"]
						if "LOC" in ner["entity"]:
							# ========================================= clearence not location ========================================
							entity_location = ner["entity"]["LOC"]

							temp_location = dbmodel.is_candidate_loc(db_location, location_collection, entity_position, entity_location)
							loc_clear = dbmodel.is_real_loc(db_location, location_collection, temp_location)
							sentence_ne = dbmodel.ner_replace_loc(sentence_ne, loc_clear)
							# ========================================= end clearence not location ====================================
						if "CON" in ner["entity"] :
							if "sakit" in ner["entity"]["CON"]:
								sentence_ne = dbmodel.validation_CON(sentence_ne, "sakit")
					else:
						sentence_ne = ner["text_tweet"]

					ner["id"] = sentences["id"]
					ner["url"] = sentences["url"]
					ner["username"] = sentences["username"]
					ner["text_tweet"] = sentence_ne
					ner["time"] = sentences["time"]
					# if ner and ("/NUM" in sentence_ne and "/LOC" in sentence_ne):
						# apabila array ner tidak kosong dan berisikan entitas NUM dan LOC maka jalankan statement berikut
					cursor_insert_data = dbmodel.insert_ner_to_db(month_data_ner, day, ner)
					print cursor_insert_data
	return True