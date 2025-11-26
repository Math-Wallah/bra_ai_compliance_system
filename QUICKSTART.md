# BRA AI Compliance System - Quick Start Guide

## What's Included

This ZIP file contains a complete, ready-to-run AI-powered taxpayer compliance and fraud detection system for the Balochistan Revenue Authority (BRA).

### Package Contents:
- **Python Flask Application** - Multi-page web interface
- **Machine Learning Models** - Anomaly detection and risk scoring
- **Sample Dataset** - 50 taxpayers with realistic tax return data
- **HTML Templates** - 9 pages with interactive dashboards
- **Documentation** - Comprehensive README and API documentation

## System Requirements

- **Python:** 3.7 or higher
- **Operating System:** Windows, macOS, or Linux
- **RAM:** Minimum 2GB
- **Disk Space:** ~50MB

## Installation (5 minutes)

### Step 1: Extract the ZIP File
```bash
unzip bra_ai_compliance_system.zip
cd bra_ai_flask_app
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Pandas (data processing)
- NumPy (numerical computing)
- Scikit-learn (machine learning)

### Step 3: Run the Application
```bash
python app.py
```

You should see output like:
```
✓ AI System Initialized Successfully
 * Running on http://0.0.0.0:5000
```

### Step 4: Open in Browser
Navigate to: **http://localhost:5000**

## What You'll See

### 🏠 Dashboard
- Key statistics (total taxpayers, returns, audits, tax recovery)
- Top 10 high-risk taxpayers
- System status

### 🔍 Anomalies
- Taxpayers with unusual tax patterns
- Anomaly scores and explanations
- Direct investigation links

### 📈 Risk Scores
- All taxpayers ranked by compliance risk
- Risk levels: CRITICAL, HIGH, MEDIUM, LOW
- Anomaly analysis

### 📋 Audit Prioritization
- Ranked list of audit candidates
- Highest-risk cases first
- Optimized audit planning

### 👤 Taxpayer Details
- Complete taxpayer profile
- Tax return history
- Audit findings
- Risk assessment

### 📊 Reports
- Industry distribution
- Compliance statistics
- Analytics

### 📚 Documentation
- System overview
- How to use each feature
- Risk level explanations

## Sample Data

The system comes with **50 sample taxpayers** including:
- Diverse industries (Software, Restaurants, Consulting, Transport, Finance)
- Quarterly tax returns (2023-2024)
- Audit history with findings
- Realistic fraud patterns

### Key Features Demonstrated:
✓ **Anomaly Detection** - Identifies inflated input tax claims  
✓ **Risk Scoring** - Predicts non-compliance probability  
✓ **Audit Prioritization** - Ranks taxpayers by risk  
✓ **Industry Benchmarking** - Compares against sector norms  

## How It Works

### 1. Data Loading
The system loads three CSV files:
- `taxpayer_master.csv` - Taxpayer information
- `tax_returns.csv` - Historical returns
- `audit_history.csv` - Audit results (training data)

### 2. Feature Engineering
Extracts key features:
- Input Tax Ratio (compared to industry average)
- Revenue Growth Rate
- Days Since Registration
- Number of Returns Filed

### 3. Anomaly Detection
**Algorithm:** Isolation Forest
- Detects unusual patterns
- Flags suspicious taxpayers
- Provides anomaly scores (0-1)

### 4. Risk Scoring
**Algorithm:** Gradient Boosting Machine
- Trained on historical audit data
- Predicts compliance risk
- Categorizes into risk levels

### 5. Audit Prioritization
- Ranks taxpayers by risk score
- Highest-risk cases first
- Optimizes auditor resources

## Key Pages Explained

| Page | Purpose | Key Metric |
| --- | --- | --- |
| **Dashboard** | Overview & quick stats | Top 10 high-risk |
| **Anomalies** | Pattern detection | Anomaly Score (0-1) |
| **Risk Scores** | Compliance prediction | Risk Score (0-1) |
| **Audit Queue** | Audit planning | Risk Level (CRITICAL/HIGH/MEDIUM/LOW) |
| **Taxpayer Detail** | Deep dive analysis | Complete profile |
| **Reports** | Analytics & trends | Industry stats |

## Understanding Risk Levels

| Level | Score | Meaning | Action |
| --- | --- | --- | --- |
| **CRITICAL** | 0.70-1.00 | Very likely non-compliant | Immediate audit |
| **HIGH** | 0.50-0.69 | Probably non-compliant | Priority audit |
| **MEDIUM** | 0.30-0.49 | Some risk factors | Routine audit |
| **LOW** | 0.00-0.29 | Likely compliant | Standard monitoring |

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install -r requirements.txt`

