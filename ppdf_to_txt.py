#import required modules
import re
from pathlib import Path 
import glob
import pdfplumber
import os

#Funcion to convert pdf to txt
def extract_pdf_to_txt(input_folder, output_folder, debug=False):
    
    input_path = Path(input_folder)
    pdf_files = glob.glob(f'{input_path}/*.pdf')
    
    for myfile in pdf_files:
        with pdfplumber.open(myfile) as pdf:
            # iterate over each page
            for page in pdf.pages:
            # extract text
                text = page.extract_text()
            
                #1.==> Get **Contract ID** to add as a title for converted textfile
                Contract_ID = r"DocuSign\s+Envelope\s+ID:\s+(.*)"
                contract_id = re.findall(Contract_ID,text)[0]
                
                #Check If Output Folder exists..if not then Create new one.
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                
                #Write PDFs Extracted Data to Text files by Creating .txt file for each PDF file                                             
                with open(f'{output_folder}/{contract_id}.txt','a+', encoding="utf-8") as f:
                    f.write(text)
                    
#Function Call
extract_pdf_to_txt('C:/Users/Guest_01/Desktop/2023_input', 'C:/Users/Guest_01/Desktop/202P', debug=True)
