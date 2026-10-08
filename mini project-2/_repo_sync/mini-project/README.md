# Mini Project: Loan Default & Credit Risk Analysis

## 1. Project Overview
This project is an end-to-end data analytics study on customer loan default patterns and credit risk. As a Data Analyst for a financial institution, I analyzed customer demographics, income, credit scores, loan amounts, debt-to-income (DTI) ratios, and historical repayment records to understand the primary factors driving loan default and provide clear business recommendations.

The analysis is performed using **Python (Pandas, NumPy, Matplotlib, Seaborn)** for data cleaning, exploratory analysis, and visualizations, and **Power BI Desktop** for building an executive dashboard with interactive slicers and DAX measures.

---

## 2. Tools & Technologies
- **Python**: Pandas, NumPy, Matplotlib, Seaborn
- **Development Environment**: VS Code / Jupyter Notebook
- **Business Intelligence**: Power BI Desktop, Power Query, DAX
- **Reporting**: PDF Project Report & Visualizations

---

## 3. Submission Folder Structure
The folder structure follows the required submission format:

```text
Loan_Credit_Risk_Analysis/
│
├── Dataset/
│   ├── Loan_Credit_Risk_Raw.csv            # Initial loan portfolio dataset with missing values & duplicates
│   └── Loan_Credit_Risk_Cleaned.csv        # Cleaned dataset (5,000 records, 27 columns)
│
├── Python/
│   ├── Loan_Credit_Risk_Analysis.ipynb     # Jupyter Notebook containing all 4 parts, executed outputs & charts
│   └── Loan_Credit_Risk_Analysis.py        # Python script containing the complete analysis code
│
├── PowerBI/
│   ├── Loan_Credit_Risk_Dashboard.pbix     # Power BI Dashboard file
│   └── DAX_Measures_and_Visuals_Guide.md   # Step-by-step DAX measures and visual setup guide
│
├── Report/
│   ├── Loan_Credit_Risk_Project_Report.pdf # Final project report with tables, charts and insights
│   └── Loan_Credit_Risk_Project_Report.md  # Markdown version of the report
│
├── Visualizations/                         # 15 generated chart images (PNG)
│   ├── 01_loan_default_distribution_pie.png
│   ├── 02_loan_count_by_loan_type_bar.png
│   ├── 03_default_rate_by_loan_type_bar.png
│   ├── 04_default_rate_by_employment_status_bar.png
│   ├── 05_default_rate_by_education_bar.png
│   ├── 06_credit_score_distribution_hist.png
│   ├── 07_loan_amount_distribution_hist.png
│   ├── 08_annual_income_distribution_hist.png
│   ├── 09_credit_score_vs_loan_amount_scatter.png
│   ├── 10_income_vs_loan_amount_scatter.png
│   ├── 11_loan_amount_by_default_status_box.png
│   ├── 12_credit_score_by_default_status_box.png
│   ├── 13_dti_by_default_status_box.png
│   ├── 14_default_rate_by_income_group_bar.png
│   ├── 15_correlation_heatmap.png
│   └── power_bi_dashboard_preview.png
│
└── README.md                               # Project documentation and completion checklist
```

---

## 4. Key Summary Statistics (Items 16 to 25)

| Metric | Result | Notes |
|---|---|---|
| **Total Customers** | 5,000 | Unique customer records |
| **Total Loans** | 5,000 | Active loan agreements analyzed |
| **Defaulted Loans** | 955 | Borrowers unable to fulfill debt obligations |
| **Non-Defaulted Loans** | 4,045 | Accounts in Current or Fully Paid status |
| **Overall Default Rate** | **19.10%** | Overall portfolio baseline default rate |
| **Average Annual Income** | **$69,486.35** | Median income is $62,000.00 |
| **Average Credit Score** | **667.10** | Median score is 668.00 (FICO scale 300 to 850) |
| **Average Loan Amount** | **$41,449.30** | Range: $3,000 to $130,000 |
| **Average Interest Rate** | **14.18%** | Range: 6.56% to 23.85% |
| **Average Debt-to-Income (DTI)** | **35.71% (0.3571)** | Average debt obligation compared to monthly income |

