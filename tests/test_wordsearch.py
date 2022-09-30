"""
Unit tests for the formula module of PyValem
"""

import unittest
from wordsearch import WordSearch


class WordSearchTest(unittest.TestCase):
    def test_simple_wordsearch(self):

        wordlist = [
            "MERCURY",
            "VENUS",
            "EARTH",
            "MARS",
            "JUPITER",
            "SATURN",
            "URANUS",
            "NEPTUNE",
        ]
        wordsearch = WordSearch(
            13,
            13,
            wordlist,
        )
        success, msg = wordsearch.make()
        self.assertTrue(success)
        self.assertIn(wordlist[-1], wordsearch.wordsearch_text)

        svg = wordsearch.make_wordsearch_svg(wordsearch.grid)
        self.assertIn('text-anchor="middle"', svg)

        self.assertIn(
            """<text x="300.0" y="452.0" text-anchor="middle" class="wordlist">EARTH</text>
<text x="300.0" y="477.0" text-anchor="middle" class="wordlist">JUPITER</text>
<text x="300.0" y="502.0" text-anchor="middle" class="wordlist">MARS</text>
<text x="300.0" y="527.0" text-anchor="middle" class="wordlist">MERCURY</text>
<text x="700.0" y="452.0" text-anchor="middle" class="wordlist">NEPTUNE</text>
<text x="700.0" y="477.0" text-anchor="middle" class="wordlist">SATURN</text>
<text x="700.0" y="502.0" text-anchor="middle" class="wordlist">URANUS</text>
<text x="700.0" y="527.0" text-anchor="middle" class="wordlist">VENUS</text>""",
            svg,
        )

        svg = wordsearch.make_wordsearch_svg(wordsearch.grid, ncols=3)
        self.assertIn(
            """<text x="233.0" y="452.0" text-anchor="middle" class="wordlist">EARTH</text>
<text x="233.0" y="477.0" text-anchor="middle" class="wordlist">JUPITER</text>
<text x="233.0" y="502.0" text-anchor="middle" class="wordlist">MARS</text>
<text x="499.0" y="452.0" text-anchor="middle" class="wordlist">MERCURY</text>
<text x="499.0" y="477.0" text-anchor="middle" class="wordlist">NEPTUNE</text>
<text x="499.0" y="502.0" text-anchor="middle" class="wordlist">SATURN</text>
<text x="765.0" y="452.0" text-anchor="middle" class="wordlist">URANUS</text>
<text x="765.0" y="477.0" text-anchor="middle" class="wordlist">VENUS</text>""",
            svg,
        )

        svg = wordsearch.make_wordsearch_svg(wordsearch.grid, ncols=4)
        wordlist_svg = """<text x="200.0" y="452.0" text-anchor="middle" class="wordlist">EARTH</text>
<text x="200.0" y="477.0" text-anchor="middle" class="wordlist">JUPITER</text>
<text x="400.0" y="452.0" text-anchor="middle" class="wordlist">MARS</text>
<text x="400.0" y="477.0" text-anchor="middle" class="wordlist">MERCURY</text>
<text x="600.0" y="452.0" text-anchor="middle" class="wordlist">NEPTUNE</text>
<text x="600.0" y="477.0" text-anchor="middle" class="wordlist">SATURN</text>
<text x="800.0" y="452.0" text-anchor="middle" class="wordlist">URANUS</text>
<text x="800.0" y="477.0" text-anchor="middle" class="wordlist">VENUS</text>"""
        self.assertIn(wordlist_svg, svg)

        svg = wordsearch.make_wordsearch_svg(wordsearch.grid, ncols=5)
        self.assertIn(wordlist_svg, svg)

    def test_masked_wordsearch(self):
        wordsearch = WordSearch(
            15,
            15,
            wordlist_filename="tests/states.txt",
            mask="circle",
            output_filestem="states",
            allow_backwards_words=True,
        )
        success, msg = wordsearch.make()
        self.assertTrue(success)
        wordsearch_text = wordsearch.wordsearch_text
        self.assertIn("TEXAS", wordsearch_text)
        self.assertEqual(wordsearch_text[0], " ")
