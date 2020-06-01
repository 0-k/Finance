class Config:

    indices = {
                'SP_500': '^GSPC',
                'Nasdaq': '^IXIC',
                'Dax': '^GDAXI',
                'FTSE_100': '^FTSE',
                'Hang_Seng': '^HSI',
                'SEE': '000001.SS',
                'Nikkei': '^N225',
                'Ibovespa': '^BVSP',
                'Vix': '^VIX',
                }

    commodities = {
                'Gold': 'GC=F',
                'Silver': 'SI=F',
                'Copper': 'HG=F',
                'Heating_Oil': 'HO=F',
                'Gas': 'NG=F',
                'Corn': 'C=F',
                'Lumber': 'LB=F',
                'Cocoa': 'CC=F',
                'Cement': 'HEI.DE',
                }

    currencies = {
                'USD_EUR': 'EURUSD=X',
                'USD_GBP': 'GBPUSD=X',
                'EUR_CHF': 'EURCHF=X',
                'USD_JPY': 'JPY=X',
                'USD_HKD': 'HKD=X',
                'USD_CNY': 'CNY=X',
                'USD_SGD': 'SGD=X',
                'USD_INR': 'INR=X',
                }

    treasuries = {
                '3M_Treasury': '^IRX',
                '5Y_Treasury': '^FVX',
                '10Y_Treasury': '^TNX',
                '30Y_Treasury': '^TYX'
                }

    columns = {
                'SP_500': 'PCT',
                'Nasdaq': 'PCT',
                'Dax': 'PCT',
                'FTSE_100': 'PCT',
                'Hang_Seng': 'PCT',
                'SEE': 'PCT',
                'Nikkei': 'PCT',
                'Ibovespa': 'PCT',
                'Vix': 'PCT',

                'Gold': 'PCT',
                'Silver': 'PCT',
                'Copper': 'PCT',
                'Heating_Oil': 'PCT',
                'Gas': 'PCT',
                'Corn': 'PCT',
                'Lumber': 'PCT',
                'Cocoa': 'PCT',
                'Cement': 'PCT',

                'USD_EUR': 'PCT',
                'USD_GBP': 'PCT',
                'EUR_CHF': 'PCT',
                'USD_JPY': 'PCT',
                'USD_HKD': 'PCT',
                'USD_CNY': 'PCT',
                'USD_SGD': 'PCT',
                'USD_INR': 'PCT',

                '3M_Treasury': 'DIFF',
                '5Y_Treasury': 'DIFF',
                '10Y_Treasury': 'DIFF',
                '30Y_Treasury': 'DIFF'
                }
