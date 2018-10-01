#!/usr/bin/python

# This Python script would read log file line by line
# analyze log based on rules defined in rules file

# Assumption :  reading logs line by line is considered as streaming

import os
import time
import re
import yaml
from datetime import datetime


def load_yaml():    
#This funtion would load new rules as well from YAML files
    with open('rules.yaml', 'r') as f:
        data = yaml.load(f)

    global rsp_time 
    global errors

    rsp_time = data["rules"]["response_time"]
    errors = data["rules"]["errors"]

    print('response_time :'+ str(data["rules"]["response_time"]))
    print('errors :' + str(data["rules"]["errors"]))

    
def check_response_time():
    print ("I am analyzing log")
    #os.system('sh error_count.sh')
    os.system("awk '$1~/^[0-9]+$/' 'out.log' | cut -d ' ' -f 1,2,5 > .resp_time")
    count = 0
    dict1 = {}
    f = open('.resp_time','r')

    lines = [line for line in f.readlines() if line.strip()]

    for resp_time in lines:

        searchObj = re.search( r'(.*) (.*) .(.*).', resp_time)
        
        s = searchObj.group(1)+' '+ searchObj.group(2).split(".",maxsplit=1)[0]
        d = datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
        t = time.mktime(d.timetuple())        
        
        dict1[t] = searchObj.group(3).split("ms",maxsplit=1)[0]
    
    for k,v in dict1.items():
        print(k, 'corresponds to ', dict1[k]) 
        
        while (count <= 5):
            print("I am in wile loop")
            if(float(dict1[k]) > float(rsp_time)):
                cont_resp = 1
            else:
                cont_resp = 0
                break
            count = count + 1

        if(cont_resp == 1):
            print("we have response time > "+rsp_time+" for continuous 5secs")
        else:
            print("we do not have respnse time > "+rsp_time+" for continuous 5secs")
        
 
def check_number_errors():
    print ("I am printing errors with in a minute")
    os.system('sh error_count.sh')
    f = open('.error_count','r')
    lines = [line for line in f.readlines() if line.strip()]
    
    for error_count in lines:
        searchObj = re.search( r'(.*) (.*?) (.*)', error_count)

        if(int(searchObj.group(1)) > errors):
            print('Error count :'+searchObj.group(1)+'  '+'date and timestamp :'+searchObj.group(2) +' '+searchObj.group(3))
        # a function can be called for notification or update the file with relevant information
        else:
            pass
    f.close()        
        
def histogram_error():
    date1 = input("provide from date of errors in YYYY-MM-DD format :")
    year, month, day = map(int, date1.split('-'))
    from_date = datetime(year, month, day)
    date2 = input("provide from date of errors in YYYY-MM-DD format :")
    year, month, day = map(int, date2.split('-'))
    end_date = datetime(year, month, day)

    print("from date :",from_date)
    print("end_date :",end_date)

    try:
        if(from_date.timetuple() < end_date.timetuple()):
            # call function to check number of errors between this timestamp
            errors = num_errors(str(date1),str(date2))
            print("number of errors between given timestamp :",errors)
        else:
            raise ValueError("invalid end date",end_date)
    except ValueError as exp:
        print("please enter end date greater than from date :",exp)

def num_errors(from_date,end_date):
    os.system("grep -i 'ERROR' out.log | cut -d ' ' -f 1,8 > .errors")
    f = open('.errors','r')
    count = 0
    
    for lines in f.readlines():
        if(re.search(from_date,lines)):
            count = count + 1
        elif(re.search(end_date,lines)):
            count = count + 1
        else:
            break
    return count

if __name__ == "__main__":
    load_yaml()
    check_response_time()
    check_number_errors()
    histogram_error()
