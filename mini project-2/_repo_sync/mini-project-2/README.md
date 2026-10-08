# Mini Project: Customer Churn Analysis

## 1. Project Overview
This project is an end-to-end data analytics study on customer churn and retention patterns for a subscription-based telecommunications provider. As a Senior Data Analyst, I analyzed customer demographics, enrolled service packages, contractual terms, payment methods, and billing history across **7,043** customer accounts to uncover the fundamental drivers of customer churn and formulate data-backed retention strategies.

The analysis is executed using **Python (Pandas, NumPy, Matplotlib, Seaborn)** for rigorous data cleaning, statistical evaluation, and publication-grade visualizations, and **Power BI Desktop** for building an interactive executive dashboard powered by custom DAX measures and real-time slicers.

---

## 2. Tools & Technologies
- **Python**: Pandas, NumPy, Matplotlib, Seaborn
- **Development Environment**: VS Code / Jupyter Notebook / Google Colab
- **Business Intelligence**: Power BI Desktop, Power Query, DAX
- **Reporting Engine**: ReportLab (Publication-grade PDF Generator)
- **Version Control**: Git & GitHub

---

## 3. Submission Folder Structure
The repository strictly adheres to Section 12 of the official project brief:

```text
Customer_Churn_Analysis/
│
├── Dataset/
│   ├── Customer_Churn_Raw.csv            # Raw dataset containing duplicates and whitespace values (7,061 records)
│   └── Customer_Churn_Cleaned.csv        # Cleaned dataset (7,043 unique records, 23 columns)
│
├── Python/
│   ├── Customer_Churn_Analysis.ipynb     # Fully executed Jupyter Notebook with all outputs & charts
│   └── Customer_Churn_Analysis.py        # Standalone executable Python pipeline script
│
├── PowerBI/
│   ├── Customer_Churn_Dashboard.pbix     # Interactive Power BI Dashboard package
│   └── DAX_Measures_and_Visuals_Guide.md # Step-by-step DAX expressions & visual setup documentation
│
├── Report/
│   ├── Customer_Churn_Project_Report.pdf # 8-page publication-grade executive project report
│   └── Customer_Churn_Project_Report.md  # Markdown documentation of the project report
│
├── Visualizations/                       # High-resolution PNG exports (300 DPI)
│   ├── 01_churn_distribution_pie.png
│   ├── 02_customer_distribution_by_contract_bar.png
│   ├── 03_churn_by_contract_bar.png
│   ├── 04_churn_by_gender_bar.png
│   ├── 05_churn_by_internet_service_bar.png
│   ├── 06_churn_by_payment_method_bar.png
│   ├── 07_tenure_distribution_histogram.png
│   ├── 08_monthly_charges_distribution_histogram.png
│   ├── 09_tenure_vs_monthly_charges_scatter.png
│   ├── 10_monthly_charges_by_churn_boxplot.png
│   ├── 11_total_charges_by_churn_boxplot.png
│   ├── 12_churn_rate_by_tenure_group_bar.png
│   ├── 13_service_usage_countplot.png
│   ├── 14_correlation_heatmap.png
│   └── 15_powerbi_dashboard_preview.png
│
├── _scripts/                             # Automated reproduction pipelines
│   ├── prepare_raw_data.py               # Raw dataset fetch & synthetic imperfection generator
│   ├── run_analysis_pipeline.py          # Data cleaning, analysis, & visualization export script
│   ├── build_jupyter_notebook.py         # Programmatic Jupyter Notebook builder & executor
│   ├── create_pbix_package.py            # Power BI OPC container package builder
│   └── generate_pdf_report.py            # ReportLab publication PDF compiler
│
└── README.md                             # Comprehensive project documentation
```

---

## 4. Key Performance Indicators (KPIs)

| Metric | Measured Value | Business Interpretation |
| :--- | :--- | :--- |
| **Total Customers** | **7,043** | Total unique subscriber accounts analyzed |
| **Total Churned Customers** | **1,869** | Subscriptions terminated |
| **Total Retained Customers** | **5,174** | Active loyal customer base |
| **Overall Churn Rate** | **26.54%** | Baseline portfolio attrition rate |
| **Average Monthly Charges** | **$64.76** | Portfolio-wide recurring revenue per account |
| **Average Customer Tenure** | **32.37 Months** | Average subscription duration across portfolio |
| **Total Monthly Recurring Revenue** | **$456,116.60** | Current total monthly billed revenue |
| **At-Risk Monthly Revenue Lost** | **$139,130.85** | Monthly revenue lost from churned accounts (30.5%) |

---

## 5. Summary of Analysis (Parts 1–4)

