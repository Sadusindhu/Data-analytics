"""
Script: generate_raw_dataset.py
Purpose: Generates a realistic financial retail loan dataset for Credit Risk & Loan Default Analysis.
Includes authentic banking distributions, risk relationships, and realistic imperfections (missing values, duplicates, outliers)
to thoroughly demonstrate data cleaning and preparation.
"""

import numpy as np
import pandas as pd

def generate_loan_dataset(n_records=5000, random_state=42):
    np.random.seed(random_state)
    
    # 1. Customer Demographics
    cust_ids = [f"CUST-{1000 + i}" for i in range(1, n_records + 1)]
    genders = np.random.choice(["Male", "Female"], size=n_records, p=[0.53, 0.47])
    ages = np.random.randint(21, 68, size=n_records)
    
    educations = np.random.choice(
        ["High School", "Bachelor", "Master", "PhD"],
        size=n_records,
        p=[0.25, 0.48, 0.21, 0.06]
    )
    
    employment_statuses = np.random.choice(
        ["Employed", "Self-Employed", "Unemployed"],
        size=n_records,
        p=[0.70, 0.22, 0.08]
    )
    
    marital_statuses = np.random.choice(
        ["Married", "Single", "Divorced"],
        size=n_records,
        p=[0.52, 0.35, 0.13]
    )
    
    dependents = np.random.choice([0, 1, 2, 3, 4], size=n_records, p=[0.42, 0.26, 0.20, 0.09, 0.03])
    
    # Employment Years roughly proportional to age
    max_exp = np.maximum(0, ages - 20)
    employment_years = np.array([
        0 if emp == "Unemployed" else int(np.random.uniform(0.5, max(1, m * 0.85)))
        for emp, m in zip(employment_statuses, max_exp)
    ])
    
    # Annual Income (log-normal, skewed with respect to education and employment)
    base_income = np.random.lognormal(mean=11.0, sigma=0.45, size=n_records) # median ~60k
    edu_multiplier = {"High School": 0.82, "Bachelor": 1.05, "Master": 1.30, "PhD": 1.55}
    emp_multiplier = {"Employed": 1.0, "Self-Employed": 1.15, "Unemployed": 0.35}
    
    annual_income = np.array([
        round(base_income[i] * edu_multiplier[educations[i]] * emp_multiplier[employment_statuses[i]], -2)
        for i in range(n_records)
    ])
    annual_income = np.clip(annual_income, 18000, 220000)
    
    # Credit Score (300 to 850)
    # Younger or unemployed or previously defaulted tend to have lower scores
    base_credit = np.random.normal(loc=670, scale=85, size=n_records)
    credit_scores = np.clip(base_credit, 300, 850).astype(int)
    
    existing_loans = np.random.choice([0, 1, 2, 3, 4, 5], size=n_records, p=[0.28, 0.32, 0.22, 0.12, 0.04, 0.02])
    
    # 2. Loan Specifics
    loan_ids = [f"LN-2023-{10000 + i}" for i in range(1, n_records + 1)]
    loan_types = np.random.choice(
        ["Personal", "Home", "Auto", "Education", "Business"],
        size=n_records,
        p=[0.30, 0.24, 0.22, 0.14, 0.10]
    )
    
    # Loan Amount depending on Loan Type
    loan_amounts = []
    for l_type, inc in zip(loan_types, annual_income):
        if l_type == "Home":
            amt = np.random.uniform(45000, 130000)
        elif l_type == "Business":
            amt = np.random.uniform(20000, 90000)
        elif l_type == "Auto":
            amt = np.random.uniform(10000, 48000)
        elif l_type == "Education":
            amt = np.random.uniform(6000, 40000)
        else: # Personal
            amt = np.random.uniform(3000, 32000)
        loan_amounts.append(round(amt, -2))
    loan_amounts = np.array(loan_amounts)
    
    loan_terms = np.random.choice([12, 24, 36, 48, 60], size=n_records, p=[0.12, 0.20, 0.36, 0.18, 0.14])
    
    # Interest Rate based on Credit Score and Loan Type
    # Lower credit score -> higher interest rate (Risk-based pricing)
    interest_rates = []
    for cs, lt in zip(credit_scores, loan_types):
        base_rate = 14.5 - (cs - 650) * 0.022
        if lt == "Home":
            base_rate -= 2.5
        elif lt == "Business":
            base_rate += 1.8
        elif lt == "Personal":
            base_rate += 2.0
        elif lt == "Auto":
            base_rate -= 0.5
        noise = np.random.normal(0, 0.7)
        rate = np.clip(base_rate + noise, 5.5, 24.5)
        interest_rates.append(round(rate, 2))
    interest_rates = np.array(interest_rates)
    
    # Monthly Installment Calculation (Standard Amortization Formula)
    monthly_installments = []
    for P, r_ann, n in zip(loan_amounts, interest_rates, loan_terms):
        r_mo = (r_ann / 100.0) / 12.0
        if r_mo > 0:
            pmt = P * (r_mo * (1 + r_mo)**n) / ((1 + r_mo)**n - 1)
        else:
            pmt = P / n
        monthly_installments.append(round(pmt, 2))
    monthly_installments = np.array(monthly_installments)
    
    # Monthly Income
    monthly_income = annual_income / 12.0
    
    # Debt-to-Income Ratio (DTI)
    # Existing non-housing debt payment + new installment / monthly income
    existing_debt_payments = existing_loans * np.random.uniform(100, 280, size=n_records)
    total_monthly_debt = existing_debt_payments + monthly_installments
    dti_ratios = np.round(total_monthly_debt / monthly_income, 3)
    dti_ratios = np.clip(dti_ratios, 0.08, 0.75)
    
    # Previous Defaults
    # Higher for lower credit scores
    prev_defaults_prob = np.where(credit_scores < 580, 0.38, np.where(credit_scores < 680, 0.14, 0.03))
    has_prev_default = np.random.binomial(1, prev_defaults_prob)
    prev_defaults = np.where(has_prev_default == 1, np.random.choice([1, 2, 3], size=n_records, p=[0.72, 0.21, 0.07]), 0)
    
    # Credit History Category
    credit_histories = []
    for cs, pd_val in zip(credit_scores, prev_defaults):
        if cs >= 740 and pd_val == 0:
            credit_histories.append("Excellent")
        elif cs >= 670 and pd_val <= 1:
            credit_histories.append("Good")
        elif cs >= 580:
            credit_histories.append("Fair")
        else:
            credit_histories.append("Poor")
            
    property_ownerships = np.random.choice(["Rent", "Mortgage", "Own"], size=n_records, p=[0.44, 0.38, 0.18])
    regions = np.random.choice(["North", "South", "East", "West", "Central"], size=n_records, p=[0.24, 0.22, 0.20, 0.18, 0.16])
    
    # 3. Default Probability Model (Realistic Financial Credit Risk Logistic Scoring)
    # Higher risk drivers: low credit score, high DTI, previous defaults, unemployed, high loan amount vs income
    score_factor = -(credit_scores - 660) / 75.0
    dti_factor = (dti_ratios - 0.35) * 5.0
    prev_def_factor = prev_defaults * 1.1
    unemp_factor = np.where(employment_statuses == "Unemployed", 1.2, 0.0)
    loan_to_inc = (loan_amounts / annual_income - 0.5) * 1.5
    
    # Logit calculation
    z = -2.15 + 0.65 * score_factor + 0.55 * dti_factor + 0.60 * prev_def_factor + 0.45 * unemp_factor + 0.35 * loan_to_inc
    prob_default = 1.0 / (1.0 + np.exp(-z))
    prob_default = np.clip(prob_default, 0.02, 0.88)
    
    defaults = np.random.binomial(1, prob_default)
    default_status = np.where(defaults == 1, "Yes", "No")
    
    # Loan Status
    loan_statuses = []
    for d in defaults:
        if d == 1:
            loan_statuses.append("Defaulted")
        else:
            loan_statuses.append(np.random.choice(["Fully Paid", "Current"], p=[0.58, 0.42]))
            
    df = pd.DataFrame({
        "Customer_ID": cust_ids,
        "Gender": genders,
        "Age": ages,
        "Education": educations,
        "Employment_Status": employment_statuses,
        "Marital_Status": marital_statuses,
        "Dependents": dependents,
        "Annual_Income": annual_income,
        "Credit_Score": credit_scores,
        "Existing_Loans": existing_loans,
        "Loan_ID": loan_ids,
        "Loan_Type": loan_types,
        "Loan_Amount": loan_amounts,
        "Loan_Term_Months": loan_terms,
        "Interest_Rate": interest_rates,
        "Monthly_Installment": monthly_installments,
        "Debt_to_Income_Ratio": dti_ratios,
        "Employment_Years": employment_years,
        "Previous_Defaults": prev_defaults,
        "Credit_History": credit_histories,
        "Property_Ownership": property_ownerships,
        "Region": regions,
        "Loan_Status": loan_statuses,
        "Default_Status": default_status
    })
    
    # 4. Inject Realistic Imperfections for Part 2 Cleaning Demonstration
    # A) Missing values in a few columns
    null_idx_inc = np.random.choice(df.index, size=42, replace=False)
    df.loc[null_idx_inc, "Annual_Income"] = np.nan
    
    null_idx_exp = np.random.choice(df.index, size=36, replace=False)
    df.loc[null_idx_exp, "Employment_Years"] = np.nan
    
    null_idx_cs = np.random.choice(df.index, size=28, replace=False)
    df.loc[null_idx_cs, "Credit_Score"] = np.nan
    
    null_idx_dti = np.random.choice(df.index, size=22, replace=False)
    df.loc[null_idx_dti, "Debt_to_Income_Ratio"] = np.nan
    
    # B) Inject 25 duplicate rows
    duplicate_rows = df.sample(n=25, random_state=101)
    df_with_dups = pd.concat([df, duplicate_rows], ignore_index=True)
    
    # C) Inject 3 entry outliers
    outlier_idx_1 = 45
    df_with_dups.loc[outlier_idx_1, "Annual_Income"] = -45000.0  # Erroneous negative value
    outlier_idx_2 = 180
    df_with_dups.loc[outlier_idx_2, "Loan_Amount"] = 999999.0   # Extreme data entry typo
    
    return df_with_dups

if __name__ == "__main__":
    df_raw = generate_loan_dataset(5000)
    raw_path = "Dataset/Loan_Credit_Risk_Raw.csv"
    df_raw.to_csv(raw_path, index=False)
    print(f"Raw dataset generated successfully at {raw_path}")
    print(f"Shape: {df_raw.shape}")
    print(f"Missing values:\n{df_raw.isnull().sum()[df_raw.isnull().sum() > 0]}")
    print(f"Duplicate rows: {df_raw.duplicated().sum()}")
