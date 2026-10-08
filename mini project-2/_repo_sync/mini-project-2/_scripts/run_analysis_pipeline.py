"""
Script: run_analysis_pipeline.py
Purpose: Performs end-to-end data processing, exploratory data analysis, and publication-quality
visualizations for Mini Project: Customer Churn Analysis according to project specifications.
Generates:
1. Dataset/Customer_Churn_Cleaned.csv
2. Visualizations/01_churn_distribution_pie.png through 15_powerbi_dashboard_preview.png
3. Prints exact quantitative metrics for Parts 1, 2, 3 and Business Insights
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

os.makedirs("Dataset", exist_ok=True)
os.makedirs("Visualizations", exist_ok=True)

# -------------------------------------------------------------
# PART 1: DATA LOADING
# -------------------------------------------------------------
print("=" * 60)
print("PART 1: DATA LOADING")
print("=" * 60)

raw_path = os.path.join("Dataset", "Customer_Churn_Raw.csv")
df_raw = pd.read_csv(raw_path)
print(f"Loaded Raw Dataset from {raw_path}")
print(f"Raw Shape: {df_raw.shape}")
print(f"Columns: {df_raw.columns.tolist()}")

# -------------------------------------------------------------
# PART 2: DATA EXPLORATION & CLEANING
# -------------------------------------------------------------
print("\n" + "=" * 60)
print("PART 2: DATA EXPLORATION & CLEANING")
print("=" * 60)

print("Checking duplicate records...")
num_duplicates = df_raw.duplicated().sum()
print(f"Duplicate records found: {num_duplicates}")

df_cleaned = df_raw.drop_duplicates().copy()
print(f"Shape after removing duplicates: {df_cleaned.shape}")

print("\nChecking data types and missing values in raw columns...")
print("Original Total_Charges dtype:", df_cleaned['Total_Charges'].dtype)

# In Total_Charges, empty spaces ' ' correspond to tenure = 0
spaces_count = (df_cleaned['Total_Charges'].astype(str).str.strip() == '').sum()
print(f"Whitespace / blank values in Total_Charges: {spaces_count}")

# Replace blanks with NaN, then convert to numeric
df_cleaned['Total_Charges'] = pd.to_numeric(df_cleaned['Total_Charges'].astype(str).str.strip(), errors='coerce')

# For tenure == 0, Total_Charges is legitimately 0.0
df_cleaned['Total_Charges'] = df_cleaned['Total_Charges'].fillna(0.0)
print(f"Missing values remaining in Total_Charges: {df_cleaned['Total_Charges'].isnull().sum()}")

# Map Senior_Citizen to 'No'/'Yes' for better business interpretability while retaining original in a column
df_cleaned['Senior_Citizen_Label'] = df_cleaned['Senior_Citizen'].map({0: 'No', 1: 'Yes'})

# 15. Create customer tenure groups
def assign_tenure_group(tenure):
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

df_cleaned['Tenure_Group'] = df_cleaned['Tenure_Months'].apply(assign_tenure_group)
tenure_order = ['0-12 Months', '13-24 Months', '25-36 Months', '37-48 Months', '49-60 Months', '61-72 Months']
df_cleaned['Tenure_Group'] = pd.Categorical(df_cleaned['Tenure_Group'], categories=tenure_order, ordered=True)

# Save Cleaned Dataset
cleaned_csv_path = os.path.join("Dataset", "Customer_Churn_Cleaned.csv")
df_cleaned.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned dataset saved to {cleaned_csv_path} with shape {df_cleaned.shape}")
print(f"Missing values in entire dataset: {df_cleaned.isnull().sum().sum()}")

# -------------------------------------------------------------
# PART 3: DATA ANALYSIS (Items 17 to 38)
# -------------------------------------------------------------
print("\n" + "=" * 60)
print("PART 3: DATA ANALYSIS")
print("=" * 60)

total_customers = len(df_cleaned)
total_churned = (df_cleaned['Churn'] == 'Yes').sum()
total_retained = (df_cleaned['Churn'] == 'No').sum()
overall_churn_rate = (total_churned / total_customers) * 100
avg_monthly_charges = df_cleaned['Monthly_Charges'].mean()
avg_total_charges = df_cleaned['Total_Charges'].mean()
avg_tenure = df_cleaned['Tenure_Months'].mean()

print(f"17. Total Customers: {total_customers:,}")
print(f"18. Total Churned Customers: {total_churned:,}")
print(f"19. Total Retained Customers: {total_retained:,}")
print(f"20. Overall Churn Rate: {overall_churn_rate:.2f}%")
print(f"21. Average Monthly Charges: ${avg_monthly_charges:.2f}")
print(f"22. Average Total Charges: ${avg_total_charges:.2f}")
print(f"23. Average Customer Tenure: {avg_tenure:.2f} months")

print("\n24. Customers by Gender:")
print(df_cleaned['Gender'].value_counts())

print("\n25. Customers by Contract Type:")
print(df_cleaned['Contract'].value_counts())

print("\n26. Customers by Internet Service:")
print(df_cleaned['Internet_Service'].value_counts())

print("\n27. Customers by Payment Method:")
print(df_cleaned['Payment_Method'].value_counts())

print("\n28. Churn Rate by Gender:")
churn_by_gender = df_cleaned.groupby('Gender')['Churn'].apply(lambda s: (s == 'Yes').mean() * 100)
print(churn_by_gender)

print("\n29. Churn Rate by Contract Type:")
churn_by_contract = df_cleaned.groupby('Contract')['Churn'].apply(lambda s: (s == 'Yes').mean() * 100)
print(churn_by_contract)

print("\n30. Churn Rate by Internet Service:")
churn_by_internet = df_cleaned.groupby('Internet_Service')['Churn'].apply(lambda s: (s == 'Yes').mean() * 100)
print(churn_by_internet)

print("\n31. Churn Rate by Payment Method:")
churn_by_payment = df_cleaned.groupby('Payment_Method')['Churn'].apply(lambda s: (s == 'Yes').mean() * 100)
print(churn_by_payment)

print("\n32. Churn Rate by Senior Citizen Status:")
churn_by_senior = df_cleaned.groupby('Senior_Citizen_Label')['Churn'].apply(lambda s: (s == 'Yes').mean() * 100)
print(churn_by_senior)

print("\n33. Churn Rate by Tenure Group:")
churn_by_tenure_grp = df_cleaned.groupby('Tenure_Group', observed=False)['Churn'].apply(lambda s: (s == 'Yes').mean() * 100)
print(churn_by_tenure_grp)

print("\n34. Monthly Charges Comparison (Churned vs Retained):")
charges_comp = df_cleaned.groupby('Churn')['Monthly_Charges'].agg(['mean', 'median', 'std'])
print(charges_comp)

print("\n35. Customer Tenure Comparison (Churned vs Retained):")
tenure_comp = df_cleaned.groupby('Churn')['Tenure_Months'].agg(['mean', 'median', 'std'])
print(tenure_comp)

print("\n36. Top 10 Customers by Total Charges:")
top10_customers = df_cleaned.nlargest(10, 'Total_Charges')[['Customer_ID', 'Tenure_Months', 'Contract', 'Monthly_Charges', 'Total_Charges', 'Churn']]
print(top10_customers.to_string(index=False))

# -------------------------------------------------------------
# PART 4: PYTHON VISUALIZATIONS (14 Visualizations)
# -------------------------------------------------------------
print("\n" + "=" * 60)
print("PART 4: GENERATING 14 HIGH-RESOLUTION VISUALIZATIONS")
print("=" * 60)

# Colors
COLOR_PRIMARY = "#1E3A8A"     # Deep Navy
COLOR_SECONDARY = "#0284C7"   # Sky Blue
COLOR_ACCENT = "#EF4444"      # Crimson / Red for Churn
COLOR_RETAINED = "#10B981"    # Emerald / Green for Retained
COLOR_PALETTE = ["#10B981", "#EF4444"]

# 1. Churn Distribution - Pie Chart
fig, ax = plt.subplots(figsize=(7, 6))
churn_counts = df_cleaned['Churn'].value_counts()
colors_pie = [COLOR_RETAINED, COLOR_ACCENT]
explode = (0, 0.08)
wedges, texts, autotexts = ax.pie(
    churn_counts, 
    labels=['Retained (No)', 'Churned (Yes)'], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors_pie, 
    explode=explode,
    shadow=True,
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)
for at in autotexts:
    at.set_color('white')
ax.set_title('Customer Churn Distribution', fontsize=14, fontweight='bold', pad=20, color='#0F172A')
plt.tight_layout()
plt.savefig('Visualizations/01_churn_distribution_pie.png')
plt.close()
print("Saved 01_churn_distribution_pie.png")

# 2. Customer Distribution by Contract - Bar Chart
fig, ax = plt.subplots(figsize=(8, 5))
contract_counts = df_cleaned['Contract'].value_counts()
bars = ax.bar(contract_counts.index, contract_counts.values, color=['#2563EB', '#3B82F6', '#60A5FA'], width=0.55, edgecolor='#1E3A8A', linewidth=1.2)
for bar in bars:
    height = bar.get_height()
    pct = (height / len(df_cleaned)) * 100
    ax.annotate(f'{height:,}\n({pct:.1f}%)',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1E293B')
ax.set_title('Customer Distribution by Contract Type', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Number of Customers', fontsize=11, fontweight='semibold')
ax.set_xlabel('Contract Type', fontsize=11, fontweight='semibold')
ax.set_ylim(0, max(contract_counts.values) * 1.15)
plt.tight_layout()
plt.savefig('Visualizations/02_customer_distribution_by_contract_bar.png')
plt.close()
print("Saved 02_customer_distribution_by_contract_bar.png")

# 3. Churn by Contract - Bar Chart (Churn Rate %)
fig, ax = plt.subplots(figsize=(8, 5))
contract_churn = df_cleaned.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).reindex(['Month-to-month', 'One year', 'Two year'])
bars = ax.bar(contract_churn.index, contract_churn.values, color=['#EF4444', '#F59E0B', '#10B981'], width=0.5, edgecolor='#334155', linewidth=1.2)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='#0F172A')
ax.set_title('Churn Rate by Contract Type', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
ax.set_xlabel('Contract Type', fontsize=11, fontweight='semibold')
ax.set_ylim(0, max(contract_churn.values) * 1.18)
plt.tight_layout()
plt.savefig('Visualizations/03_churn_by_contract_bar.png')
plt.close()
print("Saved 03_churn_by_contract_bar.png")

# 4. Churn by Gender - Bar Chart
fig, ax = plt.subplots(figsize=(7, 5))
gender_churn = df_cleaned.groupby('Gender')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
bars = ax.bar(gender_churn.index, gender_churn.values, color=['#3B82F6', '#EC4899'], width=0.45, edgecolor='#1E293B', linewidth=1.2)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('Churn Rate by Gender', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
ax.set_xlabel('Gender', fontsize=11, fontweight='semibold')
ax.set_ylim(0, 35)
plt.tight_layout()
plt.savefig('Visualizations/04_churn_by_gender_bar.png')
plt.close()
print("Saved 04_churn_by_gender_bar.png")

# 5. Churn by Internet Service - Bar Chart
fig, ax = plt.subplots(figsize=(8, 5))
internet_churn = df_cleaned.groupby('Internet_Service')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)
bars = ax.bar(internet_churn.index, internet_churn.values, color=['#EF4444', '#3B82F6', '#10B981'], width=0.5, edgecolor='#1E293B', linewidth=1.2)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('Churn Rate by Internet Service Type', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
ax.set_xlabel('Internet Service', fontsize=11, fontweight='semibold')
ax.set_ylim(0, max(internet_churn.values) * 1.18)
plt.tight_layout()
plt.savefig('Visualizations/05_churn_by_internet_service_bar.png')
plt.close()
print("Saved 05_churn_by_internet_service_bar.png")

# 6. Churn by Payment Method - Bar Chart
fig, ax = plt.subplots(figsize=(9, 5))
pm_churn = df_cleaned.groupby('Payment_Method')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)
bars = ax.barh(pm_churn.index, pm_churn.values, color=['#DC2626', '#F59E0B', '#3B82F6', '#10B981'], height=0.55, edgecolor='#1E293B', linewidth=1.2)
for bar in bars:
    width = bar.get_width()
    ax.annotate(f' {width:.1f}%',
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(4, 0), textcoords="offset points",
                ha='left', va='center', fontsize=10, fontweight='bold')
ax.set_title('Churn Rate by Payment Method', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
ax.set_xlim(0, max(pm_churn.values) * 1.18)
plt.tight_layout()
plt.savefig('Visualizations/06_churn_by_payment_method_bar.png')
plt.close()
print("Saved 06_churn_by_payment_method_bar.png")

# 7. Tenure Distribution - Histogram
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df_cleaned['Tenure_Months'], bins=36, kde=True, color='#2563EB', edgecolor='white', ax=ax, alpha=0.7)
ax.axvline(df_cleaned['Tenure_Months'].mean(), color='#DC2626', linestyle='--', linewidth=2, label=f'Mean: {avg_tenure:.1f} Mo')
ax.axvline(df_cleaned['Tenure_Months'].median(), color='#16A34A', linestyle='-', linewidth=2, label=f'Median: {df_cleaned["Tenure_Months"].median():.0f} Mo')
ax.set_title('Customer Tenure Distribution (Months)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Tenure (Months)', fontsize=11, fontweight='semibold')
ax.set_ylabel('Customer Count', fontsize=11, fontweight='semibold')
ax.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
plt.savefig('Visualizations/07_tenure_distribution_histogram.png')
plt.close()
print("Saved 07_tenure_distribution_histogram.png")

# 8. Monthly Charges Distribution - Histogram
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df_cleaned['Monthly_Charges'], bins=35, kde=True, color='#0284C7', edgecolor='white', ax=ax, alpha=0.7)
ax.axvline(df_cleaned['Monthly_Charges'].mean(), color='#DC2626', linestyle='--', linewidth=2, label=f'Mean: ${avg_monthly_charges:.2f}')
ax.axvline(df_cleaned['Monthly_Charges'].median(), color='#16A34A', linestyle='-', linewidth=2, label=f'Median: ${df_cleaned["Monthly_Charges"].median():.2f}')
ax.set_title('Monthly Charges Distribution ($)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Monthly Charges ($)', fontsize=11, fontweight='semibold')
ax.set_ylabel('Customer Count', fontsize=11, fontweight='semibold')
ax.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
plt.savefig('Visualizations/08_monthly_charges_distribution_histogram.png')
plt.close()
print("Saved 08_monthly_charges_distribution_histogram.png")

# 9. Tenure vs Monthly Charges - Scatter Plot
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=df_cleaned, 
    x='Tenure_Months', 
    y='Monthly_Charges', 
    hue='Churn', 
    palette={'No': '#10B981', 'Yes': '#EF4444'}, 
    alpha=0.6, 
    s=25, 
    edgecolor=None,
    ax=ax
)
ax.set_title('Customer Tenure vs Monthly Charges by Churn Status', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Tenure (Months)', fontsize=11, fontweight='semibold')
ax.set_ylabel('Monthly Charges ($)', fontsize=11, fontweight='semibold')
ax.legend(title='Churn', frameon=True, facecolor='white')
plt.tight_layout()
plt.savefig('Visualizations/09_tenure_vs_monthly_charges_scatter.png')
plt.close()
print("Saved 09_tenure_vs_monthly_charges_scatter.png")

# 10. Monthly Charges by Churn - Box Plot
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(
    data=df_cleaned, 
    x='Churn', 
    y='Monthly_Charges', 
    palette={'No': '#10B981', 'Yes': '#EF4444'}, 
    width=0.45, 
    boxprops=dict(alpha=0.85),
    ax=ax
)
med_no = df_cleaned[df_cleaned['Churn'] == 'No']['Monthly_Charges'].median()
med_yes = df_cleaned[df_cleaned['Churn'] == 'Yes']['Monthly_Charges'].median()
ax.text(0, med_no + 3, f'Median: ${med_no:.1f}', horizontalalignment='center', fontweight='bold', color='#065F46')
ax.text(1, med_yes + 3, f'Median: ${med_yes:.1f}', horizontalalignment='center', fontweight='bold', color='#991B1B')
ax.set_title('Monthly Charges Distribution by Churn Status', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Churn Status', fontsize=11, fontweight='semibold')
ax.set_ylabel('Monthly Charges ($)', fontsize=11, fontweight='semibold')
plt.tight_layout()
plt.savefig('Visualizations/10_monthly_charges_by_churn_boxplot.png')
plt.close()
print("Saved 10_monthly_charges_by_churn_boxplot.png")

# 11. Total Charges by Churn - Box Plot
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(
    data=df_cleaned, 
    x='Churn', 
    y='Total_Charges', 
    palette={'No': '#10B981', 'Yes': '#EF4444'}, 
    width=0.45, 
    boxprops=dict(alpha=0.85),
    ax=ax
)
t_med_no = df_cleaned[df_cleaned['Churn'] == 'No']['Total_Charges'].median()
t_med_yes = df_cleaned[df_cleaned['Churn'] == 'Yes']['Total_Charges'].median()
ax.text(0, t_med_no + 200, f'Median: ${t_med_no:,.0f}', horizontalalignment='center', fontweight='bold', color='#065F46')
ax.text(1, t_med_yes + 200, f'Median: ${t_med_yes:,.0f}', horizontalalignment='center', fontweight='bold', color='#991B1B')
ax.set_title('Total Charges Distribution by Churn Status', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Churn Status', fontsize=11, fontweight='semibold')
ax.set_ylabel('Total Charges ($)', fontsize=11, fontweight='semibold')
plt.tight_layout()
plt.savefig('Visualizations/11_total_charges_by_churn_boxplot.png')
plt.close()
print("Saved 11_total_charges_by_churn_boxplot.png")

# 12. Churn Rate by Tenure Group - Bar Chart
fig, ax = plt.subplots(figsize=(9, 5))
tenure_grp_churn = df_cleaned.groupby('Tenure_Group', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
colors_t = ['#DC2626', '#EA580C', '#F59E0B', '#3B82F6', '#0284C7', '#10B981']
bars = ax.bar(tenure_grp_churn.index, tenure_grp_churn.values, color=colors_t, width=0.55, edgecolor='#1E293B', linewidth=1.2)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_title('Churn Rate by Customer Tenure Group', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Churn Rate (%)', fontsize=11, fontweight='semibold')
ax.set_xlabel('Tenure Group', fontsize=11, fontweight='semibold')
ax.set_ylim(0, max(tenure_grp_churn.values) * 1.18)
plt.tight_layout()
plt.savefig('Visualizations/12_churn_rate_by_tenure_group_bar.png')
plt.close()
print("Saved 12_churn_rate_by_tenure_group_bar.png")

# 13. Service Usage - Count Plot (Key Services vs Churn)
services = ['Online_Security', 'Tech_Support', 'Online_Backup', 'Device_Protection']
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
axes = axes.flatten()

for i, srv in enumerate(services):
    sns.countplot(
        data=df_cleaned, 
        x=srv, 
        hue='Churn', 
        palette={'No': '#10B981', 'Yes': '#EF4444'}, 
        ax=axes[i],
        edgecolor='#1E293B',
        linewidth=0.8
    )
    axes[i].set_title(f'Churn by {srv.replace("_", " ")}', fontsize=11, fontweight='bold')
    axes[i].set_xlabel('')
    axes[i].set_ylabel('Customer Count', fontsize=9)
    axes[i].legend(title='Churn', frameon=True)

plt.suptitle('Customer Churn across Key Value-Added Services', fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('Visualizations/13_service_usage_countplot.png')
plt.close()
print("Saved 13_service_usage_countplot.png")

# 14. Correlation Heatmap
# Encode categorical variables for correlation heatmap
corr_df = pd.DataFrame()
corr_df['Tenure_Months'] = df_cleaned['Tenure_Months']
corr_df['Monthly_Charges'] = df_cleaned['Monthly_Charges']
corr_df['Total_Charges'] = df_cleaned['Total_Charges']
corr_df['Senior_Citizen'] = df_cleaned['Senior_Citizen']
corr_df['Partner'] = (df_cleaned['Partner'] == 'Yes').astype(int)
corr_df['Dependents'] = (df_cleaned['Dependents'] == 'Yes').astype(int)
corr_df['Phone_Service'] = (df_cleaned['Phone_Service'] == 'Yes').astype(int)
corr_df['Paperless_Billing'] = (df_cleaned['Paperless_Billing'] == 'Yes').astype(int)
corr_df['Contract_Month_to_Month'] = (df_cleaned['Contract'] == 'Month-to-month').astype(int)
corr_df['Contract_Two_Year'] = (df_cleaned['Contract'] == 'Two year').astype(int)
corr_df['Internet_Fiber'] = (df_cleaned['Internet_Service'] == 'Fiber optic').astype(int)
corr_df['Payment_Electronic_Check'] = (df_cleaned['Payment_Method'] == 'Electronic check').astype(int)
corr_df['Churn'] = (df_cleaned['Churn'] == 'Yes').astype(int)

fig, ax = plt.subplots(figsize=(10, 8))
corr_matrix = corr_df.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(
    corr_matrix, 
    annot=True, 
    fmt='.2f', 
    cmap='coolwarm', 
    vmin=-0.6, 
    vmax=0.6, 
    linewidths=0.5, 
    mask=mask,
    cbar_kws={'shrink': 0.8},
    ax=ax
)
ax.set_title('Correlation Heatmap: Demographics, Services, Billing & Churn', fontsize=13, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(fontsize=9)
plt.tight_layout()
plt.savefig('Visualizations/14_correlation_heatmap.png')
plt.close()
print("Saved 14_correlation_heatmap.png")

# 15. Power BI Dashboard Layout Preview
fig = plt.figure(figsize=(16, 9), facecolor='#0F172A')
gs = fig.add_gridspec(6, 6, hspace=0.45, wspace=0.35, left=0.04, right=0.96, top=0.92, bottom=0.05)

# Header Title
fig.text(0.04, 0.95, "CUSTOMER CHURN & RETENTION ANALYTICS DASHBOARD", fontsize=18, fontweight='bold', color='#FFFFFF')
fig.text(0.68, 0.95, "Power BI Executive Report | Telecom Analytics Division", fontsize=11, color='#94A3B8')

# Row 0: 6 KPI Cards
kpis = [
    ("TOTAL CUSTOMERS", f"{total_customers:,}", "#38BDF8"),
    ("CHURNED CUSTOMERS", f"{total_churned:,}", "#F87171"),
    ("RETAINED CUSTOMERS", f"{total_retained:,}", "#34D399"),
    ("CHURN RATE %", f"{overall_churn_rate:.2f}%", "#FB923C"),
    ("AVG MONTHLY CHARGE", f"${avg_monthly_charges:.2f}", "#A78BFA"),
    ("AVG TENURE", f"{avg_tenure:.1f} Mo", "#FBBF24")
]

for col_idx, (title, val, color) in enumerate(kpis):
    ax_kpi = fig.add_subplot(gs[0, col_idx])
    ax_kpi.set_facecolor('#1E293B')
    ax_kpi.text(0.5, 0.65, val, fontsize=16, fontweight='bold', color=color, ha='center', va='center')
    ax_kpi.text(0.5, 0.25, title, fontsize=8, fontweight='bold', color='#94A3B8', ha='center', va='center')
    ax_kpi.set_xticks([])
    ax_kpi.set_yticks([])
    for spine in ax_kpi.spines.values():
        spine.set_color('#334155')

# Visual 1: Churn Donut (Row 1-2, Col 0-1)
ax1 = fig.add_subplot(gs[1:3, 0:2])
ax1.set_facecolor('#1E293B')
wedges, _, _ = ax1.pie(churn_counts, colors=['#10B981', '#EF4444'], autopct='%1.1f%%',
                       pctdistance=0.75, startangle=90, textprops={'color': 'white', 'fontsize': 8, 'weight': 'bold'},
                       wedgeprops=dict(width=0.45, edgecolor='#0F172A'))
ax1.set_title("1. Churn Distribution", color='#F1F5F9', fontsize=10, fontweight='bold', pad=8)

# Visual 2: Churn Rate by Contract (Row 1-2, Col 2-3)
ax2 = fig.add_subplot(gs[1:3, 2:4])
ax2.set_facecolor('#1E293B')
bars2 = ax2.bar(contract_churn.index, contract_churn.values, color=['#EF4444', '#F59E0B', '#10B981'], width=0.45)
for b in bars2:
    ax2.annotate(f"{b.get_height():.1f}%", (b.get_x() + b.get_width()/2, b.get_height()),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color='white', fontsize=8, weight='bold')
ax2.set_title("2. Churn Rate by Contract", color='#F1F5F9', fontsize=10, fontweight='bold')
ax2.tick_params(colors='#94A3B8', labelsize=7)
ax2.set_ylim(0, 50)
for spine in ax2.spines.values(): spine.set_color('#334155')

# Visual 3: Churn Rate by Internet Service (Row 1-2, Col 4-5)
ax3 = fig.add_subplot(gs[1:3, 4:6])
ax3.set_facecolor('#1E293B')
bars3 = ax3.bar(internet_churn.index, internet_churn.values, color=['#EF4444', '#38BDF8', '#10B981'], width=0.45)
for b in bars3:
    ax3.annotate(f"{b.get_height():.1f}%", (b.get_x() + b.get_width()/2, b.get_height()),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color='white', fontsize=8, weight='bold')
ax3.set_title("3. Churn Rate by Internet Service", color='#F1F5F9', fontsize=10, fontweight='bold')
ax3.tick_params(colors='#94A3B8', labelsize=7)
ax3.set_ylim(0, 50)
for spine in ax3.spines.values(): spine.set_color('#334155')

# Visual 4: Churn Rate by Payment Method (Row 3-4, Col 0-2)
ax4 = fig.add_subplot(gs[3:5, 0:2])
ax4.set_facecolor('#1E293B')
bars4 = ax4.barh(pm_churn.index, pm_churn.values, color=['#DC2626', '#F59E0B', '#38BDF8', '#10B981'], height=0.45)
for b in bars4:
    ax4.annotate(f" {b.get_width():.1f}%", (b.get_width(), b.get_y() + b.get_height()/2),
                 xytext=(2, 0), textcoords="offset points", ha='left', va='center', color='white', fontsize=7, weight='bold')
ax4.set_title("4. Churn Rate by Payment Method", color='#F1F5F9', fontsize=10, fontweight='bold')
ax4.tick_params(colors='#94A3B8', labelsize=7)
ax4.set_xlim(0, 55)
for spine in ax4.spines.values(): spine.set_color('#334155')

# Visual 5: Customer Count by Tenure Group (Row 3-4, Col 2-4)
ax5 = fig.add_subplot(gs[3:5, 2:4])
ax5.set_facecolor('#1E293B')
t_counts = df_cleaned['Tenure_Group'].value_counts().loc[tenure_order]
bars5 = ax5.bar(range(len(t_counts)), t_counts.values, color='#0284C7', width=0.5)
ax5.set_xticks(range(len(t_counts)))
ax5.set_xticklabels([f"T{i+1}" for i in range(len(t_counts))], fontsize=8, color='#94A3B8')
for b in bars5:
    ax5.annotate(f"{b.get_height():,}", (b.get_x() + b.get_width()/2, b.get_height()),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color='white', fontsize=7, weight='bold')
ax5.set_title("5. Customers by Tenure Group (T1=0-12m)", color='#F1F5F9', fontsize=10, fontweight='bold')
ax5.tick_params(colors='#94A3B8', labelsize=7)
ax5.set_ylim(0, max(t_counts.values)*1.18)
for spine in ax5.spines.values(): spine.set_color('#334155')

# Visual 6 & 8: Contract & Gender Distributions (Row 3-4, Col 4-6)
ax6 = fig.add_subplot(gs[3:5, 4:6])
ax6.set_facecolor('#1E293B')
g_counts = df_cleaned['Gender'].value_counts()
ax6.bar(g_counts.index, g_counts.values, color=['#38BDF8', '#EC4899'], width=0.45)
for b in ax6.patches:
    ax6.annotate(f"{b.get_height():,}", (b.get_x() + b.get_width()/2, b.get_height()),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color='white', fontsize=8, weight='bold')
ax6.set_title("8. Customer Distribution by Gender", color='#F1F5F9', fontsize=10, fontweight='bold')
ax6.tick_params(colors='#94A3B8', labelsize=8)
for spine in ax6.spines.values(): spine.set_color('#334155')

# Visual 9 & 10: Slicers Bar & Bottom Status (Row 5, Col 0-6)
ax_bottom = fig.add_subplot(gs[5, :])
ax_bottom.set_facecolor('#1E293B')
slicers_info = "[SLICERS ACTIVE: Gender (All) | Contract (All) | Internet (All) | Payment (All) | Senior (All) | Churn (All)]"
ax_bottom.text(0.02, 0.65, slicers_info, color='#38BDF8', fontsize=8, weight='bold')
details_info = f"10. Customer Details Table Matrix: 7,043 Customer Records | Churned: {total_churned:,} | Monthly Charges: ${df_cleaned['Monthly_Charges'].sum():,.2f} | Total Value: ${df_cleaned['Total_Charges'].sum():,.2f}"
ax_bottom.text(0.02, 0.25, details_info, color='#94A3B8', fontsize=8)
ax_bottom.set_xticks([])
ax_bottom.set_yticks([])
for spine in ax_bottom.spines.values(): spine.set_color('#334155')

plt.savefig('Visualizations/15_powerbi_dashboard_preview.png', dpi=300)
plt.close()
print("Saved 15_powerbi_dashboard_preview.png")

print("\nAll pipeline tasks executed successfully!")
