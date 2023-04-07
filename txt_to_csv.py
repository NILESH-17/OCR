#Import Required Modules
import calendar
from datetime import datetime, timedelta

def days_in_month(dt):
    return calendar.monthrange(dt.year, dt.month)[1]

def monthly_range(dt_start, dt_end):
    forward = dt_end >= dt_start
    finish = False
    dt = dt_start

    while not finish:
        yield dt.date()
        if forward:
            days = days_in_month(dt)
            dt = dt + timedelta(days=days)            
            finish = dt > dt_end
        else:
            _tmp_dt = dt.replace(day=1) - timedelta(days=1)
            dt = (_tmp_dt.replace(day=dt.day))
            finish = dt < dt_end
#date_start = datetime(2017, 1, 1)
#date_end = datetime(2016, 6, 1)

#for p in monthly_range(date_start, date_end):
#    print(type(p))

#------------------------------------------------------------
#-----------------  
import calendar
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import pdfplumber
import glob
import os
import re
import codecs
from pathlib import Path
from datetime import datetime

#Function to convert text files to csv
def text_to_csv(input_folder, output_folder, debug=True):
    data = []
    
    #Define path for Input Folder
    input_path = Path(input_folder)
    my_files = glob.glob(f'{input_path}/*.txt')
  
    if len(my_files) == 0:
        raise FileNotFoundError("nothing.txt was not found or is a directory")
    
    for myfile in my_files:
        client_data = {}
        
        if '.' in myfile[:-4]:
            myfile = myfile.replace('.','')
            
        with codecs.open(myfile, 'r', encoding="latin1") as f: 
            c= f.read()
        
        #in  some cases total pay includes "," to remove "," replacing it.
        c = c.replace(',','')
        
        #Write RE pattern to extract Required Data
        
        Tier_re = r"Tier\s+(\d)" 
        Hours_re = r"Arbor\s+Tutors\s+agrees\s+to\s+provide\s(\d+.*\d+)\s+hours" 
        Total_pay_re = r"Client\s+agrees\s+to\s+pay\s+a\s+total\s+of\s+[$]\s+[.*]\s+(\d+.*)"
        Client_name = r"This\s+agreement\s+is\s+between\s+(.*).*[(]" 
        Contract_ID = r"DocuSign\s+Envelope\s+ID:\s+(.*)" 
        Contract_Date = r"\d+/\d+/\d+" 
        Contract_Type_NEGOTIATED_CONTRACT_FOR_TUTORING = r"NEGOTIATED\s+CONTRACT\s+FOR\s+TUTORING"
        Contract_Type_CONTRACT_FOR_TUTORING = r"CONTRACT\S+FOR\S+TUTORING"
        Contract_discount = r"receiving\s+a\s+discount\s+of\s+(.*\d+)"
        Phone_number_1 = r"(\d+-\d+-\d+|\d+)\s+.*\s+.*?\s+Phone\s+Number"
        Phone_number_1 = r"(\d{10})"
        Phone_number_2 = r"(\d+-\d+-\d+|\d+).*\s+Phone\s+Number"
        Phone_number_2 = r"([\d]{3}-{0,1}[\d]{3}-{0,1}[\d]{4}).*\s+Phone\s+Number"
        Phone_number_2 = r"([\d]{3}-[\d]{3}-[\d]{4})"
        Total_pay_re1 = r"agrees\s+to\s+pay\s+a\s+total\s+of\s+[$]\s+[.]\s+(\d+(?:\.\d+)?)"
        Total_pay_re2 = r"agrees\s+to\s+pay\s+a\s+total\s+of\s+[$]\s+(\d.*)"
        Subject = r"tutoring\s+to\s+Client\s+or\s+(.*)\s+their\s+dependent"
        Bonus_hours = r"(\d.*\d+)\s+hours\s+of\s+tutoring|for\s+free"
        Guarantee_score = r"guarantees\s+a\s+score\s+of\s+(\d.*\d+)"
        Initial_payment = r"initial\s+payment\s+of\s+[$]\s+(\d.*)\s+to\s+Arbor\s+Tutors"
        Fee_structure = r"[$](.*)"
               
        #Apply regex on Extracted data
        
        tier= re.findall(Tier_re, c)[0]
        hours = re.findall(Hours_re, c)[0]
        client_name = re.findall(Client_name, c)[0]
        contract_id = re.findall(Contract_ID,c )[0]
        contract_date = re.findall(Contract_Date,c)
        negotiated_contract_for_tutoring = re.findall(Contract_Type_NEGOTIATED_CONTRACT_FOR_TUTORING, c)
        contract_for_tutoring = re.findall(Contract_Type_CONTRACT_FOR_TUTORING, c)
        contract_discount = re.findall(Contract_discount,c)
        phone_number_1 = re.findall(Phone_number_1,c)
        phone_number_2 = re.findall(Phone_number_2,c)
        subject = re.findall(Subject,c)
        bonus_hours = re.findall(Bonus_hours,c)
        guarantee_score = re.findall(Guarantee_score,c)
        initial_payment = re.findall(Initial_payment,c)
        #-------FEE STRUCTURE
        fee_structure = re.findall(Fee_structure,c)
        
        
        #Write if-else block to parse required data
        
        # type of Contract
        if negotiated_contract_for_tutoring:
            negotiated_contract_for_tutoring = set(negotiated_contract_for_tutoring)
            negotiated_contract_for_tutoring = " ".join(str(x) for x in negotiated_contract_for_tutoring)
            client_data['type_of_contract'] = 'negotiated contract for tutoring'
        elif contract_for_tutoring:
            client_data['type_of_contract'] = 'contract for tutoring'
        else:
            client_data['type_of_contract'] = None
        
        #Contract ID
        if contract_id:
            client_data['contract_id'] = contract_id.replace('\r','')
        else:
            client_data['contractid'] = None
        
        #Client Name
        if Client_name:
            client_name = client_name.replace(' ','')
            client_name = re.sub(r"\B([A-Z])", r" \1", client_name)
            client_data['name'] = client_name
        else:
            client_data['name'] = None
        
        #Tier
        if tier:
            client_data['tier'] = int(tier)
        else:
            client_data['tier'] = np.nan
        
        #Hours
        if hours:
            hours = int(hours.replace(' ','')[:2])
            client_data['tutoring_hours'] = int(hours)
        else:
            client_data['tutoring_hours'] = np.nan
        
        #Total Pay
        try:
            total_pay1 = re.findall(Total_pay_re1, c)[0]
            client_data['total_pay'] = float(total_pay1)
        except:
            total_pay2 = re.findall(Total_pay_re2, c)[0]
            total_pay2 = total_pay2.replace(',','')
            total_pay2 = total_pay2.replace(' ','')
            total_pay2 = re.findall("\d+\.\d+", total_pay2)
            total_pay2 = ''.join(total_pay2)
            client_data['total_pay'] = float(total_pay2)

        # Contract Date
        if contract_date:
            client_data['contract_date'] =  contract_date[0]#datetime.strptime(contract_date,'%m/%d/%Y') #Convert contract date to datetime type
        else:
            client_data['contract_date'] = None
        
        #Subject
        if subject:
            client_data['subject']  = subject[0].replace('\r','')
        else:
            client_data['subject']  = None
        
        #Bonus hours
        if bonus_hours:
            bonus_hours = bonus_hours[0].replace(' ','')
            client_data['bonus_hours']  = int(bonus_hours)
        else:
            client_data['bonus_hours']  = np.nan
        
        #Guarantee Score
        if guarantee_score:
            guarantee_score = guarantee_score[0].replace(' ','')
            client_data['guarantee_score']  = int(guarantee_score)
        else:
            client_data['guarantee_score']  = np.nan
        
        #Phone Number
        if phone_number_1:
             #phone_number_1 = ''.join(phone_number_1)
             client_data['phone_number'] = phone_number_1[0]
        elif phone_number_2:
             client_data['phone_number'] = phone_number_2[0].replace('-','')
        
        #Initial payment
        if initial_payment:
            client_data['initial_payment'] = float(initial_payment[0])
        else:
            client_data['initial_payment'] = np.nan
        
        #Fee Structure
        
        #1. --> FIRST INSTALLMENT DATE

        first_installment_date = fee_structure[2]
        FID = r"o\s+n\s+(.*)\s[$]"
        FID_ = re.findall(FID, first_installment_date)
        first_installment_date = ''.join(map(str,FID_))
        first_installment_date = first_installment_date.replace(' ','')
        
        if first_installment_date:
            first_installment_date = datetime.strptime(first_installment_date, '%B%d%Y')
            client_data['fee_start_date'] = first_installment_date
        else:
            client_data['fee_start_date'] = np.nan
        
        #2.-->  Last_installment_date
   
        last_installment_date = fee_structure[-1]
        last_installment_date = last_installment_date.strip('on')
        last_installment_date = last_installment_date.replace('\r','')
        last_installment_date = last_installment_date.replace('.','')
    
        if last_installment_date and 'on' in last_installment_date:
            last_installment_date = last_installment_date.split('on')[-1]
            last_installment_date = last_installment_date.replace(' ','')
            last_installment_date = datetime.strptime(last_installment_date, '%B%d%Y')
            client_data['fee_end_date'] = last_installment_date
        else:
            client_data['fee_end_date'] = np.nan
        
        #3.Number of Installments 
        
        if first_installment_date and last_installment_date:
            start = datetime.strptime(str(first_installment_date).split(' ')[0], "%Y-%m-%d")
            end =   datetime.strptime(str(last_installment_date).split(' ')[0], "%Y-%m-%d")

            # Get the interval between two dates
            diff = relativedelta.relativedelta(end, start)

            diff_in_months = diff.months + diff.years * 12
            number_of_installments = diff_in_months + 1 
            client_data['number_of_installments'] = int(number_of_installments)
        else:
            client_data['number_of_installments'] = np.nan
      
        
        #4. Fee Amount
        
        installment_amount = fee_structure[2]
        installment_amt_re = r"(\d.*.)\s+o n"
        installment_amt = re.findall(installment_amt_re, installment_amount)
        installment_amt = ''.join(i for i in installment_amt)
        installment_amt = installment_amt.replace(' ','')
        
        if installment_amt:
            client_data['fee_amount'] = installment_amt
        else:
            client_data['fee_amount'] = np.nan
        
        
        #Fee Structure
        
        fee_dates = []
        if installment_amt and first_installment_date:
            for pay_date in monthly_range(first_installment_date,last_installment_date):
                fee_dates.append(pay_date)
 
        fee_structure = {}
        for date in fee_dates:
            fee_structure[date] = installment_amt
            
        client_data['fee_structure'] = fee_structure
   
        #append Client data to data
        data.append(client_data)
    
    #Convert data to DF
    df = pd.DataFrame(data)
    df.to_csv(f'{output_folder}/processed_{date.today()}.csv')
    return df

parsed_df = text_to_csv('C:/Users/Guest_01/Desktop/2023_output', 'C:/Users/Guest_01/Desktop/2023_output')
#parsed_df.to_csv()
parsed_df
