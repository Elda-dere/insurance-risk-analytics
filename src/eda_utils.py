import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_loss_ratio_by_category(df, category_col):
    \"\"\"Plot loss ratio by category\"\"\"
    loss_by_cat = df.groupby(category_col).agg({
        'TotalClaims': 'sum',
        'TotalPremium': 'sum'
    })
    loss_by_cat['LossRatio'] = loss_by_cat['TotalClaims'] / loss_by_cat['TotalPremium']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    loss_by_cat['LossRatio'].sort_values().plot(kind='bar', ax=ax)
    ax.set_title(f'Loss Ratio by {category_col}')
    ax.set_ylabel('Loss Ratio')
    ax.axhline(y=1, color='r', linestyle='--', label='Break-even (1.0)')
    ax.legend()
    return fig

def create_temporal_analysis(df):
    \"\"\"Analyze trends over time\"\"\"
    if 'TransactionMonth' in df.columns:
        monthly = df.groupby(pd.Grouper(key='TransactionMonth', freq='ME')).agg({
            'TotalClaims': 'sum',
            'TotalPremium': 'sum',
            'HasClaim': 'mean'
        })
        monthly['LossRatio'] = monthly['TotalClaims'] / monthly['TotalPremium']
        
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        monthly['TotalPremium'].plot(ax=axes[0], title='Total Premium Over Time')
        monthly['TotalClaims'].plot(ax=axes[1], title='Total Claims Over Time')
        monthly['LossRatio'].plot(ax=axes[2], title='Loss Ratio Over Time')
        axes[2].axhline(y=1, color='r', linestyle='--')
        plt.tight_layout()
        return fig, monthly
    return None, None
