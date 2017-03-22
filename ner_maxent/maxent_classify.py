import func as f
import template_feature as tf
import math
import pprint

class Maxent_Classify:

	func = f.Func()
	template_feature = tf.template_feature_set
	classifier = "none"

	def weights(self):
		count_fet_set = len(self.classifier.weights())
		data = self.classifier.weight_with_index(count_fet_set)
		return data

	def prob(self, weightset, featureset, labels):
		probability = {}
		sigmaf = {}
		for label in labels:
			sigmaf[label] = self.prob_label(weightset, featureset, label)

		normalize = self.normalize(sigmaf)
		for label in labels:
			probability[label] = (1/normalize)*sigmaf[label]

		return probability

	def normalize(self, prob_label_data):
		return sum(prob_label_data.values())

	def prob_label(self, weightset, featureset, label):
		sigmaf = 0
		for fin, fval in enumerate(featureset):
			val = int(fval.replace("f",""))
			if val in self.template_feature[label] and featureset[fval] == 1:
				f_lambda = weightset[label][fval][featureset[fval]] * featureset[fval]
				sigmaf+=f_lambda
		result = math.exp(sigmaf)

		return result

	def pdist(self, featureset):
		weights = self.weights()
		labels = self.classifier.labels() 
		result = self.prob(weights, featureset, labels)

		return result


# feat = {'f1': 0, 'f2': 0, 'f3': 1, 'f4': 1, 'f5': 0, 'f6': 0, 'f7': 1}

# m = maxent_classify()
# w = m.weight()
# labels = m.classifier.labels() 
# print m.prob(w, feat, labels)
# pprint.pprint(m.weight())