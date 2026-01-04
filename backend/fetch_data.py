from pytrends.request import TrendReq

def fetch_google_trend_data(keyword, timeframe='today 12-m'):
    pytrends = TrendReq(hl='en-US', tz=780)
    
    pytrends.build_payload([keyword], timeframe=timeframe, geo='NZ')
    
    interest_over_time = pytrends.interest_over_time()
    
    interest_by_region = pytrends.interest_by_region(resolution='REGION')
    
    return {
        'interest_over_time': interest_over_time,
        'interest_by_region': interest_by_region
    }