import requests
import pandas as pd

# Show all columns
pd.set_option('display.max_columns', None)
# Set a very wide display width (adjust as needed for your screen)
pd.set_option('display.width', 2000)

# Set up the request header (required by SEC)
headers = {'User-Agent': "hbirring@seattleu.edu"}

# Step 1: Retrieve all company tickers and CIKs
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient='index')

# Step 2: Pad CIKs with leading zeros
companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)

# Step 3: Find Alphabet Inc. (Google) by ticker or name
google_row = companyCIK[
    companyCIK['title'].str.contains("Alphabet", case=False) | 
    companyCIK['ticker'].isin(['GOOG', 'GOOGL'])
]
cik = google_row.iloc[0].cik_str

# Step 4: Fetch company facts (XBRL data)
facts_url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
facts_resp = requests.get(facts_url, headers=headers)
facts = facts_resp.json()

# Step 5: Define the keys for the required data points
keys = {
    'revenue': 'RevenueFromContractWithCustomerExcludingAssessedTax',
    'asset': 'Assets',
    'net_income': 'NetIncomeLoss',
    'cash': 'CashAndCashEquivalentsAtCarryingValue',
    'equity': 'StockholdersEquity'
}

# Step 6: Extract annual (FY) values for each key
def extract_facts(fact_key):
    try:
        fact_data = facts['facts']['us-gaap'][fact_key]['units']['USD']
        annual = [item for item in fact_data if item.get('fy') and item.get('form', '').startswith('10-')]
        return annual
    except KeyError:
        return []

# Step 7: Build a DataFrame with all relevant data
records = []
for item in extract_facts(keys['revenue']):
    fy = item.get('fy')
    fp = item.get('fp')
    form = item.get('form')
    accn = item.get('accn')
    filed = item.get('filed')
    frame = item.get('frame')
    start = item.get('start')
    end = item.get('end')
    revenue = item.get('val')
    
    # Find matching values for other keys in the same fiscal year and form
    def find_val(key):
        for x in extract_facts(keys[key]):
            if x.get('fy') == fy and x.get('form') == form and x.get('fp') == fp:
                return x.get('val')
        return None

    asset = find_val('asset')
    net_income = find_val('net_income')
    cash = find_val('cash')
    equity = find_val('equity')

    records.append({
        'start': start,
        'end': end,
        'revenue': revenue,
        'asset': asset,
        'net_income': net_income,
        'cash': cash,
        'equity': equity,
        'accn': accn,
        'fy': fy,
        'fp': fp,
        'form': form,
        'filed': filed,
        'frame': frame
    })

df = pd.DataFrame(records)

# Optional: sort by fiscal year descending
df = df.sort_values(by='fy', ascending=False)
print(df)


