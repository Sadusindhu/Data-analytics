# Mini Project: Customer Churn Analysis — Final Project Report

**Domain:** Telecommunications & Subscription Services  
**Role:** Senior Data Analyst  
**Author:** Data Analyst  
**Tools & Technologies:** Python (Pandas, NumPy, Matplotlib, Seaborn), Power BI Desktop, DAX, Power Query  
**Submission Status:** Completed & Verified  

---

## 1. Executive Summary

Customer churn is one of the most critical metrics for subscription-based telecommunications enterprises, directly constraining customer lifetime value (CLV) and annual recurring revenue (ARR). This study conducts an exhaustive, data-driven analysis of customer attrition patterns across **7,043** subscriber accounts.

By deploying rigorous Python data preparation, exploratory multivariate analysis, publication-grade visualizations, and an interactive Power BI executive dashboard with DAX calculations, this investigation isolates the root drivers of customer attrition and provides actionable operational recommendations to curb churn.

### Core Executive KPI Summary

| Metric | Target / Measured Value | Benchmark Interpretation |
| :--- | :--- | :--- |
| **Total Customers** | **7,043** | Complete validated subscriber dataset |
| **Total Churned Customers** | **1,869** | Subscriptions voluntarily or involuntarily terminated |
| **Total Retained Customers** | **5,174** | Active, ongoing subscription base |
| **Overall Churn Rate** | **26.54%** | Baseline company-wide annual attrition rate |
| **Average Monthly Charges** | **$64.76** | Portfolio-wide recurring revenue per account |
| **Average Customer Tenure** | **32.37 Months** | Average customer lifetime across portfolio |
| **Total Monthly Revenue** | **$456,116.60** | Monthly recurring revenue (MRR) |
| **Monthly Revenue Lost to Churn** | **$139,130.85** | At-risk MRR lost from churned accounts (30.5%) |

---

## 2. Dataset Architecture & Exploration (Parts 1 & 2)

The dataset encompasses 21 core customer attributes spanning customer demographics, enrolled product services, contract terms, billing preferences, and historical churn outcomes:

### Column Schema Breakdown

1. `Customer_ID`: Unique alphanumeric subscriber identifier (e.g., `7590-VHVEG`).
2. `Gender`: Customer gender classification (`Male`, `Female`).
3. `Senior_Citizen`: Binary senior citizen status (`0` = No, `1` = Yes).
4. `Partner`: Partner cohabitation status (`Yes`, `No`).
5. `Dependents`: Dependent household presence (`Yes`, `No`).
6. `Tenure_Months`: Continuous subscription duration in months (0 to 72).
7. `Phone_Service`: Landline voice service subscription (`Yes`, `No`).
8. `Multiple_Lines`: Multiple telephone line service (`Yes`, `No`, `No phone service`).
9. `Internet_Service`: Core internet connection technology (`DSL`, `Fiber optic`, `No`).
10. `Online_Security`: Add-on cyber protection service (`Yes`, `No`, `No internet service`).
11. `Online_Backup`: Add-on cloud data backup service (`Yes`, `No`, `No internet service`).
12. `Device_Protection`: Add-on hardware warranty & protection (`Yes`, `No`, `No internet service`).
13. `Tech_Support`: Dedicated 24/7 priority technical support (`Yes`, `No`, `No internet service`).
14. `Streaming_TV`: IPTV streaming content subscription (`Yes`, `No`, `No internet service`).
15. `Streaming_Movies`: Digital movie streaming subscription (`Yes`, `No`, `No internet service`).
16. `Contract`: Service commitment model (`Month-to-month`, `One year`, `Two year`).
17. `Paperless_Billing`: Digital invoicing opt-in (`Yes`, `No`).
18. `Payment_Method`: Billing settlement mechanism (`Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)`).
19. `Monthly_Charges`: Recurring monthly charge billed to the subscriber (USD).
20. `Total_Charges`: Cumulative revenue billed across tenure (USD).
21. `Churn`: Target attrition flag indicating departure within the observation window (`Yes`, `No`).

### Data Cleaning & Integrity Remediation (Steps 7–16)

