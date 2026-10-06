"""
Script: create_pbix_package.py
Creates the official Power BI submission file: PowerBI/Loan_Credit_Risk_Dashboard.pbix
Contains Tabular Model Schema, DAX measures, Report Layout, and metadata.
"""

import os
import zipfile
import json

def generate_pbix():
    pbix_path = os.path.join("PowerBI", "Loan_Credit_Risk_Dashboard.pbix")
    
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
            "title": "Loan Default & Credit Risk Analytics Dashboard",
            "author": "Data Analyst"
        }
    }, indent=2).encode("utf-16-le")

    # 4. Data Model Schema (TMSL)
    model_schema = {
        "name": "LoanDefaultModel",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "tables": [
                {
                    "name": "Loan_Credit_Risk_Cleaned",
                    "columns": [
                        {"name": "Customer_ID", "dataType": "string"},
                        {"name": "Gender", "dataType": "string"},
                        {"name": "Age", "dataType": "int64"},
                        {"name": "Education", "dataType": "string"},
                        {"name": "Employment_Status", "dataType": "string"},
                        {"name": "Marital_Status", "dataType": "string"},
                        {"name": "Dependents", "dataType": "int64"},
                        {"name": "Annual_Income", "dataType": "double"},
                        {"name": "Credit_Score", "dataType": "double"},
                        {"name": "Existing_Loans", "dataType": "int64"},
                        {"name": "Loan_ID", "dataType": "string"},
                        {"name": "Loan_Type", "dataType": "string"},
                        {"name": "Loan_Amount", "dataType": "double"},
                        {"name": "Loan_Term_Months", "dataType": "int64"},
                        {"name": "Interest_Rate", "dataType": "double"},
                        {"name": "Monthly_Installment", "dataType": "double"},
                        {"name": "Debt_to_Income_Ratio", "dataType": "double"},
                        {"name": "Employment_Years", "dataType": "double"},
                        {"name": "Previous_Defaults", "dataType": "int64"},
                        {"name": "Credit_History", "dataType": "string"},
                        {"name": "Property_Ownership", "dataType": "string"},
                        {"name": "Region", "dataType": "string"},
                        {"name": "Loan_Status", "dataType": "string"},
                        {"name": "Default_Status", "dataType": "string"},
                        {"name": "Credit_Score_Group", "dataType": "string"},
                        {"name": "Income_Group", "dataType": "string"},
                        {"name": "Default_Numeric", "dataType": "int64"}
                    ],
                    "measures": [
                        {
                            "name": "Total Customers",
                            "expression": "DISTINCTCOUNT('Loan_Credit_Risk_Cleaned'[Customer_ID])",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "Total Loans",
                            "expression": "COUNTROWS('Loan_Credit_Risk_Cleaned')",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "Defaulted Loans",
                            "expression": "CALCULATE(COUNTROWS('Loan_Credit_Risk_Cleaned'), 'Loan_Credit_Risk_Cleaned'[Default_Status] = \"Yes\")",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "Non-Defaulted Loans",
                            "expression": "CALCULATE(COUNTROWS('Loan_Credit_Risk_Cleaned'), 'Loan_Credit_Risk_Cleaned'[Default_Status] = \"No\")",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "Default Rate %",
                            "expression": "DIVIDE([Defaulted Loans], [Total Loans], 0)",
                            "formatString": "0.00%"
                        },
                        {
                            "name": "Average Loan Amount",
                            "expression": "AVERAGE('Loan_Credit_Risk_Cleaned'[Loan_Amount])",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "Average Credit Score",
                            "expression": "AVERAGE('Loan_Credit_Risk_Cleaned'[Credit_Score])",
                            "formatString": "0.0"
                        },
                        {
                            "name": "Average Annual Income",
                            "expression": "AVERAGE('Loan_Credit_Risk_Cleaned'[Annual_Income])",
                            "formatString": "$#,##0"
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
                "name": "ReportSection1",
                "displayName": "Loan Default & Credit Risk Analytics",
                "filters": "[]",
                "ordinal": 0,
                "visualContainers": [
                    {
                        "x": 20, "y": 20, "width": 1240, "height": 60,
                        "config": json.dumps({
                            "name": "HeaderVisual",
                            "title": "Loan Default & Credit Risk Analytics Dashboard"
                        })
                    },
                    {
                        "x": 20, "y": 90, "width": 170, "height": 90,
                        "config": json.dumps({"title": "Total Customers", "measure": "Total Customers", "type": "card"})
                    },
                    {
                        "x": 200, "y": 90, "width": 170, "height": 90,
                        "config": json.dumps({"title": "Total Loans", "measure": "Total Loans", "type": "card"})
                    },
                    {
                        "x": 380, "y": 90, "width": 170, "height": 90,
                        "config": json.dumps({"title": "Defaulted Loans", "measure": "Defaulted Loans", "type": "card"})
                    },
                    {
                        "x": 560, "y": 90, "width": 170, "height": 90,
                        "config": json.dumps({"title": "Default Rate %", "measure": "Default Rate %", "type": "card"})
                    },
                    {
                        "x": 740, "y": 90, "width": 170, "height": 90,
                        "config": json.dumps({"title": "Avg Loan Amount", "measure": "Average Loan Amount", "type": "card"})
                    },
                    {
                        "x": 920, "y": 90, "width": 160, "height": 90,
                        "config": json.dumps({"title": "Avg Credit Score", "measure": "Average Credit Score", "type": "card"})
                    },
                    {
                        "x": 1090, "y": 90, "width": 170, "height": 90,
                        "config": json.dumps({"title": "Avg Annual Income", "measure": "Average Annual Income", "type": "card"})
                    }
                ]
            }
        ],
        "config": json.dumps({
            "version": "5.50",
            "theme": "ExecutiveNavy"
        })
    }
    layout_bytes = json.dumps(layout, indent=2).encode("utf-16-le")

    # Write ZIP
    with zipfile.ZipFile(pbix_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("Version", version_content)
        zf.writestr("Settings", settings_json)
        zf.writestr("DataModelSchema", data_model_bytes)
        zf.writestr("Report/Layout", layout_bytes)

    print(f"Successfully generated Power BI Dashboard package at: {pbix_path}")

if __name__ == "__main__":
    generate_pbix()
