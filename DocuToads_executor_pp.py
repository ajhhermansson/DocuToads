# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 12:09:13 2014

@author: Henrik Alf Jonas Hermansson, Department of Political Science, University of Copenhagen. hajh@ifs.ku.dk 
"""
"This code was written by Henrik Hermansson, who reserves some rights. This code may be modified and used by anyone, granted that this source is cited."

#Import packages and local code snippets
import string
import re
import os
import sys
import traceback
import pp
import numpy
import pylab
import collections
import csv
import time
import bs4

from DocuToads_subfunctions import *

def DocuToads_executor_pp(fileandpath1, fileandpath2, propname, legname, caseid, artnames1, artnames2, outpath, plottype, by_article, backtrace, cutoff):    
    warning = None
    exception = None
    
    try:
        # Open files 
        file1= open(fileandpath1, 'rU')
        file2= open(fileandpath2, 'rU')

        text1= file1.read() # string
        file1.close()
        text2= file2.read() # string
        file2.close()
        
        # Clean strings and transform to lists of words
        text1 = clean_and_make_list(text1) # List of words
        text2 = clean_and_make_list(text2) # List of words

        #Calculate length of documents
        lentext1 = len(text1) # Integer
        lentext2 = len(text2) # Integer   
        
        # Create DT matrix
        matrix = text_compare(text1, text2) # numpy array       
        
        # Create backtrace, calculate MED
        output = superloop(matrix, cutoff) # List, first item is MED, second item is list of lists. Each of those lists contains three items; the column (integer), row (integer) and type of change/match (string).
        del matrix     
        
        # Output on an article-by-article basis
        if by_article == "article":
            text1artindex = artindexer(text1) # List of integers
            text2artindex = artindexer(text2)
            data = article_data_sorter(output[0], text1artindex, text2artindex, lentext1, lentext2, artnames1, artnames2, propname, legname, caseid)
            with open(outpath + "outdocs/" + caseid + '.csv', "wb") as g: # Save results
                writer = csv.writer(g, delimiter = ";")
                for row in data:
                    writer.writerow(row)
            g.close()         
            # List of lists. Each list contains; propname, article name, destination article name, number of: match, addition, substitution, transposition, deletion
 
        # Output on a document basis               
        else:
            coutput = collections.Counter(list(zip(*output[0])[2]))
            data = [[caseid, propname, legname, lentext1, lentext2, "All", "All", coutput["match"], coutput["addition"], coutput["substitution"], coutput["transposition"], coutput["deletion"]]]
    
            with open(outpath + "outdocs/" + caseid + '.csv', "wb") as g: # Save results
                writer = csv.writer(g, delimiter = ";")
                for row in data:
                    writer.writerow(row)
            g.close()
            
        # Save the backtrace            
        if backtrace == "yes":
            backtrace_writer(output[0], text1, text2, outpath, propname, legname, caseid)    

        # Remove texts that are no longer needed from active memory
        del text1
        del text2        
            
        # Plot output
        if plottype != "none":
            if plottype == "block":
                b_m = backtrace_block_matrix(lentext1, lentext2, output[0])
            if plottype == "bar":
                b_m = backtrace_bar_matrix(output[0])
            if plottype == "line":
                b_m = backtrace_line_matrix(lentext1, lentext2, output[0])               
            if by_article == "article":
                plotter(b_m, outpath, propname, legname, by_article, text1artindex, text2artindex, lentext1, lentext2, artnames1, artnames2)
            else:
                plotter(b_m, outpath, propname, legname, by_article, plottype, "", "", lentext1, lentext2, "", "")

    except:
        exception = traceback.format_exc()
        warandexc = [[propname], [legname], [warning], [exception]]
        with open(outpath + 'warnings/' + caseid + '.csv', "wb") as g: # Save results
            writer = csv.writer(g, delimiter = ";")
            writer.writerow(warandexc)
        g.close()        
    
    
        
    


    

    
