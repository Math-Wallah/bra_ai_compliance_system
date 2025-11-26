"""
Data Processor Module
Handles loading, cleaning, and preparing data for the AI system
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

class DataProcessor:
    """Loads and processes data from CSV files"""
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.master_data = None
        self.returns_data = None
        self.audit_data = None
    
    def load_data(self):
        """Load all CSV files"""
        print("Loading data...")
        
        # Load master data
        master_path = os.path.join(self.data_dir, 'taxpayer_master.csv')
        self.master_data = pd.read_csv(master_path)
        print(f"✓ Loaded {len(self.master_data)} taxpayers")
        
        # Load returns data
        returns_path = os.path.join(self.data_dir, 'tax_returns.csv')
        self.returns_data = pd.read_csv(returns_path)
        print(f"✓ Loaded {len(self.returns_data)} tax returns")
        
        # Load audit data
        audit_path = os.path.join(self.data_dir, 'audit_history.csv')
        self.audit_data = pd.read_csv(audit_path)
        print(f"✓ Loaded {len(self.audit_data)} audit records")
        
        # Clean and prepare data
        self._prepare_data()
    
    def _prepare_data(self):
        """Clean and prepare data for analysis"""
        # Convert date columns
        self.master_data['Registration_Date'] = pd.to_datetime(self.master_data['Registration_Date'])
        self.returns_data['Tax_Period'] = pd.to_datetime(self.returns_data['Tax_Period'])
        self.audit_data['Audit_Start_Date'] = pd.to_datetime(self.audit_data['Audit_Start_Date'])
        
        # Ensure numeric columns
        self.returns_data['Gross_Revenue'] = pd.to_numeric(self.returns_data['Gross_Revenue'])
        self.returns_data['Tax_Liability'] = pd.to_numeric(self.returns_data['Tax_Liability'])
        self.returns_data['Input_Tax_Claim'] = pd.to_numeric(self.returns_data['Input_Tax_Claim'])
        self.audit_data['Tax_Recovery'] = pd.to_numeric(self.audit_data['Tax_Recovery'])
    
    def get_taxpayer_features(self, taxpayer_id):
        """Extract features for a specific taxpayer"""
        # Get taxpayer info
        taxpayer = self.master_data[self.master_data['Taxpayer_ID'] == taxpayer_id]
        if taxpayer.empty:
            return None
        
        # Get returns for this taxpayer
        returns = self.returns_data[self.returns_data['Taxpayer_ID'] == taxpayer_id]
        
        if returns.empty:
            return None
        
        # Calculate features
        latest_return = returns.iloc[-1]
        
        # Input Tax Ratio
        input_tax_ratio = latest_return['Input_Tax_Claim'] / latest_return['Gross_Revenue'] if latest_return['Gross_Revenue'] > 0 else 0
        
        # Revenue growth (if multiple returns)
        revenue_growth = 0
        if len(returns) > 1:
            prev_revenue = returns.iloc[-2]['Gross_Revenue']
            curr_revenue = latest_return['Gross_Revenue']
            revenue_growth = (curr_revenue - prev_revenue) / prev_revenue if prev_revenue > 0 else 0
        
        # Industry info
        industry = taxpayer.iloc[0]['Industry_Code']
        
        features = {
            'Taxpayer_ID': taxpayer_id,
            'Business_Name': taxpayer.iloc[0]['Business_Name'],
            'Industry_Code': industry,
            'Industry_Name': taxpayer.iloc[0]['Industry_Name'],
            'Gross_Revenue': latest_return['Gross_Revenue'],
            'Tax_Liability': latest_return['Tax_Liability'],
            'Input_Tax_Claim': latest_return['Input_Tax_Claim'],
            'Input_Tax_Ratio': input_tax_ratio,
            'Revenue_Growth': revenue_growth,
            'Num_Returns': len(returns),
            'Days_Since_Registration': (datetime.now() - taxpayer.iloc[0]['Registration_Date']).days
        }
        
        return features
    
    def get_industry_benchmark(self, industry_code):
        """Get average input tax ratio for an industry"""
        industry_returns = self.returns_data.merge(
            self.master_data[self.master_data['Industry_Code'] == industry_code][['Taxpayer_ID']],
            on='Taxpayer_ID'
        )
        
        if industry_returns.empty:
            return 0.1  # Default benchmark
        
        avg_ratio = (industry_returns['Input_Tax_Claim'].sum() / industry_returns['Gross_Revenue'].sum()) if industry_returns['Gross_Revenue'].sum() > 0 else 0.1
        return avg_ratio
    
    def get_all_taxpayer_features(self):
        """Get features for all taxpayers"""
        features_list = []
        for tp_id in self.master_data['Taxpayer_ID']:
            features = self.get_taxpayer_features(tp_id)
            if features:
                features_list.append(features)
        
        return pd.DataFrame(features_list)
