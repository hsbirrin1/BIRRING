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
assets_dataframe = pd.DataFrame(companyFacts.json()['facts']['us-gaap']['Assets']['units']['USD'])

assets_dataframe = assets_dataframe[assets_dataframe.frame.notna()]
print(assets_dataframe)

# Pull all liabilities to filter and later merge
liabilities_dataframe = pd.DataFrame(companyFacts.json()['facts']['us-gaap']['Liabilities']['units']['USD'])

liabilities_dataframe = liabilities_dataframe[liabilities_dataframe.frame.notna()]
print(liabilities_dataframe)

assets_dataframe_filtered = assets_dataframe[assets_dataframe['form'] == '10-K']
liabilities_dataframe_filtered = liabilities_dataframe[liabilities_dataframe['form'] == '10-K']

print(assets_dataframe_filtered)
print(liabilities_dataframe_filtered)

# merge assets and liabilites
merged_df = pd.merge(assets_dataframe_filtered, liabilities_dataframe_filtered, on = 'accn')

print(merged_df)

# drop columns
merged_df = merged_df.drop(merged_df.columns[10:], axis = 1)
print(merged_df)

# ratio of assets to liabilites 
merged_df['ratio_assets_liabilities'] = merged_df['val_y'] / merged_df['val_x']

print(merged_df)

#import plotly.eexpress
import plotly.express as px
pd.options.plotting.backend = "plotly"

graph = merged_df.plot( x = 'filed_x', y = 'ratio_assets_liabilities',
                                title = f"Google Debt Ratio",
                                labels = {
                                    "Debt Ratio": "Value in $",
                                    "filed date": "Quarter End Data"
                                })

graph.show()

