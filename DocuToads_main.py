# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 11:56:15 2014

@author: Henrik Alf Jonas Hermansson, Department of Political Science, University of Copenhagen. hajh@ifs.ku.dk 
"""
"This code was written by Henrik Hermansson, who reserves some rights. This code may be modified and used by anyone, granted that this source is cited."

# Import modules
import time
import math
import string
import re
import os
import sys
import traceback
import pp
import numpy
import subprocess
import pylab
import collections
import csv
import bs4
import matplotlib

# Module list needed for paralell computing
mods = ("math", "matplotlib", "string", "re", "os", "time", "sys", "traceback", "numpy", "pylab", "collections", "csv", "bs4")

# Import local code
from DocuToads_subfunctions import *

# Local code list needed for paralell computing
codes = clean_and_make_list, artindexer, text_compare, superloop, backtrace_line_matrix, backtrace_block_matrix, backtrace_bar_matrix, plotter, article_data_sorter, backtrace_writer



### INPUT BELOW

# Provide caselist
caselist = [] # Define up list of cases. Each row should contain (as strings): path to text 1, path to text 2, short name for text 1, short name for text 2, short name for case

# Set parameters
outpath = '' # Set path for output folder
plottype = "none" # Decide which kind of graph to create - "block", "bar" and "line" are available. If no plot wanted set to "none" 
backtrace = "yes" # Decide whether to save a table of the exact edit operations found, i.e. the backtrace - "yes"=yes
by_article = "noarticle" # Decide whether to split results article-by-article, based on the first text - "article" or "noarticle"
cutoff = 5 # Decide how many words in sequence there must be for the algorithm to detect an transposition, default value is 5

# Instruct python to use several CPU:s, default value is 1
ppservers = ()
ncpus = 30
job_server = pp.Server(ncpus, ppservers=ppservers)

### INPUT ABOVE



# Create paths for output
if not os.path.exists(outpath):
    os.makedirs(outpath)
    os.makedirs(outpath + 'backtraces/')
    os.makedirs(outpath + 'outdocs/')
    os.makedirs(outpath + 'plots/')
    os.makedirs(outpath + 'warnings/')

# Combines the list of cases and the parameters to be fed to the algorithm
to_process = []
for i, case in enumerate(caselist):    
    to_process.append((case[0], case[1], case[2], case[3], case[4], case[5], case[6], outpath, plottype, by_article, backtrace, cutoff))

    
      
#Runs DocuToads algorithm using paralell jobs on different CPU:s
jobs = []
for i, case in enumerate(to_process):
    job = job_server.submit(DocuToads_executor_pp, case, codes, mods)    
    jobs.append(job)

# Reports progress of algorithm - copy-paste into console for update
job_server.print_stats()
