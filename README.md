# Business KPI Root Cause Analysis System

An interactive business analytics application for monitoring key performance indicators, analyzing performance fluctuations, identifying potential contributing factors, and generating automated reports.

## Live Demo

(https://kpirootcauseanalysis-fakdmm9af4dlpnumzkiecq.streamlit.app/)

## Project Overview

The system analyzes business transaction data to monitor important KPIs including Quantity, Sales, Profit, and Discount.

It combines exploratory data analysis, statistical analysis, visualization, root cause analysis, and machine learning-based prediction in an interactive Streamlit application.

## Key Highlights

- Analyzed 9,994 business transaction records
- Monitored Quantity, Sales, Profit, and Discount KPIs
- Performed correlation, distribution, and trend analysis
- Identified potential factors associated with KPI changes
- Built an interactive Streamlit dashboard for KPI monitoring and analysis
- Implemented automated explanations for KPI drops
- Added linear regression-based KPI prediction
- Generated automated PDF reports with visual analysis
- Implemented user signup and login authentication using SQLite3

## Main Features

### KPI Monitoring

Provides an interactive view of important business KPIs and their performance.

### Exploratory Data Analysis

Uses correlation, distribution, trend, and outlier analysis to understand KPI behavior.

### Root Cause Analysis

Analyzes relationships between business variables to identify potential factors associated with KPI performance changes.

### KPI Prediction

Uses linear regression to provide KPI predictions based on the available business data.

### Interactive Dashboard

Built with Streamlit and includes visual analytics for business performance analysis.

### Automated Reports

Generates PDF reports containing visual summaries, correlation heatmaps, distributions, outlier analysis, and key insights.

### User Authentication

Includes signup and login functionality using SQLite3.

## Technologies

- Python
- Pandas
- Scikit-learn
- Streamlit
- Plotly
- Matplotlib
- Seaborn
- ReportLab
- SQLite3

## Project Structure

```text
kpi_root_cause_analysis/
└── kpi_root_cause_analysis_system_final/
    ├── __pycache__/
    ├── my_pages/
    ├── reports/
    ├── app.py
    ├── auth.py
    ├── requirements.txt
    ├── test.py
    └── users.db

git clone https://github.com/Tejashwini1204/kpi_root_cause_analysis.git
cd kpi_root_cause_analysis

pip install -r kpi_root_cause_analysis_system_final/requirements.txt

streamlit run kpi_root_cause_analysis_system_final/app.py
