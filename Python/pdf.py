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

#========================== definitions ============================================
#image_path = 'testarea/testimage'



import os,string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib import utils
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak


def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def pdfDirectory(imageDirectory, outputPDFName):
    print 'creating ', outputPDFName
    doc = SimpleDocTemplate(outputPDFName,pagesize=landscape(A4),
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    story1 = []
    story2 = []
    story = []
    for root, dirs, files in os.walk(imageDirectory):
        files.sort()
        for name in files:
            if 'True' in name:
                filepath = os.path.join(root, name)
                story1.append( get_image(filepath, width = 22*cm) ) 
            if 'False' in name:
                filepath = os.path.join(root, name)
                story2.append( get_image(filepath, width = 22*cm) ) 
                    
        
    for i in range(len(story1)):
        story.append(story1[i])
        story.append(story2[i])
        story.append(PageBreak())
    
    doc.build(story)
    



#========================== main program ============================================

import sys

def main(argv):

# Parse command-line arguments

   input_path = sys.argv[1]
   name = sys.argv[2]

   print 'Input path is ', input_path

#   pdfDirectory(input_path,string.split(strinput_path,'/')[-1])
   pdfDirectory(input_path, name)
   

if __name__ == "__main__":
   main(sys.argv[1:])
