"""
BRA AI Compliance and Fraud Detection System
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

# Import the AI modules
from data_processor import DataProcessor
from risk_scorer import RiskScorer
from anomaly_detector import AnomalyDetector

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize data processor and models
data_processor = None
risk_scorer = None
anomaly_detector = None

def initialize_system():
    """Initialize the AI system with data"""
    global data_processor, risk_scorer, anomaly_detector
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load data
    data_processor = DataProcessor(data_dir)
    data_processor.load_data()
    
    # Initialize models
    anomaly_detector = AnomalyDetector(data_processor)
    anomaly_detector.train()
    
    risk_scorer = RiskScorer(data_processor, anomaly_detector)
    risk_scorer.train()
    
    print("✓ AI System Initialized Successfully")

# Initialize on startup
initialize_system()

# ===== ROUTES =====

@app.route('/')
def index():
    """Dashboard Home Page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main Dashboard with Overview"""
    stats = {
        'total_taxpayers': len(data_processor.master_data),
        'total_returns_filed': len(data_processor.returns_data),
        'audits_completed': len(data_processor.audit_data),
        'tax_recovery': data_processor.audit_data['Tax_Recovery'].sum() if len(data_processor.audit_data) > 0 else 0
    }
    
    # Get high-risk taxpayers
    all_scores = risk_scorer.score_all_taxpayers()
    high_risk = all_scores.nlargest(10, 'Risk_Score')[['Taxpayer_ID', 'Business_Name', 'Risk_Score', 'Industry_Name']]
    
    return render_template('dashboard.html', 
                         stats=stats,
                         high_risk_taxpayers=high_risk.to_dict('records'))

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    """API endpoint for dashboard statistics"""
    stats = {
        'total_taxpayers': len(data_processor.master_data),
        'total_returns_filed': len(data_processor.returns_data),
        'audits_completed': len(data_processor.audit_data),
        'tax_recovery': float(data_processor.audit_data['Tax_Recovery'].sum()) if len(data_processor.audit_data) > 0 else 0,
        'compliance_rate': float((len(data_processor.audit_data[data_processor.audit_data['Audit_Finding'] == 'Compliant']) / len(data_processor.audit_data) * 100)) if len(data_processor.audit_data) > 0 else 0
    }
    return jsonify(stats)

@app.route('/api/high-risk-taxpayers')
def api_high_risk_taxpayers():
    """API endpoint for high-risk taxpayers"""
    all_scores = risk_scorer.score_all_taxpayers()
    high_risk = all_scores.nlargest(15, 'Risk_Score')[['Taxpayer_ID', 'Business_Name', 'Risk_Score', 'Industry_Name', 'Anomaly_Score']]
    return jsonify(high_risk.to_dict('records'))

@app.route('/anomalies')
def anomalies():
    """Anomaly Detection Page"""
    anomalies_list = anomaly_detector.detect_all_anomalies()
    return render_template('anomalies.html', anomalies=anomalies_list.to_dict('records'))

@app.route('/api/anomalies')
def api_anomalies():
    """API endpoint for anomalies"""
    anomalies_list = anomaly_detector.detect_all_anomalies()
    return jsonify(anomalies_list.to_dict('records'))

@app.route('/risk-scoring')
def risk_scoring():
    """Risk Scoring Page"""
    all_scores = risk_scorer.score_all_taxpayers()
    return render_template('risk_scoring.html', scores=all_scores.to_dict('records'))

@app.route('/api/risk-scores')
def api_risk_scores():
    """API endpoint for risk scores"""
    all_scores = risk_scorer.score_all_taxpayers()
    return jsonify(all_scores.to_dict('records'))

@app.route('/taxpayer/<taxpayer_id>')
def taxpayer_detail(taxpayer_id):
    """Detailed Taxpayer Profile"""
    taxpayer = data_processor.master_data[data_processor.master_data['Taxpayer_ID'] == taxpayer_id]
    
    if taxpayer.empty:
        return "Taxpayer not found", 404
    
    taxpayer_info = taxpayer.iloc[0].to_dict()
    
    # Get returns for this taxpayer
    returns = data_processor.returns_data[data_processor.returns_data['Taxpayer_ID'] == taxpayer_id]
    
    # Get audit history
    audits = data_processor.audit_data[data_processor.audit_data['Taxpayer_ID'] == taxpayer_id]
    
    # Get risk score
    risk_score = risk_scorer.score_taxpayer(taxpayer_id)
    
    return render_template('taxpayer_detail.html',
                         taxpayer=taxpayer_info,
                         returns=returns.to_dict('records'),
                         audits=audits.to_dict('records'),
                         risk_score=risk_score)

@app.route('/api/taxpayer/<taxpayer_id>')
def api_taxpayer_detail(taxpayer_id):
    """API endpoint for taxpayer details"""
    taxpayer = data_processor.master_data[data_processor.master_data['Taxpayer_ID'] == taxpayer_id]
    
    if taxpayer.empty:
        return jsonify({'error': 'Taxpayer not found'}), 404
    
    taxpayer_info = taxpayer.iloc[0].to_dict()
    returns = data_processor.returns_data[data_processor.returns_data['Taxpayer_ID'] == taxpayer_id]
    audits = data_processor.audit_data[data_processor.audit_data['Taxpayer_ID'] == taxpayer_id]
    risk_score = risk_scorer.score_taxpayer(taxpayer_id)
    
    return jsonify({
        'taxpayer': taxpayer_info,
        'returns': returns.to_dict('records'),
        'audits': audits.to_dict('records'),
        'risk_score': risk_score
    })

@app.route('/audit-prioritization')
def audit_prioritization():
    """Audit Prioritization Dashboard"""
    all_scores = risk_scorer.score_all_taxpayers()
    # Sort by risk score and get top candidates
    audit_candidates = all_scores.nlargest(20, 'Risk_Score')
    
    return render_template('audit_prioritization.html',
                         candidates=audit_candidates.to_dict('records'))

@app.route('/api/audit-candidates')
def api_audit_candidates():
    """API endpoint for audit candidates"""
    all_scores = risk_scorer.score_all_taxpayers()
    audit_candidates = all_scores.nlargest(20, 'Risk_Score')
    return jsonify(audit_candidates.to_dict('records'))

@app.route('/reports')
def reports():
    """Reports and Analytics Page"""
    # Industry-wise statistics
    industry_stats = data_processor.master_data.groupby('Industry_Name').size().to_dict()
    
    # Compliance statistics
    if len(data_processor.audit_data) > 0:
        compliance_stats = data_processor.audit_data['Audit_Finding'].value_counts().to_dict()
    else:
        compliance_stats = {}
    
    return render_template('reports.html',
                         industry_stats=industry_stats,
                         compliance_stats=compliance_stats)

@app.route('/api/industry-stats')
def api_industry_stats():
    """API endpoint for industry statistics"""
    industry_stats = data_processor.master_data.groupby('Industry_Name').size().to_dict()
    return jsonify(industry_stats)

@app.route('/api/compliance-stats')
def api_compliance_stats():
    """API endpoint for compliance statistics"""
    if len(data_processor.audit_data) > 0:
        compliance_stats = data_processor.audit_data['Audit_Finding'].value_counts().to_dict()
    else:
        compliance_stats = {}
    return jsonify(compliance_stats)

@app.route('/documentation')
def documentation():
    """System Documentation Page"""
    return render_template('documentation.html')

@app.route('/settings')
def settings():
    """Settings Page"""
    return render_template('settings.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
