import maxent as m
import func as f
import maxent as m
import stopwordremoval as s
import removetag as r

#create object class maxent
# classify = m.Maxent()

# func = f.Func()


# sentence = "3 warga situbondo meninggal karena dbd"
# classifier = func.open_file('iis_ll0_2.pickle')
# ner = classify.training_ner(sentence.encode("utf8"), classifier)
# print ner

#create object class maxent
classify = m.Maxent()

#create object class stopword removal
stopword = s.StopwordRemoval()

#create object class remove tag
tag = r.RemoveTag()

paragraph = []

paragraph.append("di tegal/LOC 45/NUM orang menderita/CON dbd. 41/NUM meninggal/CON 30/NUM orang 41/NUM meninggal/CON dirawat")
paragraph.append("di malang/LOC 4/NUM orang menderita/CON dbd")
paragraph.append("10/NUM orang mati/CON karena dbd di bantul/LOC @macanbantul")
# paragraph.append("warga sleman/LOC 4/NUM orang menderita/CON dbd")
# paragraph.append("cirebon/LOC meninggal/CON karena dbd")
# paragraph.append("jakarta/LOC meninggal/CON karena dbd")
# paragraph.append("4/NUM warga bandung/LOC meninggal/CON karena dbd")
# paragraph.append("5/NUM warga grobogan/LOC meninggal/CON karena dbd")
# paragraph.append("kota/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
# paragraph.append("pemerintah/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
# paragraph.append("dinas/ORG kesehatan/ORG sleman/LOC 5/NUM orang mati/CON karena dbd")
# paragraph.append("10/NUM warga klaten/LOC 5/NUM orang mati/CON karena dbd")
# paragraph.append("4/NUM warga solo/LOC tewas/CON terkena/CON dbd")
# paragraph.append("4/NUM warga bantul/LOC tewas/CON terkena/CON dbd")
# paragraph.append("6/NUM warga lumajang/LOC tewas/CON terkena/CON dbd")
# paragraph.append("8/NUM warga bekasi/LOC tewas/CON terkena/CON dbd")
# paragraph.append("#info @janggal 20/NUM warga klaten/LOC tewas/CON terkena/CON dbd bit.ly/1KuKsxO")
# paragraph.append("meninggal/CON dunia, 3/NUM orang di klaten/LOC karena dbd")

#==========================================================================
# TRAIN IIS
#==========================================================================
# Preprocessing Train
#--------------------------------------------------------------------------
#clean tag. example : #, @, link internet 
paragraph_clean_tag = tag.tag_removal(paragraph, "train")
#clean stopword. example : yah, hlo 
paragraph_clean_stopword = stopword.stopword_removal(paragraph_clean_tag, "train")
#finalisasi clean sentence
paragraph_clean = paragraph_clean_stopword
#--------------------------------------------------------------------------
# Proses Training IIS
#--------------------------------------------------------------------------
classifier = classify.training_weight_iis(paragraph_clean)
# print classifier
# classifier.show_most_informative_features(35)