import csv
from hl7apy.core import Message, Segment
from datetime import datetime

#def convert_date_to_hl7_format(date_str):
#    try:
#        # Assuming input format is YYYY/MM/DD
#        return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y%m%d')
#    except ValueError:
#        print(f"Failed to convert date: {date_str} DOB FIELD")
#        return None

def csv_to_hl7(csv_filename):
    hl7_messages = []
    # Get current date and time
    now = datetime.now()

    # Format as YYYYMMDDHHMMSS
    formatted_date = now.strftime('%Y%m%d%H%M%S')
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        ##hsn_list is for making sure we don't repeat redundant fields like msh or pid
        hsn_list = []
        index = 1
        for row in reader:
            # Create MSH segment
            #####msh = Segment("MSH", msg)
            #print(row['LAB_ID'])
            if row['LAB_ID'] not in hsn_list:
                index = 1 # we use this to track Multiple segments
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
                #msg.pid.PID_7 = convert_date_to_hl7_format(row["PATIENT_DOB"])
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
                msg.dg1.DG1_1 = '1'
                msg.dg1.DG1_3 = row['DX_CODE']
                msg.dg1.DG1_4 = 'Description???'
                msg.dg1.DG1_19 = ''
                
                msg.gt1.GT1_1 = '1'
                msg.gt1.GT1_2 = 'Account# ???'
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
                msg.in1.IN1_17 = 'Relationship code ????'
                msg.in1.IN1_18 = row['PATIENT_DOB']
                msg.in1.IN1_19 = row['PATIENT_ADDRESS']
                msg.in1.IN1_36 = row['INS1_POLICY_NUM']
                msg.in1.IN1_49 = ''
                
                #print(pid)
                hl7_messages.append(msg)
                
            ft1 = msg.add_segment('FT1')
            ft1.ft1_1 = f'{index}'
            ft1.ft1_22 = row['LAB_ID']
            
            ##we put the labid in the hsn_list for check on the next itteration
            hsn_list.append(row['LAB_ID'])
            
            index = index + 1
            ##
    return hl7_messages


##Main Function
if __name__ == "__main__":
    # Convert CSV to HL7
    hl7_list = csv_to_hl7('test.csv')

    #print(hl7_list)
    # Print or store the HL7 messages

    #for hl7 in hl7_list:
        #print(hl7.msh.value)
        #print(hl7.pid.value)
   
    # for hl7 in hl7_list:
       # print(hl7.ft1.ft1_22.value)
   
    #file.write(str(hl7_list))
    for hl7 in hl7_list:
        with open(f'{hl7.ft1.ft1_22.value}.hl7', 'w') as file:
            file.write(hl7.msh.value + '\n')
            file.write(hl7.pid.value + '\n')
            file.write(hl7.pv1.value + '\n')
            for transaction in hl7.ft1:
                file.write(transaction.value + '\n')
            #file.write(hl7.ft1.value + '\n')
            file.write(hl7.dg1.value + '\n')
            file.write(hl7.gt1.value + '\n')
            file.write(hl7.in1.value + '\n')
            file.write('\n\n\n')