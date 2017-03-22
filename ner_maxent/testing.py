#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from nltk import word_tokenize
import dbmodel as d
from decimal import Decimal

#create object class database model
class Testing:

	dbmodel = d.DBModel()

	def test_from_db(self, data_train, data_test):
		dbmodel = d.DBModel()

		db_source = data_train
		db_testing = data_test


		tp = 0
		fp = 0
		fn = 0
		tn = 0
		sentences = 0
		labels_training = 0
		labels_test = 0
		for date_day in range(1,32):
			day = ""
			day_str = str(date_day)
			if len(day_str) == 1:
				day = "0"+day_str
			else:
				day = day_str

			cursor = dbmodel.get_data_all(db_source,day);
			for doc in cursor :
				sentences+=1
				cur = dbmodel.get_data_one_from_id(db_testing, day, doc["id"])
				for doc2 in cur:
					data_label = doc["text_tweet"]
					data_test = doc2["text_tweet"]
					token_label = word_tokenize(data_label)
					token_test = word_tokenize(data_test)
					if(len(token_label) == len(token_test)):
						for index, label in enumerate(token_label):
							arr_lab = token_label[index].split("/")
							arr_test = token_test[index].split("/")
							if arr_lab[0] == arr_test[0]:
								if ("/" in token_label[index]):
									labels_training+=1
									token_label[index] = arr_lab[0].lower()+"/"+arr_lab[1]	
									if (token_label[index] == token_test[index]):
										# terpilih benar
										labels_test+=1
										tp+=1
									elif ("/" in token_label[index]) and ("/" not in token_test[index]):
										# tidak terpilih padahal benar
										fn+=1
									elif ("/" in token_test[index]) and (arr_test[1] != arr_lab[1]):
										# terpilih tetapi tidak benar
										labels_test+=1
										fp+=1

									else:
										# tidak terpilih dan tidak benar (TIDAK DIPAKAI)
										tn+=1
								else:
									if (("/" in token_test[index]) and ("/" not in token_label[index])):
										# terpilih tetapi tidak benar
										labels_test+=1
										fp+=1
		p = Decimal(tp/Decimal((tp+fp)))
		r = Decimal(tp/Decimal((tp+fn)))
		fm = 2*((p*r)/(r+p))

		result  = {}
		result["SENTENCES"] = sentences
		result["LABEL_TRAINING"] = labels_training
		result["LABEL_TEST"] = labels_test
		result["TP"] = tp 
		result["FP"] = fp
		result["FN"] = fn
		result["PRECISION"] = p.normalize()
		result["RECALL"] = r.normalize()
		result["F-MEASURE"] = fm.normalize()		

		return result
