import sys
import pathlib
# print(sys.executable)
from pdf2image import convert_from_path
import os

print("Hello")

outputDir = 'output/'
# Change line 11
homeDir = '/Users/tgotfrid/Documents/CSE590G/pdf-to-png/'
# Change line 12 and 13
conference = 'CHI'
year = '2019'

def convert():

    for file in os.listdir(homeDir):
        if not file.endswith('.pdf'):
            continue
        else:
            pdfTitle = file.replace('.pdf', '')
            pages = convert_from_path(file)
            # outputPDFDir = os.path.join(outputDir, pdfTitle)
            # pathlib.Path(outputPDFDir).mkdir(parents=True, exist_ok=True)
    
            counter = 1
            for page in pages:
                myfile = os.path.join(outputDir, conference + year + '_' + pdfTitle + '_page_' + str(counter)+'.png')
                counter = counter + 1
                page.save(myfile, "PNG")
                print(myfile)

convert()