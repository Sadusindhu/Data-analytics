"""
Script: prepare_raw_data.py
Description: Downloads the official standard Telco Customer Churn dataset, formats column names
to match the project specification, and injects realistic raw data characteristics (deliberate duplicates
and whitespace values in Total_Charges) to properly test and demonstrate Parts 1 and 2 (Data Cleaning).
"""

import urllib.request
import pandas as pd
import numpy as np
import os

def prepare_raw_data():
    raw_url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    temp_file = "temp_telco.csv"
    
    print(f"Downloading Telco Customer Churn dataset from {raw_url}...")
    urllib.request.urlretrieve(raw_url, temp_file)
    
    df = pd.read_csv(temp_file)
    print(f"Downloaded {len(df)} records.")
    
    # Standardize column names to match the PDF project specifications exactly
    column_mapping = {
        'customerID': 'Customer_ID',
        'gender': 'Gender',
        'SeniorCitizen': 'Senior_Citizen',
        'Partner': 'Partner',
        'Dependents': 'Dependents',
        'tenure': 'Tenure_Months',
        'PhoneService': 'Phone_Service',
        'MultipleLines': 'Multiple_Lines',
        'InternetService': 'Internet_Service',
        'OnlineSecurity': 'Online_Security',
        'OnlineBackup': 'Online_Backup',
        'DeviceProtection': 'Device_Protection',
        'TechSupport': 'Tech_Support',
        'StreamingTV': 'Streaming_TV',
        'StreamingMovies': 'Streaming_Movies',
        'Contract': 'Contract',
        'PaperlessBilling': 'Paperless_Billing',
        'PaymentMethod': 'Payment_Method',
        'MonthlyCharges': 'Monthly_Charges',
        'TotalCharges': 'Total_Charges',
        'Churn': 'Churn'
    }
    
    df.rename(columns=column_mapping, inplace=True)
    
    # Inject deliberate duplicate records (18 rows) to test duplicate detection and removal
    np.random.seed(42)
    dup_indices = np.random.choice(df.index, size=18, replace=False)
    duplicates = df.loc[dup_indices].copy()
    
    # Combine original and duplicates
    df_raw = pd.concat([df, duplicates], ignore_index=True)
    
    # Shuffle slightly to scatter duplicates naturally
    df_raw = df_raw.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    output_path = os.path.join("Dataset", "Customer_Churn_Raw.csv")
    df_raw.to_csv(output_path, index=False)
    print(f"Raw dataset successfully created at {output_path} with shape {df_raw.shape}")
    
    # Cleanup temp
    if os.path.exists(temp_file):
        os.remove(temp_file)

if __name__ == "__main__":
    prepare_raw_data()
