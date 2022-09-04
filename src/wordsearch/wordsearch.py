# wordsearch.py
# Christian Hill, 2022.
import os
import sys
import random
from copy import deepcopy
from .masks import Mask, CircleMask, SquaresMask


class WordSearch:

    # Maximum number of rows and columns.
    NMAX = 32
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    masks = {None: Mask, "circle": CircleMask, "squares": SquaresMask}

    def __init__(
        self,
        nrows,
        ncols,
        wordlist=None,
        wordlist_filename=None,
        output_filestem="wordsearch",
        mask=None,
        allow_backwards_words=False,
    ):
        if wordlist is None and wordlist_filename is None:
            raise ValueError("You must provide one of wordlist and" "wordlist_filename")
        if not wordlist and not wordlist_filename:
            raise ValueError(
                "You must not provide both wordlist and" " wordlist_filename."
            )

        self.nrows = nrows
        self.ncols = ncols

        if nrows > self.NMAX or ncols > self.NMAX:
            raise ValueError(f"Maximum number of rows and columns is {self.NMAX}.")

        self.output_filestem = output_filestem
        self.mask = self.masks[mask](nrows, ncols)
        self.allow_backwards_words = allow_backwards_words
        self.success = False

        if wordlist_filename:
            wordlist = self._get_wordlist(wordlist_filename)
        self.wordlist = sorted(wordlist, key=lambda w: len(w), reverse=True)

        # Obviously, no word can be longer than the maximum dimension.
        max_word_len = max(nrows, ncols)
        if max(len(word) for word in wordlist) > max_word_len:
            raise ValueError(
                "Word list contains a word with too many letters."
                " The maximum is {}".format(max_word_len)
            )

    def make(self, nattempts=10):
        """Make a word search, attempting to fit words into the specified grid."""

        # We try nattempts times (with random orientations) before giving up.
        for i in range(nattempts):
            self.success = self._make_wordsearch()
            if self.success:
                if self.grid:
                    return True, f"Fitted the words in {i+1} attempt(s)"
        else:
            return (
                False,
                f"I failed to place all the words after" f" {nattempts} attempts.",
            )

    def _make_wordsearch(self):
        """Attempt to make a word search with the given parameters."""

        # Make the grid and apply a mask (locations a letter cannot be placed).
        self.grid = [[" "] * self.ncols for _ in range(self.nrows)]
        if self.mask:
            self.mask.apply(self.grid)

        def fill_grid_randomly():
            """Fill up the empty, unmasked positions with random letters."""
            for irow in range(self.nrows):
                for icol in range(self.ncols):
                    if self.grid[irow][icol] == " ":
                        self.grid[irow][icol] = random.choice(self.alphabet)

        def remove_mask(grid):
            """Remove the mask, for text output, by replacing with whitespace."""
            for irow in range(self.nrows):
                for icol in range(self.ncols):
                    if grid[irow][icol] == "*":
                        grid[irow][icol] = " "

        def test_candidate(irow, icol, dx, dy, word):
            """Test the candidate location (icol, irow) for word in orientation
            dx, dy)."""
            for j in range(len(word)):
                if self.grid[irow][icol] not in (" ", word[j]):
                    return False
                irow += dy
                icol += dx
            return True

        def place_word(word):
            """Place word randomly in the grid and return True, if possible."""

            # Left, down, and the diagonals.
            dxdy_choices = [(0, 1), (1, 0), (1, 1), (1, -1)]
            random.shuffle(dxdy_choices)
            for (dx, dy) in dxdy_choices:
                if self.allow_backwards_words and random.choice([True, False]):
                    # If backwards words are allowed, simply reverse word.
                    word = word[::-1]
                # Work out the minimum and maximum column and row indexes, given
                # the word length.
                n = len(word)
                colmin = 0
                colmax = self.ncols - n if dx else self.ncols - 1
                rowmin = 0 if dy >= 0 else n - 1
                rowmax = self.nrows - n if dy >= 0 else self.nrows - 1
                if colmax - colmin < 0 or rowmax - rowmin < 0:
                    # No possible place for the word in this orientation.
                    continue
                # Build a list of candidate locations for the word.
                candidates = []
                for irow in range(rowmin, rowmax + 1):
                    for icol in range(colmin, colmax + 1):
                        if test_candidate(irow, icol, dx, dy, word):
                            candidates.append((irow, icol))
                # If we don't have any candidates, try the next orientation.
                if not candidates:
                    continue
                # Pick a random candidate location and place the word in this
                # orientation.
                loc = irow, icol = random.choice(candidates)
                for j in range(n):
                    self.grid[irow][icol] = word[j]
                    irow += dy
                    icol += dx
                # We're done: no need to try any more orientations.
                break
            else:
                # If we're here, it's because we tried all orientations but
                # couldn't find anywhere to place the word. Oh dear.
                return False
            return True

        # Iterate over the word list and try to place each word (without spaces).
        for word in self.wordlist:
            word = word.replace(" ", "")
            if not place_word(word):
                # We failed to place word, so bail.
                return False

        # grid is a list of lists, so we need to deepcopy here for an independent
        # copy to keep as the solution (without random letters in unfilled spots).
        self.solution = deepcopy(self.grid)
        fill_grid_randomly()
        remove_mask(self.grid)
        remove_mask(self.solution)

        return True

    @property
    def grid_text(self):
        """Output a text version of the filled grid wordsearch."""
        return "\n".join(" ".join(c for c in line) for line in self.grid)

    @property
    def wordlist_text(self):
        """Output a text version of the list of the words to find."""
        return "\n".join(self.wordlist)

    @property
    def wordsearch_text(self):
        """Output the wordsearch grid and list of words to find."""
        return self.grid_text + "\n" + self.wordlist_text

    def _svg_preamble(self, width, height):
        """Output the SVG preamble, with styles, to open file object fo."""

        return """<?xml version="1.0" encoding="utf-8"?>
        <svg xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" >
        <defs>
        <style type="text/css"><![CDATA[
        line, path {{
          stroke: black;
          stroke-width: 4;
          stroke-linecap: square;
        }}
        path {{
          fill: none;
        }}
        
        text {{
          font: bold 24px Verdana, Helvetica, Arial, sans-serif;
        }}
      
        ]]>
        </style>
        </defs>
        """.format(
            width, height
        )

    def grid_as_svg(self, grid, width, height):
        """Return the wordsearch grid as a sequence of SVG <text> elements."""

        # A bit of padding at the top.
        YPAD = 20
        # There is some (not much) wiggle room to squeeze in wider grids by
        # reducing the letter spacing.
        letter_width = min(32, width / self.ncols)
        grid_width = letter_width * self.ncols
        # The grid is centred; this is the padding either side of it.
        XPAD = (width - grid_width) / 2
        letter_height = letter_width
        grid_height = letter_height * self.nrows
        s = []

        # Output the grid, one letter at a time, keeping track of the y-coord.
        y = YPAD + letter_height / 2
        for irow in range(self.nrows):
            x = XPAD + letter_width / 2
            for icol in range(self.ncols):
                letter = grid[irow][icol]
                if letter != " ":
                    s.append(
                        '<text x="{}" y="{}" text-anchor="middle">{}</text>'.format(
                            x, y, letter
                        )
                    )
                x += letter_width
            y += letter_height

        # We return the last y-coord used, to decide where to put the word list.
        return y, "\n".join(s)

    def wordlist_svg(self, width, height, y0):
        """Return a list of the words to find as a sequence of <text> elements."""

        # Use two columns of words to save (some) space.
        n = len(self.wordlist)
        col1, col2 = self.wordlist[: n // 2], self.wordlist[n // 2 :]

        def word_at(x, y, word):
            """The SVG element for word centred at (x, y)."""
            return (
                '<text x="{}" y="{}" text-anchor="middle" class="wordlist">'
                "{}</text>".format(x, y, word)
            )

        s = []
        x = width * 0.25
        # Build the list of <text> elements for each column of words.
        y0 += 25
        for i, word in enumerate(col1):
            s.append(word_at(x, y0 + 25 * i, word))
        x = width * 0.75
        for i, word in enumerate(col2):
            s.append(word_at(x, y0 + 25 * i, word))
        return "\n".join(s)

    def make_wordsearch_svg(self, grid, width=1000, height=1414):
        """Return the wordsearch grid as SVG."""

        svg = self._svg_preamble(width, height)
        y0, svg_grid = self.grid_as_svg(grid, width, height)
        svg += svg_grid
        # If there's room print the word list.
        if y0 + 25 * len(self.wordlist) // 2 < height:
            svg += self.wordlist_svg(width, height, y0)
        svg += "</svg>"
        return svg

    def write_wordsearch_and_solution_svg(self, width=1000, height=1414):
        """Save the wordsearch grid and its solution as an SVG files to filename."""

        if not self.success:
            raise Exception("No successful grid was made to output!")
        svg_filename = self.output_filestem + ".svg"
        with open(svg_filename, "w") as fo:
            print(self.make_wordsearch_svg(self.grid, width, height), file=fo)
        svg_solution_filename = self.output_filestem + "-solution.svg"
        with open(svg_solution_filename, "w") as fo:
            print(self.make_wordsearch_svg(self.solution, width, height), file=fo)

    def _get_wordlist(self, wordlist_filename):
        """Read in the word list from wordlist_filename."""
        wordlist = []
        with open(wordlist_filename) as fi:
            for line in fi:
                # The word is upper-cased and comments and blank lines are ignored.
                line = line.strip().upper()
                if not line or line.startswith("#"):
                    continue
                wordlist.append(line)
        return wordlist
