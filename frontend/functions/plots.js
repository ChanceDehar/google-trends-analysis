const dates = resultsData.dates;
const values = resultsData.values;

const trendTrace = {
    x: dates,
    y: values,
    type: 'scatter',
    mode: 'markers',
    name: keyword,
    marker: { color: '#1a472a', size: 8 }
};

const trendLayout = {
    title: `Search Interest: ${keyword}`,
    xaxis: { title: 'Date' },
    yaxis: { title: 'Interest' },
    showlegend: false
};

Plotly.newPlot('trend-plot', [trendTrace], trendLayout);

if (resultsData.stl) {
    const stlTraces = [
        {
            x: dates,
            y: values,
            name: 'Original',
            xaxis: 'x',
            yaxis: 'y'
        },
        {
            x: dates,
            y: resultsData.stl.trend,
            name: 'Trend',
            xaxis: 'x2',
            yaxis: 'y2'
        },
        {
            x: dates,
            y: resultsData.stl.seasonal,
            name: 'Seasonal',
            xaxis: 'x3',
            yaxis: 'y3'
        },
        {
            x: dates,
            y: resultsData.stl.resid,
            name: 'Residual',
            xaxis: 'x4',
            yaxis: 'y4'
        }
    ];

    const stlLayout = {
        title: 'STL Decomposition',
        grid: { rows: 4, columns: 1 },
        xaxis: { title: '' },
        yaxis: { title: 'Original' },
        xaxis2: { title: '' },
        yaxis2: { title: 'Trend' },
        xaxis3: { title: '' },
        yaxis3: { title: 'Seasonal' },
        xaxis4: { title: 'Date' },
        yaxis4: { title: 'Residual' },
        height: 800
    };

    Plotly.newPlot('stl-plot', stlTraces, stlLayout);
}

if (resultsData.piecewise && resultsData.piecewise.breakpoint !== null) {
    const bpIndex = resultsData.piecewise.breakpoint_index;
    const line1Y = resultsData.piecewise.line1_y;
    const line2Y = resultsData.piecewise.line2_y;
    
    const line1X = dates.slice(0, bpIndex + 1);
    const line2X = dates.slice(bpIndex);

    const dataTrace = {
        x: dates,
        y: values,
        type: 'scatter',
        mode: 'markers',
        name: 'Data',
        marker: { color: '#1a472a', size: 6 }
    };

    const fit1Trace = {
        x: line1X,
        y: line1Y,
        type: 'scatter',
        mode: 'lines',
        name: 'Segment 1',
        line: { color: '#e74c3c', width: 3 }
    };

    const fit2Trace = {
        x: line2X,
        y: line2Y,
        type: 'scatter',
        mode: 'lines',
        name: 'Segment 2',
        line: { color: '#3498db', width: 3 }
    };

    const piecewiseLayout = {
        title: 'Piecewise Regression',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Interest' },
        showlegend: true
    };

    Plotly.newPlot('piecewise-plot', [dataTrace, fit1Trace, fit2Trace], piecewiseLayout);
}