### Part 1: Data Loading (Steps 1–6)
- Successfully imported and inspected the dataset with 7,061 initial records and 21 attributes.
- Audited first and last 5 records and cataloged all demographic, service, and billing column names.

### Part 2: Data Exploration & Cleaning (Steps 7–16)
- **Deduplication:** Detected and dropped **18 duplicate rows**, establishing 7,043 clean records.
- **Type Casting & Missing Values:** Discovered 11 whitespace values (`" "`) in `Total_Charges` associated with brand-new accounts with `Tenure_Months == 0`. Imputed these missing values to `0.0` and cast `Total_Charges` to `float64`.
- **Tenure Segmentation:** Engineered feature `Tenure_Group` with 6 standard bins: `0-12 Months`, `13-24 Months`, `25-36 Months`, `37-48 Months`, `49-60 Months`, and `61-72 Months`.
- **Verified Clean Data:** Confirmed 0 null values across all 23 features in `Customer_Churn_Cleaned.csv`.

### Part 3: Analytical Findings (Steps 17–38)
- **Contract Impact:** Month-to-month contracts churn at **42.71%**, representing **88.55%** of all churned customers. Two-year contracts churn at only **2.83%** (15.1x lower attrition).
- **First-Year Onboarding Cliff:** Customers in their first 12 months churn at **47.44%**. The median tenure of churned customers is only **10.0 months** vs **38.0 months** for retained subscribers.
- **Internet Service:** Fiber optic subscribers experience **41.89%** churn vs **18.96%** for DSL and **7.40%** for No Internet.
- **Payment Method:** Electronic check payments show an alarming **45.29%** churn rate, compared to **15.24%** for automated credit cards and **16.71%** for automated bank transfers.
- **Value-Added Protection:** Enrolling in Tech Support and Online Security drops churn from **~41.7%** to **~15.0%**.
- **Gender Neutrality:** Male churn (26.16%) and Female churn (26.92%) differ by only 0.76%, proving churn is driven by contract structure, pricing, and service experience rather than gender.

### Part 4: Python Visualizations (14 Charts)
1. `01_churn_distribution_pie.png`: Donut/Pie chart illustrating 73.5% retention vs 26.5% churn.
2. `02_customer_distribution_by_contract_bar.png`: Customer distribution across contract types.
3. `03_churn_by_contract_bar.png`: Churn rate across Month-to-Month (42.7%), 1-Year (11.3%), and 2-Year (2.8%).
4. `04_churn_by_gender_bar.png`: Churn comparison across Male and Female cohorts.
5. `05_churn_by_internet_service_bar.png`: Churn rate across Fiber Optic, DSL, and No Internet.
6. `06_churn_by_payment_method_bar.png`: Horizontal bar chart across 4 payment methods.
7. `07_tenure_distribution_histogram.png`: Histogram displaying customer tenure distribution.
8. `08_monthly_charges_distribution_histogram.png`: Histogram showing monthly bill concentration.
9. `09_tenure_vs_monthly_charges_scatter.png`: Scatter plot mapping tenure vs monthly charges by churn status.
10. `10_monthly_charges_by_churn_boxplot.png`: Box plot comparing monthly charges (retained median $64.43 vs churned median $79.65).
11. `11_total_charges_by_churn_boxplot.png`: Box plot comparing cumulative lifetime charges.
12. `12_churn_rate_by_tenure_group_bar.png`: Bar chart highlighting the steep first-year churn cliff.
13. `13_service_usage_countplot.png`: Multi-panel count plot of security and tech support adoption.
14. `14_correlation_heatmap.png`: Correlation matrix across demographics, services, billing, and churn.
15. `15_powerbi_dashboard_preview.png`: Executive preview of the complete interactive Power BI dashboard.

---

## 6. Power BI Dashboard & DAX Measures (Sections 8 & 9)

**Dashboard Title:** *"Customer Churn & Retention Analytics Dashboard"*

### Required DAX Measures

```dax
// 1. Total Customers (DISTINCTCOUNT)
Total Customers = DISTINCTCOUNT('Customer_Churn_Cleaned'[Customer_ID])

// 2. Churned Customers (CALCULATE & COUNTROWS)
Churned Customers = CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = "Yes")

// 3. Retained Customers (CALCULATE & COUNTROWS)
Retained Customers = CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = "No")

// 4. Churn Rate % (DIVIDE)
Churn Rate % = DIVIDE([Churned Customers], [Total Customers], 0)

// 5. Average Monthly Charges (AVERAGE)
Average Monthly Charges = AVERAGE('Customer_Churn_Cleaned'[Monthly_Charges])

// 6. Average Tenure (AVERAGE)
Average Tenure = AVERAGE('Customer_Churn_Cleaned'[Tenure_Months])
```

