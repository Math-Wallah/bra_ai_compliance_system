"""
Anomaly Detection Module
Detects unusual tax return patterns using Isolation Forest
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    """Detects anomalies in tax returns using Isolation Forest"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def train(self):
        """Train the anomaly detection model"""
        print("Training Anomaly Detection Model...")
        
        # Prepare features
        features_df = self.data_processor.get_all_taxpayer_features()
        
        # Select features for anomaly detection
        feature_cols = ['Input_Tax_Ratio', 'Revenue_Growth', 'Days_Since_Registration']
        X = features_df[feature_cols].fillna(0)
        
        # Handle infinite values
        X = X.replace([np.inf, -np.inf], 0)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.model.fit(X_scaled)
        
        self.feature_names = feature_cols
        print(f"✓ Anomaly Detection Model Trained (Features: {', '.join(feature_cols)})")
    
    def detect_anomaly(self, taxpayer_id):
        """Detect if a taxpayer has anomalous behavior"""
        features = self.data_processor.get_taxpayer_features(taxpayer_id)
        if not features:
            return None
        
        # Prepare feature vector
        X = np.array([[
            features['Input_Tax_Ratio'],
            features['Revenue_Growth'],
            features['Days_Since_Registration']
        ]])
        
        # Handle infinite values
        X = np.where(np.isinf(X), 0, X)
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        anomaly_score = -self.model.score_samples(X_scaled)[0]  # Negate so higher = more anomalous
        anomaly_score = max(0, min(1, (anomaly_score + 1) / 2))  # Normalize to [0, 1]
        
        return {
            'Taxpayer_ID': taxpayer_id,
            'Business_Name': features['Business_Name'],
            'Industry_Name': features['Industry_Name'],
            'Input_Tax_Ratio': round(features['Input_Tax_Ratio'], 4),
            'Revenue_Growth': round(features['Revenue_Growth'], 4),
            'Anomaly_Score': round(anomaly_score, 4),
            'Is_Anomalous': anomaly_score > 0.5
        }
    
    def detect_all_anomalies(self):
        """Detect anomalies for all taxpayers"""
        anomalies = []
        for tp_id in self.data_processor.master_data['Taxpayer_ID']:
            anomaly = self.detect_anomaly(tp_id)
            if anomaly:
                anomalies.append(anomaly)
        
        df = pd.DataFrame(anomalies)
        # Sort by anomaly score descending
        df = df.sort_values('Anomaly_Score', ascending=False)
        return df
    
    def get_anomaly_explanation(self, taxpayer_id):
        """Get explanation for why a taxpayer is flagged as anomalous"""
        features = self.data_processor.get_taxpayer_features(taxpayer_id)
        if not features:
            return None
        
        industry = features['Industry_Code']
        benchmark = self.data_processor.get_industry_benchmark(industry)
        
        explanation = {
            'Taxpayer_ID': taxpayer_id,
            'Input_Tax_Ratio': round(features['Input_Tax_Ratio'], 4),
            'Industry_Benchmark': round(benchmark, 4),
            'Deviation': round(features['Input_Tax_Ratio'] - benchmark, 4),
            'Deviation_Percentage': round((features['Input_Tax_Ratio'] - benchmark) / benchmark * 100, 2) if benchmark > 0 else 0,
            'Revenue_Growth': round(features['Revenue_Growth'], 4),
            'Explanation': self._generate_explanation(features, benchmark)
        }
        
        return explanation
    
    def _generate_explanation(self, features, benchmark):
        """Generate human-readable explanation for anomaly"""
        explanations = []
        
        # Check input tax ratio
        ratio_deviation = (features['Input_Tax_Ratio'] - benchmark) / benchmark if benchmark > 0 else 0
        if ratio_deviation > 1:
            explanations.append(f"Input tax claim is {ratio_deviation*100:.1f}% higher than industry benchmark")
        elif ratio_deviation < -0.5:
            explanations.append(f"Input tax claim is {abs(ratio_deviation)*100:.1f}% lower than industry benchmark")
        
        # Check revenue growth
        if features['Revenue_Growth'] > 0.5:
            explanations.append(f"Revenue grew by {features['Revenue_Growth']*100:.1f}% (unusually high)")
        elif features['Revenue_Growth'] < -0.3:
            explanations.append(f"Revenue declined by {abs(features['Revenue_Growth'])*100:.1f}%")
        
        return " | ".join(explanations) if explanations else "No significant anomalies detected"
