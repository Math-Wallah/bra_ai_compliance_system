# BRA AI Compliance and Fraud Detection System

A comprehensive Python Flask application that implements an AI-powered taxpayer compliance and fraud detection system for the Balochistan Revenue Authority (BRA).

## Overview

This system uses advanced machine learning algorithms to:
- **Detect Anomalies:** Identify unusual tax return patterns using Isolation Forest
- **Score Risk:** Predict compliance risk using Gradient Boosting Machine
- **Prioritize Audits:** Rank taxpayers for audit based on risk scores
- **Analyze Trends:** Generate reports and analytics on compliance patterns

## System Architecture

### Components

1. **Data Processor** (`data_processor.py`)
   - Loads and prepares data from CSV files
   - Extracts features for machine learning models
   - Calculates industry benchmarks

2. **Anomaly Detector** (`anomaly_detector.py`)
   - Trains Isolation Forest model on taxpayer features
   - Detects unusual patterns in tax returns
   - Provides explanations for flagged anomalies

3. **Risk Scorer** (`risk_scorer.py`)
   - Trains Gradient Boosting Classifier on historical audit data
   - Predicts compliance risk for each taxpayer
   - Ranks taxpayers by risk level

4. **Flask Application** (`app.py`)
   - Multi-page web interface
   - REST API endpoints for data access
   - Real-time dashboard and reporting

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Steps

1. **Extract the ZIP file:**
   ```bash
   unzip bra_ai_system.zip
   cd bra_ai_flask_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare data:**
   ```bash
   python generate_data.py
   ```
   This creates sample CSV files in the `data/` directory.

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the web interface:**
   Open your browser and navigate to: `http://localhost:5000`

## Dataset Structure

The system uses three CSV files:

### 1. Taxpayer Master Data (`taxpayer_master.csv`)
| Column | Type | Description |
| --- | --- | --- |
| Taxpayer_ID | String | Unique identifier (e.g., BRA-0001) |
| Business_Name | String | Official business name |
| NTN_CNIC | String | National Tax Number or CNIC |
| Industry_Code | String | SIC code (e.g., 62010) |
| Industry_Name | String | Industry description |
| Registration_Date | DateTime | Date of registration |

### 2. Tax Returns (`tax_returns.csv`)
| Column | Type | Description |
| --- | --- | --- |
| Taxpayer_ID | String | Link to master data |
| Tax_Period | Date | End date of filing period |
| Gross_Revenue | Numeric | Total revenue from services |
| Tax_Liability | Numeric | Calculated tax due |
| Input_Tax_Claim | Numeric | Tax paid on inputs claimed |

### 3. Audit History (`audit_history.csv`)
| Column | Type | Description |
| --- | --- | --- |
| Taxpayer_ID | String | Link to master data |
| Tax_Period | Date | Period audited |
| Audit_Start_Date | DateTime | Date audit began |
| Audit_Finding | String | Compliant/Non-Compliant |
| Tax_Recovery | Numeric | Amount recovered |
| Reason_Code | String | Reason for non-compliance |

## Features

### Dashboard
- Real-time statistics (total taxpayers, returns, audits, tax recovery)
- Top 10 high-risk taxpayers
- System status and last update time

### Anomaly Detection
- Isolation Forest algorithm for pattern detection
- Comparison against industry benchmarks
- Anomaly score visualization

### Risk Scoring
- Gradient Boosting Machine predictions
- Risk level categorization (CRITICAL, HIGH, MEDIUM, LOW)
- Feature importance analysis

### Audit Prioritization
- Ranked list of audit candidates
- Risk-based prioritization
- Direct access to taxpayer details

### Taxpayer Profiles
- Comprehensive taxpayer information
- Tax return history
- Audit history and findings
- Risk assessment details

## Machine Learning Models

### Anomaly Detection Model
**Algorithm:** Isolation Forest
**Features:**
- Input Tax Ratio
- Revenue Growth Rate
- Days Since Registration

**Output:** Anomaly Score (0-1)

### Risk Scoring Model
**Algorithm:** Gradient Boosting Classifier
**Features:**
- Input Tax Ratio
- Revenue Growth
- Days Since Registration
- Anomaly Score
- Number of Returns Filed

