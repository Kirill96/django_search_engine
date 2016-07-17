from search.models import *
import math


def searcher(request):

	N = len(Document.objects.all())
	avr_len = sum([elem.len_of_doc for elem in Document.objects.all()]) / float(N)

	docs = []
	d_request = {}
	for word in request.split():
		temp = [elem.doc for elem in Index.objects.filter(word__iexact=word)]
		if word in d_request:
			d_request[word] += len(temp)
		else:
			d_request[word] = len(temp)
		docs += temp

	docs = list(set(docs))
	docs.sort(key=lambda doc: score(d_request, doc, N, avr_len), reverse=True)

	return docs

def score(d_request, doc, N, avr_len):

	rank = 0
	for (word, n_docs) in d_request.items():
		try:
			freq = Index.objects.filter(word__iexact=word).get(doc=doc).freq
		except Index.DoesNotExist:
			freq = 0
		rank += math.log((N - n_docs + 0.5) / (n_docs + 0.5)) * (freq * (2.0 + 1)) / (freq + 2.0*(1 - 0.75 + 0.75*doc.len_of_doc / avr_len))

	return rank


