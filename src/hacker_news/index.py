import fileinput
import time
import operator
import abc

from itertools import islice
from collections import Counter
from datetime import datetime
from django.conf import settings
from hacker_news.constants import FULL_DATE_FORMAT, ALL_DATE_FORMATS


def extract_dates(date_string):
    date_obj = datetime.strptime(date_string, FULL_DATE_FORMAT)
    return [date_obj.strftime(f) for f in ALL_DATE_FORMATS]


def parse_input_line(line):
    return line.split('\t')


class BaseIndex(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.clear()

    def clear(self):
        self._index = {}

    @abc.abstractmethod
    def _add_term_to_index(self, term, query):
        pass

    def add_to_index(self, date_string, query):
        for date_term in extract_dates(date_string):
            index._add_term_to_index(date_term, query)
    
    def count(self, term):
        return len(self._index[term]) if term in self._index else 0

    @abc.abstractmethod
    def top_queries(self, term, size):
        pass

    def build_from_scratch(self, size):
        self.clear()
        with open(settings.INDEX_FILE_NAME, 'r') as lines:
            processed_input = map(parse_input_line, islice(lines, size))
            for date_string, query in processed_input:
                self.add_to_index(date_string, query.strip())
        self.ready()

    def ready(self):
        pass


class UnorderedMultisetIndex(BaseIndex):
    ''' The entire index is built in ~95s when using UnorderedMultisetIndex '''

    def _add_term_to_index(self, term, query):
        if term not in self._index:
            # collections.Counter is an implementation of an Unordered Multiset
            self._index[term] = Counter()
        self._index[term][query] += 1

    def top_queries(self, term, size):
        if term not in self._index:
            return []
        return self._index[term].most_common(size)


class OrderedListIndex(BaseIndex):
    ''' The entire index is built in ~110s when using OrderedListIndex '''

    def _add_term_to_index(self, term, query):
        if term not in self._index:
            self._index[term] = {}
        if query not in self._index[term]:
            self._index[term][query] = 0
        self._index[term][query] += 1

    def top_queries(self, term, size):
        if term not in self._index:
            return []
        return self._index[term][:size]

    def ready(self):
        for key, queries_map in self._index.items():
            self._index[key] = sorted(queries_map.items(), key=operator.itemgetter(1), reverse=True)
            del queries_map


index = UnorderedMultisetIndex()
