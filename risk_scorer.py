"""
Risk Scoring Module
Predicts compliance risk using Gradient Boosting Machine (XGBoost-like approach)
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class RiskScorer:
    """Predicts compliance risk for taxpayers"""
    
    def __init__(self, data_processor, anomaly_detector):
        self.data_processor = data_processor
        self.anomaly_detector = anomaly_detector
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def train(self):
        """Train the risk scoring model on historical audit data"""
        print("Training Risk Scoring Model...")
        
        # Prepare features for all taxpayers
        features_df = self.data_processor.get_all_taxpayer_features()
        
        # Add anomaly scores
        anomalies = self.anomaly_detector.detect_all_anomalies()
        features_df = features_df.merge(
            anomalies[['Taxpayer_ID', 'Anomaly_Score']],
            on='Taxpayer_ID',
            how='left'
        )
        
        # Merge with audit data to get labels
        audit_labels = self.data_processor.audit_data.copy()
        audit_labels['Is_Non_Compliant'] = (audit_labels['Audit_Finding'] == 'Non-Compliant').astype(int)
        audit_labels = audit_labels.groupby('Taxpayer_ID').agg({'Is_Non_Compliant': 'max'}).reset_index()
        
        # Merge features with labels
        training_data = features_df.merge(audit_labels, on='Taxpayer_ID', how='left')
        training_data['Is_Non_Compliant'] = training_data['Is_Non_Compliant'].fillna(0).astype(int)
        
        # Select features
        feature_cols = [
            'Input_Tax_Ratio',
            'Revenue_Growth',
            'Days_Since_Registration',
            'Anomaly_Score',
            'Num_Returns'
        ]
        
        X = training_data[feature_cols].fillna(0)
        X = X.replace([np.inf, -np.inf], 0)
        y = training_data['Is_Non_Compliant']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Gradient Boosting Classifier
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_scaled, y)
        
        self.feature_names = feature_cols
        
        # Print feature importance
        print(f"✓ Risk Scoring Model Trained")
        print("Feature Importance:")
        for fname, importance in zip(feature_cols, self.model.feature_importances_):
            print(f"  - {fname}: {importance:.4f}")
    
    def score_taxpayer(self, taxpayer_id):
        """Calculate risk score for a specific taxpayer"""
        features = self.data_processor.get_taxpayer_features(taxpayer_id)
        if not features:
            return None
        
        # Get anomaly score
        anomaly = self.anomaly_detector.detect_anomaly(taxpayer_id)
        anomaly_score = anomaly['Anomaly_Score'] if anomaly else 0
        
        # Prepare feature vector
        X = np.array([[
            features['Input_Tax_Ratio'],
            features['Revenue_Growth'],
            features['Days_Since_Registration'],
            anomaly_score,
            features['Num_Returns']
        ]])
        
        # Handle infinite values
        X = np.where(np.isinf(X), 0, X)
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict probability of non-compliance
        risk_score = self.model.predict_proba(X_scaled)[0][1]  # Probability of class 1 (Non-Compliant)
        
        return {
            'Taxpayer_ID': taxpayer_id,
            'Business_Name': features['Business_Name'],
            'Industry_Name': features['Industry_Name'],
            'Risk_Score': round(risk_score, 4),
            'Risk_Level': self._get_risk_level(risk_score),
            'Anomaly_Score': round(anomaly_score, 4)
        }
    
    def score_all_taxpayers(self):
        """Calculate risk scores for all taxpayers"""
        scores = []
        for tp_id in self.data_processor.master_data['Taxpayer_ID']:
            score = self.score_taxpayer(tp_id)
            if score:
                scores.append(score)
        
        df = pd.DataFrame(scores)
        # Sort by risk score descending
        df = df.sort_values('Risk_Score', ascending=False)
        return df
    
    def _get_risk_level(self, risk_score):
        """Categorize risk score into levels"""
        if risk_score >= 0.7:
            return 'CRITICAL'
        elif risk_score >= 0.5:
            return 'HIGH'
        elif risk_score >= 0.3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if self.model is None:
            return None
        
        importance_dict = {}
        for fname, importance in zip(self.feature_names, self.model.feature_importances_):
            importance_dict[fname] = round(float(importance), 4)
        
        return importance_dict
    
    def get_risk_explanation(self, taxpayer_id):
        """Get explanation for a taxpayer's risk score"""
        score_info = self.score_taxpayer(taxpayer_id)
        features = self.data_processor.get_taxpayer_features(taxpayer_id)
        
        if not score_info or not features:
            return None
        
        # Get anomaly explanation
        anomaly_exp = self.anomaly_detector.get_anomaly_explanation(taxpayer_id)
        
        explanation = {
            'Taxpayer_ID': taxpayer_id,
            'Risk_Score': score_info['Risk_Score'],
            'Risk_Level': score_info['Risk_Level'],
            'Key_Factors': {
                'Input_Tax_Ratio': round(features['Input_Tax_Ratio'], 4),
                'Revenue_Growth': round(features['Revenue_Growth'], 4),
                'Anomaly_Score': score_info['Anomaly_Score'],
                'Num_Returns': features['Num_Returns']
            },
            'Anomaly_Explanation': anomaly_exp['Explanation'],
            'Recommendation': self._get_recommendation(score_info['Risk_Level'])
        }
        
        return explanation
    
    def _get_recommendation(self, risk_level):
        """Get audit recommendation based on risk level"""
        recommendations = {
            'CRITICAL': 'Immediate audit recommended. Potential fraud indicators detected.',
            'HIGH': 'Priority audit recommended. Multiple risk factors present.',
            'MEDIUM': 'Routine audit recommended. Some anomalies detected.',
            'LOW': 'Standard monitoring. No immediate action required.'
        }
        return recommendations.get(risk_level, 'Review recommended.')
