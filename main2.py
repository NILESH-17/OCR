import pdfplumber
import sys

with pdfplumber.open('C:/Users/Guest_01/Desktop/2023_input/__.pdf') as pdf:
    
    # iterate over each page
    for page in pdf.pages:
       # extract text
        text = page.extract_text()
        with open('C:/Users/Guest_01/Desktop/2023_output/extract.txt','a') as f:
            f.write(text)
        print(text)
