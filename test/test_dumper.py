#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append('..')
from dumper import cleaning_tweets


class MyListTest(unittest.TestCase):

    def test_sentence_screen_names_end(self):
        res = cleaning_tweets('test @screenname.')
        self.assertEqual(res, 'test.')

    def test_sentence_screen_names_start(self):
        res = cleaning_tweets('@screenname test.')
        self.assertEqual(res, 'test.')

    def test_sentence_http_links(self):
        res = cleaning_tweets('test http://t.co/yfkfFSf23a test.')
        self.assertEqual(res, 'test test.')

    def test_sentence_https_links(self):
        res = cleaning_tweets('test https://t.co/yfkfFSf23a test.')
        self.assertEqual(res, 'test test.')

    def test_sentence_several_links(self):
        res = cleaning_tweets(
            'test https://t.co/yfkfFSf23a http://www.g/2e test.')
        self.assertEqual(res, 'test test.')

    def test_sentence_full_links(self):
        res = cleaning_tweets(
            'test https://www.yandex.ru/ https://www.yandex.ru/ru/ https://www.yandex.ru/ru http://www.g/2e test.')
        self.assertEqual(res, 'test test.')
if __name__ == '__main__':
    unittest.main()
