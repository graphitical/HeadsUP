import PyPDF2 as ppdf
from pathlib import Path
import os, sys

def main():
    n = 0 # debugging
    if len(sys.argv) < 2:
        print('usage: pdf_retitler.py input/pdf/dir output/pdf/dir')
    else:
        DIR = sys.argv[1]
        NEW_DIR = sys.argv[2]
        if not os.path.exists(NEW_DIR):
            os.mkdir(NEW_DIR)

        for file in Path(DIR).rglob('*.pdf'):
            print('Old File Name:',file.name)
            input_pdf = ppdf.PdfFileReader(os.path.join(DIR,file.name),'rb')
            

            pdf_title = input_pdf.getDocumentInfo().title
            print('PDF Title:',pdf_title)
            # manipulate title to be whatever you want
            new_fname = ''.join(filter(str.isalnum, pdf_title)) + '.pdf'
            print('New File Name',new_fname)

            # new path to save retitled pdf file
            output_path = os.path.join(NEW_DIR,new_fname)
            print('Out Path:',output_path)
            
            # copy current pdf
            output_pdf = ppdf.PdfFileWriter()
            for page in input_pdf.pages:
                output_pdf.addPage(page)
                
            # save pdf
            with open(output_path,'wb') as output_file:
                output_pdf.write(output_file)
                
            # debugging
            # if n > 2: break
            # n += 1


if __name__ == '__main__':
    main()
