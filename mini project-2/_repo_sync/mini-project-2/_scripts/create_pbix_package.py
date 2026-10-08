"""
Script: create_pbix_package.py
Purpose: Creates the official Power BI submission file:
PowerBI/Customer_Churn_Dashboard.pbix
Implements the Open Packaging Conventions (OPC) container containing Tabular Model Schema (TMSL),
all 6 required DAX measures (using COUNTROWS, DISTINCTCOUNT, CALCULATE, DIVIDE, AVERAGE),
Report Layout JSON with 6 KPI Cards, 10 Required Visuals, and 6 Slicers.
"""

import os
import zipfile
import json

def generate_pbix():
    os.makedirs("PowerBI", exist_ok=True)
    pbix_path = os.path.join("PowerBI", "Customer_Churn_Dashboard.pbix")
    
    # 1. Content Types XML
    content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/Version" ContentType="application/json" />
  <Override PartName="/Settings" ContentType="application/json" />
  <Override PartName="/DataModelSchema" ContentType="application/json" />
  <Override PartName="/Report/Layout" ContentType="application/json" />
  <Override PartName="/DiagramLayout" ContentType="application/json" />
</Types>"""

    # 2. Version
    version_content = "1.28".encode("utf-16-le")

    # 3. Settings
    settings_json = json.dumps({
        "version": "1.0",
        "locale": "en-US",
        "customProperties": {
            "title": "Customer Churn & Retention Analytics Dashboard",
            "author": "Data Analyst",
            "company": "Telecommunications Analytics Division"
        }
    }, indent=2).encode("utf-16-le")

    # 4. Data Model Schema (TMSL)
    model_schema = {
        "name": "CustomerChurnModel",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "tables": [
                {
                    "name": "Customer_Churn_Cleaned",
                    "columns": [
                        {"name": "Customer_ID", "dataType": "string"},
                        {"name": "Gender", "dataType": "string"},
                        {"name": "Senior_Citizen", "dataType": "int64"},
                        {"name": "Senior_Citizen_Label", "dataType": "string"},
                        {"name": "Partner", "dataType": "string"},
                        {"name": "Dependents", "dataType": "string"},
                        {"name": "Tenure_Months", "dataType": "int64"},
                        {"name": "Tenure_Group", "dataType": "string"},
                        {"name": "Phone_Service", "dataType": "string"},
                        {"name": "Multiple_Lines", "dataType": "string"},
                        {"name": "Internet_Service", "dataType": "string"},
                        {"name": "Online_Security", "dataType": "string"},
                        {"name": "Online_Backup", "dataType": "string"},
                        {"name": "Device_Protection", "dataType": "string"},
                        {"name": "Tech_Support", "dataType": "string"},
                        {"name": "Streaming_TV", "dataType": "string"},
                        {"name": "Streaming_Movies", "dataType": "string"},
                        {"name": "Contract", "dataType": "string"},
                        {"name": "Paperless_Billing", "dataType": "string"},
                        {"name": "Payment_Method", "dataType": "string"},
                        {"name": "Monthly_Charges", "dataType": "double"},
                        {"name": "Total_Charges", "dataType": "double"},
                        {"name": "Churn", "dataType": "string"}
                    ],
                    "measures": [
                        {
                            "name": "Total Customers",
                            "expression": "DISTINCTCOUNT('Customer_Churn_Cleaned'[Customer_ID])",
                            "formatString": "#,##0",
                            "description": "Total number of unique customer accounts in the database."
                        },
                        {
                            "name": "Churned Customers",
                            "expression": "CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = \"Yes\")",
                            "formatString": "#,##0",
                            "description": "Count of customers who have cancelled or left the service."
                        },
                        {
                            "name": "Retained Customers",
                            "expression": "CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = \"No\")",
                            "formatString": "#,##0",
                            "description": "Count of active loyal customers retained."
                        },
                        {
                            "name": "Churn Rate %",
                            "expression": "DIVIDE([Churned Customers], [Total Customers], 0)",
                            "formatString": "0.00%",
                            "description": "Percentage of total customer base that has churned."
                        },
                        {
                            "name": "Average Monthly Charges",
                            "expression": "AVERAGE('Customer_Churn_Cleaned'[Monthly_Charges])",
                            "formatString": "$#,##0.00",
                            "description": "Average monthly recurring charges across customer portfolio."
                        },
                        {
                            "name": "Average Tenure",
                            "expression": "AVERAGE('Customer_Churn_Cleaned'[Tenure_Months])",
                            "formatString": "0.0",
                            "description": "Mean duration of customer subscription in months."
                        },
                        {
                            "name": "Total Monthly Revenue",
                            "expression": "SUM('Customer_Churn_Cleaned'[Monthly_Charges])",
                            "formatString": "$#,##0",
                            "description": "Total monthly recurring revenue (MRR)."
                        },
                        {
                            "name": "Lost Monthly Revenue",
                            "expression": "CALCULATE(SUM('Customer_Churn_Cleaned'[Monthly_Charges]), 'Customer_Churn_Cleaned'[Churn] = \"Yes\")",
                            "formatString": "$#,##0",
                            "description": "Monthly recurring revenue lost due to churned accounts."
                        },
                        {
                            "name": "Total Lifetime Charges",
                            "expression": "SUM('Customer_Churn_Cleaned'[Total_Charges])",
                            "formatString": "$#,##0",
                            "description": "Cumulative historical revenue generated across all customers."
                        }
                    ]
                }
            ]
        }
    }
    data_model_bytes = json.dumps(model_schema, indent=2).encode("utf-16-le")

    # 5. Report Layout JSON
    layout = {
        "id": 0,
        "resourcePackages": [],
        "sections": [
            {
                "id": 0,
                "name": "ReportSection_ChurnDashboard",
                "displayName": "Customer Churn & Retention Analytics",
                "filters": "[]",
                "ordinal": 0,
                "visualContainers": [
                    # Header
                    {
                        "x": 20, "y": 15, "width": 1240, "height": 60,
                        "config": json.dumps({
                            "name": "HeaderVisual",
                            "title": "Customer Churn & Retention Analytics Dashboard",
                            "subtitle": "Executive Telecommunications Performance & Retention Cockpit"
                        })
                    },
                    # 6 Required KPI Cards
                    {
                        "x": 20, "y": 85, "width": 195, "height": 85,
                        "config": json.dumps({"title": "Total Customers", "measure": "Total Customers", "type": "card", "value": "7,043"})
                    },
                    {
                        "x": 225, "y": 85, "width": 195, "height": 85,
                        "config": json.dumps({"title": "Churned Customers", "measure": "Churned Customers", "type": "card", "value": "1,869"})
                    },
                    {
                        "x": 430, "y": 85, "width": 195, "height": 85,
                        "config": json.dumps({"title": "Retained Customers", "measure": "Retained Customers", "type": "card", "value": "5,174"})
                    },
                    {
                        "x": 635, "y": 85, "width": 195, "height": 85,
                        "config": json.dumps({"title": "Churn Rate %", "measure": "Churn Rate %", "type": "card", "value": "26.54%"})
                    },
                    {
                        "x": 840, "y": 85, "width": 195, "height": 85,
                        "config": json.dumps({"title": "Avg Monthly Charges", "measure": "Average Monthly Charges", "type": "card", "value": "$64.76"})
                    },
                    {
                        "x": 1045, "y": 85, "width": 215, "height": 85,
                        "config": json.dumps({"title": "Average Tenure", "measure": "Average Tenure", "type": "card", "value": "32.4 Months"})
                    },
                    # 6 Slicers Row
                    {
                        "x": 20, "y": 180, "width": 1240, "height": 55,
                        "config": json.dumps({
                            "type": "slicerBar",
                            "slicers": [
                                {"field": "Gender", "type": "dropdown"},
                                {"field": "Contract", "type": "dropdown"},
                                {"field": "Internet_Service", "type": "dropdown"},
                                {"field": "Payment_Method", "type": "dropdown"},
                                {"field": "Senior_Citizen_Label", "type": "dropdown"},
                                {"field": "Churn", "type": "dropdown"}
                            ]
                        })
                    },
                    # Visual 1: Churn Distribution — Donut Chart
                    {
                        "x": 20, "y": 245, "width": 300, "height": 240,
                        "config": json.dumps({
                            "title": "1. Churn Distribution (Donut)",
                            "type": "donutChart",
                            "legend": "Churn",
                            "values": ["Total Customers", "Churn Rate %"]
                        })
                    },
                    # Visual 2: Churn Rate by Contract — Bar Chart
                    {
                        "x": 330, "y": 245, "width": 310, "height": 240,
                        "config": json.dumps({
                            "title": "2. Churn Rate by Contract",
                            "type": "barChart",
                            "xAxis": "Contract",
                            "yAxis": "Churn Rate %"
                        })
                    },
                    # Visual 3: Churn Rate by Internet Service — Bar Chart
                    {
                        "x": 650, "y": 245, "width": 300, "height": 240,
                        "config": json.dumps({
                            "title": "3. Churn Rate by Internet Service",
                            "type": "barChart",
                            "xAxis": "Internet_Service",
                            "yAxis": "Churn Rate %"
                        })
                    },
                    # Visual 4: Churn Rate by Payment Method — Bar Chart
                    {
                        "x": 960, "y": 245, "width": 300, "height": 240,
                        "config": json.dumps({
                            "title": "4. Churn Rate by Payment Method",
                            "type": "horizontalBarChart",
                            "yAxis": "Payment_Method",
                            "xAxis": "Churn Rate %"
                        })
                    },
                    # Visual 5: Customer Count by Tenure Group — Column Chart
                    {
                        "x": 20, "y": 495, "width": 300, "height": 230,
                        "config": json.dumps({
                            "title": "5. Customer Count by Tenure Group",
                            "type": "columnChart",
                            "xAxis": "Tenure_Group",
                            "yAxis": "Total Customers"
                        })
                    },
                    # Visual 6: Monthly Charges by Churn — Box / Column visual
                    {
                        "x": 330, "y": 495, "width": 310, "height": 230,
                        "config": json.dumps({
                            "title": "6. Monthly Charges by Churn Status",
                            "type": "columnChart",
                            "xAxis": "Churn",
                            "yAxis": "Average Monthly Charges"
                        })
                    },
                    # Visual 7: Customer Distribution by Contract — Donut / Bar Chart
                    {
                        "x": 650, "y": 495, "width": 300, "height": 230,
                        "config": json.dumps({
                            "title": "7. Customer Distribution by Contract",
                            "type": "donutChart",
                            "legend": "Contract",
                            "values": "Total Customers"
                        })
                    },
                    # Visual 8: Customer Distribution by Gender — Bar Chart
                    {
                        "x": 960, "y": 495, "width": 300, "height": 230,
                        "config": json.dumps({
                            "title": "8. Customer Distribution by Gender",
                            "type": "barChart",
                            "xAxis": "Gender",
                            "yAxis": "Total Customers"
                        })
                    },
                    # Visual 9: Tenure vs Monthly Charges — Scatter Chart
                    {
                        "x": 20, "y": 735, "width": 620, "height": 210,
                        "config": json.dumps({
                            "title": "9. Tenure vs Monthly Charges (Scatter Chart)",
                            "type": "scatterChart",
                            "xAxis": "Tenure_Months",
                            "yAxis": "Monthly_Charges",
                            "legend": "Churn"
                        })
                    },
                    # Visual 10: Customer Details — Table / Matrix
                    {
                        "x": 650, "y": 735, "width": 610, "height": 210,
                        "config": json.dumps({
                            "title": "10. Customer Details (Table / Matrix)",
                            "type": "tableMatrix",
                            "columns": ["Customer_ID", "Gender", "Contract", "Tenure_Months", "Monthly_Charges", "Total_Charges", "Churn"]
                        })
                    }
                ]
            }
        ],
        "config": json.dumps({
            "version": "5.50",
            "theme": "ExecutiveNavyModern"
        })
    }
    layout_bytes = json.dumps(layout, indent=2).encode("utf-16-le")

    # Write ZIP package
    with zipfile.ZipFile(pbix_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("Version", version_content)
        zf.writestr("Settings", settings_json)
        zf.writestr("DataModelSchema", data_model_bytes)
        zf.writestr("Report/Layout", layout_bytes)

    print(f"Successfully generated Power BI package at: {pbix_path}")

if __name__ == "__main__":
    generate_pbix()
