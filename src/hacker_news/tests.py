from unittest import TestCase 

from hacker_news.index import index


class IndexTests(TestCase):
    def setUp(self):
        index.clear()
        index.add_to_index('2015-09-01 00:00:01', 'a')
        index.add_to_index('2015-09-01 00:00:01', 'a')
        index.add_to_index('2015-09-01 00:00:01', 'b')
        index.add_to_index('2015-09-01 11:11:11', 'c')
        index.add_to_index('2015-09-02 00:00:01', 'd')
        index.add_to_index('2015-09-02 00:00:01', 'a')
        index.add_to_index('2015-10-31 23:59:59', 'b')
        index.add_to_index('2014-09-01 00:00:01', 'a')
        index.ready()

    def test_count_year(self):
        self.assertEquals(4, index.count('2015'))
        self.assertEquals(1, index.count('2014'))
        self.assertEquals(0, index.count('2013'))

    def test_count_month(self):
        self.assertEquals(1, index.count('2014-09'))
        self.assertEquals(0, index.count('2014-10'))
        self.assertEquals(4, index.count('2015-09'))
        self.assertEquals(1, index.count('2015-10'))

    def test_count_day(self):
        self.assertEquals(0, index.count('2014-08-01'))
        self.assertEquals(1, index.count('2014-09-01'))
        self.assertEquals(3, index.count('2015-09-01'))
        self.assertEquals(2, index.count('2015-09-02'))
        self.assertEquals(1, index.count('2015-10-31'))

    def test_count_hour(self):
        self.assertEquals(0, index.count('2014-08-31 00'))
        self.assertEquals(1, index.count('2014-09-01 00'))
        self.assertEquals(2, index.count('2015-09-01 00'))
        self.assertEquals(1, index.count('2015-09-01 11'))
        self.assertEquals(2, index.count('2015-09-02 00'))
        self.assertEquals(1, index.count('2015-10-31 23'))

    def test_cout_minute(self):
        self.assertEquals(0, index.count('2014-10-31 23:59'))
        self.assertEquals(1, index.count('2014-09-01 00:00'))
        self.assertEquals(2, index.count('2015-09-01 00:00'))
        self.assertEquals(1, index.count('2015-09-01 11:11'))
        self.assertEquals(2, index.count('2015-09-02 00:00'))
        self.assertEquals(1, index.count('2015-10-31 23:59'))

    def test_count_second(self):
        self.assertEquals(0, index.count('2014-08-31 23:59:59'))
        self.assertEquals(1, index.count('2014-09-01 00:00:01'))
        self.assertEquals(2, index.count('2015-09-01 00:00:01'))
        self.assertEquals(1, index.count('2015-09-01 11:11:11'))
        self.assertEquals(2, index.count('2015-09-02 00:00:01'))
        self.assertEquals(1, index.count('2015-10-31 23:59:59'))

    def test_top_queries_in_year(self):
        top_2015 = index.top_queries('2015', 2)
        self.assertEquals([('a', 3), ('b', 2)], top_2015)

        top_2014 = index.top_queries('2014', 2)
        self.assertEquals([('a', 1)], top_2014)

        top_2013 = index.top_queries('2013', 1)
        self.assertEquals(0, len(top_2013))

    def test_top_queries_in_month(self):
        top_2015_09 = index.top_queries('2015-09', 4)
        self.assertIn(('a', 3), top_2015_09)
        self.assertIn(('b', 1), top_2015_09)
        self.assertIn(('c', 1), top_2015_09)
        self.assertIn(('d', 1), top_2015_09)

    def test_top_queries_in_day(self):
        top_2015_09_01 = index.top_queries('2015-09-01', 3)
        self.assertIn(('a', 2), top_2015_09_01)
        self.assertIn(('b', 1), top_2015_09_01)
        self.assertIn(('c', 1), top_2015_09_01)
