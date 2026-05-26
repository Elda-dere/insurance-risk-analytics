import pandas as pd
import numpy as np
from pathlib import Path

def load_insurance_data(filepath=None):
    \"\"\"Load insurance dataset\"\"\"
    if filepath is None:
        filepath = Path(__file__).parent.parent / "data" / "insurance_data.csv"
    
    df = pd.read_csv(filepath)
    
    # Convert date columns if exists
    if 'TransactionMonth' in df.columns:
        df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'])
    
    # Calculate derived metrics
    df['LossRatio'] = df['TotalClaims'] / df['TotalPremium'].replace(0, np.nan)
    df['Margin'] = df['TotalPremium'] - df['TotalClaims']
    df['HasClaim'] = (df['TotalClaims'] > 0).astype(int)
    
    return df

def clean_data(df):
    \"\"\"Basic data cleaning\"\"\"
    df_clean = df.copy()
    
    # Remove rows with negative premiums
    df_clean = df_clean[df_clean['TotalPremium'] > 0]
    
    # Cap outliers at 99th percentile for claims
    cap = df_clean['TotalClaims'].quantile(0.99)
    df_clean['TotalClaims_capped'] = df_clean['TotalClaims'].clip(upper=cap)
    
    return df_clean
