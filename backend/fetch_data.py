from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import time

def fetch_google_trend_data(keyword, timeframe='today 12-m'):
    max_retries = 3
    retry_delay = 60
    
    for attempt in range(max_retries):
        try:
            pytrends = TrendReq(hl='en-US', tz=780)
            
            pytrends.build_payload([keyword], timeframe=timeframe, geo='NZ')
            
            interest_over_time = pytrends.interest_over_time()
            
            interest_by_region = pytrends.interest_by_region(resolution='REGION')
            
            return {
                'interest_over_time': interest_over_time,
                'interest_by_region': interest_by_region
            }
        except TooManyRequestsError:
            if attempt < max_retries - 1:
                print(f"Rate limited, waiting {retry_delay} seconds before retry {attempt + 1}/{max_retries}")
                time.sleep(retry_delay)
            else:
                raise Exception("Google Trends rate limit exceeded. Please wait a few minutes and try again.")
        except Exception as e:
            raise Exception(f"Error fetching Google Trends data: {str(e)}")