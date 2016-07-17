# -*- coding: utf-8 -*-
import parser_html
import multiprocessing as mp
import indexer


def _crawler(queue, w):
	while True:
		elem = queue.get()
		if elem == None:
			break
		url, h = elem
		if h == 0 or w == 0:
			break
		else:
			html = parser_html.Parsed_html(url)
			indexer.add_index(html)
			links = html.links
			if not (links == [] or links is None) and h-1 != 0:
				for link in links[:w]:
					queue.put((link, h-1))
		queue.task_done()
	queue.task_done()


def crawler(links, h, w):
	nCPU = 2
	queue = mp.JoinableQueue()

	if len(links) == 0:
		return None

	for link in links:
		queue.put((link, h))

	workers = []
	for i in range(nCPU):
		worker = mp.Process(target = _crawler, args = (queue, w))
		workers.append(worker)
		worker.start()

	queue.join()
	queue.put(None)
	queue.put(None)

	for i in range(nCPU):
		workers[i].join(None)
	#return None


