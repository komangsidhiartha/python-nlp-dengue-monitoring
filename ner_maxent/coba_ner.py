import maxent as m
import func as f
import pprint

classify = m.Maxent()
func = f.Func()

classifier = func.open_file('/Users/pwcahyo/Tesis/ner_maxent/iis_minll1.5.pickle')
sentence = "3 warga situbondo meninggal karena dbd"
classifier.show_most_informative_features(48)

# pprint.pprint(classifier.weight_with_index(48))
classify.training_ner(sentence.encode("utf8"), classifier)