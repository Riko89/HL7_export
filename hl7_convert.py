#### Written by Eric Remington Davey  ####
import csv
from hl7apy.core import Message, Segment
from datetime import datetime
import os
from Libraries.encode64 import FileEncoder # calling our encode64.py code FileEncoder Class

def parse_relationship_code_coronis(relationship_string):
    relationship_string = relationship_string.upper()
    codes = {
        'SELF': '01',
        'SPOUSE': '02',
        'CHILD': '03',
        'OTHER': '04',
        'GRANDPARENT': '05',
        'GRANDCHILD': '06',
        'NEPHEW': '07',
        'NIECE': '07',
        'ADOPTED': '08',
        'ADOPTED CHILD': '08',
        'FOSTER CHILD': '09',
        'WARD': '10',
        'STEPCHILD': '11',
        'EMPLOYEE': '12',
        'UNKNOWN': '13',
        'HANDICAPPED': '14',
        'SPONSORED': '15',
        'MINOR': '16',
        'SIG. OTHER': '17',
        'MOTHER': '18',
        'FATHER': '19',
        'EMANCIPATED': '20',
        'ORGAN DRN.': '21',
        'CADAVER DNR.': '22',
        'PLAINTIFF': '23',
        'NO FIN.': '24',
        'LIFE PARTNER': '25',
        'OTHER ADULT': '26'
    }
    relation_code = codes.get(relationship_string)
    if code:
        print('relationship_code matched')
    else:
        relation_code = '13'
        print('no relationship_code, putting 13 as unknown')
    return relation_code

def read_encoded_file(lab_id):
    content = ''
    lab_id = f'Encoded_{lab_id}'
    for file_name in os.listdir('./processed'):
        name_without_extension, extension = os.path.splitext(file_name)
        if name_without_extension == lab_id:
            #print('Matched!')
            with open(f'./processed/{file_name}', 'r') as file:
                content = file.read()
            break
        else:
            content = '^APPLICATION^PDF^BASE64^'
        
    return content

