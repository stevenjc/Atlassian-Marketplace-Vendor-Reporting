# Atlassian Marketplace Vendor Search

Purpose: Correlate a list of emails and emails domains to transactions/licenses in the Atlassian Marketplace automatically.

This python utility takes lists of search terms as single column CSV files (without header row) and searchs for active licenses and transactions (within 60days) tied to those terms. The output is a licenses and transactions csv files for each 

## Important Note 

Created by Steven Colon.

This script is not supported by SmartBear Software

## Install Instructions 

Made on Python 3.7.1

Requires the requests python library - http://docs.python-requests.org/en/master/ 

Download Repo locally

## Configuration Instructions
config.json file is required in the same directory as the migration script. 

Example config can be found 

REPORT_DIR: Output Directory for Reports.

VENDOR_ID: Vendor ID issued by Atlassian.

ADD_ON: ID of Vendor Add-on

AUTH_EMAIL: Email of account with Reporting Permissions to Vendor Account.

AUTH_TOKEN: Authentication token generated from account with Reporting Permissions to Vendor Account. Generate token here - https://id.atlassian.com/manage-profile/security/api-tokens

SEARCH_FILES: Array(List) of files that contain search text *NOTE Files should be single column csv with search terms.

All fields are required. 


## Execution Instructions

Execute script 
`python atlassian_text_search.py`

## License

   Copyright 2020 Steven Colon

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.



