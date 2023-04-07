#Import Required Modules
import pdfplumber
import glob
import os
import re
import codecs

#Define path for Input Folder
#os.chdir('C:/Users/Guest_01/Desktop/2023_input')
#my_files = glob.glob('*.pdf')
#print(my_files)

#Funcion to convert pdf to txt
def extract_pdf_to_txt():
    for myfile in my_files:
        with pdfplumber.open(myfile) as pdf:
            # iterate over each page
            for page in pdf.pages:
            # extract text
                text = page.extract_text()
                print(text)
                with open(f'C:/Users/Guest_01/Desktop/2023_output/{myfile[:-4]}.txt','a', encoding="utf-8") as f:
                    f.write(text)

#extract_pdf_to_txt()
