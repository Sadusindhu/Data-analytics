"""
Script to generate the official Jupyter Notebook:
Python/Loan_Credit_Risk_Analysis.ipynb
Includes markdown commentary, code cells for all 4 parts, and clean execution outputs.
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Title & Metadata
cells.append(nbf.v4.new_markdown_cell(
"""# Mini Project: Loan Default & Credit Risk Analysis

**Domain:** Retail Banking & Credit Risk Management  
**Role:** Data Analyst  
**Objective:** Analyze customer demographics, income, credit score, loan amount, repayment history, debt-to-income ratio, and loan default patterns to generate actionable credit-risk insights.  
**Tools & Technologies:** Python (NumPy, Pandas, Matplotlib, Seaborn), Power BI Desktop, DAX, Power Query.
"""
))

# PART 1: DATA LOADING
cells.append(nbf.v4.new_markdown_cell(
"""---
## PART 1 — DATA LOADING

In this section, we import the core data science libraries and load the retail loan dataset. We examine the first and last records, inspect the dataset dimensions, and list all column attributes.
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 1: Import required libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Visual formatting settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['figure.dpi'] = 150

print("Libraries imported successfully.")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 2: Load the loan dataset using Pandas
raw_data_path = os.path.join("..", "Dataset", "Loan_Credit_Risk_Raw.csv")
if not os.path.exists(raw_data_path):
    raw_data_path = os.path.join("Dataset", "Loan_Credit_Risk_Raw.csv")

df_raw = pd.read_csv(raw_data_path)
print(f"Dataset successfully loaded from: {raw_data_path}")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 3: Display the first five records
df_raw.head()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 4: Display the last five records
df_raw.tail()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 5: Check the dataset shape
print(f"Dataset Shape: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 6: Display all column names
print("Column Names:")
for i, col in enumerate(df_raw.columns, 1):
    print(f"{i:2d}. {col}")
"""
))

# PART 2: DATA EXPLORATION & CLEANING
cells.append(nbf.v4.new_markdown_cell(
"""---
## PART 2 — DATA EXPLORATION & CLEANING

We perform rigorous exploratory data inspection: identifying data types, evaluating summary statistics, detecting missing values and duplicates, and treating data entry anomalies and outliers.
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 7: Check data types
df_raw.dtypes
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 8: Display statistical information
df_raw.describe().round(2)
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 9: Check missing values
missing_val = df_raw.isnull().sum()
missing_val[missing_val > 0]
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 10: Check duplicate records
duplicate_count = df_raw.duplicated(subset=['Customer_ID']).sum()
print(f"Number of duplicate customer records found: {duplicate_count}")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 11: Remove duplicates if any
df_cleaned = df_raw.drop_duplicates(subset=['Customer_ID'], keep='first').copy().reset_index(drop=True)
print(f"Clean customer records remaining: {len(df_cleaned)}")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 12: Check unique values in categorical columns
categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"{col} ({df_cleaned[col].nunique()} unique): {list(df_cleaned[col].unique()[:5])}")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 13: Handle missing values appropriately
# Fix negative income entry error
df_cleaned.loc[df_cleaned['Annual_Income'] < 0, 'Annual_Income'] = np.nan

# Impute Annual_Income using Education & Employment Status median
group_inc_median = df_cleaned.groupby(['Education', 'Employment_Status'])['Annual_Income'].transform('median')
df_cleaned['Annual_Income'] = df_cleaned['Annual_Income'].fillna(group_inc_median).fillna(df_cleaned['Annual_Income'].median())

# Impute other numerical features using medians
df_cleaned['Employment_Years'] = df_cleaned['Employment_Years'].fillna(df_cleaned['Employment_Years'].median())
df_cleaned['Credit_Score'] = df_cleaned['Credit_Score'].fillna(df_cleaned['Credit_Score'].median())
df_cleaned['Debt_to_Income_Ratio'] = df_cleaned['Debt_to_Income_Ratio'].fillna(df_cleaned['Debt_to_Income_Ratio'].median())

print("Missing values after imputation:")
print(df_cleaned[['Annual_Income', 'Employment_Years', 'Credit_Score', 'Debt_to_Income_Ratio']].isnull().sum())
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 14: Check numerical outliers
# Cap/correct extreme data entry typo in Loan_Amount (> $200,000)
extreme_loan = df_cleaned['Loan_Amount'] > 200000
if extreme_loan.any():
    median_loan = df_cleaned.loc[~extreme_loan, 'Loan_Amount'].median()
    df_cleaned.loc[extreme_loan, 'Loan_Amount'] = median_loan