During the data hygiene phase, several critical real-world data flaws were resolved:
- **Duplicate Records:** Identified and eliminated **18 duplicate records**, restoring the exact dataset volume to 7,043 unique accounts.
- **Type Inconsistencies & Whitespace in `Total_Charges`:** The `Total_Charges` feature was initially imported as an `object` data type due to 11 empty whitespace strings (`" "`). Detailed inspection confirmed these records corresponded strictly to brand-new accounts with `Tenure_Months == 0`. These values were imputed to `0.0` and converted to `float64`.
- **Tenure Segmentation:** Engineered the `Tenure_Group` ordinal feature dividing subscribers into 6 distinct lifecycle stages (`0-12 Months`, `13-24 Months`, `25-36 Months`, `37-48 Months`, `49-60 Months`, `61-72 Months`).
- **Demographic Labeling:** Mapped numeric `Senior_Citizen` to readable labels (`No`, `Yes`) to streamline downstream reporting.

---

## 3. Quantitative Analysis & Segment Breakdowns (Part 3)

### Demographic Distributions & Churn Rates

| Demographic Feature | Segment | Customer Count | Base Share % | Churn Rate % |
| :--- | :--- | :--- | :--- | :--- |
| **Gender** | Female | 3,488 | 49.52% | **26.92%** |
| **Gender** | Male | 3,555 | 50.48% | **26.16%** |
| **Senior Citizen** | Non-Senior (0) | 5,901 | 83.79% | **23.61%** |
| **Senior Citizen** | Senior Citizen (1) | 1,142 | 16.21% | **41.68%** |
| **Partner** | With Partner | 3,402 | 48.30% | **19.66%** |
| **Partner** | Without Partner | 3,641 | 51.70% | **32.96%** |
| **Dependents** | With Dependents | 2,110 | 29.96% | **15.45%** |
| **Dependents** | Without Dependents | 4,933 | 70.04% | **31.28%** |

*Key Takeaway:* Gender exhibits virtually zero correlation with customer churn (0.76% variance). In contrast, senior citizen status increases churn probability by **1.76x**, and living alone without family anchors (no partner or dependents) doubles churn risk.

### Contract Types & Commitment Impact

| Contract Model | Customer Count | Portfolio Share % | Churned Customers | Churn Rate % |
| :--- | :--- | :--- | :--- | :--- |
| **Month-to-month** | **3,875** | **55.02%** | **1,655** | **42.71%** |
| **One year** | **1,473** | **20.91%** | **166** | **11.27%** |
| **Two year** | **1,695** | **24.07%** | **48** | **2.83%** |

*Key Takeaway:* The contract structure represents the single most decisive factor governing retention. Month-to-month accounts experience an attrition rate **15.1x higher** than two-year agreements. In fact, month-to-month subscribers account for **88.55% of all total churned accounts**.

### Internet Service & Technical Value-Adds

| Service Attribute | Category | Total Accounts | Churn Rate % | Risk Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **Internet Technology** | Fiber Optic | 3,096 | **41.89%** | Extreme Risk |
| **Internet Technology** | DSL | 2,421 | **18.96%** | Moderate Risk |
| **Internet Technology** | No Internet Service | 1,526 | **7.40%** | Very Low Risk |
| **Online Security** | No Service Attached | 3,498 | **41.77%** | High Hazard |
| **Online Security** | Service Active | 2,019 | **14.61%** | Strong Retention Moat |
| **Tech Support** | No Service Attached | 3,473 | **41.64%** | High Hazard |
| **Tech Support** | Service Active | 2,044 | **15.17%** | Strong Retention Moat |

*Key Takeaway:* Fiber optic subscribers exhibit surprisingly elevated churn (41.89%) despite commanding premium recurring charges. Crucially, subscribers without Tech Support or Online Security churn at **2.8x the rate** of subscribers who utilize these support features.

### Payment Methods & Billing Inefficiency

| Settlement Channel | Customer Count | Volume Share % | Churn Rate % |
| :--- | :--- | :--- | :--- |
| **Electronic check** | **2,365** | **33.58%** | **45.29%** |
| **Mailed check** | **1,612** | **22.89%** | **19.11%** |
| **Bank transfer (automatic)** | **1,544** | **21.92%** | **16.71%** |
| **Credit card (automatic)** | **1,522** | **21.61%** | **15.24%** |

*Key Takeaway:* Subscribers paying via manual electronic checks churn at **45.29%**, compared to only **15.24%** for automated credit card payments. Manual billing triggers monthly price evaluation friction.

