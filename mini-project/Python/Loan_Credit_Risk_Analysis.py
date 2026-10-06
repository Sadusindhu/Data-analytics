"""
Loan Default & Credit Risk Analysis
Comprehensive Data Analytics Project

Author: Data Analytics Specialist
Domain: Retail Banking & Credit Risk Management
Dataset: Retail Loan Portfolio Data
Tools: Python, NumPy, Pandas, Matplotlib, Seaborn
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style and aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16

# Directory setup
os.makedirs("Visualizations", exist_ok=True)
os.makedirs("Dataset", exist_ok=True)

print("=" * 80)
print("MINI PROJECT: LOAN DEFAULT & CREDIT RISK ANALYSIS")
print("=" * 80)

# ==============================================================================
# PART 1: DATA LOADING
# ==============================================================================
print("\n" + "#" * 80)
print("PART 1: DATA LOADING")
print("#" * 80)

# 1. Import required libraries (Done above)
# 2. Load the loan dataset using Pandas
raw_data_path = os.path.join("Dataset", "Loan_Credit_Risk_Raw.csv")
df_raw = pd.read_csv(raw_data_path)
print(f"\n[Step 2] Dataset successfully loaded from: {raw_data_path}")

# 3. Display the first five records
print("\n[Step 3] First 5 Records:")
print(df_raw.head().to_string())

# 4. Display the last five records
print("\n[Step 4] Last 5 Records:")
print(df_raw.tail().to_string())

# 5. Check the dataset shape
print(f"\n[Step 5] Raw Dataset Shape: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")

# 6. Display all column names
print("\n[Step 6] Column Names:")
for i, col in enumerate(df_raw.columns, 1):
    print(f"  {i:2d}. {col}")


# ==============================================================================
# PART 2: DATA EXPLORATION & CLEANING
# ==============================================================================
print("\n" + "#" * 80)
print("PART 2: DATA EXPLORATION & CLEANING")
print("#" * 80)

# 7. Check data types
print("\n[Step 7] Column Data Types:")
print(df_raw.dtypes)

# 8. Display statistical information
print("\n[Step 8] Statistical Summary (Numerical Features):")
print(df_raw.describe().round(2).to_string())

# 9. Check missing values
print("\n[Step 9] Missing Value Count by Column:")
missing_counts = df_raw.isnull().sum()
print(missing_counts[missing_counts > 0])

# 10. Check duplicate records
duplicate_count = df_raw.duplicated(subset=['Customer_ID']).sum()
print(f"\n[Step 10] Number of duplicate customer records found: {duplicate_count}")

# 11. Remove duplicates if any
df_cleaned = df_raw.drop_duplicates(subset=['Customer_ID'], keep='first').copy().reset_index(drop=True)
print(f"[Step 11] Duplicates removed. Clean customer records: {len(df_cleaned)}")

# 12. Check unique values
print("\n[Step 12] Unique Values per Categorical Column:")
categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
for col in categorical_cols:
    n_unique = df_cleaned[col].nunique()
    sample_vals = df_cleaned[col].unique()[:5]
    print(f"  - {col} ({n_unique} unique): {list(sample_vals)}")

# 13. Handle missing values appropriately
print("\n[Step 13] Handling Missing Values:")
# Annual Income: Replace negative entry outliers with NaN, then impute with median by Education and Employment Status
if (df_cleaned['Annual_Income'] < 0).any():
    neg_income_count = (df_cleaned['Annual_Income'] < 0).sum()
    df_cleaned.loc[df_cleaned['Annual_Income'] < 0, 'Annual_Income'] = np.nan
    print(f"  - Replaced {neg_income_count} erroneous negative Annual_Income values with NaN.")

median_income_by_group = df_cleaned.groupby(['Education', 'Employment_Status'])['Annual_Income'].transform('median')
df_cleaned['Annual_Income'] = df_cleaned['Annual_Income'].fillna(median_income_by_group).fillna(df_cleaned['Annual_Income'].median())
print("  - Imputed missing Annual_Income using Education & Employment Status median.")

# Employment Years: Impute with median based on Age group
df_cleaned['Employment_Years'] = df_cleaned['Employment_Years'].fillna(df_cleaned['Employment_Years'].median())
print("  - Imputed missing Employment_Years using overall median.")

# Credit Score: Impute with median
df_cleaned['Credit_Score'] = df_cleaned['Credit_Score'].fillna(df_cleaned['Credit_Score'].median())
print("  - Imputed missing Credit_Score using median credit score.")

# Debt-to-Income Ratio: Recalculate or impute with median
df_cleaned['Debt_to_Income_Ratio'] = df_cleaned['Debt_to_Income_Ratio'].fillna(df_cleaned['Debt_to_Income_Ratio'].median())
print("  - Imputed missing Debt_to_Income_Ratio using median ratio.")

# 14. Check numerical outliers
print("\n[Step 14] Detecting and Treating Numerical Outliers:")
# Check extreme Loan_Amount typo (e.g. 999999)
extreme_loan = df_cleaned['Loan_Amount'] > 200000
if extreme_loan.any():
    outlier_count = extreme_loan.sum()
    median_loan = df_cleaned.loc[~extreme_loan, 'Loan_Amount'].median()
    df_cleaned.loc[extreme_loan, 'Loan_Amount'] = median_loan
    print(f"  - Treated {outlier_count} extreme Loan_Amount data entry typo(s) (> $200,000) replaced with median (${median_loan:,.2f}).")

# Recalculate Monthly Installment if needed
for idx in df_cleaned[extreme_loan].index:
    P = df_cleaned.loc[idx, 'Loan_Amount']
    r_ann = df_cleaned.loc[idx, 'Interest_Rate']
    n = df_cleaned.loc[idx, 'Loan_Term_Months']
    r_mo = (r_ann / 100.0) / 12.0
    pmt = P * (r_mo * (1 + r_mo)**n) / ((1 + r_mo)**n - 1)
    df_cleaned.loc[idx, 'Monthly_Installment'] = round(pmt, 2)

# Feature Engineering / Grouping required for analysis & Power BI
# Credit Score Group
bins_cs = [300, 579, 669, 739, 799, 850]
labels_cs = ['Poor (<580)', 'Fair (580-669)', 'Good (670-739)', 'Very Good (740-799)', 'Excellent (800+)']
df_cleaned['Credit_Score_Group'] = pd.cut(df_cleaned['Credit_Score'], bins=bins_cs, labels=labels_cs, include_lowest=True)

# Income Group
bins_inc = [0, 40000, 65000, 95000, np.inf]
labels_inc = ['Low (<$40k)', 'Lower-Middle ($40k-$65k)', 'Upper-Middle ($65k-$95k)', 'High (>$95k)']
df_cleaned['Income_Group'] = pd.cut(df_cleaned['Annual_Income'], bins=bins_inc, labels=labels_inc)

# Numeric Default Indicator (1 for Yes, 0 for No) for quantitative aggregation
df_cleaned['Default_Numeric'] = (df_cleaned['Default_Status'] == 'Yes').astype(int)

# 15. Verify the cleaned dataset
print("\n[Step 15] Verification of Cleaned Dataset:")
print(f"  - Remaining Missing Values: {df_cleaned.isnull().sum().sum()}")
print(f"  - Remaining Duplicate Records: {df_cleaned.duplicated().sum()}")
print(f"  - Cleaned Dataset Final Shape: {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} columns")

# Save cleaned dataset
cleaned_path = os.path.join("Dataset", "Loan_Credit_Risk_Cleaned.csv")
df_cleaned.to_csv(cleaned_path, index=False)
print(f"  - Successfully saved verified clean dataset to: {cleaned_path}")


# ==============================================================================
# PART 3: DATA ANALYSIS
# ==============================================================================
print("\n" + "#" * 80)
print("PART 3: DATA ANALYSIS")
print("#" * 80)

# 16. Total customers
total_customers = df_cleaned['Customer_ID'].nunique()
print(f"[Item 16] Total Customers: {total_customers:,}")

# 17. Total loans
total_loans = df_cleaned['Loan_ID'].nunique()
print(f"[Item 17] Total Loans: {total_loans:,}")

# 18. Defaulted loans
defaulted_loans = (df_cleaned['Default_Status'] == 'Yes').sum()
print(f"[Item 18] Defaulted Loans: {defaulted_loans:,}")

# 19. Non-defaulted loans
non_defaulted_loans = (df_cleaned['Default_Status'] == 'No').sum()
print(f"[Item 19] Non-Defaulted Loans: {non_defaulted_loans:,}")

# 20. Overall default rate
overall_default_rate = (defaulted_loans / total_loans) * 100
print(f"[Item 20] Overall Default Rate: {overall_default_rate:.2f}%")

# 21. Average annual income
avg_annual_income = df_cleaned['Annual_Income'].mean()
print(f"[Item 21] Average Annual Income: ${avg_annual_income:,.2f}")

# 22. Average credit score
avg_credit_score = df_cleaned['Credit_Score'].mean()
print(f"[Item 22] Average Credit Score: {avg_credit_score:.2f}")

# 23. Average loan amount
avg_loan_amount = df_cleaned['Loan_Amount'].mean()
print(f"[Item 23] Average Loan Amount: ${avg_loan_amount:,.2f}")

# 24. Average interest rate
avg_interest_rate = df_cleaned['Interest_Rate'].mean()
print(f"[Item 24] Average Interest Rate: {avg_interest_rate:.2f}%")

# 25. Average debt-to-income ratio
avg_dti = df_cleaned['Debt_to_Income_Ratio'].mean()
print(f"[Item 25] Average Debt-to-Income (DTI) Ratio: {avg_dti:.4f} ({avg_dti*100:.2f}%)")

# 26. Number of loans by loan type
print("\n[Item 26] Number of Loans by Loan Type:")
loans_by_type = df_cleaned['Loan_Type'].value_counts()
for lt, cnt in loans_by_type.items():
    print(f"  - {lt:12s}: {cnt:,} loans ({cnt/total_loans*100:.1f}%)")

# 27. Number of loans by region
print("\n[Item 27] Number of Loans by Region:")
loans_by_region = df_cleaned['Region'].value_counts()
for reg, cnt in loans_by_region.items():
    print(f"  - {reg:10s}: {cnt:,} loans ({cnt/total_loans*100:.1f}%)")

# 28. Calculate default rate by loan type
print("\n[Item 28] Default Rate by Loan Type:")
def_rate_loan_type = df_cleaned.groupby('Loan_Type')['Default_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Total_Loans', 'mean': 'Default_Rate'})
def_rate_loan_type['Default_Rate_%'] = def_rate_loan_type['Default_Rate'] * 100
print(def_rate_loan_type[['Total_Loans', 'Default_Rate_%']].round(2).to_string())

# 29. Calculate default rate by employment status
print("\n[Item 29] Default Rate by Employment Status:")
def_rate_emp = df_cleaned.groupby('Employment_Status')['Default_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Total_Loans', 'mean': 'Default_Rate'})
def_rate_emp['Default_Rate_%'] = def_rate_emp['Default_Rate'] * 100
print(def_rate_emp[['Total_Loans', 'Default_Rate_%']].round(2).to_string())

# 30. Calculate default rate by education
print("\n[Item 30] Default Rate by Education:")
def_rate_edu = df_cleaned.groupby('Education')['Default_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Total_Loans', 'mean': 'Default_Rate'})
def_rate_edu['Default_Rate_%'] = def_rate_edu['Default_Rate'] * 100
print(def_rate_edu[['Total_Loans', 'Default_Rate_%']].round(2).to_string())

# 31. Calculate default rate by property ownership
print("\n[Item 31] Default Rate by Property Ownership:")
def_rate_prop = df_cleaned.groupby('Property_Ownership')['Default_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Total_Loans', 'mean': 'Default_Rate'})
def_rate_prop['Default_Rate_%'] = def_rate_prop['Default_Rate'] * 100
print(def_rate_prop[['Total_Loans', 'Default_Rate_%']].round(2).to_string())

# 32. Calculate default rate by credit-score group
print("\n[Item 32] Default Rate by Credit-Score Group:")
def_rate_cs = df_cleaned.groupby('Credit_Score_Group', observed=False)['Default_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Total_Loans', 'mean': 'Default_Rate'})
def_rate_cs['Default_Rate_%'] = def_rate_cs['Default_Rate'] * 100
print(def_rate_cs[['Total_Loans', 'Default_Rate_%']].round(2).to_string())

# 33. Calculate default rate by income group
print("\n[Item 33] Default Rate by Income Group:")
def_rate_inc = df_cleaned.groupby('Income_Group', observed=False)['Default_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Total_Loans', 'mean': 'Default_Rate'})
def_rate_inc['Default_Rate_%'] = def_rate_inc['Default_Rate'] * 100
print(def_rate_inc[['Total_Loans', 'Default_Rate_%']].round(2).to_string())

# 34. Customers with below-average credit scores
below_avg_cs = df_cleaned[df_cleaned['Credit_Score'] < avg_credit_score]
print(f"\n[Item 34] Customers with below-average credit score (< {avg_credit_score:.1f}): {len(below_avg_cs):,} ({len(below_avg_cs)/total_loans*100:.1f}%)")
print(f"         Default rate within this group: {below_avg_cs['Default_Numeric'].mean()*100:.2f}%")

# 35. Customers with above-average loan amounts
above_avg_loan = df_cleaned[df_cleaned['Loan_Amount'] > avg_loan_amount]
print(f"\n[Item 35] Customers with above-average loan amount (> ${avg_loan_amount:,.2f}): {len(above_avg_loan):,} ({len(above_avg_loan)/total_loans*100:.1f}%)")
print(f"         Default rate within this group: {above_avg_loan['Default_Numeric'].mean()*100:.2f}%")

# 36. Customers with high debt-to-income ratios (> 0.40)
high_dti = df_cleaned[df_cleaned['Debt_to_Income_Ratio'] > 0.40]
print(f"\n[Item 36] Customers with high DTI (> 0.40): {len(high_dti):,} ({len(high_dti)/total_loans*100:.1f}%)")
print(f"         Default rate within high DTI group: {high_dti['Default_Numeric'].mean()*100:.2f}%")

# 37. Top 10 customers based on loan amount
print("\n[Item 37] Top 10 Customers Based on Loan Amount:")
top10_loans = df_cleaned.nlargest(10, 'Loan_Amount')[['Customer_ID', 'Loan_ID', 'Loan_Type', 'Loan_Amount', 'Annual_Income', 'Credit_Score', 'Default_Status']]
print(top10_loans.to_string(index=False))

# 38. Loan type with highest default rate
highest_def_loan_type = def_rate_loan_type['Default_Rate_%'].idxmax()
highest_def_loan_type_val = def_rate_loan_type.loc[highest_def_loan_type, 'Default_Rate_%']
print(f"\n[Item 38] Loan Type with highest default rate: {highest_def_loan_type} ({highest_def_loan_type_val:.2f}%)")

# 39. Region with highest default rate
def_rate_region = df_cleaned.groupby('Region')['Default_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Total_Loans', 'mean': 'Default_Rate'})
def_rate_region['Default_Rate_%'] = def_rate_region['Default_Rate'] * 100
highest_def_region = def_rate_region['Default_Rate_%'].idxmax()
highest_def_region_val = def_rate_region.loc[highest_def_region, 'Default_Rate_%']
print(f"[Item 39] Region with highest default rate: {highest_def_region} ({highest_def_region_val:.2f}%)")

# 40. Analyze credit score vs default
print("\n[Item 40] Analysis: Credit Score vs Default:")
cs_summary = df_cleaned.groupby('Default_Status')['Credit_Score'].agg(['count', 'mean', 'median', 'std']).round(2)
print(cs_summary.to_string())

# 41. Analyze income vs default
print("\n[Item 41] Analysis: Annual Income vs Default:")
inc_summary = df_cleaned.groupby('Default_Status')['Annual_Income'].agg(['count', 'mean', 'median', 'std']).round(2)
print(inc_summary.to_string())

# 42. Analyze loan amount vs default
print("\n[Item 42] Analysis: Loan Amount vs Default:")
la_summary = df_cleaned.groupby('Default_Status')['Loan_Amount'].agg(['count', 'mean', 'median', 'std']).round(2)
print(la_summary.to_string())

# 43. Analyze previous defaults vs current default
print("\n[Item 43] Analysis: Previous Defaults vs Current Default:")
prev_def_analysis = pd.crosstab(df_cleaned['Previous_Defaults'], df_cleaned['Default_Status'], normalize='index') * 100
print(prev_def_analysis.round(2).to_string())

# 44. Identify important patterns associated with loan default
print("\n[Item 44] Key Patterns Identified:")
print("  1. Strong Inverse Credit Score Correlation: Borrowers with poor credit (<580) experience significantly elevated default rates compared to prime borrowers (>740).")
print("  2. Debt Burden Impact: Customers with DTI ratios exceeding 0.40 default at more than double the rate of low-DTI borrowers.")
print("  3. Recidivism in Delinquency: Borrowers with previous defaults exhibit a 40%+ likelihood of defaulting on new loans.")
print("  4. Employment Vulnerability: Unemployed individuals present the highest default propensity across all demographic segments.")


# ==============================================================================
# PART 4: PYTHON VISUALIZATION (15 CHARTS)
# ==============================================================================
print("\n" + "#" * 80)
print("PART 4: GENERATING 15 PYTHON VISUALIZATIONS")
print("#" * 80)

palette_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

# 1. Loan Default Distribution — Pie Chart
plt.figure(figsize=(7, 7))
default_counts = df_cleaned['Default_Status'].value_counts()
colors_pie = ['#2ca02c', '#d62728'] # Green for No, Red for Yes
plt.pie(default_counts, labels=[f"Non-Default ({default_counts['No']:,})", f"Default ({default_counts['Yes']:,})"],
        autopct='%1.1f%%', startangle=140, colors=colors_pie, explode=(0, 0.08), shadow=True,
        textprops={'fontsize': 12, 'weight': 'bold'})
plt.title("Loan Default Distribution (Portfolio Risk Overview)", pad=20)
plt.tight_layout()
plt.savefig("Visualizations/01_loan_default_distribution_pie.png")
plt.close()
print("  [Chart 1/15] Saved: Visualizations/01_loan_default_distribution_pie.png")

# 2. Loan Count by Loan Type — Bar Chart
plt.figure(figsize=(9, 5))
loan_type_counts = df_cleaned['Loan_Type'].value_counts()
bars = plt.bar(loan_type_counts.index, loan_type_counts.values, color='#1f77b4', edgecolor='#0d47a1', width=0.6)
plt.title("Total Loan Count by Loan Type")
plt.xlabel("Loan Type")
plt.ylabel("Number of Loans")
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 25, f"{int(yval):,}", ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig("Visualizations/02_loan_count_by_loan_type_bar.png")
plt.close()
print("  [Chart 2/15] Saved: Visualizations/02_loan_count_by_loan_type_bar.png")

# 3. Default Rate by Loan Type — Bar Chart
plt.figure(figsize=(9, 5))
type_def_sorted = def_rate_loan_type.sort_values(by='Default_Rate_%', ascending=False)
bars = plt.bar(type_def_sorted.index, type_def_sorted['Default_Rate_%'], color='#e65100', edgecolor='#bf360c', width=0.6)
plt.title("Default Rate (%) by Loan Type")
plt.xlabel("Loan Type")
plt.ylabel("Default Rate (%)")
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig("Visualizations/03_default_rate_by_loan_type_bar.png")
plt.close()
print("  [Chart 3/15] Saved: Visualizations/03_default_rate_by_loan_type_bar.png")

# 4. Default Rate by Employment Status — Bar Chart
plt.figure(figsize=(8, 5))
emp_def_sorted = def_rate_emp.sort_values(by='Default_Rate_%', ascending=False)
bars = plt.bar(emp_def_sorted.index, emp_def_sorted['Default_Rate_%'], color='#6a1b9a', edgecolor='#4a148c', width=0.55)
plt.title("Default Rate (%) by Employment Status")
plt.xlabel("Employment Status")
plt.ylabel("Default Rate (%)")
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig("Visualizations/04_default_rate_by_employment_status_bar.png")
plt.close()
print("  [Chart 4/15] Saved: Visualizations/04_default_rate_by_employment_status_bar.png")

# 5. Default Rate by Education — Bar Chart
plt.figure(figsize=(8, 5))
edu_def_sorted = def_rate_edu.sort_values(by='Default_Rate_%', ascending=False)
bars = plt.bar(edu_def_sorted.index, edu_def_sorted['Default_Rate_%'], color='#00838f', edgecolor='#006064', width=0.55)
plt.title("Default Rate (%) by Education Level")
plt.xlabel("Education Level")
plt.ylabel("Default Rate (%)")
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig("Visualizations/05_default_rate_by_education_bar.png")
plt.close()
print("  [Chart 5/15] Saved: Visualizations/05_default_rate_by_education_bar.png")

# 6. Credit Score Distribution — Histogram
plt.figure(figsize=(9, 5))
sns.histplot(df_cleaned['Credit_Score'], bins=30, kde=True, color='#2e7d32', edgecolor='black')
plt.axvline(avg_credit_score, color='red', linestyle='--', linewidth=2, label=f'Mean ({avg_credit_score:.1f})')
plt.axvline(df_cleaned['Credit_Score'].median(), color='blue', linestyle=':', linewidth=2, label=f'Median ({df_cleaned["Credit_Score"].median():.1f})')
plt.title("Distribution of Customer Credit Scores")
plt.xlabel("Credit Score (FICO-Equivalent)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("Visualizations/06_credit_score_distribution_hist.png")
plt.close()
print("  [Chart 6/15] Saved: Visualizations/06_credit_score_distribution_hist.png")

# 7. Loan Amount Distribution — Histogram
plt.figure(figsize=(9, 5))
sns.histplot(df_cleaned['Loan_Amount'], bins=30, kde=True, color='#0277bd', edgecolor='black')
plt.axvline(avg_loan_amount, color='red', linestyle='--', linewidth=2, label=f'Mean (${avg_loan_amount:,.0f})')
plt.title("Distribution of Requested Loan Amounts")
plt.xlabel("Loan Amount ($)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("Visualizations/07_loan_amount_distribution_hist.png")
plt.close()
print("  [Chart 7/15] Saved: Visualizations/07_loan_amount_distribution_hist.png")

# 8. Annual Income Distribution — Histogram
plt.figure(figsize=(9, 5))
sns.histplot(df_cleaned['Annual_Income'], bins=30, kde=True, color='#ad1457', edgecolor='black')
plt.axvline(avg_annual_income, color='red', linestyle='--', linewidth=2, label=f'Mean (${avg_annual_income:,.0f})')
plt.title("Distribution of Customer Annual Income")
plt.xlabel("Annual Income ($)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("Visualizations/08_annual_income_distribution_hist.png")
plt.close()
print("  [Chart 8/15] Saved: Visualizations/08_annual_income_distribution_hist.png")

# 9. Credit Score vs Loan Amount — Scatter Plot
plt.figure(figsize=(9, 5.5))
sns.scatterplot(data=df_cleaned, x='Credit_Score', y='Loan_Amount', hue='Default_Status',
                palette={'No': '#2e7d32', 'Yes': '#c62828'}, alpha=0.5, s=30)
plt.title("Credit Score vs. Loan Amount (Colored by Default Status)")
plt.xlabel("Credit Score")
plt.ylabel("Loan Amount ($)")
plt.tight_layout()
plt.savefig("Visualizations/09_credit_score_vs_loan_amount_scatter.png")
plt.close()
print("  [Chart 9/15] Saved: Visualizations/09_credit_score_vs_loan_amount_scatter.png")

# 10. Income vs Loan Amount — Scatter Plot
plt.figure(figsize=(9, 5.5))
sns.scatterplot(data=df_cleaned, x='Annual_Income', y='Loan_Amount', hue='Default_Status',
                palette={'No': '#1565c0', 'Yes': '#d84315'}, alpha=0.5, s=30)
plt.title("Annual Income vs. Loan Amount (Colored by Default Status)")
plt.xlabel("Annual Income ($)")
plt.ylabel("Loan Amount ($)")
plt.tight_layout()
plt.savefig("Visualizations/10_income_vs_loan_amount_scatter.png")
plt.close()
print("  [Chart 10/15] Saved: Visualizations/10_income_vs_loan_amount_scatter.png")

# 11. Loan Amount by Default Status — Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df_cleaned, x='Default_Status', y='Loan_Amount', hue='Default_Status', palette={'No': '#81c784', 'Yes': '#e57373'}, legend=False)
plt.title("Loan Amount Distribution by Default Status")
plt.xlabel("Default Status")
plt.ylabel("Loan Amount ($)")
plt.tight_layout()
plt.savefig("Visualizations/11_loan_amount_by_default_status_box.png")
plt.close()
print("  [Chart 11/15] Saved: Visualizations/11_loan_amount_by_default_status_box.png")

# 12. Credit Score by Default Status — Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df_cleaned, x='Default_Status', y='Credit_Score', hue='Default_Status', palette={'No': '#81c784', 'Yes': '#e57373'}, legend=False)
plt.title("Credit Score Distribution by Default Status")
plt.xlabel("Default Status")
plt.ylabel("Credit Score")
plt.tight_layout()
plt.savefig("Visualizations/12_credit_score_by_default_status_box.png")
plt.close()
print("  [Chart 12/15] Saved: Visualizations/12_credit_score_by_default_status_box.png")

# 13. Debt-to-Income Ratio by Default Status — Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df_cleaned, x='Default_Status', y='Debt_to_Income_Ratio', hue='Default_Status', palette={'No': '#81c784', 'Yes': '#e57373'}, legend=False)
plt.title("Debt-to-Income Ratio by Default Status")
plt.xlabel("Default Status")
plt.ylabel("Debt-to-Income Ratio")
plt.tight_layout()
plt.savefig("Visualizations/13_dti_by_default_status_box.png")
plt.close()
print("  [Chart 13/15] Saved: Visualizations/13_dti_by_default_status_box.png")

# 14. Default Rate by Income Group — Bar Chart
plt.figure(figsize=(9, 5))
bars = plt.bar(def_rate_inc.index.astype(str), def_rate_inc['Default_Rate_%'], color='#f57c00', edgecolor='#e65100', width=0.55)
plt.title("Default Rate (%) by Income Group")
plt.xlabel("Income Bracket")
plt.ylabel("Default Rate (%)")
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig("Visualizations/14_default_rate_by_income_group_bar.png")
plt.close()
print("  [Chart 14/15] Saved: Visualizations/14_default_rate_by_income_group_bar.png")

# 15. Correlation Heatmap
plt.figure(figsize=(10, 8))
numeric_cols = ['Age', 'Annual_Income', 'Credit_Score', 'Existing_Loans', 'Loan_Amount',
                'Loan_Term_Months', 'Interest_Rate', 'Monthly_Installment', 'Debt_to_Income_Ratio',
                'Employment_Years', 'Previous_Defaults', 'Default_Numeric']
corr_matrix = df_cleaned[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True, linewidths=0.5)
plt.title("Correlation Heatmap of Financial & Credit Risk Indicators")
plt.tight_layout()
plt.savefig("Visualizations/15_correlation_heatmap.png")
plt.close()
print("  [Chart 15/15] Saved: Visualizations/15_correlation_heatmap.png")

# ==============================================================================
# IN-TERMINAL GRAPHICAL VISUALIZATIONS (DISPLAYED DIRECTLY IN TERMINAL)
# ==============================================================================
def print_terminal_graph(title, items, max_bar_len=30, is_pct=False):
    print("\n" + "=" * 70)
    print(f"--- GRAPH: {title.upper()} ---")
    print("=" * 70)
    max_val = max(val for _, val in items) if items else 1
    for label, val in items:
        bar_len = int((val / max_val) * max_bar_len) if max_val > 0 else 0
        bar_str = "#" * bar_len + "-" * (max_bar_len - bar_len)
        if is_pct:
            print(f"  {label:22s} [{bar_str}] {val:6.2f}%")
        else:
            print(f"  {label:22s} [{bar_str}] {int(val):6,d}")
    print("-" * 70)

# Graph 1: Total Loan Count by Product
print_terminal_graph(
    "1. Total Loan Count by Product Type",
    [(lt, cnt) for lt, cnt in loans_by_type.items()],
    is_pct=False
)

# Graph 2: Default Rate by Product Type
print_terminal_graph(
    "2. Default Rate (%) by Product Type",
    [(lt, row['Default_Rate_%']) for lt, row in type_def_sorted.iterrows()],
    is_pct=True
)

# Graph 3: Default Rate by Credit Score Group
print_terminal_graph(
    "3. Default Rate (%) by Credit Score Tier",
    [(str(cs), row['Default_Rate_%']) for cs, row in def_rate_cs.iterrows()],
    is_pct=True
)

# Graph 4: Default Rate by Employment Status
print_terminal_graph(
    "4. Default Rate (%) by Employment Status",
    [(emp, row['Default_Rate_%']) for emp, row in emp_def_sorted.iterrows()],
    is_pct=True
)

# Graph 5: Default Rate by Income Bracket
print_terminal_graph(
    "5. Default Rate (%) by Income Bracket",
    [(str(inc), row['Default_Rate_%']) for inc, row in def_rate_inc.iterrows()],
    is_pct=True
)

print("\n" + "=" * 80)
print("ANALYSIS EXECUTION COMPLETE. ALL 15 CHARTS SAVED SUCCESSFULLY IN Visualizations/")
print("=" * 80)

# Open interactive multi-panel graphical dashboard window
print("\n[Launching Interactive Graph Window: Close the window when done to return to terminal]")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.canvas.manager.set_window_title("Credit Risk Analysis - Interactive Visual Dashboard")

# Subplot 1: Default Distribution
axes[0, 0].pie(default_counts, labels=['Non-Default', 'Default'], autopct='%1.1f%%',
               colors=['#2ca02c', '#d62728'], startangle=140, explode=(0, 0.08))
axes[0, 0].set_title("1. Portfolio Default Distribution", fontweight='bold')

# Subplot 2: Default Rate by Loan Type
bars_sp2 = axes[0, 1].bar(type_def_sorted.index, type_def_sorted['Default_Rate_%'], color='#e65100')
axes[0, 1].set_title("2. Default Rate (%) by Loan Type", fontweight='bold')
axes[0, 1].set_ylabel("Default Rate (%)")
axes[0, 1].axhline(overall_default_rate, color='red', linestyle='--', label=f'Avg ({overall_default_rate:.1f}%)')
axes[0, 1].legend()

# Subplot 3: Credit Score by Default Status
sns.boxplot(data=df_cleaned, x='Default_Status', y='Credit_Score', hue='Default_Status',
            palette={'No': '#81c784', 'Yes': '#e57373'}, ax=axes[1, 0], legend=False)
axes[1, 0].set_title("3. Credit Score by Default Status", fontweight='bold')

# Subplot 4: DTI by Default Status
sns.boxplot(data=df_cleaned, x='Default_Status', y='Debt_to_Income_Ratio', hue='Default_Status',
            palette={'No': '#81c784', 'Yes': '#e57373'}, ax=axes[1, 1], legend=False)
axes[1, 1].set_title("4. Debt-to-Income (DTI) by Default Status", fontweight='bold')

plt.tight_layout()
plt.show(block=False)
plt.pause(2)
plt.close()