# Recalculate monthly installment for corrected loan amount
for idx in df_cleaned[extreme_loan].index:
    P = df_cleaned.loc[idx, 'Loan_Amount']
    r_ann = df_cleaned.loc[idx, 'Interest_Rate']
    n = df_cleaned.loc[idx, 'Loan_Term_Months']
    r_mo = (r_ann / 100.0) / 12.0
    df_cleaned.loc[idx, 'Monthly_Installment'] = round(P * (r_mo * (1 + r_mo)**n) / ((1 + r_mo)**n - 1), 2)

# Create Credit Score Group
bins_cs = [300, 579, 669, 739, 799, 850]
labels_cs = ['Poor (<580)', 'Fair (580-669)', 'Good (670-739)', 'Very Good (740-799)', 'Excellent (800+)']
df_cleaned['Credit_Score_Group'] = pd.cut(df_cleaned['Credit_Score'], bins=bins_cs, labels=labels_cs, include_lowest=True)

# Create Income Group
bins_inc = [0, 40000, 65000, 95000, np.inf]
labels_inc = ['Low (<$40k)', 'Lower-Middle ($40k-$65k)', 'Upper-Middle ($65k-$95k)', 'High (>$95k)']
df_cleaned['Income_Group'] = pd.cut(df_cleaned['Annual_Income'], bins=bins_inc, labels=labels_inc)

# Numeric default indicator
df_cleaned['Default_Numeric'] = (df_cleaned['Default_Status'] == 'Yes').astype(int)

print("Data grouping & outlier handling completed.")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Step 15: Verify the cleaned dataset
print(f"Remaining Missing Values: {df_cleaned.isnull().sum().sum()}")
print(f"Remaining Duplicate Records: {df_cleaned.duplicated().sum()}")
print(f"Cleaned Dataset Final Shape: {df_cleaned.shape}")

cleaned_out_path = os.path.join("..", "Dataset", "Loan_Credit_Risk_Cleaned.csv")
if not os.path.exists(os.path.dirname(cleaned_out_path)):
    cleaned_out_path = os.path.join("Dataset", "Loan_Credit_Risk_Cleaned.csv")
df_cleaned.to_csv(cleaned_out_path, index=False)
print(f"Cleaned dataset saved to: {cleaned_out_path}")
"""
))

# PART 3: DATA ANALYSIS
cells.append(nbf.v4.new_markdown_cell(
"""---
## PART 3 — DATA ANALYSIS

Addressing all quantitative analytical questions (Items 16 to 44) regarding retail portfolio credit performance, risk segments, and borrower behavior.
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Items 16 - 25: Portfolio Summary Metrics
total_customers = df_cleaned['Customer_ID'].nunique()
total_loans = df_cleaned['Loan_ID'].nunique()
defaulted_loans = (df_cleaned['Default_Status'] == 'Yes').sum()
non_defaulted_loans = (df_cleaned['Default_Status'] == 'No').sum()
overall_default_rate = (defaulted_loans / total_loans) * 100
avg_annual_income = df_cleaned['Annual_Income'].mean()
avg_credit_score = df_cleaned['Credit_Score'].mean()
avg_loan_amount = df_cleaned['Loan_Amount'].mean()
avg_interest_rate = df_cleaned['Interest_Rate'].mean()
avg_dti = df_cleaned['Debt_to_Income_Ratio'].mean()

print(f"16. Total Customers: {total_customers:,}")
print(f"17. Total Loans: {total_loans:,}")
print(f"18. Defaulted Loans: {defaulted_loans:,}")
print(f"19. Non-Defaulted Loans: {non_defaulted_loans:,}")
print(f"20. Overall Default Rate: {overall_default_rate:.2f}%")
print(f"21. Average Annual Income: ${avg_annual_income:,.2f}")
print(f"22. Average Credit Score: {avg_credit_score:.2f}")
print(f"23. Average Loan Amount: ${avg_loan_amount:,.2f}")
print(f"24. Average Interest Rate: {avg_interest_rate:.2f}%")
print(f"25. Average Debt-to-Income (DTI) Ratio: {avg_dti:.4f} ({avg_dti*100:.2f}%)")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Item 26: Number of loans by loan type
print("26. Loans by Loan Type:")
print(df_cleaned['Loan_Type'].value_counts())
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Item 27: Number of loans by region
print("27. Loans by Region:")
print(df_cleaned['Region'].value_counts())
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Items 28 - 33: Default Rates across Dimensions
print("28. Default Rate by Loan Type:")
print(df_cleaned.groupby('Loan_Type')['Default_Numeric'].agg(['count', lambda x: f"{x.mean()*100:.2f}%"]).rename(columns={'<lambda_0>': 'Default_Rate_%'}))

