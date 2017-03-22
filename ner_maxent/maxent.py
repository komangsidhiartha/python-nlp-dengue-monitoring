#!/usr/bin/python
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import MaxentClassifier, classify
import maxent_classify
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from pymongo import MongoClient
import numpy as np
import feature as f
import func
import regexp as regx
import string
import re
import gazetter as g
import sys

class Maxent:
	#regex find word (w) and label (lbl), especially in data train
	w = regx.w
	lbl = regx.lbl

	#call class function
	func = func.Func()

	#call class steming
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()

	#mongodb connection
	client = MongoClient()
	db = client.indo_db
	gaz_o = g.gaz_o

	# maxent_classify = maxent_classify.Maxent_Classify()

	def binary_feature(self, sentence, type_feature):
		self.sentence = sentence
		#define unclean temporary array data train and label
		train = []
		#jika training iis maka lakukan pencarian binary feature dengan label
		#contoh : (dict(f1=0, f2=0, f3=0, f4=0, f5=1, f6=0, f7=1}, "NUM"))
		if type_feature == "train_iis":
			for index, data in enumerate(sentence): 
				label = []
				token = word_tokenize(data)
				for index, data in enumerate(token):
					if "/" in data :
						#add label to array
						label.append(self.lbl.search(token[index]).group(1))
						#add word to array
						token[index] = self.w.search(token[index]).group(1)
					else:
						label.append("O")
				for index, data in enumerate(token):
					#feature processing panggil class feature
					featuretrain = f.Feature()
					result = featuretrain.template_feature(token, label, index)
					#result = template_feature(token, label, index)
					train.append(result) 
		else:
			#jika anotasi ner maka hanya melakukan pencarian binary feature, tidak dengan label
			#contoh : (dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=1}))
			token = word_tokenize(sentence)
			label = []
			for index, data in enumerate(token):
				#feature processing panggil class feature
				featuretrain = f.Feature()
				result = featuretrain.template_feature(token, label, index)
				#result = template_feature(token, label, index)
				train.append(result) 
		# filter array empty/none karena Other atau entitas O tidak diproses
		train_set = filter(None, train)
		return train_set

	def training_weight_iis(self, paragraph, min_lldelta=None):
		train = []
		for index, data in enumerate(paragraph):
			sentence = sent_tokenize(data)
			# Pemecahan paragraf kedalam kalimat
			for index, data in enumerate(sentence):	
				sent_lower = data.lower()
				tokenize = word_tokenize(sent_lower)
				div_sentence = []
				for data in tokenize:
					if "/" not in data:
						# ubah menjadi kata dasar
						sent_stem = self.stemmer.stem(data)
						data = sent_stem
					elif "/con" in data:
						# ubah menjadi kata dasar kemudian dicocokan kedalam gazeter kondisi
						sent_stem = self.stemmer.stem(self.w.search(data).group(1))
						data = sent_stem+"/CON"
					elif "/" in data:
						word = self.w.search(data).group(1)
						label = self.lbl.search(data).group(1)
						data = word+"/"+label.upper()
					div_sentence.append(data)
				train.append(" ".join(div_sentence))

		#melakukan training dengan sentence yang sudah diubah kedalam kata dasar

		me_classifier = MaxentClassifier.train(self.binary_feature(train, "train_iis"), algorithm='iis', trace=100, max_iter=2000, min_lldelta=min_lldelta)
		# me_classifier = MaxentClassifier.train(self.binary_feature(train, "train_iis"), algorithm='iis', trace=100, max_iter=2000, min_ll=0.1)
		return me_classifier

	def training_ner(self, paragraph, classification):
		sentence = sent_tokenize(paragraph)
		#print paragraph
		
		#result = []
		train = []
		sentence_ne = ""
		# 1. Pemecahan paragraf kedalam kalimat
		for index, data in enumerate(sentence):	
			tokenize = word_tokenize(data)
			div_sentence = []
			for word in tokenize:
				#check_kota = len(list(self.db.cities.find({"kota":re.compile("^"+word+"$", re.IGNORECASE)})))>=1
				check_kota = (self.db.location.find({"$text": {"$search": word.lower()}}).count())>=1
				# print "word : %s, check : %s"%(word,check_kota) 
				if not check_kota and word not in self.gaz_o:
					#apabila kata bukan kota maka dibuat kata dasar
					sent_stem = self.stemmer.stem(word)
					word = sent_stem
				div_sentence.append(word)
			train.append(" ".join(div_sentence))
			#ket parameter : self.div_sentence_ner(kalimat_dengan_kata_dasar, kalimat_asli, jenis_klasifikasi) 
			sentence_ne = self.div_sentence_ner("".join(train), " ".join(tokenize), classification)
			#result.append(sentence_ne)
			#reset array train agar tidak diikutkan training ner
			train = []

		return sentence_ne

	def div_sentence_ner(self, sentence_stem, sentence_unstem, classification):
		#kalimat sudah dicari kata dasar
		sentence_stem = sentence_stem.lower()
		sent_stem_conv = self.func.terbilang_to_number(sentence_stem)

		#kalimat asli (tidak di jadikan kata dasar)
		sentence_unstem = sentence_unstem.lower()
		sent_unstem_conv = self.func.terbilang_to_number(sentence_unstem)

		featureset = self.binary_feature(sent_stem_conv, "train_ner")
		# ==== from nltk
		# self.maxent_classify.classifier = classification
		# ==== end from nltk

		# ==== from nltk
		self.classification = classification
		# ==== end bymyself
		token = word_tokenize(sent_unstem_conv)

		entity = ["ORG", "LOC", "NUM", "CON"]
		temp_sentence = []

		# create array object result untuk penampung array balikan
		result = {} 

		result_entity = {}
		result_index_entity = {}
		
		temp_entity = []

		for index, feature in enumerate(featureset):
			#print token[index]
			#print index
			if sum(feature.values()) != 0:
				# print classification.explain(feature, columns=5)
				# print classification.labels()
				# print feature
				print ' '*20+'%s' %token[index]
				#jika bukan other atau sum feature tidak sama dengan 0
				print ' '*4+'p(ORG)      p(LOC)      p(NUM)      p(CON)'
				print '-'*(28+24)
				# ==== from nltk
				pdist = classification.prob_classify(feature)
				# pclass = classification.classify(feature)
				# print pclass
				# print pdist.samples()
				# print pdist.logprob('ORG')
				en = np.array([pdist.prob('ORG'), pdist.prob('LOC'), pdist.prob('NUM'), pdist.prob('CON')])
				# ==== end from nltk

				# ==== by myself
				# pdist = self.maxent_classify.pdist(feature)
				# en = np.array([pdist['ORG'], pdist['LOC'], pdist['NUM'], pdist['CON']])
				# ==== end bymyself
				en_index = np.argmax(en)
				print en
				print

				temp_position = []
				if "/" not in token[index]:
					#replace word original with word label
					temp_replace = token[index].replace(token[index], token[index]+"/"+entity[en_index])
					#apabila entitas maka append
					temp_sentence.append(temp_replace)

					if token[index] in result_index_entity :
						result_index_entity[token[index]].append(index)
					else :
						temp_position.append(index)
						result_index_entity[token[index]] = temp_position

					if entity[en_index] in result_entity:
						#apabila index array entitas didalam result entitas, maka ambil array entitas tersebut, kemudian tambahkan data baru
						data = result_entity[entity[en_index]]
						data.append(token[index])
					else:
						#apabila ada entitas baru maka kosongkan array dan buat index array baru
						temp_entity = []
						temp_entity.append(token[index])
						result_entity[entity[en_index]] = temp_entity
			else:
				#apabila bukan entitas maka append
				temp_sentence.append(token[index])

			#print " ".join(temp_sentence)
			sentence = " ".join(temp_sentence)

		result["text_tweet"] = sentence
		result["entity"] = result_entity
		result["entity_position"] = result_index_entity
		
		#print result
		return result
