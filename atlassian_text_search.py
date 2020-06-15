import json
import os
import requests
from datetime import datetime, timedelta
import boto3, botocore
import csv

with open('config.json', 'r') as file:
    config = json.load(file)


auth_email=config['AUTH_EMAIL']
auth_pw=config['AUTH_PW']
report_dir=config['REPORT_DIR']
search_files=config["SEARCH_FILES"]
vendor_id=config["VENDOR_ID"]
addon=config["ADD_ON"]

base_url = "https://marketplace.atlassian.com/rest/2/vendors/"+vendor_id+"/reporting/"

def license_lookup(search_text, time_range, index, row_num, inputfile):
    print("Searching for - " + search_text)  
    #Starting date for the query. Format: Date
    start_date= str(datetime.strftime(datetime.now() - timedelta(int(time_range)), '%Y-%m-%d'))
    #End date for the query. Format: Date
    end_date=str(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    #The date field against which filters will be applied. Valid values: end, start
    date_type="start"
    #Text to search for in license fields (license id, customer information and partner information)
    text=search_text
    #If specified, retrieve marketing funnel attribution data
    with_attribution="false"
    #Specifies the response format. If unspecified, the 'Accept' header will be used.Valid values: csv, json
    accept="csv"
    export_licenses= base_url+"licenses/export?addon="+addon+"&text="+text+"&withAttribution="+with_attribution+"&accept="+accept+"&status=active"
    
    #"&startDate="+start_date+"&endDate="+end_date+"&dateType="+date_type+
    print(export_licenses)
    
    info = requests.get(export_licenses, auth=(auth_email, auth_pw))
    # Write to .CSV
    filename = report_dir+'licenses_'+inputfile
    f = open(filename, "a", encoding="utf-8")
    split = info.text.split("\n")
    line_num=0 #track line number in single API call
    for line in split:
        if index is not 0:
            if line_num is not 0:
                print("************DATA*****************")
                print(line)
                f.write(line)
                f.write("\n")
        elif index is 0:
            if row_num is 0:
                print("<<<<<<<<<HEADER>>>>>>>>>")
                f.write(line)
                f.write("\n")
            elif line_num is not 0:
                print("************DATA*****************")
                print(line)
                f.write(line)
                f.write("\n")
        line_num = line_num + 1
    f.close()

def transactions_lookup(search_text, time_range, index, row_num, inputfile):
    print("Searching for - " + search_text)  
    #Starting date for the query. Format: Date
    start_date= str(datetime.strftime(datetime.now() - timedelta(int(time_range)), '%Y-%m-%d'))
    #End date for the query. Format: Date
    end_date=str(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    #The date field against which filters will be applied. Valid values: end, start
    date_type="start"
    #Text to search for in license fields (license id, customer information and partner information)
    text=search_text
    #Specifies the response format. If unspecified, the 'Accept' header will be used.Valid values: csv, json
    accept="csv"
    export_transactions=base_url+"sales/transactions/export?addon="+addon+"&text="+text+"&accept="+accept+"&startDate="+start_date+"&endDate="+end_date+"&dateType="+date_type
    
    #"&startDate="+start_date+"&endDate="+end_date+"&dateType="+date_type+
    print(export_transactions)
    
    info = requests.get(export_transactions, auth=(auth_email, auth_pw))
    # Write to .CSV
    filename = report_dir+'transactions_'+inputfile
    f = open(filename, "a", encoding="utf-8")
    split = info.text.split("\n")
    line_num=0 # track line number in single API call
    for line in split:
        if index is not 0:
            if line_num is not 0:
                print("************DATA*****************")
                print(line)
                f.write(line + "\n")
        elif index is 0:
            if row_num is 0:
                print("<<<<<<<<<HEADER>>>>>>>>>")
                f.write(line + "\n")
            elif line_num is not 0:
                print("************DATA*****************")
                print(line)
                f.write(line + "\n")
        line_num = line_num + 1
    f.close()
    
if __name__ == '__main__':
    index = 0 # track file number
    for filename in search_files:
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            row_num = 0 # track row number in a single file
            for row in readCSV:
                license_lookup(row[0],'60', index, row_num, filename)
                row_num = row_num + 1
        index = index + 1
    index = 0
    for filename in search_files:
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            row_num = 0
            for row in readCSV:
                transactions_lookup(row[0],'30', index, row_num, filename)
                row_num = row_num + 1
        index = index + 1