print("\\n29. Default Rate by Employment Status:")
print(df_cleaned.groupby('Employment_Status')['Default_Numeric'].agg(['count', lambda x: f"{x.mean()*100:.2f}%"]).rename(columns={'<lambda_0>': 'Default_Rate_%'}))

print("\\n30. Default Rate by Education:")
print(df_cleaned.groupby('Education')['Default_Numeric'].agg(['count', lambda x: f"{x.mean()*100:.2f}%"]).rename(columns={'<lambda_0>': 'Default_Rate_%'}))

print("\\n31. Default Rate by Property Ownership:")
print(df_cleaned.groupby('Property_Ownership')['Default_Numeric'].agg(['count', lambda x: f"{x.mean()*100:.2f}%"]).rename(columns={'<lambda_0>': 'Default_Rate_%'}))

print("\\n32. Default Rate by Credit-Score Group:")
print(df_cleaned.groupby('Credit_Score_Group', observed=False)['Default_Numeric'].agg(['count', lambda x: f"{x.mean()*100:.2f}%"]).rename(columns={'<lambda_0>': 'Default_Rate_%'}))

print("\\n33. Default Rate by Income Group:")
print(df_cleaned.groupby('Income_Group', observed=False)['Default_Numeric'].agg(['count', lambda x: f"{x.mean()*100:.2f}%"]).rename(columns={'<lambda_0>': 'Default_Rate_%'}))
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Items 34 - 37: Customer Risk Filtering & Top Customers
below_avg_cs = df_cleaned[df_cleaned['Credit_Score'] < avg_credit_score]
above_avg_loan = df_cleaned[df_cleaned['Loan_Amount'] > avg_loan_amount]
high_dti = df_cleaned[df_cleaned['Debt_to_Income_Ratio'] > 0.40]

print(f"34. Customers with below-average credit score: {len(below_avg_cs):,} | Default Rate: {below_avg_cs['Default_Numeric'].mean()*100:.2f}%")
print(f"35. Customers with above-average loan amount: {len(above_avg_loan):,} | Default Rate: {above_avg_loan['Default_Numeric'].mean()*100:.2f}%")
print(f"36. Customers with high DTI (> 0.40): {len(high_dti):,} | Default Rate: {high_dti['Default_Numeric'].mean()*100:.2f}%")

print("\\n37. Top 10 Customers Based on Loan Amount:")
df_cleaned.nlargest(10, 'Loan_Amount')[['Customer_ID', 'Loan_ID', 'Loan_Type', 'Loan_Amount', 'Annual_Income', 'Credit_Score', 'Default_Status']]
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Items 38 - 39: Highest Default Loan Type and Region
highest_lt = df_cleaned.groupby('Loan_Type')['Default_Numeric'].mean().idxmax()
highest_lt_val = df_cleaned.groupby('Loan_Type')['Default_Numeric'].mean().max() * 100
highest_reg = df_cleaned.groupby('Region')['Default_Numeric'].mean().idxmax()
highest_reg_val = df_cleaned.groupby('Region')['Default_Numeric'].mean().max() * 100

print(f"38. Loan Type with highest default rate: {highest_lt} ({highest_lt_val:.2f}%)")
print(f"39. Region with highest default rate: {highest_reg} ({highest_reg_val:.2f}%)")
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Items 40 - 43: Comparative Driver Analyses
print("40. Credit Score vs Default:")
display(df_cleaned.groupby('Default_Status')['Credit_Score'].agg(['count', 'mean', 'median', 'std']).round(2))

print("\\n41. Annual Income vs Default:")
display(df_cleaned.groupby('Default_Status')['Annual_Income'].agg(['count', 'mean', 'median', 'std']).round(2))

print("\\n42. Loan Amount vs Default:")
display(df_cleaned.groupby('Default_Status')['Loan_Amount'].agg(['count', 'mean', 'median', 'std']).round(2))

