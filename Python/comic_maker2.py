#!/usr/bin/python

# Generate PDF file
# python executable

#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################
#  Written by Zhihua Liang 2013
#  zliang5@central.uh.edu
#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################

import glob
import os
import re
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.units import inch

#----------------------------------------------------------------------
def sorted_nicely( l ): 
    """ 

    """ 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#----------------------------------------------------------------------
def create_comic( path):
    """"""
    filename = os.path.join(path, fname + ".pdf")
    doc = SimpleDocTemplate(filename,pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    width = 7.5*inch
    height = 9.5*inch    
    
    pictures = sorted_nicely(glob.glob(path + "\\%s*" % fname))
    
    Story.append(PageBreak())
    
    x = 0
    page_nums = {100:'%s_101-200.pdf', 200:'%s_201-300.pdf',
                 300:'%s_301-400.pdf', 400:'%s_401-500.pdf',
                 500:'%s_end.pdf'}
    for pic in pictures:
        parts = pic.split("\\")
        p = parts[-1].split("%s" % fname)
        page_num = int(p[-1].split(".")[0])
        print "page_num => ", page_num
        
        im = Image(pic, width, height)
        Story.append(im)
        Story.append(PageBreak())
        
        if page_num in page_nums.keys():
            print "%s created" % filename 
            doc.build(Story)
            filename = os.path.join(path, page_nums[page_num] % fname)
            doc = SimpleDocTemplate(filename,
                                    pagesize=letter,
                                    rightMargin=72,leftMargin=72,
                                    topMargin=72,bottomMargin=18)
            Story=[]
        print pic
        x += 1
        
    doc.build(Story)
    print "%s created" % filename
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    create_comic(sys.argv[1])
