# Mini Project Report: Loan Default & Credit Risk Analysis

**Author:** Data Analyst Specialist  
**Domain:** Retail Banking & Credit Risk Management  
**Dataset:** 5,000 Retail Loan Records  
**Tools & Technologies:** Python (NumPy, Pandas, Matplotlib, Seaborn), Power BI Desktop, DAX, Power Query  
**Output Documents:** `Loan_Credit_Risk_Project_Report.pdf`, `Loan_Credit_Risk_Analysis.ipynb`, `Loan_Credit_Risk_Cleaned.csv`, `Loan_Credit_Risk_Dashboard.pbix`  

---

## 1. Project Objective & Scope

Financial institutions operate in an environment where extending credit entails credit risk—the probability that a borrower defaults on scheduled repayments. 

This project analyzes comprehensive customer loan portfolios encompassing:
- Customer demographics (Age, Gender, Education, Employment Status, Marital Status, Dependents)
- Financial solvency metrics (Annual Income, Credit Score, Existing Loan Count, Debt-to-Income Ratio)
- Loan specifics (Loan Type, Loan Amount, Loan Term, Interest Rate, Monthly Installment)
- Historical credit conduct (Previous Defaults, Credit History Tier)
- Collateral & geography (Property Ownership, Region)
- Repayment outcome (Loan Status, Default Status)

The primary goal is to identify multi-dimensional risk drivers associated with retail loan defaults, calculate essential portfolio credit metrics, build high-impact statistical visualizations, create an interactive Power BI risk monitoring dashboard, and propose actionable underwriting policies.

---

## 2. Tools & Technologies

| Tool / Technology | Purpose & Implementation |
|---|---|
| **Python 3.13** | Core runtime for data processing pipelines and quantitative modeling. |
| **Pandas & NumPy** | Ingestion, deduplication, missing value imputation, grouping, and aggregations. |
| **Matplotlib & Seaborn** | Exploratory and risk distribution charts (histograms, box plots, scatter plots, heatmaps). |
| **Power BI Desktop** | Executive risk intelligence dashboard, dynamic KPI cards, and cross-filtering slicers. |
| **DAX Expressions** | Calculation of measures using `CALCULATE`, `DIVIDE`, `COUNTROWS`, `DISTINCTCOUNT`, and `AVERAGE`. |
| **ReportLab** | Automated compilation of publication-grade PDF project reports. |

---

## 3. Dataset Description & Data Cleaning (Part 1 & Part 2)

### 3.1 Raw Dataset Profile
- **Total Records:** 5,025 rows
- **Total Attributes:** 24 features
- **Missing Values:**
  - `Annual_Income`: 43 missing values (0.86%)
  - `Credit_Score`: 28 missing values (0.56%)
  - `Debt_to_Income_Ratio`: 22 missing values (0.44%)
  - `Employment_Years`: 36 missing values (0.72%)
- **Duplicate Records:** 25 duplicated rows detected.
- **Outliers / Entry Typos:** Erroneous negative value in `Annual_Income` (-$45,000) and entry typo in `Loan_Amount` ($999,999).

### 3.2 Cleaning & Preprocessing Pipeline
1. **Deduplication:** Dropped 25 redundant records based on unique customer identifier (`Customer_ID`), establishing a 5,000-customer clean portfolio.
2. **Outlier Correction:** Scrubbed negative income to `NaN` and replaced with subgroup median. Capped the extreme loan amount typo to the portfolio median ($29,900) and updated the monthly installment using standard amortization formulas.
3. **Conditional Imputation:** 
   - `Annual_Income` was imputed using the conditional median grouped by `Education` level and `Employment_Status`.
   - `Credit_Score` (median 668), `Debt_to_Income_Ratio` (median 0.29), and `Employment_Years` (median 6.0 years) were imputed using overall distributional medians.
4. **Feature Engineering:**
   - **Credit Score Group:** Segmented into FICO tiers: `Poor (<580)`, `Fair (580-669)`, `Good (670-739)`, `Very Good (740-799)`, and `Excellent (800+)`.
   - **Income Group:** Binned into `Low (<$40k)`, `Lower-Middle ($40k-$65k)`, `Upper-Middle ($65k-$95k)`, and `High (>$95k)`.
   - **Default_Numeric:** Binary flag (1 for Yes, 0 for No).
5. **Output Verification:** 0 missing values, 0 duplicate records across 5,000 rows and 27 columns. Exported to `Dataset/Loan_Credit_Risk_Cleaned.csv`.

---

## 4. Quantitative Portfolio Analysis (Part 3: Questions 16–44)