### Problem: "Port 5000 already in use"
**Solution:** Edit `app.py` line 156, change `port=5000` to `port=5001`

### Problem: "No such file or directory: data/taxpayer_master.csv"
**Solution:** Ensure you're in the `bra_ai_flask_app` directory

### Problem: Models not training
**Solution:** Check that CSV files have data (run `head data/*.csv`)

## Next Steps

### 1. Explore the Sample Data
- Browse different risk levels
- Investigate high-risk taxpayers
- Review anomaly explanations

### 2. Understand the Models
- Read the documentation page
- Review feature importance
- Check model accuracy

### 3. Customize for Real Data
- Replace CSV files with actual BRA data
- Retrain models with real audit history
- Adjust risk thresholds as needed

### 4. Deploy to Production
- Set up database (PostgreSQL/MySQL)
- Configure authentication
- Deploy on web server (Nginx/Apache)
- Set up automated retraining

## API Endpoints

The system provides REST APIs for integration:

```
GET /api/dashboard-stats          → Dashboard statistics
GET /api/high-risk-taxpayers      → Top risk cases
GET /api/anomalies                → Detected anomalies
GET /api/risk-scores              → All risk scores
GET /api/audit-candidates         → Audit queue
GET /api/taxpayer/<id>            → Taxpayer details
GET /api/industry-stats           → Industry analytics
GET /api/compliance-stats         → Compliance data
```

## File Structure

```
bra_ai_flask_app/
├── app.py                    # Main application (156 lines)
├── data_processor.py         # Data loading (150 lines)
├── anomaly_detector.py       # Anomaly detection (170 lines)
├── risk_scorer.py            # Risk scoring (200 lines)
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── data/
│   ├── taxpayer_master.csv   # 50 taxpayers
│   ├── tax_returns.csv       # 350+ returns
│   └── audit_history.csv     # 30+ audit records
└── templates/
    ├── base.html             # Base layout
    ├── index.html            # Dashboard
    ├── anomalies.html        # Anomaly page
    ├── risk_scoring.html     # Risk page
    ├── audit_prioritization.html  # Audit queue
    ├── taxpayer_detail.html  # Profile page
    ├── reports.html          # Analytics
    ├── documentation.html    # Help page
    └── 404.html              # Error page
```

## Performance

- **Startup Time:** ~5-10 seconds (model training)
- **Dashboard Load:** <1 second
- **API Response:** <500ms
- **Memory Usage:** ~100-200MB

## Support

For questions or issues:
1. Check the **Documentation** page in the app
2. Review the **README.md** file
3. Examine the **Python source code** (well-commented)

## Key Features Demonstrated

✅ **Multi-page Flask Application**  
✅ **Isolation Forest for Anomaly Detection**  
✅ **Gradient Boosting for Risk Scoring**  
✅ **Industry Benchmarking**  
✅ **Real-time Dashboard**  
✅ **REST API Endpoints**  
✅ **Responsive HTML/CSS UI**  
✅ **Sample Dataset (50 taxpayers)**  
✅ **Complete Documentation**  

## License

Developed for the Balochistan Revenue Authority.

---

**Ready to start?** Run `python app.py` and open http://localhost:5000

**Questions?** Check the Documentation page in the app or read README.md