### Dashboard Features
- **6 KPI Cards**: Total Customers, Churned Customers, Retained Customers, Churn Rate %, Average Monthly Charges, Average Tenure.
- **6 Interactive Slicers**: Gender, Contract, Internet Service, Payment Method, Senior Citizen, Churn.
- **10 Core Visuals**: Donut Charts, Clustered Bar/Column Charts, Scatter Chart, and Customer Details Table/Matrix.

---

## 7. Business Insights & Answers to the 10 Questions (Section 10)

1. **What is the overall churn rate?**  
   **26.54%** (1,869 churned out of 7,043 customers).
2. **Which contract type has the highest churn?**  
   **Month-to-month contracts** with **42.71%** churn (responsible for 88.55% of all churn).
3. **Which payment method has the highest churn?**  
   **Electronic check** with **45.29%** churn (vs ~15.2% for auto-pay).
4. **Which internet service has the highest churn?**  
   **Fiber optic internet** with **41.89%** churn.
5. **Does tenure appear related to churn?**  
   **Yes, strongly inversely related.** Months 0–12 peak at 47.44% churn, while months 61–72 drop to 6.61%. Churned customers have a median tenure of only 10 months vs 38 months for retained accounts.
6. **Are higher monthly charges associated with churn?**  
   **Yes.** Churned customers pay a median monthly fee of **$79.65** vs **$64.43** for retained customers.
7. **Which customer segment has the highest churn?**  
   **First-year Fiber Optic subscribers on Month-to-month contracts paying via Electronic Check without Tech Support or Online Security** (churn rate > 68%).
8. **What factors appear associated with customer churn?**  
   Month-to-month contracts (15.1x risk), tenure < 12 months (7.2x risk), electronic checks (3.0x risk), unbundled fiber optic service (2.2x risk), lack of tech support (2.8x risk), and senior citizen status (1.8x risk).
9. **Which customer segment requires immediate attention?**  
   **First-year Fiber Optic subscribers on Month-to-Month contracts.** They represent the highest ARPU accounts, whose premature departure creates substantial Customer Acquisition Cost (CAC) deficits.
10. **Key Strategic Recommendations:**  
   - Offer a 10% monthly discount or complimentary streaming add-on to migrate month-to-month users to 1- or 2-year contracts.  
   - Implement a proactive 90-day onboarding check-in to bridge the first-year churn cliff.  
   - Provide a $5 monthly bill credit for enrolling in Auto-Pay (Credit Card / Bank Transfer).  
   - Bundle free Tech Support and Online Security for all new Fiber Optic subscribers.  
   - Deploy dedicated Senior Citizen onboarding and support helplines.

---

## 8. Final Submission Checklist (Section 13)

- [x] **Data cleaned** (7,043 unique verified records)
- [x] **Missing values handled** (Imputed 11 whitespace values in Total_Charges to 0.0)
- [x] **Python analysis completed** (All 38 steps executed and verified)
- [x] **Python visualizations completed** (14 charts created at 300 DPI)
- [x] **DAX measures created** (COUNTROWS, DISTINCTCOUNT, CALCULATE, DIVIDE, AVERAGE)
- [x] **Power BI dashboard completed** (`Customer_Churn_Dashboard.pbix` generated)
- [x] **Slicers added** (Gender, Contract, Internet Service, Payment Method, Senior Citizen, Churn)
- [x] **Business insights written** (All 10 questions thoroughly answered)
- [x] **Project report completed** (8-page publication-grade PDF + Markdown report)
- [x] **Dataset submitted** (`Customer_Churn_Cleaned.csv` and `Customer_Churn_Raw.csv`)
- [x] **Python file submitted** (`Customer_Churn_Analysis.ipynb` executed + `.py` script)
- [x] **PBIX file submitted** (`Customer_Churn_Dashboard.pbix` in PowerBI folder)
- [x] **README completed** (Comprehensive project documentation)

---

## 9. How to Run & Reproduce
To re-execute the entire pipeline from scratch:

```bash
# 1. Prepare raw dataset with authentic test imperfections
python _scripts/prepare_raw_data.py

# 2. Run analysis pipeline, data cleaning, and export all 15 visualization charts
python _scripts/run_analysis_pipeline.py

# 3. Build and execute Jupyter Notebook in-place with all outputs
python _scripts/build_jupyter_notebook.py

# 4. Generate official Power BI .pbix file
python _scripts/create_pbix_package.py

# 5. Compile 8-page publication-grade PDF project report
python _scripts/generate_pdf_report.py
```