### 4.1 Summary Portfolio Performance (Items 16–25)
- **16. Total Customers:** 5,000
- **17. Total Loans:** 5,000
- **18. Defaulted Loans:** 955
- **19. Non-Defaulted Loans:** 4,045
- **20. Overall Default Rate:** **19.10%**
- **21. Average Annual Income:** $69,486.35 (Median: $62,000)
- **22. Average Credit Score:** 667.10 (Range: 300 – 850)
- **23. Average Loan Amount:** $41,449.30 (Range: $3,000 – $130,000)
- **24. Average Interest Rate:** 14.18% (Range: 6.56% – 23.85%)
- **25. Average Debt-to-Income (DTI) Ratio:** 0.3571 (35.71%)

### 4.2 Portfolio Distribution & Default Rates by Segment (Items 26–33)

#### By Loan Product (Item 26 & 28):
| Loan Type | Loan Count | Share (%) | Default Count | Default Rate (%) |
|---|---|---|---|---|
| **Personal** | 1,474 | 29.5% | 163 | 11.06% |
| **Home** | 1,203 | 24.1% | 420 | **34.91%** |
| **Auto** | 1,123 | 22.5% | 162 | 14.43% |
| **Education** | 715 | 14.3% | 94 | 13.15% |
| **Business** | 485 | 9.7% | 116 | 23.92% |

#### By Employment Status (Item 29):
| Employment Status | Loan Count | Share (%) | Default Rate (%) |
|---|---|---|---|
| **Employed** | 3,465 | 69.3% | 17.23% |
| **Self-Employed** | 1,136 | 22.7% | 15.67% |
| **Unemployed** | 399 | 8.0% | **45.11%** |

#### By Education Level (Item 30):
| Education | Loan Count | Share (%) | Default Rate (%) |
|---|---|---|---|
| **High School** | 1,241 | 24.8% | 22.80% |
| **Bachelor** | 2,442 | 48.8% | 19.98% |
| **Master** | 1,015 | 20.3% | 14.48% |
| **PhD** | 302 | 6.0% | 12.25% |

#### By Property Ownership (Item 31):
| Property Ownership | Loan Count | Default Rate (%) |
|---|---|---|
| **Mortgage** | 1,858 | 18.14% |
| **Rent** | 2,249 | 19.25% |
| **Own** | 893 | 20.72% |

#### By Credit Score Tier (Item 32):
| Credit Score Group | Range | Loan Count | Default Rate (%) | Risk Tier |
|---|---|---|---|---|
| **Poor** | < 580 | 793 | **37.45%** | Critical Subprime |
| **Fair** | 580 – 669 | 1,758 | 22.58% | Elevated |
| **Good** | 670 – 739 | 1,435 | 13.52% | Moderate |
| **Very Good** | 740 – 799 | 699 | 8.30% | Prime |
| **Excellent** | 800 – 850 | 315 | **2.86%** | Super Prime |

#### By Income Bracket (Item 33):
| Income Bracket | Range | Loan Count | Default Rate (%) |
|---|---|---|---|
| **Low** | < $40,000 | 1,094 | **33.91%** |
| **Lower-Middle** | $40,000 – $65,000 | 1,607 | 19.60% |
| **Upper-Middle** | $65,000 – $95,000 | 1,268 | 13.96% |
| **High** | > $95,000 | 1,031 | **8.92%** |

### 4.3 High-Risk Portfolio Subsets (Items 34–39)
- **34. Below-Average Credit Score (< 667.1):** 2,480 customers (49.6% of portfolio). Default rate: **27.22%**.
- **35. Above-Average Loan Amount (> $41,449):** 1,748 customers (35.0% of portfolio). Default rate: **31.18%**.
- **36. High Debt-to-Income (> 0.40):** 1,837 customers (36.7% of portfolio). Default rate: **34.30%**.
- **38. Loan Type with Highest Default Rate:** **Home Loans (34.91%)**.
- **39. Region with Highest Default Rate:** **South (20.13%)**, followed by East (19.49%) and West (18.85%).

### 4.4 Driver Comparison Summaries (Items 40–43)
- **40. Credit Score vs Default:** Performing borrowers have a mean score of **678.12** vs **620.42** for defaulted borrowers (58-point gap).
- **41. Annual Income vs Default:** Performing borrowers earn an average of **$73,082.48** vs **$54,254.55** for defaulted borrowers.
- **42. Loan Amount vs Default:** Performing loans average **$37,242.42** vs **$59,267.96** for defaulted loans ($22,025 higher principal).
- **43. Previous Defaults Recidivism:**
  - 0 Previous Defaults: **15.57%** default rate
  - 1 Previous Default: **39.57%** default rate
  - 2 Previous Defaults: **45.99%** default rate
  - 3 Previous Defaults: **63.27%** default rate

---

## 5. Visualizations Overview (Part 4)

