# Power BI Dashboard Implementation Guide
## Project: Loan Default & Credit Risk Analytics Dashboard

---

### 1. Overview & Data Source Connection

This guide provides step-by-step instructions to assemble the interactive **"Loan Default & Credit Risk Analytics Dashboard"** in Microsoft Power BI Desktop using the processed dataset.

- **Data File:** `Dataset/Loan_Credit_Risk_Cleaned.csv`
- **Rows:** 5,000 records
- **Columns:** 27 fields
- **Granularity:** 1 record per loan agreement / customer

#### Steps to Import Data:
1. Open **Microsoft Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Select `Dataset/Loan_Credit_Risk_Cleaned.csv` and click **Load** (or **Transform Data** to verify schema in Power Query).
4. Verify column data types:
   - `Customer_ID`, `Loan_ID`, `Gender`, `Education`, `Employment_Status`, `Marital_Status`, `Loan_Type`, `Credit_History`, `Property_Ownership`, `Region`, `Loan_Status`, `Default_Status`, `Credit_Score_Group`, `Income_Group`: **Text**
   - `Age`, `Dependents`, `Existing_Loans`, `Loan_Term_Months`, `Previous_Defaults`, `Default_Numeric`: **Whole Number**
   - `Annual_Income`, `Credit_Score`, `Loan_Amount`, `Interest_Rate`, `Monthly_Installment`, `Debt_to_Income_Ratio`: **Decimal Number / Fixed Decimal (Currency)**

---

### 2. DAX Measures Specification

In the **Report View**, create a dedicated Measures table:
- Click **Enter Data**, name the table `_Key_Measures`, and click **Load**.
- Right-click `_Key_Measures` and select **New Measure**. Enter each formula below:

```dax
// -------------------------------------------------------------
// 1. Total Customers
// -------------------------------------------------------------
Total Customers = 
DISTINCTCOUNT('Loan_Credit_Risk_Cleaned'[Customer_ID])
```
*Formatting:* Whole Number with thousands separator (e.g. `5,000`).

```dax
// -------------------------------------------------------------
// 2. Total Loans
// -------------------------------------------------------------
Total Loans = 
COUNTROWS('Loan_Credit_Risk_Cleaned')
```
*Formatting:* Whole Number with thousands separator (e.g. `5,000`).

```dax
// -------------------------------------------------------------
// 3. Defaulted Loans
// -------------------------------------------------------------
Defaulted Loans = 
CALCULATE(
    COUNTROWS('Loan_Credit_Risk_Cleaned'),
    'Loan_Credit_Risk_Cleaned'[Default_Status] = "Yes"
)
```
*Formatting:* Whole Number (e.g. `955`).

```dax
// -------------------------------------------------------------
// 4. Non-Defaulted Loans
// -------------------------------------------------------------
Non-Defaulted Loans = 
CALCULATE(
    COUNTROWS('Loan_Credit_Risk_Cleaned'),
    'Loan_Credit_Risk_Cleaned'[Default_Status] = "No"
)
```
*Formatting:* Whole Number (e.g. `4,045`).

```dax
// -------------------------------------------------------------
// 5. Default Rate %
// -------------------------------------------------------------
Default Rate % = 
DIVIDE(
    [Defaulted Loans],
    [Total Loans],
    0
)
```
*Formatting:* Percentage with 2 decimal places (e.g. `19.10%`).

```dax
// -------------------------------------------------------------
// 6. Average Loan Amount
// -------------------------------------------------------------
Average Loan Amount = 
AVERAGE('Loan_Credit_Risk_Cleaned'[Loan_Amount])
```
*Formatting:* Currency (`$#,##0`).

```dax
// -------------------------------------------------------------
// 7. Average Credit Score
// -------------------------------------------------------------
Average Credit Score = 
AVERAGE('Loan_Credit_Risk_Cleaned'[Credit_Score])
```
*Formatting:* Decimal Number (`#0.0`).

```dax
// -------------------------------------------------------------
// 8. Average Annual Income
// -------------------------------------------------------------
Average Annual Income = 
AVERAGE('Loan_Credit_Risk_Cleaned'[Annual_Income])
```
*Formatting:* Currency (`$#,##0`).

---

### 3. Dashboard Layout & Visuals Setup

#### Dashboard Canvas Configuration:
- **Canvas Size:** 16:9 (1920 x 1080 px or 1280 x 720 px)
- **Background Color:** `#F8F9FA` (Off-White / Light Grey)
- **Card Background:** `#FFFFFF` (White) with subtle border shadow (Grey `#E0E0E0`)
- **Accent Primary:** Dark Navy (`#1A365D`)
- **Accent Danger (Default):** Crimson Red (`#C53030`)
- **Accent Success (Performing):** Forest Green (`#2F855A`)

