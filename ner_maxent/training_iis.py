#!/usr/bin/python

import pickle
import maxent as m
import stopwordremoval as s
import removetag as r
import regexp as regx
import dbmodel as d


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Bedakan data yang digunakan untuk training iis dan proses ner, karena prosesnya juga berbeda
# misal pada training IIS Yogyakarta/LOC masih tetap di pertahankan, 
# akan tetapi pada NER menjadi Yogyakarta LOC (atau dihilangkan simbol /)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def execute(data_bulan, min_lldelta=None):
	#create object class maxent
	classify = m.Maxent()

	#create object class stopword removal
	stopword = s.StopwordRemoval()

	#create object class remove tag
	tag = r.RemoveTag()

	#create object class dbmodel
	dbmodel = d.DBModel()


	#==========================================================================
	# PELATIHAN IIS
	#==========================================================================
	paragraph = []

	count_data_training = 0
	for collection in range(1,32):
		if len(str(collection)) == 1 :
			collection = "0%s"%(str(collection))

		documents = dbmodel.get_data_with_label(data_bulan,str(collection))
		for document in documents:
			# print document
			data = document["_id"]
			if "/" in data:
				count_data_training+=1
				#jika ada label maka lakukan append
	 			paragraph.append(document["_id"].encode("utf8"))
	# --------------------------------------------------------------------------
	# Proses Training IIS
	# --------------------------------------------------------------------------
	print "Jumlah data training : %i"%count_data_training
	if min_lldelta is None:
		min_lldelta = 0.05
	classifier = classify.training_weight_iis(paragraph, min_lldelta)
	#--------------------------------------------------------------------------

	f = open('train.pickle', 'wb')
	pickle.dump(classifier, f)
	f.close()