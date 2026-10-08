# Power BI DAX Measures & Visual Implementation Guide

**Dashboard Title:** Customer Churn & Retention Analytics Dashboard  
**Dataset:** `Customer_Churn_Cleaned.csv` (7,043 rows, 23 columns)  
**Target File:** `PowerBI/Customer_Churn_Dashboard.pbix`

---

## 1. Executive Overview
This guide provides complete technical specifications for the **Customer Churn & Retention Analytics Dashboard** built in Power BI Desktop. It details:
1. Power Query M-Code data ingestion and schema validation.
2. Required DAX measures demonstrating functions specified in Section 9 (`COUNTROWS`, `DISTINCTCOUNT`, `CALCULATE`, `DIVIDE`, `AVERAGE`, `SUM`).
3. Setup instructions for the 6 KPI cards, 6 slicers, and 10 interactive report visuals.

---

## 2. Power Query Data Transformation (M-Code)

To load and ensure proper data modeling in Power BI Desktop:
1. Open Power BI Desktop -> **Get Data** -> **Text/CSV** -> Select `Dataset/Customer_Churn_Cleaned.csv`.
2. Open **Power Query Editor** -> In **Advanced Editor**, review or paste the transformation script below:

```powerquery
let
    Source = Csv.Document(File.Contents("Dataset\Customer_Churn_Cleaned.csv"), [Delimiter=",", Columns=23, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Customer_ID", type text},
        {"Gender", type text},
        {"Senior_Citizen", Int64.Type},
        {"Senior_Citizen_Label", type text},
        {"Partner", type text},
        {"Dependents", type text},
        {"Tenure_Months", Int64.Type},
        {"Tenure_Group", type text},
        {"Phone_Service", type text},
        {"Multiple_Lines", type text},
        {"Internet_Service", type text},
        {"Online_Security", type text},
        {"Online_Backup", type text},
        {"Device_Protection", type text},
        {"Tech_Support", type text},
        {"Streaming_TV", type text},
        {"Streaming_Movies", type text},
        {"Contract", type text},
        {"Paperless_Billing", type text},
        {"Payment_Method", type text},
        {"Monthly_Charges", type number},
        {"Total_Charges", type number},
        {"Churn", type text}
    })
in
    #"Changed Type"
```

3. Click **Close & Apply**.

---

## 3. Required DAX Measures (Section 9 Compliance)

Create a dedicated Measures Table named `_Measures` or add the following DAX measures to table `Customer_Churn_Cleaned`:

### Measure 1: Total Customers
*Function used:* `DISTINCTCOUNT`
```dax
Total Customers = 
DISTINCTCOUNT(Customer_Churn_Cleaned[Customer_ID])
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Counts unique customer IDs across the filtered dataset.

### Measure 2: Churned Customers
*Functions used:* `CALCULATE`, `COUNTROWS`
```dax
Churned Customers = 
CALCULATE(
    COUNTROWS(Customer_Churn_Cleaned),
    Customer_Churn_Cleaned[Churn] = "Yes"
)
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Filters and counts all customer records where Churn equals "Yes".

### Measure 3: Retained Customers
*Functions used:* `CALCULATE`, `COUNTROWS`
```dax
Retained Customers = 
CALCULATE(
    COUNTROWS(Customer_Churn_Cleaned),
    Customer_Churn_Cleaned[Churn] = "No"
)
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Filters and counts active subscribers who have not terminated service.

### Measure 4: Churn Rate %
*Functions used:* `DIVIDE`
```dax
Churn Rate % = 
DIVIDE(
    [Churned Customers],
    [Total Customers],
    0
)
```
- **Format:** Percentage (`0.00%`)
- **Description:** Ratio of churned customers to total customers with zero-division protection.

### Measure 5: Average Monthly Charges
*Functions used:* `AVERAGE`
```dax
Average Monthly Charges = 
AVERAGE(Customer_Churn_Cleaned[Monthly_Charges])
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** The arithmetic mean of recurring monthly charges billed to customers.

### Measure 6: Average Tenure
*Functions used:* `AVERAGE`
```dax
Average Tenure = 
AVERAGE(Customer_Churn_Cleaned[Tenure_Months])
```
- **Format:** Decimal Number (`0.0`)
- **Description:** The mean customer subscription duration in months.

---

### Additional Business Intelligence DAX Measures

```dax
Total Monthly Revenue = 
SUM(Customer_Churn_Cleaned[Monthly_Charges])
```
- **Format:** Currency (`$#,##0`)

```dax
Lost Monthly Revenue = 
CALCULATE(
    SUM(Customer_Churn_Cleaned[Monthly_Charges]),
    Customer_Churn_Cleaned[Churn] = "Yes"
)
```
- **Format:** Currency (`$#,##0`)

```dax
Total Lifetime Charges = 
SUM(Customer_Churn_Cleaned[Total_Charges])
```
- **Format:** Currency (`$#,##0`)

```dax
High Spender Flag = 
IF(Customer_Churn_Cleaned[Monthly_Charges] >= 70, "High Spender ($70+)", "Standard Spender (<$70)")
```

---

## 4. Required KPI Cards Setup

| KPI Card | Measure | Display Value | Target Color |
| :--- | :--- | :--- | :--- |
| **1. Total Customers** | `[Total Customers]` | `7,043` | Blue `#38BDF8` |
| **2. Churned Customers** | `[Churned Customers]` | `1,869` | Coral/Red `#EF4444` |
| **3. Retained Customers** | `[Retained Customers]` | `5,174` | Emerald/Green `#10B981` |
| **4. Churn Rate %** | `[Churn Rate %]` | `26.54%` | Amber/Orange `#F59E0B` |
| **5. Average Monthly Charges** | `[Average Monthly Charges]` | `$64.76` | Indigo `#818CF8` |
| **6. Average Tenure** | `[Average Tenure]` | `32.4 Months` | Cyan `#06B6D4` |

