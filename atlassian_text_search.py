import json
import os
import requests
from datetime import datetime, timedelta
import boto3, botocore
import csv

with open('config.json', 'r') as file:
    config = json.load(file)

auth_email = config['AUTH_EMAIL']
auth_pw = config['AUTH_TOKEN']
report_dir = config['REPORT_DIR']
search_files = config["SEARCH_FILES"]
vendor_id = config["VENDOR_ID"]
addon = config["ADD_ON"]

base_url = "https://marketplace.atlassian.com/rest/2/vendors/" + vendor_id + "/reporting/"


def check_status_code(response):
    code = response.status_code
    if code == 200:
        print("Successful API Call")
    elif code == 401:
        print("ERROR: 401 Unauthorized")
        print(response.text)
        exit()
    elif code == 400:
        print("ERROR: 400 Request body is malformed or has an illegal property value.")
        print(response.text)
        exit()
    elif code == 403:
        print("ERROR: 403 User was authenticated but is not authorized for this operation.")
        print(response.text)
        exit()
    elif code == 404:
        print("ERROR: 404 Resource does not exist or is not visible to this user.")
        print(response.text)
        exit()
    elif code == 500:
        print("ERROR: 500 Unexpected internal error in the Atlassian Marketplace.")
        print(response.text)
        exit()
    elif code == 502:
        print("ERROR: 500 Unexpected error in an external service.")
        print(response.text)
        exit()
    else:
        print("ERROR: Unknown status code")
        print(response.text)
        exit()

def track_successful_searches(input_file, search_term):
    filename = report_dir + 'matches_' + input_file
    f = open(filename, "a", encoding="utf-8")
    f.write(search_term)
    f.write("\n")

def license_lookup(search_text, time_range, index, row_num, input_file):
    print("Searching for licenses associated with term - " + search_text)
    # Starting date for the query. Format: Date
    start_date = str(datetime.strftime(datetime.now() - timedelta(int(time_range)), '%Y-%m-%d'))
    # End date for the query. Format: Date
    end_date = str(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    # The date field against which filters will be applied. Valid values: end, start
    date_type = "start"
    # Text to search for in license fields (license id, customer information and partner information)
    text = search_text
    # If specified, retrieve marketing funnel attribution data. Must supply a start date after July 2018
    with_attribution = "false"
    # Specifies the response format. If unspecified, the 'Accept' header will be used.Valid values: csv, json
    accept = "csv"
    export_licenses = base_url + "licenses/export?addon=" + addon + "&text=" + text + "&withAttribution=" + with_attribution + "&accept=" + accept + "&status=active"

    # "&startDate="+start_date+"&endDate="+end_date+"&dateType="+date_type+
    print(export_licenses)

    info = requests.get(export_licenses, auth=(auth_email, auth_pw))

    check_status_code(info)

    # Write to .CSV
    filename = report_dir + 'licenses_' + input_file
    f = open(filename, "a", encoding="utf-8")
    split = info.text.split("\n")
    line_num = 0  # track line number in single API call
    for line in split:
        if str(line): #checks that string returns true indicating it is not empty
            if row_num is 0:    #First row of search terms
                # print("<<<<<<<<<HEADER>>>>>>>>>")
                f.write(line)
                f.write("\n")
            elif index is not 0 and line_num is not 0: #Not First File and Not First Line of API Call
                print("************DATA FOUND*****************")
                print(line)
                f.write(line)
                f.write("\n")
                track_successful_searches('licenses_' + input_file,text)
            elif index is 0 and line_num is not 0: #First File and Not First line of API Call
                    print("************DATA FOUND*****************")
                    print(line)
                    f.write(line)
                    f.write("\n")
                    track_successful_searches('licenses_' + input_file, text)
            line_num = line_num + 1
    f.close()


def transactions_lookup(search_text, time_range, index, row_num, input_file):
    print("Searching for transactions associated with - " + search_text)
    # Starting date for the query. Format: Date
    start_date = str(datetime.strftime(datetime.now() - timedelta(int(time_range)), '%Y-%m-%d'))
    # End date for the query. Format: Date
    end_date = str(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    # The date field against which filters will be applied. Valid values: end, start
    date_type = "start"
    # Text to search for in license fields (license id, customer information and partner information)
    text = search_text
    # Specifies the response format. If unspecified, the 'Accept' header will be used.Valid values: csv, json
    accept = "csv"
    export_transactions = base_url + "sales/transactions/export?addon=" + addon + "&text=" + text + "&accept=" + accept + "&startDate=" + start_date + "&endDate=" + end_date + "&dateType=" + date_type

    # "&startDate="+start_date+"&endDate="+end_date+"&dateType="+date_type+
    print(export_transactions)

    info = requests.get(export_transactions, auth=(auth_email, auth_pw))

    # Write to .CSV
    filename = report_dir + 'transactions_' + input_file
    f = open(filename, "a", encoding="utf-8")
    split = info.text.split("\n")
    line_num = 0  # track line number in single API call
    for line in split:
        if str(line):  # checks that string returns true indicating it is not empty
            if row_num is 0:  # First row of search terms
                # print("<<<<<<<<<HEADER>>>>>>>>>")
                f.write(line)
                f.write("\n")
            elif index is not 0 and line_num is not 0:  # Not First File and Not First Line of API Call
                print("************DATA FOUND*****************")
                print(line)
                f.write(line)
                f.write("\n")
                track_successful_searches('transactions_' + input_file, text)
            elif index is 0 and line_num is not 0:  # First File and Not First line of API Call
                print("************DATA FOUND*****************")
                print(line)
                f.write(line)
                f.write("\n")
                track_successful_searches('transactions_' + input_file, text)
            line_num = line_num + 1
    f.close()


if __name__ == '__main__':
    index = 0  # track file number
    for filename in search_files:
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            row_num = 0  # track row number in a single file
            for row in readCSV:
                license_lookup(row[0], '60', index, row_num, filename)
                row_num = row_num + 1
        index = index + 1
    index = 0
    for filename in search_files:
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            row_num = 0
            for row in readCSV:
                transactions_lookup(row[0], '30', index, row_num, filename)
                row_num = row_num + 1
        index = index + 1
