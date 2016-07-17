# -*- coding: utf-8 -*-
import parser_html
from search.models import *
from django.db import IntegrityError

def add_index(html):
	
	#html = parser_html.Parsed_html(url)

	if not html.is_error:
		doc = Document(url=html.url, title=html.title, text_of_url=html.text[:1000], is_indexed=False, len_of_doc=html.len_of_doc)

		try:
			doc.save()
		except IntegrityError:
			return False

		for (word, num) in html.dict_of_words:
			ind = Index(word=word, freq=num, doc=doc)
			ind.save()

		doc.is_indexed = True
		doc.save()
		
		return True