---

#### Section A: Header & KPI Summary Cards (Top Row)
Place 7 **Card** (or **New Card**) visuals horizontally across the top:
1. **Total Customers:** `[Total Customers]` (`5,000`)
2. **Total Loans:** `[Total Loans]` (`5,000`)
3. **Defaulted Loans:** `[Defaulted Loans]` (`955`)
4. **Default Rate %:** `[Default Rate %]` (`19.10%`) - *Callout value colored Crimson Red*
5. **Avg Loan Amount:** `[Average Loan Amount]` (`$41,449`)
6. **Avg Credit Score:** `[Average Credit Score]` (`667.1`)
7. **Avg Annual Income:** `[Average Annual Income]` (`$69,486`)

---

#### Section B: Slicers (Left-Hand Filter Sidebar or Filter Ribbon)
Add 7 **Slicer** visuals (configured as Dropdown or Tile/Buttons):
1. **Gender:** `'Loan_Credit_Risk_Cleaned'[Gender]`
2. **Education:** `'Loan_Credit_Risk_Cleaned'[Education]`
3. **Employment Status:** `'Loan_Credit_Risk_Cleaned'[Employment_Status]`
4. **Loan Type:** `'Loan_Credit_Risk_Cleaned'[Loan_Type]`
5. **Region:** `'Loan_Credit_Risk_Cleaned'[Region]`
6. **Default Status:** `'Loan_Credit_Risk_Cleaned'[Default_Status]`
7. **Credit Score Group:** `'Loan_Credit_Risk_Cleaned'[Credit_Score_Group]`

---

#### Section C: Visualizations Grid (Body Area)

| # | Visual Type | Title | X-Axis / Category | Y-Axis / Values | Legend / Details | Notes / Insights |
|---|---|---|---|---|---|---|
| **1** | **Donut Chart** | Loan Default Distribution | `Default_Status` | `[Total Loans]` | `Default_Status` | Green (`No` = 80.9%), Red (`Yes` = 19.1%) |
| **2** | **Clustered Bar Chart** | Default Rate by Loan Type | `[Default Rate %]` | `Loan_Type` | - | Sort descending: Home (34.9%) & Business (23.9%) highest |
| **3** | **Clustered Bar Chart** | Default Rate by Employment Status | `[Default Rate %]` | `Employment_Status` | - | Unemployed exhibits 45.1% default rate |
| **4** | **Clustered Column Chart**| Default Rate by Credit Score Group | `Credit_Score_Group` | `[Default Rate %]` | - | Ordered Poor to Excellent; steep drop from 37.5% to 2.9% |
| **5** | **Clustered Bar Chart** | Default Rate by Income Group | `[Default Rate %]` | `Income_Group` | - | Low (<$40k) has 33.9% default rate |
| **6** | **Clustered Column Chart**| Total Loan Amount by Loan Type | `Loan_Type` | `SUM(Loan_Amount)` | - | Shows Home & Business represent major capital exposure |
| **7** | **Clustered Bar Chart** | Average Loan Amount by Region | `[Average Loan Amount]`| `Region` | - | Evaluates regional credit exposure parity |
| **8** | **Histogram / Column** | Credit Score Distribution | `Credit_Score (binned 25)`| `[Total Loans]` | - | Normal distribution centered around 667 |
| **9** | **Scatter Chart** | Income vs Loan Amount | `Annual_Income` | `Loan_Amount` | `Default_Status` | Highlights concentration of defaults in high-leverage quadrant |
| **10**| **Table / Matrix** | Detailed Loan Performance Table | Rows: `Customer_ID`, `Loan_Type`, `Region`, `Credit_Score`, `Annual_Income`, `DTI`, `Loan_Amount`, `Default_Status` | - | Set to top 50 rows or searchable |
| **11**| **Area / Line Chart** | Default Trend / Distribution by Term | `Loan_Term_Months` | `[Default Rate %]` | - | Evaluates risk progression over term maturities (12m to 60m) |

---

### 4. Interactive Cross-Filtering Capabilities

- Clicking **"Home"** in the *Loan Type* visual filters the entire dashboard to display Home loan demographics, regional distribution, and average borrower income ($65k+).
- Selecting **"Unemployed"** in the slicer immediately flags the high default exposure (45.1%) and low credit score concentration.
- Selecting **"Poor (<580)"** credit score group filters the portfolio to isolate subprime lending performance.
