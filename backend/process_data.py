import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
import piecewise_regression

def process_trend_data(trend_data, keyword):
    results = {}
    
    df = trend_data['interest_over_time']
    if df.empty or keyword not in df.columns:
        return {'error': 'No data available for this keyword'}
    
    time_series = df[keyword].values
    dates = df.index.tolist()
    
    first_nonzero = 0
    for i, val in enumerate(time_series):
        if val > 0:
            first_nonzero = i
            break
    
    time_series = time_series[first_nonzero:]
    dates = dates[first_nonzero:]
    
    if len(time_series) == 0:
        return {'error': 'No data available for this keyword'}
    
    results['dates'] = [str(d) for d in dates]
    results['values'] = time_series.tolist()
    
    results['peak_date'] = str(dates[np.argmax(time_series)])
    results['avg_interest'] = round(np.mean(time_series), 2)
    
    if len(time_series) > 24:
        stl = STL(time_series, period=12)
        stl_result = stl.fit()
        
        results['stl'] = {
            'trend': stl_result.trend.tolist(),
            'seasonal': stl_result.seasonal.tolist(),
            'resid': stl_result.resid.tolist()
        }
    else:
        results['stl'] = None
        results['stl_message'] = f"Not enough data for STL decomposition (need 24+ months, have {len(time_series)})"
    
    if len(time_series) >= 12:
        try:
            x = np.arange(len(time_series), dtype=float)
            values = np.array(time_series, dtype=float)
            
            pw = piecewise_regression.Fit(x, values, n_breakpoints=1)
            res = pw.get_results()
            
            if res is None or not isinstance(res, dict):
                results['piecewise'] = None
                results['piecewise_message'] = "Piecewise regression could not converge on this data"
                return results
            
            est = res.get("estimates", {})
            
            if not est:
                results['piecewise'] = None
                results['piecewise_message'] = "No valid estimates found from piecewise regression"
                return results
            
            bp_dict = est.get("breakpoint1", None)
            slope1_dict = est.get("alpha1", None)
            slope2_dict = est.get("alpha2", None)
            const_dict = est.get("const", None)
            
            if bp_dict and slope1_dict and slope2_dict and const_dict:
                bp = float(bp_dict.get("estimate", 0))
                slope1 = float(slope1_dict.get("estimate", 0))
                slope2 = float(slope2_dict.get("estimate", 0))
                const1 = float(const_dict.get("estimate", 0))
                
                bpIndex = int(round(bp))
                
                line1_y = []
                for i in range(bpIndex + 1):
                    line1_y.append(const1 + slope1 * i)
                
                y_at_bp = const1 + slope1 * bp
                line2_y = []
                for i in range(bpIndex, len(time_series)):
                    line2_y.append(y_at_bp + slope2 * (i - bp))
                
                results['piecewise'] = {
                    'breakpoint': bp,
                    'breakpoint_index': bpIndex,
                    'slope1': slope1,
                    'slope2': slope2,
                    'line1_y': line1_y,
                    'line2_y': line2_y
                }
            else:
                results['piecewise'] = None
                results['piecewise_message'] = "Could not find a valid breakpoint in the data"
        except Exception as e:
            print(f"  ERROR: Piecewise regression failed: {e}")
            results['piecewise'] = None
            results['piecewise_message'] = "Piecewise regression analysis failed for this dataset"
    else:
        results['piecewise'] = None
        results['piecewise_message'] = f"Not enough data for piecewise regression (need 12+ months, have {len(time_series)})"
    
    regional_data = trend_data['interest_by_region']
    if not regional_data.empty:
        top_region_name = regional_data[keyword].idxmax()
        results['top_region'] = {
            'name': top_region_name,
            'lat': get_region_coords(top_region_name)['lat'],
            'lng': get_region_coords(top_region_name)['lng']
        }
    else:
        results['top_region'] = None
    
    return results


def get_region_coords(region_name):
    coords = {
        'Auckland': {'lat': -36.8485, 'lng': 174.7633},
        'Bay of Plenty': {'lat': -37.6878, 'lng': 176.1651},
        'Canterbury': {'lat': -43.5321, 'lng': 172.6362},
        'Gisborne': {'lat': -38.6627, 'lng': 178.0176},
        "Hawke's Bay": {'lat': -39.4928, 'lng': 176.9120},
        'Manawatu-Wanganui': {'lat': -39.9332, 'lng': 175.6109},
        'Marlborough': {'lat': -41.5140, 'lng': 173.9614},
        'Nelson': {'lat': -41.2706, 'lng': 173.2840},
        'Northland': {'lat': -35.3677, 'lng': 173.9514},
        'Otago': {'lat': -45.0312, 'lng': 169.3210},
        'Southland': {'lat': -46.4132, 'lng': 168.3538},
        'Taranaki': {'lat': -39.3558, 'lng': 174.4384},
        'Tasman': {'lat': -41.4517, 'lng': 172.8422},
        'Waikato': {'lat': -37.7870, 'lng': 175.2793},
        'Wellington': {'lat': -41.2865, 'lng': 174.7762},
        'West Coast': {'lat': -42.4500, 'lng': 171.2100}
    }
    return coords.get(region_name, {'lat': -41.2865, 'lng': 174.7762})