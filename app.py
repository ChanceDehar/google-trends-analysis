from flask import Flask, render_template, request, send_from_directory
from backend.fetch_data import fetch_google_trend_data
from backend.process_data import process_trend_data

app = Flask(__name__, 
            template_folder='frontend',
            static_folder='frontend/assets',
            static_url_path='/assets')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/functions/<path:filename>')
def functions(filename):
    return send_from_directory('frontend/functions', filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    keyword = request.form.get('keyword')
    timeframe = request.form.get('timeframe', 'today 12-m')
    
    if not keyword:
        return render_template('error.html', 
                             error_message="Please provide a keyword",
                             keyword=keyword)
    
    try:
        trend_data = fetch_google_trend_data(keyword, timeframe)
    except Exception as e:
        return render_template('error.html',
                             error_message=str(e),
                             keyword=keyword)
    
    results = process_trend_data(trend_data, keyword)
    
    if 'error' in results:
        return render_template('error.html',
                             error_message=results['error'],
                             keyword=keyword)
    
    timeframe_display = get_timeframe_display(timeframe)
    
    return render_template('results.html',
                         keyword=keyword,
                         timeframe_display=timeframe_display,
                         results=results)

def get_timeframe_display(timeframe):
    mapping = {
        'now 1-d': 'day',
        'now 7-d': 'week',
        'today 1-m': 'month',
        'today 3-m': '3 months',
        'today 12-m': 'year',
        'today 5-y': '5 years',
        'all': 'all time'
    }
    return mapping.get(timeframe, timeframe)

if __name__ == '__main__':
    app.run(debug=True, port=5000)