**Output:** Risk Score (0-1) and Risk Level (CRITICAL/HIGH/MEDIUM/LOW)

## API Endpoints

### Dashboard
- `GET /` - Main dashboard
- `GET /api/dashboard-stats` - Dashboard statistics

### Anomalies
- `GET /anomalies` - Anomaly detection page
- `GET /api/anomalies` - List of detected anomalies

### Risk Scoring
- `GET /risk-scoring` - Risk scoring page
- `GET /api/risk-scores` - All risk scores

### Audit Prioritization
- `GET /audit-prioritization` - Audit queue page
- `GET /api/audit-candidates` - Top audit candidates

### Taxpayer Details
- `GET /taxpayer/<taxpayer_id>` - Taxpayer profile page
- `GET /api/taxpayer/<taxpayer_id>` - Taxpayer data (JSON)

### Reports
- `GET /reports` - Reports and analytics
- `GET /api/industry-stats` - Industry statistics
- `GET /api/compliance-stats` - Compliance statistics

## Usage Examples

### Example 1: Identify High-Risk Taxpayers
1. Navigate to "Audit Prioritization" from the main menu
2. Review the ranked list of taxpayers
3. Click "Audit Now" to view detailed information

### Example 2: Investigate Anomalies
1. Go to "Anomalies" page
2. Review detected anomalies sorted by score
3. Click "Investigate" to see detailed analysis

### Example 3: Generate Reports
1. Visit "Reports" page
2. View industry distribution and compliance statistics
3. Export data for further analysis

## Customization

### Adding New Features
To add new features to the risk model:
1. Edit `data_processor.py` to extract the new feature
2. Update `risk_scorer.py` to include it in the feature vector
3. Retrain the model

### Updating Data
1. Replace CSV files in the `data/` directory
2. Restart the Flask application
3. The system will automatically reload and retrain models

### Connecting to a Database
The current system uses CSV files. To upgrade to a database:
1. Replace CSV loading in `data_processor.py` with database queries
2. Update the data structure as needed
3. Implement data caching for performance

## Performance Considerations

- **Data Size:** Currently optimized for up to 10,000 taxpayers
- **Model Training:** Automatic on startup (~5-10 seconds)
- **API Response Time:** <500ms for most queries
- **Memory Usage:** ~100-200MB for typical dataset

## Troubleshooting

### Issue: "ModuleNotFoundError" when running app.py
**Solution:** Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: "No such file or directory: 'data/taxpayer_master.csv'"
**Solution:** Run `python generate_data.py` to create sample data

### Issue: Port 5000 already in use
**Solution:** Change the port in `app.py` (line: `app.run(..., port=5001)`)

### Issue: Models not training
**Solution:** Check that audit history has both Compliant and Non-Compliant records

## Future Enhancements

1. **Database Integration:** Migrate from CSV to PostgreSQL/MySQL
2. **Real-time Updates:** Implement WebSocket for live data updates
3. **Advanced Analytics:** Add predictive forecasting and trend analysis
4. **Mobile App:** Develop mobile interface for field auditors
5. **API Authentication:** Implement OAuth2 for secure API access
6. **Audit Trail:** Add logging for compliance and audit purposes
7. **Export Functionality:** Generate PDF/Excel reports
8. **Multi-language Support:** Add Urdu and other local languages

## File Structure

```
bra_ai_flask_app/
├── app.py                 # Main Flask application
├── data_processor.py      # Data loading and feature engineering
├── anomaly_detector.py    # Isolation Forest implementation
├── risk_scorer.py         # Gradient Boosting implementation
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # CSV data files
│   ├── taxpayer_master.csv
│   ├── tax_returns.csv
│   └── audit_history.csv
└── templates/            # HTML templates
    ├── base.html
    ├── index.html
    ├── anomalies.html
    ├── risk_scoring.html
    ├── audit_prioritization.html
    ├── taxpayer_detail.html
    ├── reports.html
    ├── documentation.html
    └── 404.html
```

## License

This system is developed for the Balochistan Revenue Authority.

## Support

For technical support or questions, please contact the BRA IT Department.

---

**Version:** 1.0  
**Last Updated:** 2024  
**Developed by:** Noor Uddin