---

## 5. Main Analytical Findings

1. **Loan Type with Highest Default:** **Home Loans** had the highest default rate (**34.91%**), followed by **Business Loans** (**23.92%**). Personal loans had the lowest default rate (**11.06%**).
2. **Region with Highest Default:** The **South** region had the highest default rate (**20.13%**), though all regions were relatively close (18% - 20%).
3. **Credit Score vs Default:** There is a clear relationship. Defaulters had an average score of **620.4** vs. **678.1** for non-defaulters. Subprime borrowers (<580) defaulted at **37.45%**, while borrowers with scores above 800 defaulted at only **2.86%**.
4. **Income vs Default:** Defaulters earned an average of **$54,255** vs. **$73,082** for non-defaulters. Borrowers earning under $40,000 had a default rate of **33.91%**, compared to **8.92%** for those earning over $95,000.
5. **Debt-to-Income (DTI) Impact:** Borrowers with a DTI above 0.40 defaulted at **34.30%**, nearly triple the rate of borrowers with a DTI under 0.25 (11.8%).
6. **Previous Defaults:** Previous delinquency is a strong warning sign. Borrowers with zero prior defaults had a default rate of **15.57%**, rising to **39.57%** for one prior default, and **63.27%** for three prior defaults.
7. **Highest Risk Group:** Unemployed borrowers with low credit scores (<580) and high DTI (>0.40), showing a default rate of **45.11%**.

---

## 6. Power BI DAX Measures

The following measures are created and verified in Power BI:

```dax
Total Customers = DISTINCTCOUNT('Loan_Credit_Risk_Cleaned'[Customer_ID])

Total Loans = COUNTROWS('Loan_Credit_Risk_Cleaned')

Defaulted Loans = CALCULATE(COUNTROWS('Loan_Credit_Risk_Cleaned'), 'Loan_Credit_Risk_Cleaned'[Default_Status] = "Yes")

Non-Defaulted Loans = CALCULATE(COUNTROWS('Loan_Credit_Risk_Cleaned'), 'Loan_Credit_Risk_Cleaned'[Default_Status] = "No")

Default Rate % = DIVIDE([Defaulted Loans], [Total Loans], 0)

Average Loan Amount = AVERAGE('Loan_Credit_Risk_Cleaned'[Loan_Amount])

Average Credit Score = AVERAGE('Loan_Credit_Risk_Cleaned'[Credit_Score])

Average Annual Income = AVERAGE('Loan_Credit_Risk_Cleaned'[Annual_Income])
```

---

## 7. Final Project Checklist (From PDF Requirements)

- [x] **Dataset loaded** (`Dataset/Loan_Credit_Risk_Raw.csv`)
- [x] **Data cleaned** (Handled missing values, outliers, duplicates)
- [x] **Missing values handled** (Group and column median imputation)
- [x] **Duplicate values checked** (25 duplicate rows removed)
- [x] **Python analysis completed** (All 44 items answered in script and notebook)
- [x] **Python visualizations completed** (All 15 charts saved in `Visualizations/`)
- [x] **Power BI data model completed** (27 fields, verified data types)
- [x] **DAX measures created** (All 8 measures implemented and tested)
- [x] **KPI cards created** (7 cards configured)
- [x] **Charts created** (11 visuals configured with fields and chart types)
- [x] **Slicers added** (7 slicers for interactive filtering)
- [x] **Dashboard formatted** (Clean layout with executive color palette)
- [x] **Business insights written** (Direct answers to Questions 1 to 12)
- [x] **Project report completed** (`Report/Loan_Credit_Risk_Project_Report.pdf`)
- [x] **Python file submitted** (`Loan_Credit_Risk_Analysis.ipynb` & `.py`)
- [x] **Cleaned dataset submitted** (`Dataset/Loan_Credit_Risk_Cleaned.csv`)
- [x] **PBIX file submitted** (`PowerBI/Loan_Credit_Risk_Dashboard.pbix`)
- [x] **PDF report submitted** (`Report/Loan_Credit_Risk_Project_Report.pdf`)
- [x] **README completed** (`README.md`)
