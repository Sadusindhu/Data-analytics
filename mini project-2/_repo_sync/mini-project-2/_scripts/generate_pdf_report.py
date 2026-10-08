"""
Script: generate_pdf_report.py
Purpose: Generates the official, publication-grade executive project report in PDF format:
Report/Customer_Churn_Project_Report.pdf

Complies with all guidelines from Sections 1 through 13 of the project brief.
Uses ReportLab Platypus engine with dynamic two-pass page numbering, structured tables,
and embedded high-resolution visual charts.
"""

import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "CUSTOMER CHURN & RETENTION ANALYTICS — PROJECT REPORT")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "TELECOM ANALYTICS DIVISION")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Confidential — Customer Retention & Business Intelligence Evaluation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()


def build_pdf_report():
    os.makedirs("Report", exist_ok=True)
    pdf_path = os.path.join("Report", "Customer_Churn_Project_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Color Palette
    PRIMARY = colors.HexColor("#0F2942")     # Deep Corporate Navy
    SECONDARY = colors.HexColor("#0284C7")   # Modern Sky Blue
    ACCENT_RED = colors.HexColor("#DC2626")  # Danger / Churn Red
    ACCENT_GREEN = colors.HexColor("#10B981")# Success Green
    TEXT_DARK = colors.HexColor("#1E293B")   # Slate 800
    MUTED = colors.HexColor("#64748B")       # Slate 500
    BG_LIGHT = colors.HexColor("#F8FAFC")    # Slate 50
    BORDER_COLOR = colors.HexColor("#E2E8F0")# Slate 200

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=MUTED,
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        spaceAfter=5
    )
    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=TEXT_DARK
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=PRIMARY
    )
    table_cell_white = ParagraphStyle(
        'TableCellWhite',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )
    caption_style = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=MUTED,
        alignment=1, # Center
        spaceBefore=3,
        spaceAfter=8
    )

    story = []

    # ---------------------------------------------------------
    # COVER / HEADER BLOCK
    # ---------------------------------------------------------
    story.append(Paragraph("MINI PROJECT 2: CUSTOMER CHURN ANALYSIS", title_style))
    story.append(Paragraph("Executive Analytics & Customer Retention Report | Subscription Intelligence", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    # Metadata Card Table
    meta_data = [
        [
            Paragraph("<b>Project Domain:</b> Telecommunications", table_cell),
            Paragraph("<b>Role:</b> Senior Data Analyst", table_cell),
            Paragraph("<b>Dataset:</b> 7,043 Customer Records", table_cell)
        ],
        [
            Paragraph("<b>Tools:</b> Python, Pandas, Matplotlib, Seaborn", table_cell),
            Paragraph("<b>BI Tool:</b> Power BI Desktop & DAX", table_cell),
            Paragraph("<b>Status:</b> Completed & Verified", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[2.3*inch, 2.3*inch, 2.4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & CORE KPIS
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Core KPIs", h1_style))
    story.append(Paragraph(
        "This study investigates customer attrition patterns across 7,043 customer accounts of a telecommunications service provider. "
        "Through data cleaning, multivariate statistical analysis, and business intelligence dashboards in Power BI, the analysis isolates "
        "the primary drivers of customer departure and delivers actionable retention initiatives to protect annual recurring revenue.",
        body_style
    ))

    # Core KPI Summary Table
    kpi_headers = [
        Paragraph("Total Customers", table_cell_white),
        Paragraph("Churned", table_cell_white),
        Paragraph("Retained", table_cell_white),
        Paragraph("Churn Rate %", table_cell_white),
        Paragraph("Avg Monthly Charge", table_cell_white),
        Paragraph("Avg Tenure", table_cell_white)
    ]
    kpi_values = [
        Paragraph("<b>7,043</b>", table_cell_bold),
        Paragraph("<font color='#DC2626'><b>1,869</b></font>", table_cell),
        Paragraph("<font color='#10B981'><b>5,174</b></font>", table_cell),
        Paragraph("<font color='#EA580C'><b>26.54%</b></font>", table_cell),
        Paragraph("<b>$64.76</b>", table_cell),
        Paragraph("<b>32.4 Mos</b>", table_cell)
    ]
    kpi_table = Table([kpi_headers, kpi_values], colWidths=[1.16*inch]*6)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 8))

    # Executive Highlights
    story.append(Paragraph("<b>Key Strategic Findings:</b>", body_bold))
    story.append(Paragraph("• <b>The Contract Moat:</b> Month-to-month contracts suffer a catastrophic <b>42.71%</b> churn rate and generate <b>88.55%</b> of all churned volume. Two-year contract holders experience only <b>2.83%</b> churn (a 15.1x stability multiplier).", bullet_style))
    story.append(Paragraph("• <b>First-Year Onboarding Cliff:</b> <b>47.44%</b> of customers churn in their initial 12 months. The median tenure of churned customers is just <b>10.0 months</b> vs <b>38.0 months</b> for retained clients.", bullet_style))
    story.append(Paragraph("• <b>Fiber Optic Pricing Friction:</b> Fiber optic subscribers churn at <b>41.89%</b> (vs 18.96% for DSL), driven by high bills ($70–$100+) without bundled value-added support.", bullet_style))
    story.append(Paragraph("• <b>Payment Inefficiency:</b> Electronic check users churn at <b>45.29%</b>, compared to ~15.5% for automatic credit card or bank drafts.", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 2: DATA EXPLORATION & CLEANING (PARTS 1 & 2)
    # ---------------------------------------------------------
    story.append(Paragraph("2. Data Exploration & Data Cleaning Methodology", h1_style))
    story.append(Paragraph(
        "Following strict data governance protocols, raw customer data was audited for integrity, duplicate entries, data types, and missing values.",
        body_style
    ))

    audit_headers = [Paragraph("Cleaning Task", table_cell_white), Paragraph("Raw Observation", table_cell_white), Paragraph("Resolution Strategy", table_cell_white), Paragraph("Final Verification", table_cell_white)]
    audit_rows = [
        [
            Paragraph("Duplicate Detection", table_cell_bold),
            Paragraph("18 identical duplicate records", table_cell),
            Paragraph("Applied <code>drop_duplicates()</code>", table_cell),
            Paragraph("0 duplicates; 7,043 unique rows", table_cell)
        ],
        [
            Paragraph("Total_Charges Data Type", table_cell_bold),
            Paragraph("Loaded as <code>object</code> / string", table_cell),
            Paragraph("Converted via <code>pd.to_numeric()</code>", table_cell),
            Paragraph("Standardized to <code>float64</code>", table_cell)
        ],
        [
            Paragraph("Total_Charges Missing", table_cell_bold),
            Paragraph("11 blank whitespace values (' ')", table_cell),
            Paragraph("Mapped to 0.0 (tenure = 0 months)", table_cell),
            Paragraph("0 missing values remaining", table_cell)
        ],
        [
            Paragraph("Tenure Segmentation", table_cell_bold),
            Paragraph("Continuous tenure (0–72 months)", table_cell),
            Paragraph("Binned into 6 ordinal groups (0-12m to 61-72m)", table_cell),
            Paragraph("Created <code>Tenure_Group</code> feature", table_cell)
        ],
        [
            Paragraph("Senior Citizen Label", table_cell_bold),
            Paragraph("Binary numeric codes (0, 1)", table_cell),
            Paragraph("Mapped to categorical 'No'/'Yes'", table_cell),
            Paragraph("Enhanced business reporting", table_cell)
        ]
    ]
    audit_table = Table([audit_headers] + audit_rows, colWidths=[1.6*inch, 1.7*inch, 2.0*inch, 1.7*inch])
    audit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(audit_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 3: QUANTITATIVE ANALYSIS & MULTIVARIATE FINDINGS (PART 3)
    # ---------------------------------------------------------
    story.append(Paragraph("3. Quantitative Analysis & Segment Breakdowns", h1_style))
    story.append(Paragraph(
        "Below are the analytical breakdowns across core customer dimensions requested in Steps 17 to 38 of the project brief:",
        body_style
    ))

    # Breakdown Table
    breakdown_headers = [Paragraph("Dimension", table_cell_white), Paragraph("Category", table_cell_white), Paragraph("Customer Count", table_cell_white), Paragraph("Customer %", table_cell_white), Paragraph("Churn Rate %", table_cell_white)]
    breakdown_data = [
        [Paragraph("Contract Type", table_cell_bold), Paragraph("Month-to-month", table_cell), Paragraph("3,875", table_cell), Paragraph("55.02%", table_cell), Paragraph("<font color='#DC2626'><b>42.71%</b></font>", table_cell)],
        [Paragraph("Contract Type", table_cell_bold), Paragraph("One year", table_cell), Paragraph("1,473", table_cell), Paragraph("20.91%", table_cell), Paragraph("11.27%", table_cell)],
        [Paragraph("Contract Type", table_cell_bold), Paragraph("Two year", table_cell), Paragraph("1,695", table_cell), Paragraph("24.07%", table_cell), Paragraph("<font color='#10B981'><b>2.83%</b></font>", table_cell)],
        [Paragraph("Internet Service", table_cell_bold), Paragraph("Fiber optic", table_cell), Paragraph("3,096", table_cell), Paragraph("43.96%", table_cell), Paragraph("<font color='#DC2626'><b>41.89%</b></font>", table_cell)],
        [Paragraph("Internet Service", table_cell_bold), Paragraph("DSL", table_cell), Paragraph("2,421", table_cell), Paragraph("34.37%", table_cell), Paragraph("18.96%", table_cell)],
        [Paragraph("Internet Service", table_cell_bold), Paragraph("No Internet", table_cell), Paragraph("1,526", table_cell), Paragraph("21.67%", table_cell), Paragraph("<font color='#10B981'><b>7.40%</b></font>", table_cell)],
        [Paragraph("Payment Method", table_cell_bold), Paragraph("Electronic check", table_cell), Paragraph("2,365", table_cell), Paragraph("33.58%", table_cell), Paragraph("<font color='#DC2626'><b>45.29%</b></font>", table_cell)],
        [Paragraph("Payment Method", table_cell_bold), Paragraph("Mailed check", table_cell), Paragraph("1,612", table_cell), Paragraph("22.89%", table_cell), Paragraph("19.11%", table_cell)],
        [Paragraph("Payment Method", table_cell_bold), Paragraph("Bank transfer (auto)", table_cell), Paragraph("1,544", table_cell), Paragraph("21.92%", table_cell), Paragraph("16.71%", table_cell)],
        [Paragraph("Payment Method", table_cell_bold), Paragraph("Credit card (auto)", table_cell), Paragraph("1,522", table_cell), Paragraph("21.61%", table_cell), Paragraph("<font color='#10B981'><b>15.24%</b></font>", table_cell)],
        [Paragraph("Senior Status", table_cell_bold), Paragraph("Senior Citizen (Yes)", table_cell), Paragraph("1,142", table_cell), Paragraph("16.21%", table_cell), Paragraph("<font color='#DC2626'><b>41.68%</b></font>", table_cell)],
        [Paragraph("Senior Status", table_cell_bold), Paragraph("Non-Senior (No)", table_cell), Paragraph("5,901", table_cell), Paragraph("83.79%", table_cell), Paragraph("23.61%", table_cell)],
        [Paragraph("Gender", table_cell_bold), Paragraph("Female", table_cell), Paragraph("3,488", table_cell), Paragraph("49.52%", table_cell), Paragraph("26.92%", table_cell)],
        [Paragraph("Gender", table_cell_bold), Paragraph("Male", table_cell), Paragraph("3,555", table_cell), Paragraph("50.48%", table_cell), Paragraph("26.16%", table_cell)],
    ]
    bd_table = Table([breakdown_headers] + breakdown_data, colWidths=[1.5*inch, 1.8*inch, 1.2*inch, 1.1*inch, 1.4*inch])
    bd_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(bd_table)
    story.append(Spacer(1, 8))

    # Charges and Tenure Comparison
    story.append(Paragraph("<b>Billing & Tenure Comparison (Retained vs. Churned):</b>", body_bold))
    story.append(Paragraph("• <b>Monthly Charges:</b> Churned customers pay an average of <b>$74.44</b> (median $79.65) vs <b>$61.27</b> (median $64.43) for retained customers (+$15.22 median premium).", bullet_style))
    story.append(Paragraph("• <b>Tenure Duration:</b> Churned customers depart at an average of <b>17.98 months</b> (median 10.0 months) vs <b>37.57 months</b> (median 38.0 months) for retained accounts.", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 4: PYTHON VISUALIZATIONS PORTFOLIO (PART 4)
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Python Visualizations Portfolio (Visuals 1 to 14)", h1_style))
    story.append(Paragraph(
        "All 14 visualizations required by the project specifications were generated using Matplotlib and Seaborn at 300 DPI publication standards.",
        body_style
    ))

    # Grid of charts: pairs of images
    chart_pairs = [
        ("Visualizations/01_churn_distribution_pie.png", "Figure 1: Churn Distribution (Pie Chart)",
         "Visualizations/02_customer_distribution_by_contract_bar.png", "Figure 2: Customers by Contract (Bar Chart)"),
        ("Visualizations/03_churn_by_contract_bar.png", "Figure 3: Churn Rate by Contract (Bar Chart)",
         "Visualizations/04_churn_by_gender_bar.png", "Figure 4: Churn Rate by Gender (Bar Chart)"),
        ("Visualizations/05_churn_by_internet_service_bar.png", "Figure 5: Churn Rate by Internet Service",
         "Visualizations/06_churn_by_payment_method_bar.png", "Figure 6: Churn Rate by Payment Method"),
        ("Visualizations/07_tenure_distribution_histogram.png", "Figure 7: Customer Tenure Distribution",
         "Visualizations/08_monthly_charges_distribution_histogram.png", "Figure 8: Monthly Charges Distribution"),
        ("Visualizations/09_tenure_vs_monthly_charges_scatter.png", "Figure 9: Tenure vs Monthly Charges Scatter",
         "Visualizations/10_monthly_charges_by_churn_boxplot.png", "Figure 10: Monthly Charges by Churn Boxplot"),
        ("Visualizations/11_total_charges_by_churn_boxplot.png", "Figure 11: Total Charges by Churn Boxplot",
         "Visualizations/12_churn_rate_by_tenure_group_bar.png", "Figure 12: Churn Rate by Tenure Group"),
        ("Visualizations/13_service_usage_countplot.png", "Figure 13: Service Usage & Value-Add Add-ons",
         "Visualizations/14_correlation_heatmap.png", "Figure 14: Correlation Heatmap")
    ]

    for img1_path, cap1, img2_path, cap2 in chart_pairs:
        t_row = []
        if os.path.exists(img1_path):
            img1 = Image(img1_path, width=3.4*inch, height=2.1*inch)
            c1 = Paragraph(cap1, caption_style)
            col1 = [img1, c1]
        else:
            col1 = [Paragraph(f"Missing {img1_path}", caption_style)]

        if os.path.exists(img2_path):
            img2 = Image(img2_path, width=3.4*inch, height=2.1*inch)
            c2 = Paragraph(cap2, caption_style)
            col2 = [img2, c2]
        else:
            col2 = [Paragraph(f"Missing {img2_path}", caption_style)]

        img_table = Table([[col1, col2]], colWidths=[3.5*inch, 3.5*inch])
        img_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(KeepTogether(img_table))

    # ---------------------------------------------------------
    # SECTION 5: POWER BI DASHBOARD & DAX IMPLEMENTATION
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("5. Power BI Dashboard Architecture & DAX Measures", h1_style))
    story.append(Paragraph(
        "An executive Power BI Dashboard (<code>Customer_Churn_Dashboard.pbix</code>) was engineered incorporating a dark navy corporate theme, "
        "6 real-time KPI cards, 6 multi-select slicers, and 10 interactive reporting visuals.",
        body_style
    ))

    # Dashboard preview image
    pbi_preview_path = "Visualizations/15_powerbi_dashboard_preview.png"
    if os.path.exists(pbi_preview_path):
        pbi_img = Image(pbi_preview_path, width=7.0*inch, height=3.9*inch)
        story.append(pbi_img)
        story.append(Paragraph("Figure 15: Power BI Interactive Executive Dashboard Layout (Customer Churn & Retention Analytics)", caption_style))

    # DAX Table
    story.append(Paragraph("<b>Required DAX Measures Implementation (Section 9 Compliance):</b>", body_bold))
    dax_headers = [Paragraph("DAX Measure Name", table_cell_white), Paragraph("DAX Expression & Implementation", table_cell_white), Paragraph("Function Utilized", table_cell_white)]
    dax_rows = [
        [
            Paragraph("Total Customers", table_cell_bold),
            Paragraph("<code>DISTINCTCOUNT('Customer_Churn_Cleaned'[Customer_ID])</code>", table_cell),
            Paragraph("DISTINCTCOUNT", table_cell)
        ],
        [
            Paragraph("Churned Customers", table_cell_bold),
            Paragraph("<code>CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = \"Yes\")</code>", table_cell),
            Paragraph("CALCULATE, COUNTROWS", table_cell)
        ],
        [
            Paragraph("Retained Customers", table_cell_bold),
            Paragraph("<code>CALCULATE(COUNTROWS('Customer_Churn_Cleaned'), 'Customer_Churn_Cleaned'[Churn] = \"No\")</code>", table_cell),
            Paragraph("CALCULATE, COUNTROWS", table_cell)
        ],
        [
            Paragraph("Churn Rate %", table_cell_bold),
            Paragraph("<code>DIVIDE([Churned Customers], [Total Customers], 0)</code>", table_cell),
            Paragraph("DIVIDE", table_cell)
        ],
        [
            Paragraph("Average Monthly Charges", table_cell_bold),
            Paragraph("<code>AVERAGE('Customer_Churn_Cleaned'[Monthly_Charges])</code>", table_cell),
            Paragraph("AVERAGE", table_cell)
        ],
        [
            Paragraph("Average Tenure", table_cell_bold),
            Paragraph("<code>AVERAGE('Customer_Churn_Cleaned'[Tenure_Months])</code>", table_cell),
            Paragraph("AVERAGE", table_cell)
        ]
    ]
    dax_table = Table([dax_headers] + dax_rows, colWidths=[1.7*inch, 3.8*inch, 1.5*inch])
    dax_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(dax_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 6: ANSWERS TO THE 10 BUSINESS QUESTIONS (PART 10)
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("6. Business Insights & Answers to Project Questions", h1_style))
    story.append(Paragraph(
        "Below are the rigorous analytical answers to each of the 10 questions mandated in Section 10 of the project specification:",
        body_style
    ))

    questions_answers = [
        ("1. What is the overall churn rate?",
         "The overall churn rate is <b>26.54%</b>. Out of 7,043 total customers, 1,869 customers terminated their contracts while 5,174 remain actively subscribed."),
        
        ("2. Which contract type has the highest churn?",
         "<b>Month-to-month contracts</b> exhibit the highest churn rate at <b>42.71%</b>. This group accounts for 1,655 out of 1,869 (88.55%) of all company churn. One-year contracts churn at 11.27%, while Two-year contracts churn at only 2.83%."),
        
        ("3. Which payment method has the highest churn?",
         "<b>Electronic check</b> has the highest churn rate at <b>45.29%</b> (1,071 departures). In contrast, automated methods show superior retention: Credit Card (automatic) is 15.24% and Bank Transfer (automatic) is 16.71%."),
        
        ("4. Which internet service has the highest churn?",
         "<b>Fiber optic internet</b> has the highest churn rate at <b>41.89%</b> (1,297 departures), followed by DSL at 18.96% and No Internet at 7.40%."),
        
        ("5. Does tenure appear related to churn?",
         "<b>Yes, tenure is strongly inversely related to churn.</b> Churn is highest in months 0–12 (<b>47.44%</b>) and drops systematically: 28.71% (13-24m), 21.63% (25-36m), 19.03% (37-48m), 14.42% (49-60m), and only 6.61% for 61-72 months. Churned customers have a median tenure of only 10.0 months vs 38.0 months for retained customers."),
        
        ("6. Are higher monthly charges associated with churn?",
         "<b>Yes.</b> Churned customers incur substantially higher monthly recurring charges (median <b>$79.65</b> / mean $74.44) compared to retained customers (median <b>$64.43</b> / mean $61.27). Customers paying between $70 and $105/month account for the largest concentration of churn."),
        
        ("7. Which customer segment has the highest churn?",
         "The highest churn segment comprises <b>New subscribers (Tenure < 12 months) on Month-to-Month contracts using Fiber Optic internet and paying via Electronic Check without bundled Tech Support or Online Security</b>, where churn exceeds <b>68%</b>."),
        
        ("8. What factors appear associated with customer churn?",
         "Key risk drivers: (1) Month-to-month commitment (15.1x risk vs 2-yr), (2) Early tenure window (7.2x risk vs 5-yr), (3) Electronic check billing (3.0x risk vs card auto), (4) Unbundled Fiber Optic service (2.2x risk), (5) Lack of Online Security/Tech Support (2.8x risk), (6) Senior Citizen status (1.8x risk)."),
        
        ("9. Which customer segment requires immediate attention?",
         "<b>First-year Fiber Optic subscribers on Month-to-Month contracts.</b> These are premium revenue accounts ($70-$100/mo) whose premature departure within the first 10 months creates significant Customer Acquisition Cost (CAC) deficit and destroys long-term enterprise value."),
        
        ("10. Write 5–10 key business insights:",
         "1. <b>Contract Lock-in Moat:</b> Two-year contracts virtually eliminate churn (2.83%). Migrating 15% of Month-to-Month users preserves $500K+ annually.<br/>"
         "2. <b>The First-Year Survival Cliff:</b> Nearly half of all first-year subscribers churn (47.44%); onboarding during months 1–6 is the key retention battleground.<br/>"
         "3. <b>Fiber Optic Value Disconnect:</b> Premium speeds without adequate customer success generate discontent and 41.89% churn.<br/>"
         "4. <b>Payment Friction Driver:</b> Electronic check users experience monthly bill-shock; auto-pay reduces attrition to ~15%.<br/>"
         "5. <b>Value-Added Stickiness:</b> Tech Support and Online Security cut churn from ~41.7% to ~15.0%, acting as vital retention anchors.<br/>"
         "6. <b>Senior Citizen Attrition:</b> Seniors experience 41.68% churn, indicating an urgent need for simplified billing and personalized support.")
    ]

    for q, a in questions_answers:
        q_box = [
            Paragraph(f"<b>{q}</b>", table_cell_bold),
            Paragraph(a, table_cell)
        ]
        t = Table([q_box], colWidths=[2.2*inch, 4.8*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    # ---------------------------------------------------------
    # SECTION 7: FINAL SUBMISSION CHECKLIST (SECTION 13)
    # ---------------------------------------------------------
    story.append(Spacer(1, 8))
    story.append(Paragraph("7. Project Submission Verification Checklist", h1_style))
    chk_headers = [Paragraph("Milestone Deliverable", table_cell_white), Paragraph("Target Requirement", table_cell_white), Paragraph("Execution Status", table_cell_white)]
    chk_rows = [
        [Paragraph("Data Cleaned", table_cell_bold), Paragraph("Duplicates & whitespace values handled", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Missing Values Handled", table_cell_bold), Paragraph("11 Total_Charges nulls imputed to 0.0", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Python Analysis Completed", table_cell_bold), Paragraph("All 38 analytical steps computed", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Python Visualizations", table_cell_bold), Paragraph("All 14 requested charts generated at 300 DPI", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("DAX Measures Created", table_cell_bold), Paragraph("6 core DAX measures created & documented", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Power BI Dashboard", table_cell_bold), Paragraph("Interactive PBIX package with 10 visuals", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Slicers Added", table_cell_bold), Paragraph("6 slicers (Gender, Contract, Internet, PM, Senior, Churn)", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Business Insights Written", table_cell_bold), Paragraph("10 specific questions answered with recommendations", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Project Report Completed", table_cell_bold), Paragraph("Executive publication-grade PDF report compiled", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Cleaned Dataset Submitted", table_cell_bold), Paragraph("Customer_Churn_Cleaned.csv in Dataset folder", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("Python File Submitted", table_cell_bold), Paragraph("Executed .ipynb and standalone .py script", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
        [Paragraph("README Completed", table_cell_bold), Paragraph("Comprehensive documentation and user guide", table_cell), Paragraph("<font color='#10B981'><b>COMPLETED</b></font>", table_cell)],
    ]
    chk_table = Table([chk_headers] + chk_rows, colWidths=[2.2*inch, 3.5*inch, 1.3*inch])
    chk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(chk_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Publication-grade PDF report generated successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf_report()
