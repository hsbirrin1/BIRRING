# import modules 
import requests 
import pandas as pd 

# create a request header 
headers = {'User-Agent': "hbirring@seattleu.edu"}

# get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)

# print(companyTickers.json()['0']['cik_str'])

companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient= 'index')

print(companyCIK)

companyCIK['cik_str']= companyCIK['cik_str'].astype(str).str.zfill(10)

print(companyCIK)

cik = companyCIK[0:1].cik_str[0]

print(cik)

#SEC filling API Call

companyFilling = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=headers)

print(companyFilling.json()['filings'].keys())

allFilings = pd.DataFrame.from_dict(companyFilling.json()['filings']['recent'])

print(allFilings)

#print columns for cleaning up reference 

print(allFilings.columns)

print(allFilings[['accessionNumber', 'reportDate', 'form']].head(50))

print(allFilings.iloc[11])