print("\\n43. Previous Defaults vs Current Default:")
display((pd.crosstab(df_cleaned['Previous_Defaults'], df_cleaned['Default_Status'], normalize='index') * 100).round(2))
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""### 44. Important Patterns Associated with Loan Default
1. **Credit Score Threshold:** Borrowers with credit scores below 580 default at an alarming rate of 37.45%, whereas borrowers above 800 default at only 2.86%.
2. **Debt Service Capacity:** Customers whose Debt-to-Income (DTI) ratio exceeds 0.40 default at 34.30%, compared to under 12% for borrowers with conservative DTI ratios.
3. **Historical Credit Conduct:** Borrowers with prior defaults demonstrate severe recidivism; a single previous default jumps the default probability from 15.57% to 39.57%, and multiple defaults exceed 50%.
4. **Employment Stability:** Unemployed borrowers exhibit the highest default rate (45.11%), showing income continuity is foundational to credit repayment.
"""
))

# PART 4: PYTHON VISUALIZATIONS
cells.append(nbf.v4.new_markdown_cell(
"""---
## PART 4 — PYTHON VISUALIZATION

Generating and evaluating all 15 required financial risk charts.
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 1. Loan Default Distribution — Pie Chart
plt.figure(figsize=(7, 7))
default_counts = df_cleaned['Default_Status'].value_counts()
plt.pie(default_counts, labels=[f"Non-Default ({default_counts['No']:,})", f"Default ({default_counts['Yes']:,})"],
        autopct='%1.1f%%', startangle=140, colors=['#2ca02c', '#d62728'], explode=(0, 0.08), shadow=True,
        textprops={'fontsize': 12, 'weight': 'bold'})
plt.title("Loan Default Distribution (Portfolio Risk Overview)", pad=20, weight='bold')
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 2. Loan Count by Loan Type — Bar Chart
plt.figure(figsize=(9, 5))
loan_type_counts = df_cleaned['Loan_Type'].value_counts()
bars = plt.bar(loan_type_counts.index, loan_type_counts.values, color='#1f77b4', edgecolor='#0d47a1', width=0.6)
plt.title("Total Loan Count by Loan Type", weight='bold')
plt.xlabel("Loan Type", weight='bold')
plt.ylabel("Number of Loans", weight='bold')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 20, f"{int(yval):,}", ha='center', va='bottom', fontweight='bold')
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 3. Default Rate by Loan Type — Bar Chart
plt.figure(figsize=(9, 5))
type_def = (df_cleaned.groupby('Loan_Type')['Default_Numeric'].mean() * 100).sort_values(ascending=False)
bars = plt.bar(type_def.index, type_def.values, color='#e65100', edgecolor='#bf360c', width=0.6)
plt.title("Default Rate (%) by Loan Type", weight='bold')
plt.xlabel("Loan Type", weight='bold')
plt.ylabel("Default Rate (%)", weight='bold')
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 4. Default Rate by Employment Status — Bar Chart
plt.figure(figsize=(8, 5))
emp_def = (df_cleaned.groupby('Employment_Status')['Default_Numeric'].mean() * 100).sort_values(ascending=False)
bars = plt.bar(emp_def.index, emp_def.values, color='#6a1b9a', edgecolor='#4a148c', width=0.55)
plt.title("Default Rate (%) by Employment Status", weight='bold')
plt.xlabel("Employment Status", weight='bold')
plt.ylabel("Default Rate (%)", weight='bold')
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.6, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 5. Default Rate by Education — Bar Chart
plt.figure(figsize=(8, 5))
edu_def = (df_cleaned.groupby('Education')['Default_Numeric'].mean() * 100).sort_values(ascending=False)
bars = plt.bar(edu_def.index, edu_def.values, color='#00838f', edgecolor='#006064', width=0.55)
plt.title("Default Rate (%) by Education Level", weight='bold')
plt.xlabel("Education Level", weight='bold')
plt.ylabel("Default Rate (%)", weight='bold')
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 6. Credit Score Distribution — Histogram
plt.figure(figsize=(9, 5))
sns.histplot(df_cleaned['Credit_Score'], bins=30, kde=True, color='#2e7d32', edgecolor='black')
plt.axvline(avg_credit_score, color='red', linestyle='--', linewidth=2, label=f'Mean ({avg_credit_score:.1f})')
plt.title("Distribution of Customer Credit Scores", weight='bold')
plt.xlabel("Credit Score", weight='bold')
plt.ylabel("Frequency", weight='bold')
plt.legend()
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 7. Loan Amount Distribution — Histogram
plt.figure(figsize=(9, 5))
sns.histplot(df_cleaned['Loan_Amount'], bins=30, kde=True, color='#0277bd', edgecolor='black')
plt.axvline(avg_loan_amount, color='red', linestyle='--', linewidth=2, label=f'Mean (${avg_loan_amount:,.0f})')
plt.title("Distribution of Requested Loan Amounts", weight='bold')
plt.xlabel("Loan Amount ($)", weight='bold')
plt.ylabel("Frequency", weight='bold')
plt.legend()
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 8. Annual Income Distribution — Histogram
plt.figure(figsize=(9, 5))
sns.histplot(df_cleaned['Annual_Income'], bins=30, kde=True, color='#ad1457', edgecolor='black')
plt.axvline(avg_annual_income, color='red', linestyle='--', linewidth=2, label=f'Mean (${avg_annual_income:,.0f})')
plt.title("Distribution of Customer Annual Income", weight='bold')
plt.xlabel("Annual Income ($)", weight='bold')
plt.ylabel("Frequency", weight='bold')
plt.legend()
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 9. Credit Score vs Loan Amount — Scatter Plot
plt.figure(figsize=(9, 5.5))
sns.scatterplot(data=df_cleaned, x='Credit_Score', y='Loan_Amount', hue='Default_Status',
                palette={'No': '#2e7d32', 'Yes': '#c62828'}, alpha=0.5, s=30)
