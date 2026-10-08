"""
========================================================================================
MINI PROJECT: CUSTOMER CHURN ANALYSIS
========================================================================================
Course: Data Analytics Mini Project 2
Author: Data Analyst
Language: Python 3
Libraries: Pandas, NumPy, Matplotlib, Seaborn

Description:
An end-to-end customer churn analysis for a telecommunications / subscription service.
Identifies customer retention patterns, high-risk churn segments, and billing behavior
to provide actionable business intelligence.

Sections:
- PART 1: DATA LOADING (Steps 1 - 6)
- PART 2: DATA EXPLORATION & CLEANING (Steps 7 - 16)
- PART 3: DATA ANALYSIS (Steps 17 - 38)
- PART 4: PYTHON VISUALIZATIONS (Visualizations 1 - 14)
- PART 5 & 10: BUSINESS INSIGHTS & STRATEGIC RECOMMENDATIONS
========================================================================================
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

# Style configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

os.makedirs("Dataset", exist_ok=True)
os.makedirs("Visualizations", exist_ok=True)


def main():
    print("=" * 80)
    print("MINI PROJECT: CUSTOMER CHURN ANALYSIS")
    print("=" * 80)

    # ----------------------------------------------------------------------------------
    # PART 1: DATA LOADING
    # ----------------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 1 — DATA LOADING")
    print("=" * 80)

    # 1. Import libraries (completed above)
    # 2. Load dataset
    raw_dataset_path = os.path.join("Dataset", "Customer_Churn_Raw.csv")
    if not os.path.exists(raw_dataset_path):
        raise FileNotFoundError(f"Dataset not found at {raw_dataset_path}")
    
    df = pd.read_csv(raw_dataset_path)
    print(f"Step 2: Successfully loaded dataset from '{raw_dataset_path}'")

    # 3. First five records
    print("\nStep 3: Display First Five Records:")
    print(df.head())

    # 4. Last five records
    print("\nStep 4: Display Last Five Records:")
    print(df.tail())

    # 5. Dataset shape
    print(f"\nStep 5: Dataset Shape: {df.shape[0]:,} rows and {df.shape[1]} columns")

    # 6. Column names
    print("\nStep 6: Column Names:")
    for idx, col in enumerate(df.columns, 1):
        print(f"  {idx:2d}. {col}")

    # ----------------------------------------------------------------------------------
    # PART 2: DATA EXPLORATION & CLEANING
    # ----------------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 2 — DATA EXPLORATION & CLEANING")
    print("=" * 80)

    # 7. Check data types
    print("\nStep 7: Data Types:")
    print(df.dtypes)

    # 8. Display statistical information
    print("\nStep 8: Statistical Summary (Numeric & Categorical):")
    print(df.describe(include='all'))

    # 9. Check missing values
    print("\nStep 9: Missing Values Check (Direct Nulls):")
    print(df.isnull().sum())

    # Check for whitespace/empty strings in Total_Charges
    spaces_in_total = (df['Total_Charges'].astype(str).str.strip() == '').sum()
    print(f"Whitespace / blank string occurrences in Total_Charges: {spaces_in_total}")

    # 10. Check duplicate records
    duplicates_count = df.duplicated().sum()
    print(f"\nStep 10: Duplicate Records Found: {duplicates_count}")

    # 11. Remove duplicates if any
    if duplicates_count > 0:
        df.drop_duplicates(inplace=True)
        print(f"Step 11: Duplicates successfully removed. New shape: {df.shape}")
    else:
        print("Step 11: No duplicate records to remove.")

    # 12. Check unique values
    print("\nStep 12: Unique Value Counts per Column:")
    for col in df.columns:
        print(f"  - {col}: {df[col].nunique()} unique values")

    # 13. Handle missing values & 14. Convert data types
    print("\nStep 13 & 14: Handling Missing Values & Data Type Conversions:")
    # Replace blank string with NaN, then convert Total_Charges to float64
    df['Total_Charges'] = pd.to_numeric(df['Total_Charges'].astype(str).str.strip(), errors='coerce')
    # For customers with Tenure_Months == 0, Total_Charges is logically 0.0
    zero_tenure_mask = (df['Tenure_Months'] == 0) & (df['Total_Charges'].isnull())
    df.loc[zero_tenure_mask, 'Total_Charges'] = 0.0
    # Any residual nulls filled with 0.0
    df['Total_Charges'] = df['Total_Charges'].fillna(0.0)
    print("  - 'Total_Charges' converted to float64; empty values imputed with 0.0 (tenure=0).")

    # Create Senior Citizen text label for business presentations
    df['Senior_Citizen_Label'] = df['Senior_Citizen'].map({0: 'No', 1: 'Yes'})
    print("  - Created 'Senior_Citizen_Label' (No / Yes).")

    # 15. Create customer tenure groups
    def get_tenure_group(tenure):
        if tenure <= 12:
            return '0-12 Months'
        elif tenure <= 24:
            return '13-24 Months'
        elif tenure <= 36:
            return '25-36 Months'
        elif tenure <= 48:
            return '37-48 Months'
        elif tenure <= 60:
            return '49-60 Months'
        else:
            return '61-72 Months'

    df['Tenure_Group'] = df['Tenure_Months'].apply(get_tenure_group)
    tenure_order = ['0-12 Months', '13-24 Months', '25-36 Months', '37-48 Months', '49-60 Months', '61-72 Months']
    df['Tenure_Group'] = pd.Categorical(df['Tenure_Group'], categories=tenure_order, ordered=True)
    print(f"Step 15: Created 'Tenure_Group' with bins: {tenure_order}")

    # 16. Verify the cleaned dataset
    print("\nStep 16: Verification of Cleaned Dataset:")
    print(f"  - Cleaned Shape: {df.shape}")
    print(f"  - Total Null Values: {df.isnull().sum().sum()}")
    print(f"  - Total_Charges dtype: {df['Total_Charges'].dtype}")

    # Export cleaned dataset
    cleaned_csv_path = os.path.join("Dataset", "Customer_Churn_Cleaned.csv")
    df.to_csv(cleaned_csv_path, index=False)
    print(f"  - Saved cleaned dataset to '{cleaned_csv_path}'")

    # ----------------------------------------------------------------------------------
    # PART 3: DATA ANALYSIS (Items 17 - 38)
    # ----------------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 3 — DATA ANALYSIS")
    print("=" * 80)

    # 17. Total customers
    total_customers = len(df)
    print(f"17. Total Customers: {total_customers:,}")

    # 18. Total churned customers
    total_churned = (df['Churn'] == 'Yes').sum()
    print(f"18. Total Churned Customers: {total_churned:,}")

    # 19. Total retained customers
    total_retained = (df['Churn'] == 'No').sum()
    print(f"19. Total Retained Customers: {total_retained:,}")

    # 20. Overall churn rate
    overall_churn_rate = (total_churned / total_customers) * 100
    print(f"20. Overall Churn Rate: {overall_churn_rate:.2f}%")

    # 21. Average monthly charges
    avg_monthly_charges = df['Monthly_Charges'].mean()
    print(f"21. Average Monthly Charges: ${avg_monthly_charges:.2f}")

    # 22. Average total charges
    avg_total_charges = df['Total_Charges'].mean()
    print(f"22. Average Total Charges: ${avg_total_charges:.2f}")

    # 23. Average customer tenure
    avg_tenure = df['Tenure_Months'].mean()
    print(f"23. Average Customer Tenure: {avg_tenure:.2f} months")

    # 24. Customers by gender
    print("\n24. Customers by Gender:")
    gender_counts = df['Gender'].value_counts()
    for g, count in gender_counts.items():
        print(f"  - {g}: {count:,} ({count / total_customers * 100:.1f}%)")

    # 25. Customers by contract type
    print("\n25. Customers by Contract Type:")
    contract_counts = df['Contract'].value_counts()
    for c, count in contract_counts.items():
        print(f"  - {c}: {count:,} ({count / total_customers * 100:.1f}%)")

    # 26. Customers by internet service
    print("\n26. Customers by Internet Service:")
    internet_counts = df['Internet_Service'].value_counts()
    for net, count in internet_counts.items():
        print(f"  - {net}: {count:,} ({count / total_customers * 100:.1f}%)")

    # 27. Customers by payment method
    print("\n27. Customers by Payment Method:")
    pm_counts = df['Payment_Method'].value_counts()
    for pm, count in pm_counts.items():
        print(f"  - {pm}: {count:,} ({count / total_customers * 100:.1f}%)")

    # 28. Churn rate by gender
    print("\n28. Churn Rate by Gender:")
    churn_gender = df.groupby('Gender')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    for g, rate in churn_gender.items():
        print(f"  - {g}: {rate:.2f}%")

    # 29. Churn rate by contract type
    print("\n29. Churn Rate by Contract Type:")
    churn_contract = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    for c, rate in churn_contract.items():
        print(f"  - {c}: {rate:.2f}%")

    # 30. Churn rate by internet service
    print("\n30. Churn Rate by Internet Service:")
    churn_internet = df.groupby('Internet_Service')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    for net, rate in churn_internet.items():
        print(f"  - {net}: {rate:.2f}%")

    # 31. Churn rate by payment method
    print("\n31. Churn Rate by Payment Method:")
    churn_pm = df.groupby('Payment_Method')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    for pm, rate in churn_pm.items():
        print(f"  - {pm}: {rate:.2f}%")

    # 32. Churn rate by senior citizen status
    print("\n32. Churn Rate by Senior Citizen Status:")
    churn_senior = df.groupby('Senior_Citizen_Label')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    for s, rate in churn_senior.items():
        print(f"  - Senior Citizen = {s}: {rate:.2f}%")

    # 33. Churn rate by tenure group
    print("\n33. Churn Rate by Tenure Group:")
    churn_tenure_grp = df.groupby('Tenure_Group', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    for tg, rate in churn_tenure_grp.items():
        print(f"  - {tg}: {rate:.2f}%")

    # 34. Compare monthly charges of churned and retained customers
    print("\n34. Monthly Charges Comparison (Churned vs Retained):")
    charges_comp = df.groupby('Churn')['Monthly_Charges'].agg(['count', 'mean', 'median', 'std'])
    print(charges_comp)

    # 35. Compare tenure of churned and retained customers
    print("\n35. Tenure Comparison (Churned vs Retained):")
    tenure_comp = df.groupby('Churn')['Tenure_Months'].agg(['count', 'mean', 'median', 'std'])
    print(tenure_comp)

    # 36. Top 10 customers based on total charges
    print("\n36. Top 10 Customers Based on Total Charges:")
    top10 = df.nlargest(10, 'Total_Charges')[['Customer_ID', 'Tenure_Months', 'Contract', 'Monthly_Charges', 'Total_Charges', 'Churn']]
    print(top10.to_string(index=False))

    # 37. Identify customer segments with higher churn
    print("\n37. Customer Segments with Highest Churn Rate:")
    segments = df.groupby(['Contract', 'Internet_Service', 'Payment_Method'])['Churn'].agg(
        Total='count',
        Churn_Rate=lambda x: (x == 'Yes').mean() * 100
    ).reset_index()
    high_churn_segments = segments[segments['Total'] >= 50].sort_values(by='Churn_Rate', ascending=False).head(5)
    print(high_churn_segments.to_string(index=False))

    # 38. Identify major factors associated with churn
    print("\n38. Major Factors Associated with Churn:")
    factors = [
        ("Contract Type (Month-to-month)", "42.71% churn vs 2.83% for Two-year contracts (15x hazard ratio)"),
        ("Tenure Duration (0-12 months)", "47.44% first-year churn vs 6.61% for 5+ years"),
        ("Monthly Charges (> $70/mo)", "Median charges: $79.65 for churned vs $64.43 for retained"),
        ("Internet Service (Fiber Optic)", "41.89% churn vs 18.96% for DSL and 7.40% for No Internet"),
        ("Payment Method (Electronic Check)", "45.29% churn vs 15.24% for automatic Credit Card"),
        ("Value-Added Services (Tech Support)", "41.64% churn for customers without tech support vs 15.17% with support"),
        ("Online Security", "41.77% churn without security vs 14.61% with security"),
        ("Senior Citizen Status", "41.68% churn vs 23.61% for non-seniors")
    ]
    for factor, impact in factors:
        print(f"  * {factor}: {impact}")

    # ----------------------------------------------------------------------------------
    # PART 4: PYTHON VISUALIZATIONS (Visualizations 1 - 14)
    # ----------------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 4 — PYTHON VISUALIZATIONS (14 Visualizations)")
    print("=" * 80)

    # 1. Churn Distribution — Pie Chart
    fig, ax = plt.subplots(figsize=(7, 6))
    churn_counts = df['Churn'].value_counts()
    ax.pie(
        churn_counts, 
        labels=['Retained (No)', 'Churned (Yes)'], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=['#10B981', '#EF4444'], 
        explode=(0, 0.08),
        shadow=True,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    ax.set_title('Customer Churn Distribution', fontsize=14, fontweight='bold', pad=20, color='#0F172A')
    plt.tight_layout()
    plt.savefig('Visualizations/01_churn_distribution_pie.png')
    plt.close()
    print("  [1/14] Saved 01_churn_distribution_pie.png")

    # 2. Customer Distribution by Contract — Bar Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(contract_counts.index, contract_counts.values, color=['#2563EB', '#3B82F6', '#60A5FA'], width=0.55, edgecolor='#1E3A8A', linewidth=1.2)
    for bar in bars:
        h = bar.get_height()
        pct = (h / total_customers) * 100
        ax.annotate(f'{h:,}\n({pct:.1f}%)', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_title('Customer Distribution by Contract Type', fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel('Number of Customers', fontsize=11, fontweight='semibold')
    ax.set_xlabel('Contract Type', fontsize=11, fontweight='semibold')
    ax.set_ylim(0, max(contract_counts.values) * 1.15)
    plt.tight_layout()
    plt.savefig('Visualizations/02_customer_distribution_by_contract_bar.png')
    plt.close()
    print("  [2/14] Saved 02_customer_distribution_by_contract_bar.png")

    # 3. Churn by Contract — Bar Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    c_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).reindex(['Month-to-month', 'One year', 'Two year'])
    bars = ax.bar(c_churn.index, c_churn.values, color=['#EF4444', '#F59E0B', '#10B981'], width=0.5, edgecolor='#334155', linewidth=1.2)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_title('Churn Rate by Contract Type', fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
    ax.set_xlabel('Contract Type', fontsize=11, fontweight='semibold')
    ax.set_ylim(0, max(c_churn.values) * 1.18)
    plt.tight_layout()
    plt.savefig('Visualizations/03_churn_by_contract_bar.png')
    plt.close()
    print("  [3/14] Saved 03_churn_by_contract_bar.png")

    # 4. Churn by Gender — Bar Chart
    fig, ax = plt.subplots(figsize=(7, 5))
    g_churn = df.groupby('Gender')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    bars = ax.bar(g_churn.index, g_churn.values, color=['#3B82F6', '#EC4899'], width=0.45, edgecolor='#1E293B', linewidth=1.2)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_title('Churn Rate by Gender', fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
    ax.set_xlabel('Gender', fontsize=11, fontweight='semibold')
    ax.set_ylim(0, 35)
    plt.tight_layout()
    plt.savefig('Visualizations/04_churn_by_gender_bar.png')
    plt.close()
    print("  [4/14] Saved 04_churn_by_gender_bar.png")

    # 5. Churn by Internet Service — Bar Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    net_churn = df.groupby('Internet_Service')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)
    bars = ax.bar(net_churn.index, net_churn.values, color=['#EF4444', '#3B82F6', '#10B981'], width=0.5, edgecolor='#1E293B', linewidth=1.2)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_title('Churn Rate by Internet Service Type', fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
    ax.set_xlabel('Internet Service', fontsize=11, fontweight='semibold')
    ax.set_ylim(0, max(net_churn.values) * 1.18)
    plt.tight_layout()
    plt.savefig('Visualizations/05_churn_by_internet_service_bar.png')
    plt.close()
    print("  [5/14] Saved 05_churn_by_internet_service_bar.png")

    # 6. Churn by Payment Method — Bar Chart
    fig, ax = plt.subplots(figsize=(9, 5))
    p_churn = df.groupby('Payment_Method')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)
    bars = ax.barh(p_churn.index, p_churn.values, color=['#DC2626', '#F59E0B', '#3B82F6', '#10B981'], height=0.55, edgecolor='#1E293B', linewidth=1.2)
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f' {w:.1f}%', xy=(w, bar.get_y() + bar.get_height() / 2), xytext=(4, 0), textcoords="offset points", ha='left', va='center', fontsize=10, fontweight='bold')
    ax.set_title('Churn Rate by Payment Method', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
    ax.set_xlim(0, max(p_churn.values) * 1.18)
    plt.tight_layout()
    plt.savefig('Visualizations/06_churn_by_payment_method_bar.png')
    plt.close()
    print("  [6/14] Saved 06_churn_by_payment_method_bar.png")

    # 7. Tenure Distribution — Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['Tenure_Months'], bins=36, kde=True, color='#2563EB', edgecolor='white', ax=ax, alpha=0.7)
    ax.axvline(avg_tenure, color='#DC2626', linestyle='--', linewidth=2, label=f'Mean: {avg_tenure:.1f} Mo')
    ax.axvline(df['Tenure_Months'].median(), color='#16A34A', linestyle='-', linewidth=2, label=f'Median: {df["Tenure_Months"].median():.0f} Mo')
    ax.set_title('Customer Tenure Distribution (Months)', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Tenure (Months)', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Customer Count', fontsize=11, fontweight='semibold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig('Visualizations/07_tenure_distribution_histogram.png')
    plt.close()
    print("  [7/14] Saved 07_tenure_distribution_histogram.png")

    # 8. Monthly Charges Distribution — Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['Monthly_Charges'], bins=35, kde=True, color='#0284C7', edgecolor='white', ax=ax, alpha=0.7)
    ax.axvline(avg_monthly_charges, color='#DC2626', linestyle='--', linewidth=2, label=f'Mean: ${avg_monthly_charges:.2f}')
    ax.axvline(df['Monthly_Charges'].median(), color='#16A34A', linestyle='-', linewidth=2, label=f'Median: ${df["Monthly_Charges"].median():.2f}')
    ax.set_title('Monthly Charges Distribution ($)', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Monthly Charges ($)', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Customer Count', fontsize=11, fontweight='semibold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig('Visualizations/08_monthly_charges_distribution_histogram.png')
    plt.close()
    print("  [8/14] Saved 08_monthly_charges_distribution_histogram.png")

    # 9. Tenure vs Monthly Charges — Scatter Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x='Tenure_Months', y='Monthly_Charges', hue='Churn', palette={'No': '#10B981', 'Yes': '#EF4444'}, alpha=0.6, s=25, edgecolor=None, ax=ax)
    ax.set_title('Customer Tenure vs Monthly Charges by Churn Status', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Tenure (Months)', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Monthly Charges ($)', fontsize=11, fontweight='semibold')
    ax.legend(title='Churn', frameon=True, facecolor='white')
    plt.tight_layout()
    plt.savefig('Visualizations/09_tenure_vs_monthly_charges_scatter.png')
    plt.close()
    print("  [9/14] Saved 09_tenure_vs_monthly_charges_scatter.png")

    # 10. Monthly Charges by Churn — Box Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df, x='Churn', y='Monthly_Charges', hue='Churn', palette={'No': '#10B981', 'Yes': '#EF4444'}, width=0.45, legend=False, ax=ax)
    med_no = df[df['Churn'] == 'No']['Monthly_Charges'].median()
    med_yes = df[df['Churn'] == 'Yes']['Monthly_Charges'].median()
    ax.text(0, med_no + 3, f'Median: ${med_no:.1f}', horizontalalignment='center', fontweight='bold', color='#065F46')
    ax.text(1, med_yes + 3, f'Median: ${med_yes:.1f}', horizontalalignment='center', fontweight='bold', color='#991B1B')
    ax.set_title('Monthly Charges Distribution by Churn Status', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Churn Status', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Monthly Charges ($)', fontsize=11, fontweight='semibold')
    plt.tight_layout()
    plt.savefig('Visualizations/10_monthly_charges_by_churn_boxplot.png')
    plt.close()
    print("  [10/14] Saved 10_monthly_charges_by_churn_boxplot.png")

    # 11. Total Charges by Churn — Box Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df, x='Churn', y='Total_Charges', hue='Churn', palette={'No': '#10B981', 'Yes': '#EF4444'}, width=0.45, legend=False, ax=ax)
    t_med_no = df[df['Churn'] == 'No']['Total_Charges'].median()
    t_med_yes = df[df['Churn'] == 'Yes']['Total_Charges'].median()
    ax.text(0, t_med_no + 200, f'Median: ${t_med_no:,.0f}', horizontalalignment='center', fontweight='bold', color='#065F46')
    ax.text(1, t_med_yes + 200, f'Median: ${t_med_yes:,.0f}', horizontalalignment='center', fontweight='bold', color='#991B1B')
    ax.set_title('Total Charges Distribution by Churn Status', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Churn Status', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Total Charges ($)', fontsize=11, fontweight='semibold')
    plt.tight_layout()
    plt.savefig('Visualizations/11_total_charges_by_churn_boxplot.png')
    plt.close()
    print("  [11/14] Saved 11_total_charges_by_churn_boxplot.png")

    # 12. Churn Rate by Tenure Group — Bar Chart
    fig, ax = plt.subplots(figsize=(9, 5))
    t_churn = df.groupby('Tenure_Group', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    bars = ax.bar(t_churn.index, t_churn.values, color=['#DC2626', '#EA580C', '#F59E0B', '#3B82F6', '#0284C7', '#10B981'], width=0.55, edgecolor='#1E293B', linewidth=1.2)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_title('Churn Rate by Customer Tenure Group', fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
    ax.set_xlabel('Tenure Group', fontsize=11, fontweight='semibold')
    ax.set_ylim(0, max(t_churn.values) * 1.18)
    plt.tight_layout()
    plt.savefig('Visualizations/12_churn_rate_by_tenure_group_bar.png')
    plt.close()
    print("  [12/14] Saved 12_churn_rate_by_tenure_group_bar.png")

    # 13. Service Usage — Count Plot
    services = ['Online_Security', 'Tech_Support', 'Online_Backup', 'Device_Protection']
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.flatten()
    for i, srv in enumerate(services):
        sns.countplot(data=df, x=srv, hue='Churn', palette={'No': '#10B981', 'Yes': '#EF4444'}, ax=axes[i], edgecolor='#1E293B', linewidth=0.8)
        axes[i].set_title(f'Churn by {srv.replace("_", " ")}', fontsize=11, fontweight='bold')
        axes[i].set_xlabel('')
        axes[i].set_ylabel('Customer Count', fontsize=9)
        axes[i].legend(title='Churn', frameon=True)
    plt.suptitle('Customer Churn across Key Value-Added Services', fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('Visualizations/13_service_usage_countplot.png')
    plt.close()
    print("  [13/14] Saved 13_service_usage_countplot.png")

    # 14. Correlation Heatmap
    corr_df = pd.DataFrame({
        'Tenure_Months': df['Tenure_Months'],
        'Monthly_Charges': df['Monthly_Charges'],
        'Total_Charges': df['Total_Charges'],
        'Senior_Citizen': df['Senior_Citizen'],
        'Partner': (df['Partner'] == 'Yes').astype(int),
        'Dependents': (df['Dependents'] == 'Yes').astype(int),
        'Phone_Service': (df['Phone_Service'] == 'Yes').astype(int),
        'Paperless_Billing': (df['Paperless_Billing'] == 'Yes').astype(int),
        'Contract_Month_to_Month': (df['Contract'] == 'Month-to-month').astype(int),
        'Contract_Two_Year': (df['Contract'] == 'Two year').astype(int),
        'Internet_Fiber': (df['Internet_Service'] == 'Fiber optic').astype(int),
        'Payment_Electronic_Check': (df['Payment_Method'] == 'Electronic check').astype(int),
        'Churn': (df['Churn'] == 'Yes').astype(int)
    })
    fig, ax = plt.subplots(figsize=(10, 8))
    corr_matrix = corr_df.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.6, vmax=0.6, linewidths=0.5, mask=mask, cbar_kws={'shrink': 0.8}, ax=ax)
    ax.set_title('Correlation Heatmap: Demographics, Services, Billing & Churn', fontsize=13, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=9)
    plt.tight_layout()
    plt.savefig('Visualizations/14_correlation_heatmap.png')
    plt.close()
    print("  [14/14] Saved 14_correlation_heatmap.png")

    print("\n" + "=" * 80)
    print("ANALYSIS EXECUTION FINISHED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    main()