---

## 5. Required Interactive Slicers

Add a top navigation slicer bar with the following 6 slicers:
1. **Gender:** Dropdown / Tile slicer (`Customer_Churn_Cleaned[Gender]`)
2. **Contract:** Dropdown / Tile slicer (`Customer_Churn_Cleaned[Contract]`)
3. **Internet Service:** Dropdown / Tile slicer (`Customer_Churn_Cleaned[Internet_Service]`)
4. **Payment Method:** Dropdown / Tile slicer (`Customer_Churn_Cleaned[Payment_Method]`)
5. **Senior Citizen:** Dropdown / Tile slicer (`Customer_Churn_Cleaned[Senior_Citizen_Label]`)
6. **Churn:** Dropdown / Tile slicer (`Customer_Churn_Cleaned[Churn]`)

---

## 6. Required Power BI Visuals Specification

### Visual 1: Churn Distribution — Donut Chart
- **Visual Type:** Donut Chart
- **Legend:** `Customer_Churn_Cleaned[Churn]`
- **Values:** `[Total Customers]`
- **Details/Tooltip:** `[Churn Rate %]`
- **Colors:** Retained (`#10B981`), Churned (`#EF4444`)

### Visual 2: Churn Rate by Contract — Bar Chart
- **Visual Type:** Clustered Bar / Column Chart
- **X-Axis:** `Customer_Churn_Cleaned[Contract]` (Month-to-month, One year, Two year)
- **Y-Axis:** `[Churn Rate %]`
- **Data Labels:** Enabled (`42.7%`, `11.3%`, `2.8%`)

### Visual 3: Churn Rate by Internet Service — Bar Chart
- **Visual Type:** Clustered Column Chart
- **X-Axis:** `Customer_Churn_Cleaned[Internet_Service]` (DSL, Fiber optic, No)
- **Y-Axis:** `[Churn Rate %]`
- **Data Labels:** Enabled (`19.0%`, `41.9%`, `7.4%`)

### Visual 4: Churn Rate by Payment Method — Bar Chart
- **Visual Type:** Horizontal Clustered Bar Chart
- **Y-Axis:** `Customer_Churn_Cleaned[Payment_Method]`
- **X-Axis:** `[Churn Rate %]`
- **Sort:** Descending by Churn Rate (Electronic check: `45.3%`)

### Visual 5: Customer Count by Tenure Group — Column Chart
- **Visual Type:** Clustered Column Chart
- **X-Axis:** `Customer_Churn_Cleaned[Tenure_Group]` (0-12m, 13-24m, 25-36m, 37-48m, 49-60m, 61-72m)
- **Y-Axis:** `[Total Customers]`
- **Data Labels:** Enabled

### Visual 6: Monthly Charges by Churn — Box / Column Visual
- **Visual Type:** Column Chart / Box Plot Custom Visual
- **X-Axis:** `Customer_Churn_Cleaned[Churn]`
- **Y-Axis:** `[Average Monthly Charges]`
- **Values:** Retained: `$61.27`, Churned: `$74.44`

### Visual 7: Customer Distribution by Contract — Donut / Bar Chart
- **Visual Type:** Donut Chart
- **Legend:** `Customer_Churn_Cleaned[Contract]`
- **Values:** `[Total Customers]`
- **Data Labels:** Category & Percent of Total (Month-to-month: `55.0%`, Two year: `24.1%`, One year: `20.9%`)

### Visual 8: Customer Distribution by Gender — Bar Chart
- **Visual Type:** Clustered Bar Chart
- **X-Axis:** `Customer_Churn_Cleaned[Gender]`
- **Y-Axis:** `[Total Customers]`
- **Data Labels:** Male: `3,555` (50.5%), Female: `3,488` (49.5%)

### Visual 9: Tenure vs Monthly Charges — Scatter Chart
- **Visual Type:** Scatter Chart
- **X-Axis:** `Customer_Churn_Cleaned[Tenure_Months]`
- **Y-Axis:** `Customer_Churn_Cleaned[Monthly_Charges]`
- **Legend:** `Customer_Churn_Cleaned[Churn]`
- **Tooltips:** `Customer_ID`, `Contract`, `Total_Charges`

### Visual 10: Customer Details — Table / Matrix
- **Visual Type:** Table / Matrix
- **Columns / Fields:**
  1. `Customer_ID`
  2. `Gender`
  3. `Contract`
  4. `Tenure_Months`
  5. `Monthly_Charges`
  6. `Total_Charges`
  7. `Churn`
- **Features:** Conditional formatting applied on `Churn` column (Green for No, Red for Yes).

---

## 7. Color Theme Palette Specification
- **Canvas Background:** Modern Dark Navy `#0F172A` (or Crisp White `#F8FAFC` for Light Theme)
- **Card Background:** Deep Slate `#1E293B`
- **Accent Red (Churn):** `#EF4444` / `#DC2626`
- **Accent Green (Retained):** `#10B981` / `#059669`
- **Primary Brand Blue:** `#2563EB` / `#38BDF8`
- **Warning Amber:** `#F59E0B`
- **Text High-Contrast:** `#FFFFFF` (Primary), `#94A3B8` (Secondary)
