"""
Unit tests for the formula module of PyValem
"""

import unittest
from wordsearch import WordSearch

class WordSearchTest(unittest.TestCase):
    def test_simple_wordsearch(self):

        wordlist = ['MERCURY', 'VENUS', 'EARTH', 'MARS', 'JUPITER', 'SATURN',
                    'URANUS', 'NEPTUNE']
        wordsearch = WordSearch(13, 13, wordlist,)
        success, msg = wordsearch.make()
        self.assertTrue(success)
        self.assertIn(wordlist[-1], wordsearch.wordsearch_text)
         
        svg = wordsearch.make_wordsearch_svg(wordsearch.grid)
        self.assertIn('text-anchor="middle"', svg)

    def test_masked_wordsearch(self):
        wordsearch = WordSearch(15, 15, wordlist_filename='tests/states.txt', mask='circle',
                                output_filestem='states', allow_backwards_words=True)
        success, msg = wordsearch.make()
        self.assertTrue(success)
        wordsearch_text = wordsearch.wordsearch_text
        self.assertIn("TEXAS", wordsearch_text)
        self.assertEqual(wordsearch_text[0], ' ')
