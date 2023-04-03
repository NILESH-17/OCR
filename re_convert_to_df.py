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

def text_to_csv():
    
    #----
    client_data = {}

    #Define path for Input Folder
    os.chdir('C:/Users/Guest_01/Desktop/2023_output')
    my_files = glob.glob('*.txt')
    #print(my_files)

    for myfile in my_files:
        #print(myfile)
        if '.' in myfile[:-4]:
            myfile = myfile.replace('.','')
        with codecs.open(f'C:/Users/Guest_01/Desktop/2023_output/{myfile[:-4]}.txt', 'r', encoding="latin1") as f: 
            c= f.read()
        
        Tier_re = r"Tier\s+(\d)" #Tier #Done [No Issue]
        Hours_re = r"Arbor\s+Tutors\s+agrees\s+to\s+provide\s(\d+.*\d+)\s+hours" #Tutoring Hours #DONE [No Issue]
        Total_pay_re = r"Client\s+agrees\s+to\s+pay\s+a\s+total\s+of\s+[$]\s+[.*]\s+(\d+.*)"
        Client_name = r"This\s+agreement\s+is\s+between\s+(.*).*[(]" #Client_Name #DONE [No Issue]
        Contract_ID = r"DocuSign\s+Envelope\s+ID:\s+(.*)" #Contract/Document ID #Done [No Issue]
        Contract_Date = r"\d+/\d+/\d+" #Contract/Document Date #DONE [No Issue]
        Contract_Type_NEGOTIATED_CONTRACT_FOR_TUTORING = r"NEGOTIATED\s+CONTRACT\s+FOR\s+TUTORING"
        Contract_Type_CONTRACT_FOR_TUTORING = r"CONTRACT\S+FOR\S+TUTORING"
        Contract_discount = r"receiving\s+a\s+discount\s+of\s+(.*\d+)"
        Phone_number_1 = r"(\d+-\d+-\d+|\d+)\s+.*\s+.*?\s+Phone\s+Number" #Phone Number
        Phone_number_2 = r"(\d+-\d+-\d+|\d+).*\s+Phone\s+Number"
        Score = r"guarantees a score of\s+(\d.*)\+"

        tier= re.findall(Tier_re, c)[0]
        hours = re.findall(Hours_re, c)[0]
        total_pay = re.findall(Total_pay_re, c) [0]
        client_name = re.findall(Client_name, c)[0]
        contract_id = re.findall(Contract_ID,c )[0]
        contract_date = re.findall(Contract_Date, c )[0]
        negotiated_contract_for_tutoring = re.findall(Contract_Type_NEGOTIATED_CONTRACT_FOR_TUTORING, c)
        contract_for_tutoring = re.findall(Contract_Type_CONTRACT_FOR_TUTORING, c)
        contract_discount = re.findall(Contract_discount,c)
        phone_number_1 = re.findall(Phone_number_1,c)
        phone_number_2 = re.findall(Phone_number_2,c)
        score = re.findall(Score,c)[0]


        if contract_id:
            print('contract_id:', contract_id)
        else:
            print(f'Contract ID for is not available')


        if Client_name:
            client_name = client_name.replace(' ','')
            client_name = re.sub(r"\B([A-Z])", r" \1", client_name)
            print('Client_name:', client_name)
        else:
            print('not available')


        if tier:
            print('tier:', tier)
        else:
            print(f'tier for {client_name} is not availabale')

        if hours:
            hours = int(hours.replace(' ','')[:2])
            print('hours:', hours)
        else:
            print(f'hours for {client_name} is not availabale')

        if total_pay:
            total_pay = total_pay.replace(',','')
            total_pay = total_pay.replace(' ','')
            print('total_pay:', total_pay)
        else:
            print(f'total pay  for {client_name} is not availabale')


        if contract_date:
            print('contract_date:', contract_date)
        else:
            print(f'contarct date for {client_name} is not available')
        
        if contract_discount:
            print(type(contract_discount))
             #contract_discount = (contract_discount[0])
             #client_data['contract discount'] = contract_discount


        if phone_number_1:
             phone_number_1 = ''.join(phone_number_1)
             client_data['phone number'] = phone_number_1[0]
        elif phone_number_2:
             print(phone_number_2)
             client_data['phone number'] = phone_number_2[0]


        if negotiated_contract_for_tutoring:
            negotiated_contract_for_tutoring = set(negotiated_contract_for_tutoring)
            negotiated_contract_for_tutoring = " ".join(str(x) for x in negotiated_contract_for_tutoring)
            print('type_of_contract:', negotiated_contract_for_tutoring)
        elif contract_for_tutoring:
            print('type_of_contract:', contract_for_tutoring)
        else:
            print('contract type for {client name} can not be determined')
            
        client_data['contract discount'] = contract_discount[0]  
        #client_data['phone number'] = phone_number_1   
        client_data['contract id'] = contract_id
        client_data['name'] = client_name
        client_data['tier'] = tier
        client_data['tuting hours'] = hours
        client_data['contract date'] = contract_date
        client_data['total pay'] = float(total_pay)

#print(client_data)
        print(client_data)
        print(score)

text_to_csv()