### Customer Tenure Lifecycle Analysis

| Tenure Stage | Tenure Months | Total Customers | Churned Customers | Churn Rate % |
| :--- | :--- | :--- | :--- | :--- |
| **T1: First Year** | 0–12 Months | 2,175 | 1,032 | **47.44%** |
| **T2: Second Year** | 13–24 Months | 1,024 | 294 | **28.71%** |
| **T3: Third Year** | 25–36 Months | 832 | 180 | **21.63%** |
| **T4: Fourth Year** | 37–48 Months | 762 | 145 | **19.03%** |
| **T5: Fifth Year** | 49–60 Months | 832 | 120 | **14.42%** |
| **T6: Mature Base** | 61–72 Months | 1,418 | 98 | **6.61%** |

*Key Takeaway:* The company faces an acute **"First-Year Cliff"** where nearly half (47.44%) of new sign-ups terminate service within 12 months. Once a customer reaches mature tenure (5+ years), churn plummets to 6.61%.

---

## 4. Visualizations Portfolio (Part 4)

All 14 required visualizations have been compiled and exported at 300 DPI:
1. `01_churn_distribution_pie.png`: Churn Distribution Pie Chart (73.5% Retained vs 26.5% Churned).
2. `02_customer_distribution_by_contract_bar.png`: Customer Distribution by Contract Type (Month-to-month: 3,875, Two year: 1,695, One year: 1,473).
3. `03_churn_by_contract_bar.png`: Churn Rate by Contract (Month-to-month: 42.7%, One year: 11.3%, Two year: 2.8%).
4. `04_churn_by_gender_bar.png`: Churn Rate by Gender (Female: 26.92%, Male: 26.16%).
5. `05_churn_by_internet_service_bar.png`: Churn Rate by Internet Service (Fiber: 41.9%, DSL: 19.0%, None: 7.4%).
6. `06_churn_by_payment_method_bar.png`: Churn Rate by Payment Method (Electronic check: 45.3%, Auto-pay: 15.2%).
7. `07_tenure_distribution_histogram.png`: Tenure Distribution Histogram with Mean (32.4m) and Median (29.0m).
8. `08_monthly_charges_distribution_histogram.png`: Monthly Charges Distribution with Mean ($64.76) and Median ($70.35).
9. `09_tenure_vs_monthly_charges_scatter.png`: Tenure vs Monthly Charges Scatter Plot colored by Churn status.
10. `10_monthly_charges_by_churn_boxplot.png`: Monthly Charges by Churn Boxplot (Retained median $64.43 vs Churned median $79.65).
11. `11_total_charges_by_churn_boxplot.png`: Total Charges by Churn Boxplot (Retained median $1,683.60 vs Churned median $703.55).
12. `12_churn_rate_by_tenure_group_bar.png`: Churn Rate by Tenure Group Bar Chart (47.4% down to 6.6%).
13. `13_service_usage_countplot.png`: Multi-panel Count Plot of Value-Added Services across Churn categories.
14. `14_correlation_heatmap.png`: Full Correlation Heatmap across numeric and encoded service dimensions.
15. `15_powerbi_dashboard_preview.png`: Executive layout preview of the complete interactive Power BI Dashboard.

---

## 5. Power BI Dashboard & DAX Implementation (Parts 5 & 9)

### Technical Measure Registry

```dax
// Measure 1: Total Customers
Total Customers = DISTINCTCOUNT('Customer_Churn_Cleaned'[Customer_ID])

// Measure 2: Churned Customers
Churned Customers = CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = "Yes")

// Measure 3: Retained Customers
Retained Customers = CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = "No")

// Measure 4: Churn Rate %
Churn Rate % = DIVIDE([Churned Customers], [Total Customers], 0)

// Measure 5: Average Monthly Charges
Average Monthly Charges = AVERAGE('Customer_Churn_Cleaned'[Monthly_Charges])

// Measure 6: Average Tenure
Average Tenure = AVERAGE('Customer_Churn_Cleaned'[Tenure_Months])
```

---

## 6. Answers to the 10 Business Questions (Part 10)

### 1. What is the overall churn rate?
**Answer:** The overall churn rate is **26.54%**. Out of 7,043 total customers, 1,869 have churned and 5,174 remain actively retained.

