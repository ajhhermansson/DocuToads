# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 12:28:23 2016

@author: Henrik Alf Jonas Hermansson, Department of Political Science, University of Copenhagen. hajh@ifs.ku.dk 
"""
"This code was written by Henrik Hermansson, who reserves some rights. This code may be modified and used by anyone, granted that this source is cited."

import collections
import re
import numpy
import csv
import string
import pylab
import matplotlib



def article_data_sorter(backtrace, artindex1, artindex2, lentext1, lentext2, artnames1, artnames2, propname, legname, caseid):

    artranges1 = artranger(artindex1, lentext1) # Create ranges delineating each article with a lower and upper bound (index)
    artranges2 = artranger(artindex2, lentext2)

    for step in backtrace: # Loop over each step in the backtrace
        rowindex = step[1] # Establish which row (index in text 1) the step was on
        columnindex = step[0] # Same for column
        for j, ar in enumerate(artranges1):
            if ar[0] <= rowindex and rowindex <= ar[1]: # With last row, find whic article the step belongs in (text1)
                for k, ar2 in enumerate(artranges2):
                    if ar2[0] <= columnindex and columnindex <= ar2[1]: # Same for text 2
                        ar[2].append([step[2], artnames2[k]]) # Sort the step into a specific article and save it there
                        break
                break

    new_lines = []            
    for i, ar in enumerate(artranges1): # Loop over each article in text1
        ar.append(caseid)
        ar.append(propname) # save the case name
        ar.append(legname)
        ar.append(artnames1[i]) # save the name of the article
        ar.append("All") # Save indicator that this is all the changes (or matches) for this particular article
        allwords = [row[0] for row in ar[2]]
        c = collections.Counter(allwords) # With last row, count the number of matches, additions etc. Save them with the lines below
        ar.append(c["match"])
        ar.append(c["addition"])
        ar.append(c["substitution"])
        ar.append(c["transposition"])
        ar.append(c["deletion"])
        ar.append(len(allwords) - c["match"])
#        del allwords
#        if destination == "yes": #If we also want to save if sections of the article have been moved to other articles
#            wtdg = wheredidtheygo(ar, artnames2) # Identify whether parts of article was moved to other articles and if so which.
#            for line in wtdg: # Save this information into the output
#                new_lines.append([caseid, propname, legname, artnames1[i], line[0], line[1]["match"], line[1]["addition"], line[1]["substitution"], line[1]["transposition"], line[1]["deletion"]])
        ar.pop(2)
        ar.pop(1)
        ar.pop(0)
#    if destination == "yes": 
#        artranges1 = artranges1 + new_lines # Complete the saving
    del new_lines

    return artranges1       
    
    
def wheredidtheygo(ar, artnames2):
    artnames_out = []
    for i, article in enumerate(artnames2): # Loop over the articles in the second text. Remember, this function is called article-by-article from text1.
        article = [artnames2[i], []] # Make it easier to store list of matches, additions ets
        for step in ar[2]: # Loop over each step of the backtrace belonging in this article (in text1)
            if re.sub(r'\n|\s', '', str(step[1])).upper() == re.sub(r'\n|\s', '', str(article[0])).upper(): # If the backtrace belongs in this article in the second text...
                article[1].append(step[0]) #... Store that this is where the match, addition etc took place in the second text. 
        article[1] = collections.Counter(article[1]) # Reduce the backtrace to the number of matches, additions etc and store that instead
        if len(article[1]) != 0: # If none of the backtrace steps ended up in this article in text 2, sort them away, store the rest.
            artnames_out.append(article)
    return artnames_out


def article_data_sorter_reverse(backtrace, artindex1, artindex2, lentext1, lentext2, artnames1, artnames2, propname, legname, destination, caseid):

    artranges1 = artranger(artindex1, lentext1) # Create ranges delineating each article with a lower and upper bound (index)
    artranges2 = artranger(artindex2, lentext2)

    for step in backtrace: # Loop over each step in the backtrace
        rowindex = step[0] # Establish which row (index in text 1) the step was on
        columnindex = step[1] # Same for column
        for j, ar in enumerate(artranges2):
            if ar[1] <= rowindex and rowindex <= ar[0]: # With last row, find whic article the step belongs in (text1)
                for k, ar2 in enumerate(artranges1):
                    if ar2[1] <= columnindex and columnindex <= ar2[0]: # Same for text 2
                        ar[2].append([step[2], artnames2[k]]) # Sort the step into a specific article and save it there
                        break
                break

    new_lines = []            
    for i, ar in enumerate(artranges2): # Loop over each article in text1
        ar.append(caseid)
        ar.append(propname) # save the case name
        ar.append(legname)
        ar.append(artnames2[i]) # save the name of the article
        ar.append("All") # Save indicator that this is all the changes (or matches) for this particular article
        allwords = [row[1] for row in ar[2]]
        c = collections.Counter(allwords) # With last row, count the number of matches, additions etc. Save them with the lines below
        ar.append(c["match"])
        ar.append(c["addition"])
        ar.append(c["substitution"])
        ar.append(c["transposition"])
        ar.append(c["deletion"])
        ar.append(len(allwords) - c["match"])
        del allwords
        if destination == "yes": #If we also want to save if sections of the article have been moved to other articles
            wtdg = wheredidtheygo(ar, artnames1) # Identify whether parts of article was moved to other articles and if so which.
            for line in wtdg: # Save this information into the output
                new_lines.append([caseid, propname, legname, artnames2[i], line[0], line[1]["match"], line[1]["addition"], line[1]["substitution"], line[1]["transposition"], line[1]["deletion"]])
        ar.pop(2)
        ar.pop(1)
        ar.pop(0)
    if destination == "yes": 
        artranges1 = artranges1 + new_lines # Complete the saving
    del new_lines

    return artranges2      


def artindexer(textlist):	#This finds the index position of every incidence of the word "YODABABY"
    text= textlist
    artindex=[]
    for i, w in enumerate(text):
        if w == "DTBREAKPOINT":
            artindex.append(i)
    del text
    del textlist
    return artindex
    

def artranger(artindex, lentext):
    artranges = []
    if len(artindex) == 0:
        upper = 0
    else:
        for i, index in enumerate(artindex): # Loop through the article break points 
            if i == 0: # Special for the first break point, establish lowest bound of first article (recitals)
                lower = 0
            else:
                lower = artindex[i-1] # Set lower bound for all other articles
            upper = index # Set the upper bound of the article
            artranges.append([lower, upper, []]) # Save bounds to establish an index range of the article
    del artindex
    artranges.append([upper, lentext, []]) # Save the top bound of the last article
    return artranges


def backtrace_line_matrix(lentext1, lentext2, ROWbacktrace):
    matrix = [[20] * (lentext2 +1) for i in xrange(lentext1 + 1)] # Create nested list ~ a matrix with height of number of words in first text and width of number of words in second text
    matrix2 = numpy.array(matrix)
    del matrix
    del lentext1
    del lentext2

    for j, step in enumerate(ROWbacktrace):
        if ROWbacktrace[j][2] == "match":
            matrix2[ROWbacktrace[j][1]][ROWbacktrace[j][0]] = 0
        if ROWbacktrace[j][2] == "substitution":
            matrix2[ROWbacktrace[j][1]][ROWbacktrace[j][0]] = 13
        if ROWbacktrace[j][2] == "addition":
            matrix2[ROWbacktrace[j][1]][ROWbacktrace[j][0]] = 8
        if ROWbacktrace[j][2] == "deletion":
            matrix2[ROWbacktrace[j][1]][ROWbacktrace[j][0]] = 5
        if ROWbacktrace[j][2] == "transposition":
            matrix2[ROWbacktrace[j][1]][ROWbacktrace[j][0]] = 16
    del ROWbacktrace
    return matrix2

def backtrace_block_matrix(lentext1, lentext2, ROWbacktrace):
    matrix = [[20] * (lentext2 +1) for i in xrange(lentext1 + 1)] # Create nested list ~ a matrix with height of number of words in first text and width of number of words in second text
    matrix = numpy.array(matrix)
    del lentext1
    del lentext2

    rbt = ROWbacktrace[::-1]
    del ROWbacktrace

    for j, step in enumerate(rbt):
        row = rbt[j][1]
        column = rbt[j][0]
        operation = rbt[j][2]
        value = rbt[j][3]
        if operation == "match":
            matrix[row-value:row, column-value:column] = 0
        if operation == "substitution":
            matrix[:, column] = 13
            matrix[row,:] = 13
        if operation == "addition":
            matrix[:,column] = 8
        if operation == "deletion":
            matrix[row,:] = 5
#        if ROWbacktrace[j][2] == "transposition":
#            matrix[ROWbacktrace[j][1]][ROWbacktrace[j][0]] = 16
    del rbt
    return matrix
    
def backtrace_bar_matrix(rbt):
    matrix = []
    for j, step in enumerate(rbt):
        operation = rbt[j][2]
        if operation == "match":
            matrix.append([0])
        if operation == "substitution":
            matrix.append([13])
        if operation == "addition":
            matrix.append([8])
        if operation == "deletion":
            matrix.append([5])
        if operation == "transposition":
            matrix.append([16])                
    del rbt
    array = numpy.array(matrix)
    array = numpy.transpose(array)
    return array


def backtrace_writer(inputs, text1, text2, outpath, propname, legname, caseid):
    context = [["Text 1 index", "Text 2 index", "Edit operation", "Removed or substituted word", "Added or substituted word", "Word in both texts"]]
    for item in inputs:
        if item[2] == "addition":
            context.append([item[1], item[0],  item[2], "", text2[item[0]-1], ""])
        if item[2] == "deletion":
            context.append([item[1], item[0], item[2], text1[item[1]-1], "", ""])
        if item[2] == "substitution":
            if text1[item[1]-1] != text2[item[0]-1]:
                context.append([item[1], item[0], item[2], text1[item[1]-1], text2[item[0]-1], ""])   
            else:
                context.append([item[1], item[0], "", "", "", text2[item[0]-1]]) 
        if item[2] == "transposition":
            context.append([item[1], item[0], item[2], "", "", ""])   
        if item[2] == "match":
            context.append([item[1], item[0], "", "", "", text2[item[0]-1]])  
    with open(outpath + "backtraces/" + caseid + '-backtrace.csv', "wb") as g: # Save results
        writer = csv.writer(g, delimiter = ";")
        writer.writerows(context)
    g.close()  


def clean_and_make_list(text):
	text = text.upper() # Make uppercase
	text = string.split(text) # Turn into list
	text = [''.join(c for c in s if c not in string.punctuation) for s in text] # Remove punctuation
	text = [s for s in text if s] # Remove empty string created by removing punctuation
	return text



def plotter(plotarray, outpath, propname, legname, by_article, plottype, text1artindex, text2artindex, lentext1, lentext2, artnames1, artnames2):
    if plottype == "bar":
        fig, ax = matplotlib.pyplot.subplots(1, figsize=(10, 0.5)) #Set up plot
        my_cmap, my_norm = matplotlib.colors.from_levels_and_colors([-1, 4, 7, 12, 15, 19, 21], ['green', 'red', 'orange', 'yellow', 'blue', 'white']) #Designate colors by setting bins of values (first list) and colors (second list)
        pylab.pcolormesh(plotarray, cmap = my_cmap, norm=my_norm) # Fill plot with values, i.e. colors
        matplotlib.pyplot.axis([0, plotarray.shape[1], 0, 1]) # Set axis dimensions
        ax.set_xlabel("Backtrace: " + propname + " into " + legname) #Set axis label
        ax.xaxis.set_label_position('top') # Set x-aixs label position
        ax.axes.get_yaxis().set_visible(False)
        p1 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="green") # 5 Legend boxes wth their color codes
        p2 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="red")
        p3 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="orange")
        p4 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="yellow")
        p5 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="blue")
        lgd = ax.legend([p1, p2, p3, p4, p5], ["Unchanged", "Deletion", "Addition", "Substitution", "Transposition"], bbox_to_anchor=(1,-0.5), ncol=2) # Add legend ... loc='lower center', 
        
    if plottype == "block":
        fig, ax = matplotlib.pyplot.subplots(1, figsize=(10,(10*float(lentext1)/lentext2))) #Set up plot
        my_cmap, my_norm = matplotlib.colors.from_levels_and_colors([-1, 4, 7, 12, 15, 19, 21], ['green', 'red', 'orange', 'yellow', 'blue', 'white']) #Designate colors by setting bins of values (first list) and colors (second list)
        pylab.pcolormesh(plotarray, cmap = my_cmap, norm=my_norm) # Fill plot with values, i.e. colors
        ax.xaxis.tick_top() # Put x-axis ticks on top
        pylab.xticks([1.5, lentext2+0.5]) # Puts a tick on first and last word
        ax.set_xticklabels([1, lentext2]) # Labels those ticks
        pylab.yticks([1.5, lentext1+0.5]) # Same as above but for y-axis
        ax.set_yticklabels([1, lentext1]) #.. again
        ax.set_ylabel(propname) # Set axis label
        ax.set_xlabel(legname) #Set axis label
        ax.xaxis.set_label_position('top') # Set x-aixs label position
        matplotlib.pyplot.axis([0, lentext2+1, 0, lentext1+1]) # Set axis dimensions
        p1 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="green") # 5 Legend boxes wth their color codes
        p2 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="red")
        p3 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="orange")
        p4 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="yellow")
#        p5 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="blue")
        lgd = ax.legend([p1, p2, p3, p4], ["Unchanged", "Deletion", "Addition", "Substitution"], loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=2) # Add legend
        if by_article == "article": # If an article-by-article plot is requested...
            text1artranges = artranger(text1artindex, lentext1) # Find the article break points and names
            text2artranges = artranger(text2artindex, lentext2) 
            for i, art in enumerate(text2artranges):
                matplotlib.pyplot.axvline(art[1]+1, color='grey', linestyle='-', linewidth=1) # Plot line at every article break point
                matplotlib.pyplot.annotate(artnames2[i], (numpy.mean([float(art[0]), art[1]]), lentext1/25), fontsize="small", ha="center", va="center") # Plot name of every article, does not work very well when loads of articles because of space limitations
            for j, art in enumerate(text1artranges): # Same but for y-axis
                matplotlib.pyplot.axhline(art[1]+1, color='grey', linestyle='-', linewidth=1)
                matplotlib.pyplot.annotate(artnames1[j], (lentext2/25, numpy.mean([float(art[0]), art[1]])), rotation = 90, fontsize="small", ha="center", va="center")
        matplotlib.pyplot.gca().invert_yaxis() # Plot so that origo is at top left        

    if plottype == "line":
        fig, ax = matplotlib.pyplot.subplots(1, figsize=(10,(10*float(lentext1)/lentext2))) #Set up plot
        my_cmap, my_norm = matplotlib.colors.from_levels_and_colors([-1, 4, 7, 12, 15, 19, 21], ['black', '#8B0000', '#D2691E', '#FF8C00', '#F0E68C', 'white']) #Designate colors by setting bins of values (first list) and colors (second list)
        pylab.pcolormesh(plotarray, cmap = my_cmap, norm=my_norm) # Fill plot with values, i.e. colors
        ax.xaxis.tick_top() # Put x-axis ticks on top
        pylab.xticks([1.5, lentext2+0.5]) # Puts a tick on first and last word
        ax.set_xticklabels([1, lentext2]) # Labels those ticks
        pylab.yticks([1.5, lentext1+0.5]) # Same as above but for y-axis
        ax.set_yticklabels([1, lentext1]) #.. again
        ax.set_ylabel(propname) # Set axis label
        ax.set_xlabel(legname) #Set axis label
        ax.xaxis.set_label_position('top') # Set x-aixs label position
        matplotlib.pyplot.axis([0, lentext2+1, 0, lentext1+1]) # Set axis dimensions
        p1 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="black") # 5 Legend boxes wth their color codes
        p2 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="#8B0000")
        p3 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="#D2691E")
        p4 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="#FF8C00")
        p5 = matplotlib.pyplot.Rectangle((0, 0), 1, 1, fc="#F0E68C")
        lgd = ax.legend([p1, p2, p3, p4, p5], ["Unchanged", "Deletion", "Addition", "Substitution", "Transposition"], loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=2) # Add legend
        if by_article == "article": # If an article-by-article plot is requested...
            text1artranges = artranger(text1artindex, lentext1) # Find the article break points and names
            text2artranges = artranger(text2artindex, lentext2) 
            for i, art in enumerate(text2artranges):
                matplotlib.pyplot.axvline(art[1]+1, color='grey', linestyle='-', linewidth=1) # Plot line at every article break point
                matplotlib.pyplot.annotate(artnames2[i], (numpy.mean([float(art[0]), art[1]]), lentext1/25), fontsize="small", ha="center", va="center") # Plot name of every article, does not work very well when loads of articles because of space limitations
            for j, art in enumerate(text1artranges): # Same but for y-axis
                matplotlib.pyplot.axhline(art[1]+1, color='grey', linestyle='-', linewidth=1)
                matplotlib.pyplot.annotate(artnames1[j], (lentext2/25, numpy.mean([float(art[0]), art[1]])), rotation = 90, fontsize="small", ha="center", va="center")
        matplotlib.pyplot.gca().invert_yaxis() # Plot so that origo is at top left

    pylab.savefig(outpath + 'plots/' + propname + "-" + legname + "-" + plottype + '.png', bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=1000)
    pylab.close()

def superloop(mat, cutoff):
    MatShape= mat.shape
    lastrow = MatShape[0]-1
    lastcol = MatShape[1]-1
    ROWbacktrace=[]
    collist=[]
    rowlist = []
    row = lastrow
    lastrowmaxindex = lastcol
    lastusedrow = lastrow
    MED = 0

    while row >= 1: # Loop, weeeeeee!
        rowcontents = list(mat[row,:]) # Store row contents in a nice, simple list format, rather than numpy array
        maxrowindex_found = 0 # Set up loop
        maxno = -1 # Set up loop
        while maxrowindex_found == 0: #Start loop to find the best match on the row
            best_max = sorted(set(rowcontents))[maxno] #Identify the best match, the second best, etc, depending on value of maxno. First iteration will find best match, then maxno decreases and it finds second best match...           
            best_max_index = [k for k, j in enumerate(rowcontents) if j == best_max] #Identify index of best match(es)          
            if best_max == 0: #If there is no (valid) match...
                rowmax = 0 #... the rowmax is zero
                maxrowindex_found = 1 #We can't find a better (or worse) match than that, job done.
            else: #If there are potentially valid matches
                for item in best_max_index: #Loop through potential matches
                    if item not in collist and (best_max > cutoff or item == lastrowmaxindex -1):
                        if best_max == numpy.amax(mat[:, item]): #If the match is also the highest value on the column...
                            rowmax = best_max #...then we have found the highest value on the row that is simultaneously the highest value on its column
                            rowmaxindex = item # Save the index
                            maxrowindex_found = 1 #Job done.
                            break #Stops the code looking for additional candidates, which would be uneccessary
                
            maxno = maxno - 1 #If none of the potential matches where valid, ie where also highest value in their respective columns -> subtract 1 from maxno to try "worse" but potentially valid matches

        if rowmax > 0: # If there is a match
            ROWbacktrace.append([rowmaxindex, row, "match", rowmax]) # Save coordinates and that there was a match
            collist.append(rowmaxindex) # Save, for loop purposes, the columns used
            rowlist.append(row)
            lastrowmaxindex = rowmaxindex # Set current rowmax as the last rowmax in preparation for next step of loop
            lastusedrow = row
        row = row - 1 # Move on to next row
#        else:
#            lastrowmaxindex = lastrowmaxindex - 1


    del mat

    row = 0
    column = 0
    while row < lastrow and column < lastcol: # Loop over the columns     
        if row+1 not in rowlist:
            if column+1 not in collist and column+1 <= lastcol:
                ROWbacktrace.append([column+1, row+1, "substitution", 0]) # ... then we are dealing with a substitution
                collist.append(column+1) # Save backtrace coorindates for the cell diagonally down from the last cell
                rowlist.append(row+1)
                MED = MED + 1
                column = column + 1
                row = row + 1
            else:
                ROWbacktrace.append([column, row+1, "deletion", 0]) # ... then we are dealing with a substitution
                rowlist.append(row+1)
                MED = MED + 1
                row = row+1
        else:
            if column+1 not in collist:
                ROWbacktrace.append([column+1, row, "addition", 0]) #Then save the rowmaxindex in the backtrace coordinates
                collist.append(column+1)
                MED = MED + 1
                column = column+1
            else:
                bestcol = 0
                for i, item in enumerate(ROWbacktrace):
                    if row+1 == item[1] and item[0] > bestcol and (item[2] == "match"):
                        column = item[0]
                row = row+1
    while row < lastrow:
        if row+1 not in rowlist:
                ROWbacktrace.append([column, row+1, "deletion", 0]) # ... then we are dealing with a substitution
                rowlist.append(row+1)
                MED = MED + 1
                row = row+1      
        else: 
            row = row+1

    while column < lastcol:
        if column+1 not in collist:
                ROWbacktrace.append([column+1, row, "addition", 0]) # ... then we are dealing with a substitution
                collist.append(column+1)
                MED = MED + 1
                column = column+1      
        else: 
            column = column+1

#    ROWbacktrace.sort(key = lambda row: row[1])
#    for i, item in enumerate(ROWbacktrace):
#        if i>0 and i<len(ROWbacktrace)-1:
#            if item[2] == "match" and ROWbacktrace[i-1][2] != "addition" and ROWbacktrace[i-1][1] != item[1]-1:
#                ROWbacktrace[i][2] = "transposition"

    ROWbacktrace.sort(key = lambda row: row[1])
    for i, item in enumerate(ROWbacktrace):
        if i>0 and i<len(ROWbacktrace)-1:
            if item[2] == "match" and ROWbacktrace[i-1][0] != item[0]-1:
                ROWbacktrace[i][2] = "transposition"           
   
    

    return [ROWbacktrace, MED]

def text_compare(text1, text2):
    matrix2 = [[0] * (len(text2) + 1) for i in xrange(len(text1) + 1)] # Create nested list ~ a matrix with height of number of words in first text and width of number of words in second text
    matrix = numpy.array(matrix2)	#This can be edited out, but apparently is more memory efficient (if I am using it right!)
    del matrix2
    for i, word1 in enumerate(text1): # Loop over each word in text1
        for j, word2 in enumerate(text2): # Compare to each word in text2
            if word1 != word2: # If they do not match...
                matrix[i+1][j+1] = 0 # Assign a value of zero
            else: # If the words do match...
                matrix[i+1][j+1] = matrix[i][j] + 1 # Assign a value equal to the last word pair plus 1
    return matrix


