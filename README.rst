**************************
Introduction to WordSearch
**************************


WordSearch is a Python class for creating wordsearch puzzles.

Installation:
=============

The PyValem package can be installed either from PyPI using pip

.. code-block:: bash

    python3 -m pip install python-wordsearch

or from the source by running (one of the two) from the project source directory.

.. code-block:: bash

    # either
    python setup.py install

    # or
    python3 -m pip install .



Examples:
=========

Creating a Word Search Puzzle
-----------------------------

A ``WordSearch`` object can be created with the following arguments to generate a word-search:

* ``nrows``, ``ncols``: the dimensions of the word-search grid
* ``wordlist`` or ``wordlist_filename``: a list of words or the filename of a text file containing the words (one per line).
* ``output_filestem``: forms the base of the filename to use for the output SVG image. Defaults to ``'wordsearch'``, which will produced files called ``'wordsearch-search.svg'`` and ``'wordsearch-search-solution.svg'``.
* ``mask`` (optional): defines the shape of the word-search (``None``, ``'circle'`` or ``'squares'``).
* ``allow_backwards_words``: defaults to ``False``.

.. code-block:: pycon

    >>> from wordsearch import WordSearch

    >>> wordsearch = WordSearch(
   ...:     15,
   ...:     15,
   ...:     [
   ...:         "BOXER",
   ...:         "DASCHUND",
   ...:         "AIREDALE",
   ...:         "BORZOI",
   ...:         "LABRADOR",
   ...:         "CHIHUAHUA",
   ...:         "GREYHOUND",
   ...:         "POMERANIAN",
   ...:     ],
   ...:     mask="circle",
   ...:     output_filestem="dog-search",
   ...:     allow_backwards_words=True,
   ...: )
   
   >>> wordsearch.make()
  (True, 'Fitted the words in 1 attempt(s)')
  
   >>> print(wordsearch.wordsearch_text)
              C K I Z H          
          L L H E S Z R I L      
        R E F I L H W Y D Y R    
      S W C X H A J M W G R P G  
      P Q M R U D P Y M M O I R  
    F D D E P A E A B J M D D E W
    A I X C O H R I L E O P A Y Y
    P O D G B U I N R L D D S H B
    B Y V A A A A A C A U A C O U
    I O Z R O B N K A B B Q H U E
      Z V H C I Q U P R D D U N  
      O M A A K U Q G A D Y N D  
        I N L C E F W D T I D    
          L L X X G W O A I      
              M J Z C R          
    POMERANIAN
    CHIHUAHUA
    GREYHOUND
    DASCHUND
    AIREDALE
    LABRADOR
    BORZOI
    BOXER

Output to an SVG file is also possible:

    >>> wordsearch.write_wordsearch_and_solution_svg()

which produces the image:

.. image:: https://raw.githubusercontent.com/scipython/python-wordsearch/master/doc/source/_static/dog-search.svg
  :width: 600
  :alt: Example wordsearch of dog breeds