All 15 charts were generated and saved at 300 DPI resolution in `Visualizations/`:
1. `01_loan_default_distribution_pie.png`: 80.9% Non-Default vs 19.1% Default.
2. `02_loan_count_by_loan_type_bar.png`: Personal (1,474), Home (1,203), Auto (1,123), Education (715), Business (485).
3. `03_default_rate_by_loan_type_bar.png`: Home (34.9%) and Business (23.9%) exceed portfolio benchmark.
4. `04_default_rate_by_employment_status_bar.png`: Unemployed spike at 45.1%.
5. `05_default_rate_by_education_bar.png`: Inverse trend with education level.
6. `06_credit_score_distribution_hist.png`: Normal distribution centered at 667.1.
7. `07_loan_amount_distribution_hist.png`: Multimodal distribution reflecting differentiated loan products.
8. `08_annual_income_distribution_hist.png`: Right-skewed log-normal earnings curve.
9. `09_credit_score_vs_loan_amount_scatter.png`: Defaulters cluster in lower credit score brackets across all loan amounts.
10. `10_income_vs_loan_amount_scatter.png`: High loan amounts combined with modest income represent critical default cluster.
11. `11_loan_amount_by_default_status_box.png`: Demonstrates significantly higher median loan amount for defaulted accounts.
12. `12_credit_score_by_default_status_box.png`: Clear separation between performing (median 678) and defaulting (median 621) cohorts.
13. `13_dti_by_default_status_box.png`: Strong upward shift in DTI among defaulting accounts.
14. `14_default_rate_by_income_group_bar.png`: Monotonic decline in default rate as income rises (33.9% down to 8.9%).
15. `15_correlation_heatmap.png`: Quantitative correlation matrix across 12 continuous features.

---

## 6. Power BI Dashboard & DAX Implementation (Part 5)

The interactive dashboard was built and packaged in `PowerBI/Loan_Credit_Risk_Dashboard.pbix` with full documentation in `PowerBI/DAX_Measures_and_Visuals_Guide.md`.

### Core DAX Measures:
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

## 7. Business Insights & Answers (Part 6 / Section 12)

1. **Overall Default Rate:** The portfolio baseline default rate is **19.10%** (955 defaulted accounts out of 5,000 total loans).
2. **Loan Type with Highest Default Rate:** **Home Loans (34.91%)**, followed by **Business Loans (23.92%)**.
3. **Region with Highest Default Rate:** **South Region (20.13%)**, followed closely by East (19.49%) and West (18.85%).
4. **Association with Credit Score:** Strongly associated. Borrowers with credit scores < 580 experience a **37.45%** default rate, compared to **2.86%** for borrowers with credit scores >= 800.
5. **Association with Income:** Higher income provides strong default protection. Low-income borrowers (< $40k) default at **33.91%**, whereas high earners (> $95k) default at only **8.92%**.
6. **Association with DTI:** Critical association. Borrowers with DTI > 0.40 suffer a **34.30%** default rate, almost triple the rate of low-DTI borrowers (< 0.25 at 11.8%).
7. **Association with Previous Defaults:** Prior delinquencies indicate severe recidivism. A single prior default increases risk from 15.57% to **39.57%**, and 3 prior defaults reach **63.27%**.
8. **Highest Risk Customer Segment:** **Unemployed applicants with credit scores under 580 and DTI > 0.40**, exhibiting default rates above **45.11%**.
9. **Primary Default Drivers:** Credit score, debt-to-income ratio, previous default history, employment stability, and principal-to-income leverage.
10. **Loan Amount vs Default Pattern:** Defaulters have a substantially higher mean principal ($59,268) compared to non-defaulters ($37,242), indicating capital concentration risk in large unsecured/mortgage facilities.
11. **Financial Surveillance Factors:** Enforce strict DTI ceilings (max 40%), minimum credit score thresholds (620 minimum for standard approval), mandatory verification of employment continuity, and loan-to-income caps.
12. **Key Strategic Recommendations:**
   - Enforce an automatic rejection or senior underwriting escalation rule for applicants with 2+ prior defaults or FICO < 550.
   - Re-underwrite Home loan products with stricter initial equity/collateral requirements to lower the 34.9% default concentration.
   - Price risk dynamically: require risk-based interest surcharges or credit protection insurance on accounts with DTI between 0.35 and 0.45.
   - Prioritize customer acquisition across high-margin prime personal and auto loans where defaults stay under 12%.

---

## 8. Final Checklist & Submission Artifacts

- [x] Dataset loaded and schema inspected (`Dataset/Loan_Credit_Risk_Raw.csv`)
- [x] Data cleaned, missing values imputed, outliers capped (`Dataset/Loan_Credit_Risk_Cleaned.csv`)
- [x] Python analysis completed across all 44 items (`Python/Loan_Credit_Risk_Analysis.py`)
- [x] Python visualizations completed across all 15 figures (`Visualizations/`)
- [x] Jupyter Notebook fully executed with inline outputs (`Python/Loan_Credit_Risk_Analysis.ipynb`)
- [x] Power BI Data Model, DAX Measures, and Canvas configured (`PowerBI/Loan_Credit_Risk_Dashboard.pbix` & Guide)
- [x] Publication-quality PDF report compiled (`Report/Loan_Credit_Risk_Project_Report.pdf`)
- [x] Comprehensive README completed (`README.md`)
