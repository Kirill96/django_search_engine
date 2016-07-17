# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponse
from models import Document, Index
from .core import crawler, searcher
from django.core.validators import URLValidator, ValidationError

# Create your views here.
def home(request):
    if request.method == "POST":
        query = request.POST.get('query')
    else:
        query = request.GET.get('query')
    if query is None:
        return render(request, 'search/home.html', {'link':'', 'query':''})
    links = searcher.searcher(query)
    paginator = Paginator(links, 15)

    page = request.GET.get('page')
    try:
        link = paginator.page(page)
    except PageNotAnInteger:
        link = paginator.page(1)
    except EmptyPage:
        link = paginator.page(paginator.num_pages)

    return render(request, 'search/home.html', {'link':link, 'query':query})

def indexURL(request):

    if request.method == "POST":
        urls_for_indexing = []
        uv = URLValidator(schemes=['http', 'https'])

        urls_from_form = request.POST.get('url')
        if urls_from_form:
            list_urls = urls_from_form.split(", ")
            for url in list_urls:
                try:
                    uv(url)
                except ValidationError:
                    continue

                urls_for_indexing.append(url)

        file_with_urls = request.FILES.get('file_url')
        if file_with_urls:
            for url in file_with_urls:
                url = url.strip()
                try:
                    uv(url)
                except ValidationError:
                    continue

                urls_for_indexing.append(url)
        if len(urls_for_indexing):
            crawler.crawler(urls_for_indexing, 3, 3)
            text = 'Crawler completed!'
        else:
            text = 'No valid URLs'

    else:
        text = ''

    return render(request, 'search/indexURL.html', {'text':text})

def knownURL(request):
    ids = []
    docs = Document.objects.all()
    paginator = Paginator(docs, 15)
    doc_cnt = docs.count()
    for doc in docs:
        ids.append(int(doc.id))

    page = request.GET.get('page')
    try:
        doc = paginator.page(page)
    except PageNotAnInteger:
        doc = paginator.page(1)
    except EmptyPage:
        doc = paginator.page(paginator.num_pages)

    if not request.method == "POST" or request.POST.get('id') == '':
        return render(request, 'search/knownURL.html', {'doc_cnt':doc_cnt, 'doc':doc})  

    if int(request.POST.get('id')) in ids:
        id_ = request.POST.get('id')
        Document.objects.get(id=id_).delete()
        docs = Document.objects.all()
        doc_cnt = docs.count()
        paginator = Paginator(docs, 15)
        try:
            doc = paginator.page(page)
        except PageNotAnInteger:
            doc = paginator.page(1)
        except EmptyPage:
            doc = paginator.page(paginator.num_pages)

    return render(request, 'search/knownURL.html', {'doc_cnt':doc_cnt, 'doc':doc})

def stateAndEdit(request):
    ids = []
    indexes = Index.objects.all()
    paginator = Paginator(indexes, 100)
    ind_cnt = indexes.count()
    for ind in indexes:
        ids.append(int(ind.id))

    page = request.GET.get('page')
    try:
        index = paginator.page(page)
    except PageNotAnInteger:
        index = paginator.page(1)
    except EmptyPage:
        index = paginator.page(paginator.num_pages)

    if not request.method == "POST" or request.POST.get('id') == '':
        return render(request, 'search/stateAndEdit.html', {'ind_cnt':ind_cnt, 'index':index})

    if int(request.POST.get('id')) in ids:
        id_ = request.POST.get('id')
        Index.objects.get(id=id_).delete()
        indexes = Index.objects.all()
        ind_cnt = indexes.count()
        paginator = Paginator(indexes, 100)
        try:
            index = paginator.page(page)
        except PageNotAnInteger:
            index = paginator.page(1)
        except EmptyPage:
            index = paginator.page(paginator.num_pages)

    return render(request, 'search/stateAndEdit.html', {'ind_cnt':ind_cnt, 'index':index})
