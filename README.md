# DocuToads
DocuToads is an open source minimum edit distance algorithm that can handle cut-paste edit operations, created by Henrik Hermansson, who reserves some rights.

STEP BY STEP INSTRUCTIONS FOR USING DOCUTOADS

1) The texts
a. DocuToads accepts texts in .txt, utf8 format. Make sure all your texts are in this format.

b. If you want to perform an article-by-article comparison of the two texts, you need to mark the break-points between articles.

b.i. DocuToads finds the break-points using a regular expression which is looking for the word DTBREAKPOINT. Insert this word between each article (not before the first nor after the last). 

2) Install necessary Python packages:

a. time

b. math

c. string

d. re

e. os

f. sys

g. traceback

h. pp

i. numpy

j. subprocess

k. pylab

l. collections

m. csv

n. matplotlib


3) A list of cases

a. By a "case" is meant one pair of texts to be compared

b. You will need a python list of cases where each entry (case) is a list containing (in string format) in the correct order:

b.i. Path to text 1

b.ii. Path to text 2

b.iii. Short name for text 1

b.iv. Short name for text 2

b.v. Short name for case

b.vi. A list of article names in the first text, for example: ["Article 1", "Article 2", "Article 3"]. Make sure the list matches the actual number of articles separated by DTBREAKPOINT markers. Enter empty list if you don't want to perform article-by-article comparison of the two texts.

b.vii. A list of article names in the second text. Make sure the list matches the actual number of articles separated by DTBREAKPOINT markers. Enter empty list if you don't want to perform article-by-article comparison of the two texts. 

c. Name this lists "caselist" and enter into DocuToads_main.py.


4) Set the parameters

a. Open DocuToads_main.py and enter the following parameters:

a.i. outpath – The path of the desired output folder, no need to worry about sub-folders

a.ii. plottype – Determines which kind of graph to create - "block", "bar" and "line" are available. If no plot wanted set to "none".

a.iii. backtrace - Determiens whether to save a table of the exact edit operations found, i.e. the backtrace. Set to "yes" or "no".

a.iv. by_article - Determines whether to split results article-by-article, based on the first text. Set to "article" or "noarticle".

a.v. cutoff - Determines how many words in sequence there must be for the algorithm to detect a transposition, default value is 5.

a.vi. ncpus – Determines how many CPU:s DocuToads will use to process several cases simultaneously. Default is 1.

5) Run DocuToads_main.py
