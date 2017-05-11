#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
import func as f
import time

class DBModel:

	client = MongoClient()
	func = f.Func()

	def check_like_loc(self, database, collection, search_loc):
		db = self.client[database]
		return (db[collection].find({"$text": {"$search": search_loc}}).count())>=1

	def check_real_loc(self, database, collection, search_loc):
		db = self.client[database]
		return (db[collection].find({"kabupaten":search_loc}).count())>=1 or (db[collection].find({"kecamatan":search_loc}).count())>=1 or (db[collection].find({"desa":search_loc}).count())>=1

	def check_loc_and_date(self, database, collection, location, time):
		db = self.client[database]
		return db[collection].find({"$and":[{"LOC":location},{"time" :time}]}).count() >= 1

	def check_num_in_loc_and_date(self, database, collection, location, incident, time):
		db = self.client[database]
		return db[collection].find({"$and":[{"LOC":location},{"NUM":int(incident)},{"time":time}]}).count() >= 1
			
	def update_data_fwc_push_url_duplicate(self, database, collection, location, incident, time, url):
		db = self.client[database]
		result = db[collection].update(
		   	{"$and":[{"LOC":location},{"NUM":int(incident)},{"time" :time}]},
		    {"$push": {"url_duplicate": url}}
		)

		return result

	def is_candidate_loc(self, db_location, location_collection, arr_entity_position, arr_loc):
		temp_arr_kota = {}

		for loc in arr_loc:
			check_kota = self.check_like_loc(db_location, location_collection, loc)
			# print check_kota
			if check_kota>=1:
				for temp_index_loc in arr_entity_position[loc]:
					temp_arr_kota[loc+"^"+str(temp_index_loc)] = temp_index_loc
		temp_arr_duplicate = self.func.grouping_data_lokasi(temp_arr_kota)
		# print temp_arr_duplicate
		temp_arr_return = []
		for temp_loc in temp_arr_duplicate:
			temp_arr_in_list = []
			for data in temp_loc:
				data_split = data.split("^")
				data = data_split[0]
				temp_arr_in_list.append(data)
			temp_arr_return.append(temp_arr_in_list)

		# print temp_arr_return
		return temp_arr_return

	def ner_replace_loc(self, sentence, locations):
		sentence_replace = sentence.replace("/LOC","")
		# print sentence_replace
		for loc in locations:
			# print loc
			# sentence_return = sentence_replace
			split_loc = loc.split(" ")
			for result_loc_split in split_loc:
				if result_loc_split+"/LOC" not in sentence_replace:
					sentence_replace = sentence_replace.replace(result_loc_split,result_loc_split+"/LOC")
		return sentence_replace

	def is_real_loc(self, db_location, location_collection, arr_loc):
		loc_clear = []
		for location in arr_loc:
			#join kata lokasi yang berdekatan. contoh ("jakarta","selatan") menjadi ("jakarta selatan")
			loc = " ".join(location)
			# print self.check_real_loc(db_location, location_collection, loc)
			if self.check_real_loc(db_location, location_collection, loc):
				loc_clear.append(loc)
		# print loc_clear
		return loc_clear

	def district_check(self, database, collection, location):
		db = self.client[database]
		if db[collection].find({"kabupaten":location}).count() >= 1:
			district = "kabupaten"
		elif db[collection].find({"kecamatan":location}).count() >= 1:
			district = "kecamatan"
		elif db[collection].find({"desa":location}).count() >= 1:
			district = "desa"
		elif db[collection].find({"provinsi":location}).count() >= 1:
			district = "provinsi"
		else:
			district = "other"
		return district

	def top_location_of_month(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate([
				    {"$match":{"district":"kabupaten"}},
				    {"$group":{"_id":"$LOC", "NUM": {"$max":"$NUM"}, 
				                       "data": {
				                                "$push":{
				                                    "NUM":{"$max":'$NUM'}, 
				                                    "date":"$time", 
				                                    "text_tweet":"$text_tweet", 
				                                    "url_duplicate":"$url_duplicate",
				                                    "ORG":"$ORG",
				                                    "CON":"$CON"}
				                                }
				              }
				    },
				    {"$sort":{"NUM":-1}}
				])
		return cursor

	def get_lat_long_location(self, database, collection, location):
		db = self.client[database]
		cursor = db[collection].find({"$and":[{
											"kota":{"$regex":location, "$options":"-i"},
											"populasi": {"$ne":""}
											}]
									})
		return cursor

	def get_data_without_label(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": "$text_tweet", 
				        "data": {
				        	"$push":{
					                "id":"$url", 
					                "url":"$data_id", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "time":"$time_tweet"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor

	def get_data_with_label(self, database, collection):
		db = self.client[database]
		if len(str(collection)) == 1:
			collection="0%s"%(str(collection))
		check_collection = str(collection) in db.collection_names()
		if check_collection:
			cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": "$text_tweet", 
				        "data": {
				        	"$push":{
					                "id":"$id", 
					                "url":"$url", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "time":"$time"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		else:
			cursor = ""

		return cursor


	def get_data_preprocessor(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": "$text_tweet", 
				        "data": {
				        	"$push":{
					                "id":"$id", 
					                "url":"$url", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "time":"$time"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor	

		"""
		#coba get satu DATA
		res = []
		ok = []
		data = {}
		hasil = {}
		tweet = {}
		coba = {}
		#tweet["text_tweet"] = u"G Dana U Demam Berdarah Bupati JOMBANG AKAN BELI 918 Sepeda Motor U Pejabat 10 MILYAR"
		tweet["text_tweet"] = u"portalsurya kasus dbd di jember naik dua kali lipat belum klb"
		ok.append(tweet)
		data["data"] = ok
		res.append(data)
		hasil["result"] = res
		
		return hasil
		"""

		

	def get_data_unique_ner(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		    	{
	                "$match": {
	                            "$and":[{
	                                "entity.LOC": {
	                                  "$exists": "true"
	                                },
	                                "entity.NUM": {
	                                  "$exists": "true"
	                                }
	                            }]
	                      }
	                    },
				        {"$group": 
				        	{"_id": "$text_tweet", 
						        "data": {
						        	"$push":{
							                "id":"$id", 
							                "url":"$url", 
							                "username":"$username", 
							                "text_tweet":"$text_tweet",
							                "entity":"$entity",
							                "entity_position":"$entity_position",
							                "time":"$time"
						                	}
						            	}	
					    		}
				        },
			    { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor	

	def get_data_from_db_ner(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": {"LOC":"$entity.LOC", "NUM":"$entity.NUM"},
				        "data": {
				        	"$push":{
					                "id":"$id", 
					                "url":"$url", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "url_duplicate":"$url_duplicate",
					                "entity":"$entity",
					                "entity_position":"$entity_position",
					                "time":"$time"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate berdasarkan LOC (Lokasi) dan NUM (Jumlah Penderita)
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor

	def get_data_all(self, database, collection):
		db = self.client[database]
		cursor = db[collection].find({})

		return cursor

	def get_data_one_from_id(self, database, collection, id):
		db = self.client[database]
		if db["mar_ner_maxent"].find({"id":id}) >= 1:
			cursor = db[collection].find({"id":id})
		else:
			cursor = ""

		return cursor

	def bulk_insert(self, database, collection, documents):
		db = self.client[database]
		results = db[collection].insert(documents)

		return results

	def many_insert(self, database, collection, documents):
		db = self.client[database]
		results = db[collection].insert_many(documents)

		return results.inserted_ids

	def insert_sentence_clean(self, database, collection, document):
		result = {}
		db = self.client[database]
		if not document['text_tweet']:
			result = "bukan data %s (warn), tidak masuk" %document["id"]
		else:
			db[collection].insert(document)
			keterangan = "data %s (inserted sentence clean into database %s collection %s)"%(document["id"],database,collection)
			sentence = document["text_tweet"]
			result["keterangan"] = keterangan
			result["document"] = sentence
			
		return result

	def insert_ner_to_db(self, database, collection, document):
		result = {}
		db = self.client[database]
		if not document['text_tweet']:
			result = "bukan data %s (warn), tidak masuk" %document["id"]
		else:
			db[collection].insert(document)
			keterangan = "data %s (inserted into database %s collection %s)"%(document["id"],database,collection)
			sentence = document["text_tweet"]
			result["keterangan"] = keterangan
			result["document"] = sentence
			
		return result

	def get_all_collection(self, database):
		dbnames = self.client.database_names()
		if database not in dbnames:
		    return False
		else:
			db = self.client[database]
			cursor = db.collection_names()

			return cursor

	def get_location_by_name_and_month(self, database, name, month):
		db = self.client[database]
		cursor = db[month].aggregate([
				    {"$match": {
	                            "$and":[
	                            	{"district": "kabupaten"},
	                                {"LOC":name}
	                            ]
	                      }
	                    },
				    {"$group":{"_id":"$LOC", "NUM": {"$max":"$NUM"}, 
				                       "data": {
				                                "$push":{
				                                    "NUM":{"$max":'$NUM'}, 
				                                    "date":"$time", 
				                                    "text_tweet":"$text_tweet", 
				                                    "url_duplicate":"$url_duplicate",
				                                    "ORG":"$ORG",
				                                    "CON":"$CON"}
				                                }
				              }
				    },
				    {"$sort":{"NUM":-1}}
				])
		return cursor

	def get_location_by_ai_and_month(self, database, risk, month):
		db = self.client[database]
		if risk == "tinggi":
			cursor = db[month].aggregate([
				    {"$match": {
	                            "$and":[
	                            	{"district": "kabupaten"},
	                                {"NUM":{"$gt":50}}
	                            ]
	                      }
	                    },
				    {"$group":{"_id":"$LOC", "NUM": {"$max":"$NUM"}, 
				                       "data": {
				                                "$push":{
				                                    "NUM":{"$max":'$NUM'}, 
				                                    "date":"$time", 
				                                    "text_tweet":"$text_tweet", 
				                                    "url_duplicate":"$url_duplicate",
				                                    "ORG":"$ORG",
				                                    "CON":"$CON"}
				                                }
				              }
				    },
				    {"$sort":{"NUM":-1}}
				])
		elif risk == "sedang":
			cursor = db[month].aggregate([
				    {"$match": {
	                            "$and":[
	                            	{"district": "kabupaten"},
	                            	{"NUM":{"$gt":19}},
	                                {"NUM":{"$lt":56}}
	                            ]
	                      }
	                    },
				    {"$group":{"_id":"$LOC", "NUM": {"$max":"$NUM"}, 
				                       "data": {
				                                "$push":{
				                                    "NUM":{"$max":'$NUM'}, 
				                                    "date":"$time", 
				                                    "text_tweet":"$text_tweet", 
				                                    "url_duplicate":"$url_duplicate",
				                                    "ORG":"$ORG",
				                                    "CON":"$CON"}
				                                }
				              }
				    },
				    {"$sort":{"NUM":-1}}
				])
		else:
			cursor = db[month].aggregate([
				    {"$match": {
	                            "$and":[
	                            	{"district": "kabupaten"},
	                            	{"NUM":{"$lt":19}}
	                            ]
	                      }
	                    },
				    {"$group":{"_id":"$LOC", "NUM": {"$max":"$NUM"}, 
				                       "data": {
				                                "$push":{
				                                    "NUM":{"$max":'$NUM'}, 
				                                    "date":"$time", 
				                                    "text_tweet":"$text_tweet", 
				                                    "url_duplicate":"$url_duplicate",
				                                    "ORG":"$ORG",
				                                    "CON":"$CON"}
				                                }
				              }
				    },
				    {"$sort":{"NUM":-1}}
				])

		db = self.client[database]
		
		return cursor

	def get_history_incident_by_location(self, database, month, year, location):
		db = self.client[database]
		# print "database :%s, month :%s, location :%s"%(database,month,location)
		cursor = db[month].find({"$and":[{"LOC":location},{"district":"kabupaten"}]})
		documents = {}

		#dates = month.title()+" "+str(int(year)-1) //tahun 2016
		dates_month_year = month.title()+" "+str(int(year))
		dates_month_year_half = month.title()+" "+str(int(year))[2:]

		for data in cursor:
			document = []
			year_full = str(int(year))
			year_half = year_full[2:]
			str_date = ''
			if len(data['time']) >= 8:
				str_date = data["time"].replace(dates_month_year,"").replace(dates_month_year_half, "").replace(month.title(), "").replace(" ", "")
			else:
				str_date = data["time"].replace(month.title(), "").replace(" ", "")
			print data['time'], str_date, month.title(), dates_month_year, dates_month_year_half
			date = int(str_date)

			if len(str_date) == 1:
				str_date = "0"+str_date

			url = list(set(data["url_duplicate"]))

			tweet_url = self.get_tweet_from_date_and_url(month+"_"+year+"_ner", str_date, url)
			
			print tweet_url

			if date in documents:
				if documents[date][0] < data["NUM"]:
					# apabila index ada maka bandingkan, apabila lebih besar maka max data["NUM"]
					document.append(data["NUM"])
					document.append(str(data["time"]))
					document.append(tweet_url["tweet"])
					document.append(tweet_url["url"])
					documents[date] = document
			else:
				#apabila index tidak ada maka buat array object
				document.append(data["NUM"])
				document.append(str(data["time"]))
				document.append(tweet_url["tweet"])
				document.append(tweet_url["url"])
				documents[date] = document
		        
		data_sort = sorted(documents.items())
		result = []
		for data in data_sort:
			datum = []
			datum.append(data[1][0])
			datum.append(data[1][1].encode("utf8"))
			datum.append(data[1][2])
			datum.append(data[1][3])
			result.append(datum)

		return result

	def get_tweet_from_date_and_url(self, database, collection, arr_url):
		db = self.client[database]
		result  = {}
		url = []
		tweet = []
		print database, collection
		for link in arr_url :
			temp_link = link
			cursor = db[collection].find({"url":link})
			for data in cursor :
				url.append(data["url"])
				tweet.append(data["text_tweet"])

		result["url"] = url
		result["tweet"] = tweet

		return result

	def validation_CON(self, sentences, word_replace):
		sentence = []
		split_sentence = sentences.split(" ")
		for index, word in enumerate(split_sentence):
			split_word = word.split("/")
			if (split_word[0] == word_replace) and (split_sentence[index-1] == "rumah"):
				word = word_replace
			sentence.append(word)

		result = " ".join(sentence)

		return result




