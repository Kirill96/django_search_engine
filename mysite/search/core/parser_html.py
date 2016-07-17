# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import *
import urlparse
import robotparser


class Parsed_html(object):

    def __init__(self, url):
        self.url = url
        self.is_error = False

        try:
            self.download()
            self.title_from_html()
            self.text_from_html()
            self.dict_of_words_from_html()
            self.list_of_links_from_html()
        except:
            self.is_error = True
            self.soup = None
            self.text =None
            self.title = None
            self.dict_of_words = None
            self.links = None               

    def download(self):
        try:
            parsed_url = urlparse.urlparse(self.url)
            rp = robotparser.RobotFileParser()
            rp.set_url(parsed_url.scheme + "://" + parsed_url.hostname + "/robots.txt")
            rp.read()
            rp.can_fetch("*", self.url)

            html_doc = urlopen(self.url).read()
        except:
            self.is_error = True
            self.soup = None
            return None
        self.soup = BeautifulSoup(html_doc, 'html.parser')

    def text_from_html(self):
        if not self.is_error:
            [s.decompose() for s in self.soup.find_all(['style', 'script', '[document]', 'head', 'title'])]
            self.text = ' '.join(self.soup.get_text().split())
        else:
            self.text = None

    def title_from_html(self):
        if not self.is_error:
            self.title = self.soup.title.string.encode('utf-8')
        else:
            self.title = None

    def dict_of_words_from_html(self):
        if not self.is_error:
            text = self.text.replace('.', '').replace(',', '').replace('"', '').replace("'", ''). \
                            replace(':', '').replace('!', '').replace('?', '').lower()
            banned_words = [u'to', u'the', u'in', u'on', u'at', u'a', u'for', u'is', u'of', \
                    u'and', u'or', u'в', u'на', u'под', u'а', u'но', u'и', u'к', u'то'] 
            dic_words = {}
            for w in text.split():
                if w == '' or w in banned_words:
                    continue
                if (w in dic_words):
                    dic_words[w] += 1
                else:
                    dic_words[w] = 1
            dic_words = list(dic_words.items())
            dic_words.sort(key=lambda (key, value): value, reverse=True)
            self.dict_of_words = dic_words
            self.len_of_doc = sum([value for (key, value) in dic_words])
        else:
            self.dict_of_words = None       

    def list_of_links_from_html(self):
        if not self.is_error:
            links = set()
            parsed_url = urlparse.urlparse(self.url)
            for elem in self.soup.find_all('a'):
                link = elem.get('href')
                if link is None:
                    continue
                if link.startswith('//'):
                    links.add(parsed_url.scheme + ':' + link)
                elif link.startswith('/'):
                    links.add(parsed_url.scheme + '://' + parsed_url.hostname + link)
                elif link.startswith('http://') or link.startswith('https://'):
                    links.add(link)
                elif link.startswith('#') or link.startswith('javascript:'):
                    continue
                elif '://' in link:
                    continue
                else:
                    links.add(urlparse.urljoin(self.url, link))
            self.links = list(links)
        else:
            self.links = None

