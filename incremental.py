import pandas as pd
import requests
from datetime import datetime, timedelta, date
from db_insert import insert_values
import warnings

warnings.filterwarnings('ignore')

# Top 10 companies list
company_symbols = [
    'RELIANCE',
    'TCS',
    'HDFCBANK',
    'ICICIBANK',
    'BHARTIARTL',
    'SBIN',
    'INFY',
    'LICI',
    'HINDUNILVR',
    'ITC'
]

yest_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
print(f'Processing date: {str(yest_date)}')


def get_data(symbol, exchange):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}.{exchange}&apikey=DXRFLY2B3V0MBMCY'
    r = requests.get(url)
    
    if r.status_code == 200:
        return r.json()
    else:
        print(f'API call failed with status code: {r.status_code}')
        return {}
    
    
def clean_data(json_data):
    if json_data.get('Time Series (Daily)'):
        day_wise = json_data['Time Series (Daily)']
        df = pd.DataFrame(day_wise.items())
        df.rename(columns={0: 'date', 1:'ohlc_data'}, inplace=True)
        
        df['open'] = df['ohlc_data'].apply(lambda x: x.get('1. open'))
        df['high'] = df['ohlc_data'].apply(lambda x: x.get('2. high'))
        df['low'] = df['ohlc_data'].apply(lambda x: x.get('3. low'))
        df['close'] = df['ohlc_data'].apply(lambda x: x.get('4. close'))
        df['volume'] = df['ohlc_data'].apply(lambda x: x.get('5. volume'))
        
        result_df = df[df['date'] == yest_date]
        result_df['company'] = json_data['Meta Data']['2. Symbol'].split('.')[0]
        
        return result_df[['date', 'company', 'open', 'high', 'low', 'close', 'volume']]
    else:
        print('Data not available')
        return pd.DataFrame()
    

if __name__ == '__main__':
    
    exchange = 'BSE'
    for company in company_symbols:
        print(f'Processing data for company: {company}')
        try:
            json_data = get_data(company, exchange)
            df = clean_data(json_data)
            
            if len(df) > 0:
                insert_values(df, 'stock_data.ohlc_data')
            else:
                print(f'No data found for company: {company}')
        except Exception as E:
            print(f'Data insertion failed for company {company} with error: {E}')