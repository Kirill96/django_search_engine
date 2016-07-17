# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Document(models.Model):
	url = models.CharField(max_length=255, unique=True)
	title = models.CharField(max_length=100)
	text_of_url = models.TextField()
	len_of_doc = models.IntegerField()
	is_indexed = models.BooleanField()

	def __str__(self):
		return self.title + ' --> '.encode('utf-8') + str(self.is_indexed).encode('utf-8')

class Index(models.Model):
	word = models.CharField(max_length=100)
	freq = models.IntegerField()
	doc = models.ForeignKey(Document)

	def __str__(self):
		return word + ' --> ' + str(freq) + ' in $' + str(doc) + '$'