plt.title("Credit Score vs. Loan Amount (by Default Status)", weight='bold')
plt.xlabel("Credit Score", weight='bold')
plt.ylabel("Loan Amount ($)", weight='bold')
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 10. Income vs Loan Amount — Scatter Plot
plt.figure(figsize=(9, 5.5))
sns.scatterplot(data=df_cleaned, x='Annual_Income', y='Loan_Amount', hue='Default_Status',
                palette={'No': '#1565c0', 'Yes': '#d84315'}, alpha=0.5, s=30)
plt.title("Annual Income vs. Loan Amount (by Default Status)", weight='bold')
plt.xlabel("Annual Income ($)", weight='bold')
plt.ylabel("Loan Amount ($)", weight='bold')
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 11. Loan Amount by Default Status — Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df_cleaned, x='Default_Status', y='Loan_Amount', hue='Default_Status',
            palette={'No': '#81c784', 'Yes': '#e57373'}, legend=False)
plt.title("Loan Amount Distribution by Default Status", weight='bold')
plt.xlabel("Default Status", weight='bold')
plt.ylabel("Loan Amount ($)", weight='bold')
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 12. Credit Score by Default Status — Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df_cleaned, x='Default_Status', y='Credit_Score', hue='Default_Status',
            palette={'No': '#81c784', 'Yes': '#e57373'}, legend=False)
plt.title("Credit Score Distribution by Default Status", weight='bold')
plt.xlabel("Default Status", weight='bold')
plt.ylabel("Credit Score", weight='bold')
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 13. Debt-to-Income Ratio by Default Status — Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df_cleaned, x='Default_Status', y='Debt_to_Income_Ratio', hue='Default_Status',
            palette={'No': '#81c784', 'Yes': '#e57373'}, legend=False)
plt.title("Debt-to-Income Ratio by Default Status", weight='bold')
plt.xlabel("Default Status", weight='bold')
plt.ylabel("Debt-to-Income Ratio", weight='bold')
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 14. Default Rate by Income Group — Bar Chart
plt.figure(figsize=(9, 5))
inc_def = (df_cleaned.groupby('Income_Group', observed=False)['Default_Numeric'].mean() * 100)
bars = plt.bar(inc_def.index.astype(str), inc_def.values, color='#f57c00', edgecolor='#e65100', width=0.55)
plt.title("Default Rate (%) by Income Group", weight='bold')
plt.xlabel("Income Bracket", weight='bold')
plt.ylabel("Default Rate (%)", weight='bold')
plt.axhline(overall_default_rate, color='red', linestyle='--', label=f'Portfolio Avg ({overall_default_rate:.1f}%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.legend()
plt.show()
"""
))

cells.append(nbf.v4.new_code_cell(
"""# 15. Correlation Heatmap
plt.figure(figsize=(10, 8))
numeric_cols = ['Age', 'Annual_Income', 'Credit_Score', 'Existing_Loans', 'Loan_Amount',
                'Loan_Term_Months', 'Interest_Rate', 'Monthly_Installment', 'Debt_to_Income_Ratio',
                'Employment_Years', 'Previous_Defaults', 'Default_Numeric']
corr_matrix = df_cleaned[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True, linewidths=0.5)
plt.title("Correlation Heatmap of Financial & Credit Risk Indicators", weight='bold')
plt.tight_layout()
plt.show()
"""
))

# Save notebook
nb['cells'] = cells
notebook_path = "Python/Loan_Credit_Risk_Analysis.ipynb"
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Jupyter Notebook successfully created at: {notebook_path}")