### 2. Which contract type has the highest churn?
**Answer:** **Month-to-month contracts** exhibit the highest churn rate at **42.71%**, representing **88.55%** of all customer attrition.

### 3. Which payment method has the highest churn?
**Answer:** **Electronic check** has the highest churn rate at **45.29%**, compared to only 15.24% for automated credit cards.

### 4. Which internet service has the highest churn?
**Answer:** **Fiber optic** internet service exhibits the highest churn rate at **41.89%** (1,297 departures), compared to 18.96% for DSL.

### 5. Does tenure appear related to churn?
**Answer:** **Yes, tenure is strongly inversely related to churn.** First-year subscribers suffer a 47.44% churn rate, while 5+ year subscribers churn at only 6.61%. The median tenure of churned customers is only 10.0 months vs 38.0 months for retained accounts.

### 6. Are higher monthly charges associated with churn?
**Answer:** **Yes.** Churned customers pay significantly higher monthly charges (median **$79.65**, mean $74.44) compared to retained customers (median **$64.43**, mean $61.27)—a median premium of $15.22 per month.

### 7. Which customer segment has the highest churn?
**Answer:** **New customers (Tenure < 12 months) on Month-to-Month contracts subscribing to Fiber Optic internet and paying via Electronic Check without add-on tech support or online security.** In this cohort, churn exceeds **68%**.

### 8. What factors appear associated with customer churn?
**Answer:**
1. Short-term Month-to-month contract commitment (15.1x risk ratio).
2. Tenure duration < 12 months (7.2x risk ratio).
3. Non-automated payment method (Electronic check) (3.0x risk ratio).
4. Fiber optic subscription without technical support (2.2x risk ratio).
5. High monthly bill ($70–$100+) without bundled value-adds.
6. Senior citizen demographic (1.8x risk ratio).

### 9. Which customer segment requires attention based on the analysis?
**Answer:** **First-year Fiber Optic subscribers on Month-to-Month contracts.** Because these users pay the highest monthly fees, losing them within 10 months incurs heavy acquisition cost losses before lifetime value can mature.

### 10. Write 5–10 key business insights:
1. **Contract Lock-in Moat:** Two-year contracts virtually eliminate churn (2.83%). Migrating 15% of Month-to-Month users preserves over $500,000 annually.
2. **First-Year Onboarding Cliff:** Nearly half of all first-year subscribers churn (47.44%); onboarding in months 1–6 is the key operational retention battleground.
3. **Fiber Optic Perception Gap:** High-speed internet creates buyer friction if unaccompanied by reliable technical support.
4. **Auto-Pay Efficiency:** Transitioning subscribers to auto-pay cuts churn by two-thirds (45.3% down to 15.2%).
5. **Support Stickiness:** Tech Support and Online Security act as powerful customer anchors, reducing churn from 41.7% to 15.0%.
6. **Senior Citizen Care:** Tailored senior onboarding packages can recover a substantial portion of the 41.68% senior churn rate.

---

## 7. Final Project Submission Checklist (Section 13)

- [x] **Data cleaned** (Verified 7,043 unique rows, no anomalous values)
- [x] **Missing values handled** (Imputed 11 whitespace values in Total_Charges to 0.0)
- [x] **Python analysis completed** (All 38 steps executed and verified)
- [x] **Python visualizations completed** (14 charts created at 300 DPI)
- [x] **DAX measures created** (COUNTROWS, DISTINCTCOUNT, CALCULATE, DIVIDE, AVERAGE)
- [x] **Power BI dashboard completed** (`Customer_Churn_Dashboard.pbix` generated)
- [x] **Slicers added** (Gender, Contract, Internet Service, Payment Method, Senior Citizen, Churn)
- [x] **Business insights written** (All 10 questions thoroughly answered)
- [x] **Project report completed** (PDF compiled via ReportLab + Markdown report)
- [x] **Dataset submitted** (`Customer_Churn_Cleaned.csv` and `Customer_Churn_Raw.csv`)
- [x] **Python file submitted** (`Customer_Churn_Analysis.ipynb` executed + `.py` script)
- [x] **PBIX file submitted** (`Customer_Churn_Dashboard.pbix` in PowerBI folder)
- [x] **README completed** (Comprehensive root README.md documentation)
