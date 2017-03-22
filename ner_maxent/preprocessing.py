from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import sent_tokenize, word_tokenize
from pymongo import MongoClient
import removetag as r
import stopwordremoval as s
import func
import gazetter as g

class Preprocessing :
	client = MongoClient()
	db = client.indo_db

	factory = StemmerFactory()
	stemmer = factory.create_stemmer()

	tag = r.RemoveTag()
	stopword = s.StopwordRemoval()
	func = func.Func()

	def string_to_number(self, sentence):
		return self.func.terbilang_to_number(sentence)

	def stopword_removal(self, sentence, condition):
		sentence_clean_tag = self.tag.tag_removal(sentence.encode("utf8"), condition) #clean tag
		return self.stopword.stopword_removal(sentence_clean_tag, condition)

	def stemming(self, paragraph):
		sentence = sent_tokenize(paragraph)
		# train = []
		train = ""
		for index, data in enumerate(sentence):	
			tokenize = word_tokenize(data)
			div_sentence = []
			for word in tokenize:
				check_kota = (self.db.location.find({"$text": {"$search": word.lower()}}).count())>=1
				if not check_kota and word not in g.gaz_o and word not in g.gaz_org and word not in g.gaz_sp and word not in g.gaz_knd:
					#apabila kata bukan kota, organisasi dan kata sambung maka dibuat kata dasar
					sent_stem = self.stemmer.stem(word.encode("utf8"))
					word = sent_stem
				div_sentence.append(word)
			train = " ".join(div_sentence)
			# train.append(" ".join(div_sentence))
		return train

	def process(self, sentence, condition):
		a = sentence.lower()
		b = self.string_to_number(a)
		#bedakan proses training dan anotasi menggunakan condition "ner"/"train"
		c = self.stopword_removal(b, condition)
		d = self.stemming(c)
		return d

# data = Preprocessing()
# kalimat = "tiga warga ya allah moga aku cuma sakit demam biasa aku sangat takutadekku tiga warga sudah rawat rumah sakit positif demam darah"
# kalimat = "Tiga Warga positif dbd  dinkes fogging . -  beonline bit ly 1ebylve"
# print data.process(kalimat, "ner")