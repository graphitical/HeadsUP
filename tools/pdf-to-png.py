import sys
import pathlib
print(sys.executable)
from pdf2image import convert_from_path
import os

# print("Hello")

outputDir = 'output/'
homeDir = '/Users/tgotfrid/Documents/CSE590G/pdf-to-png/'

conference = 'ASSETS'
year = '2019'

def convert():

    for file in os.listdir(homeDir):
        if not file.endswith('.pdf'):
            continue
        else:
            pdfTitle = file.replace('.pdf', '')
            pages = convert_from_path(file)
    
            counter = 1
            for page in pages:
                myfile = os.path.join(outputDir, conference + '_' + year + '_' + pdfTitle + '-page-' + str(counter)+'.png')
                counter = counter + 1
                page.save(myfile, "PNG")
                # print(myfile)

convert()