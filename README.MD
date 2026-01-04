# Google Trends Analysis - New Zealand

A web application for analyzing Google Trends data with statistical analysis tools, focused on New Zealand data.

## Features

- **Statistical Analysis**: 
  - STL (Seasonal and Trend decomposition using Loess) for time series decomposition
  - Segmented regression for identifying breakpoints and trend changes
- **Interactive Visualizations**: Dynamic charts and graphs for trend exploration
- **NZ-Specific Data**: Tailored for New Zealand market analysis
- **Regional Filtering**: Bonus feature in showcase page for regional insights

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Statistical Analysis**: Python libraries (scipy, statsmodels, numpy)

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/chancedehar/google-trends-nz.git

# Navigate to project directory
cd google-trends-nz

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## Usage

1. Enter a search term to analyze
2. View statistical analysis including trend tests, decomposition, and segmented regression
3. Explore interactive visualizations
4. Use regional filtering in showcase page for deeper insights