def csv_to_hl7(csv_filename):
    hl7_messages = []
    hsn_list = [] #instantiate variables
    index = 1
    dg_index = 1
    # Get current date and time
    now = datetime.now()

    # Format as YYYYMMDDHHMMSS
    formatted_date = now.strftime('%Y%m%d%H%M%S')
    reader = ''
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
    ##hsn_list is for making sure we don't repeat redundant fields like msh or pid        
        for row in reader:
            # Create MSH segment
            #####msh = Segment("MSH", msg)
            #print(row['LAB_ID'])
            if row['LAB_ID'] not in hsn_list:
                index = 1 # we use this to track Multiple segments
                dg_index = 1
                # Create a new HL7 message
                #MAYBE CHANGE LATER
                msg = Message("ADT_A01")
                
                msg.msh.MSH_2 = "^~\&"
                msg.msh.MSH_3 = "HORIZON"
                msg.msh.MSH_4 = "PHAMATECH"
                msg.msh.MSH_5 = "PractiSource"
                msg.msh.MSH_6 = "CLINIC NAME?????"
                msg.msh.MSH_7 = f"{formatted_date}"
                msg.msh.MSH_9 = "PROCESSING ID????"
                msg.msh.MSH_10 = 'VERSION ID????'
                msg.msh.MSH_11 = 'P'
                msg.msh.MSH_12 = '2.7'
                msg.msh.MSH_19 = ''
                #msh.MSH_9 = "ADT^A01^ADT_A01"
                #msh.MSH_10 = "MessageControlID"
                #msh.MSH_11 = "P"
                #msh.MSH_12 = "2.5"

                # Add other segments (e.g., PID) based on the CSV row's data
                ###pid = Segment("PID", msg)
                msg.pid.PID_1 = '1'
                msg.pid.PID_3 = row["PATIENT_SSN"]
                msg.pid.PID_5 = row["PATIENT_NAME"]       
                msg.pid.PID_7 = row["PATIENT_DOB"] # We need to know what to put in the case of Missing Date of Birth
                msg.pid.PID_8 = row["PATIENT_SEX"]
                msg.pid.PID_11 = row["PATIENT_ADDRESS"]
                msg.pid.PID_13 = row["PATIENT_PHONE"]
                msg.pid.PID_18 = row["PATIENT_SSN"]
                msg.pid.PID_22 = ''
                
                #PD1 SECTION
                msg.pv1.PV1_1 = '1'
                msg.pv1.PV1_7 = 'Reffering Doctor (CORONIS HEALTH PROVIDING MD)????'
                #msg.pv1.PV1_7 = row['']
                msg.pv1.PV1_52 = ''
                                                                        
                ## multiple dg fields
                dg_temp = row['DX_CODE'].split(',') # get all DX codes
                for dx_code in dg_temp:
                    dg1 = msg.add_segment('DG1')
                    dg1.DG1_1 = f'{dg_index}'
                    dg1.DG1_3 = dx_code
                    dg1.DG1_4 = 'Description???'
                    dg1.DG1_19 = ''
                    dg_index = dg_index + 1
                
                msg.gt1.GT1_1 = '1'
                msg.gt1.GT1_2 = ''
                msg.gt1.GT1_3 = row['PATIENT_NAME']
                msg.gt1.GT1_5 = row['PATIENT_ADDRESS']
                msg.gt1.GT1_6 = row['PATIENT_PHONE']
                msg.gt1.GT1_8 = row['PATIENT_DOB']
                msg.gt1.GT1_9 = row['PATIENT_SEX']
                msg.gt1.GT1_55 = ''
                
                msg.in1.IN1_1 = '1'
                msg.in1.IN1_3 = 'CARRIER ID ????'
                msg.in1.IN1_4 = row['INS1_NAME']
                msg.in1.IN1_5 = row['INS1_ADDRESS']
                msg.in1.IN1_16 = row['PATIENT_NAME'] ## CHANGE LATER Will update toad script
                ##relationship code needs to be assigned based off of string
                relationship_code = parse_relationship_code_coronis(row['INS1_RELATIONSHIP_TO_INSURER'])
                
                msg.in1.IN1_17 = relationship_code
                msg.in1.IN1_18 = row['PATIENT_DOB']
                msg.in1.IN1_19 = row['PATIENT_ADDRESS']
                msg.in1.IN1_36 = row['INS1_POLICY_NUM']
                msg.in1.IN1_49 = ''
                
                msg.obx.OBX_1 = '1'
                msg.obx.OBX_2 = 'ED'
                msg.obx.OBX_3 = 'PDF'
                msg.obx.OBX_4 = 'Base64'
                read_encoded_file(row['LAB_ID'])
                msg.obx.OBX_5 = read_encoded_file(row['LAB_ID'])
                hl7_messages.append(msg)
            
            #for each itteration of loop until we reach next LAB_ID append another ft1 segment
            ft1 = msg.add_segment('FT1')
            ft1.ft1_1 = f'{index}'
            ft1.ft1_6 = 'CG'
            ft1.ft1_7 = 'CPT Code^Description'
            ft1.ft1_8 = row['DRUG_TEST']
            ft1.ft1_22 = row['LAB_ID']
            ft1.ft1_26 = '' 

            ##we put the labid in the hsn_list for check on the next itteration
            hsn_list.append(row['LAB_ID'])
            index = index + 1       #increment Index for next itteration of ft1
        
        #message_string = msg.to_er7()
    return hl7_messages


##Main Function
if __name__ == "__main__":
    # Convert CSV to HL7
    pdf_encoded = FileEncoder() #instantiate FileEncoder
    pdf_encoded.process_files()
    hl7_list = csv_to_hl7('access_output.csv')
    #testing
    #file.write(str(hl7_list))
    
    for hl7 in hl7_list:
        with open(f'{hl7.ft1.ft1_22.value}.hl7', 'w') as file:
            file.write(hl7.msh.value + '\n')
            file.write(hl7.pid.value + '\n')
            file.write(hl7.pv1.value + '\n')
            for transaction in hl7.ft1:
                file.write(transaction.value + '\n')
            #file.write(hl7.ft1.value + '\n')
            for dg1 in hl7.dg1:
                file.write(dg1.value + '\n')
            file.write(hl7.gt1.value + '\n')
            file.write(hl7.in1.value + '\n')
            file.write(hl7.obx.value + '\n')
            file.write('\n\n\n')
    
    