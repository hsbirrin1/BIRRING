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

companyCIK = companyCIK.set_index('ticker')

alphabet_cik = companyCIK.at['GOOGL', 'cik_str']

print(alphabet_cik)

# get all companies data
companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{alphabet_cik}.json", headers=headers)

#print(companyFacts.json().keys())

#print only tthe facts - factual data from the SEC
#print(companyFacts.json()['facts']['us-gaap']['Revenues'].keys())

# convert the facts on revenue to a dataframe
revenues_dataframe = pd.DataFrame(companyFacts.json()['facts']['us-gaap']['Revenues']['units']['USD'])

print(revenues_dataframe)

revenues_dataframe = revenues_dataframe[revenues_dataframe.frame.notna()]

#import plotly.eexpress
import plotly.express as px
pd.options.plotting.backend = "plotly"

graph = revenues_dataframe.plot( x = 'end', y = 'val',
                                title = f"Google Revenues",
                                labels = {
                                    "val": "Value in $",
                                    "end": "Quarter End Data"
                                })

graph.show()
