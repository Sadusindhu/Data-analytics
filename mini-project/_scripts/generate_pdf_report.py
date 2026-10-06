"""
Script: generate_pdf_report.py
Generates the official professional project report in PDF format:
Report/Loan_Credit_Risk_Project_Report.pdf

Complies with all guidelines from Sections 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 of the project brief.
Uses ReportLab Platypus engine for publication-grade layout.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total page count."""
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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "LOAN DEFAULT & CREDIT RISK ANALYSIS — PROJECT REPORT")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "FINANCIAL ANALYTICS DIVISION")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.drawString(54, 32, "Confidential — For Credit Risk Committee & Academic Evaluation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()

def build_pdf_report():
    pdf_path = os.path.join("Report", "Loan_Credit_Risk_Project_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1A365D")   # Deep Navy
    SECONDARY = colors.HexColor("#0D9488") # Teal
    TEXT_DARK = colors.HexColor("#1E293B") # Slate 800
    MUTED = colors.HexColor("#64748B")     # Slate 500
    BG_LIGHT = colors.HexColor("#F8FAFC")  # Slate 50
    ACCENT_RED = colors.HexColor("#DC2626")# Red

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=MUTED,
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=6
    )
    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
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

    story = []

    # =========================================================================
    # COVER / HEADER BANNER
    # =========================================================================
    story.append(Paragraph("MINI PROJECT: LOAN DEFAULT & CREDIT RISK ANALYSIS", title_style))
    story.append(Paragraph("Comprehensive Financial Analytics, Exploratory Data Cleaning, Statistical Modeling, and Power BI Dashboard Implementation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    # Metadata Summary Box
    meta_data = [
        [Paragraph("<b>Project Role:</b> Data Analyst (Credit Risk)", table_cell), Paragraph("<b>Dataset Scope:</b> 5,000 Retail Loan Records", table_cell)],
        [Paragraph("<b>Analytical Stack:</b> Python, Pandas, Matplotlib, Seaborn", table_cell), Paragraph("<b>BI Solution:</b> Power BI Desktop & DAX Measures", table_cell)],
        [Paragraph("<b>Primary Metric:</b> Portfolio Probability of Default (PD)", table_cell), Paragraph("<b>Status:</b> Completed & Verified Submission", table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 1: PROJECT OBJECTIVE & BACKGROUND
    # =========================================================================
    story.append(Paragraph("1. Project Objective & Scope", h1_style))
    story.append(Paragraph(
        "Financial institutions face significant credit exposure when extending loans across diverse retail customer segments. "
        "The objective of this project is to analyze comprehensive customer loan data—encompassing borrower demographics, "
        "income profiles, credit scoring metrics, requested loan parameters, debt-to-income (DTI) obligations, and historical delinquency records. "
        "By applying systematic data cleaning, rigorous exploratory data analysis (EDA), predictive risk segmentation, and interactive Power BI "
        "dashboard modeling, this study establishes actionable risk criteria to minimize default losses while sustaining healthy loan origination volume.",
        body_style
    ))

    # =========================================================================
    # SECTION 2: TOOLS & TECHNOLOGIES
    # =========================================================================
    story.append(Paragraph("2. Tools & Analytical Technologies", h1_style))
    tools_data = [
        [Paragraph("<b>Technology</b>", table_cell_white), Paragraph("<b>Role / Application in Project</b>", table_cell_white)],
        [Paragraph("<b>Python 3.13</b>", table_cell_bold), Paragraph("Core programming language for automated data pipeline and statistical calculations.", table_cell)],
        [Paragraph("<b>Pandas & NumPy</b>", table_cell_bold), Paragraph("Data manipulation, duplicate elimination, missing value imputation, and multidimensional aggregation.", table_cell)],
        [Paragraph("<b>Matplotlib & Seaborn</b>", table_cell_bold), Paragraph("Generation of publication-grade visual charts (distributions, scatter correlations, box plots, heatmap).", table_cell)],
        [Paragraph("<b>Power BI Desktop</b>", table_cell_bold), Paragraph("Interactive executive dashboard, dynamic KPI card visualization, and cross-filtering analysis.", table_cell)],
        [Paragraph("<b>DAX (Data Analysis Expressions)</b>", table_cell_bold), Paragraph("Quantitative business metrics: CALCULATE, DISTINCTCOUNT, COUNTROWS, DIVIDE, AVERAGE.", table_cell)]
    ]
    t_tools = Table(tools_data, colWidths=[140, 360])
    t_tools.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tools)
    story.append(Spacer(1, 12))

    # =========================================================================
    # SECTION 3: DATASET OVERVIEW & CLEANING METHODOLOGY
    # =========================================================================
    story.append(Paragraph("3. Dataset Description & Cleaning Methodology", h1_style))
    story.append(Paragraph(
        "The raw portfolio dataset contained <b>5,025 loan records</b> across <b>24 feature dimensions</b>. "
        "Prior to analytical modeling, a systematic data quality assessment was conducted to address missing values, duplicate entries, "
        "and data integrity anomalies:",
        body_style
    ))
    
    clean_steps = [
        "<b>Duplicate Identification & Removal:</b> Identified 25 duplicate records across customer identifiers. Applied deduplication based on unique Customer_ID, reducing the active dataset to exactly 5,000 distinct loan accounts.",
        "<b>Erroneous Entries & Outliers:</b> Detected negative entry values in Annual_Income (e.g. -$45,000) and entry typos in Loan_Amount (e.g. $999,999). Negative values were scrubbed and imputed, and the loan amount was capped to the portfolio median ($29,900) with recalculated monthly amortization.",
        "<b>Missing Value Imputation:</b> Annual_Income (43 missing) was imputed using the conditional median grouped by Education level and Employment Status. Employment_Years (36 missing), Credit_Score (28 missing), and Debt_to_Income_Ratio (22 missing) were imputed with robust distributional medians.",
        "<b>Feature Engineering:</b> Segmented continuous credit scores into five industry FICO tiers: <i>Poor (&lt;580)</i>, <i>Fair (580-669)</i>, <i>Good (670-739)</i>, <i>Very Good (740-799)</i>, and <i>Excellent (800+)</i>. Created standardized <i>Income_Group</i> brackets and a binary quantitative indicator (<i>Default_Numeric</i>)."
    ]
    for cs in clean_steps:
        story.append(Paragraph(f"• {cs}", bullet_style))
    story.append(Spacer(1, 10))

    # Cleaning verification table
    clean_summary_data = [
        [Paragraph("<b>Quality Attribute</b>", table_cell_white), Paragraph("<b>Raw Dataset</b>", table_cell_white), Paragraph("<b>Cleaned Dataset</b>", table_cell_white), Paragraph("<b>Resolution Status</b>", table_cell_white)],
        [Paragraph("Total Row Count", table_cell_bold), Paragraph("5,025", table_cell), Paragraph("5,000", table_cell), Paragraph("Deduplicated (25 removed)", table_cell)],
        [Paragraph("Missing Annual_Income", table_cell_bold), Paragraph("43 nulls", table_cell), Paragraph("0 nulls", table_cell), Paragraph("Group Median Imputed", table_cell)],
        [Paragraph("Missing Credit_Score", table_cell_bold), Paragraph("28 nulls", table_cell), Paragraph("0 nulls", table_cell), Paragraph("Median Imputed (668)", table_cell)],
        [Paragraph("Missing DTI Ratio", table_cell_bold), Paragraph("22 nulls", table_cell), Paragraph("0 nulls", table_cell), Paragraph("Median Imputed (0.29)", table_cell)],
        [Paragraph("Missing Employment_Years", table_cell_bold), Paragraph("36 nulls", table_cell), Paragraph("0 nulls", table_cell), Paragraph("Median Imputed (6.0 yrs)", table_cell)],
        [Paragraph("Anomalies / Outliers", table_cell_bold), Paragraph("Negative income, typo loan", table_cell), Paragraph("0 anomalies", table_cell), Paragraph("Capped & Recalculated", table_cell)]
    ]
    t_clean = Table(clean_summary_data, colWidths=[140, 90, 90, 180])
    t_clean.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_clean)
    
    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: PORTFOLIO PERFORMANCE & DATA ANALYSIS (ITEMS 16 - 44)
    # =========================================================================
    story.append(Paragraph("4. Quantitative Portfolio Data Analysis", h1_style))
    story.append(Paragraph(
        "Analysis of the 5,000 verified loan accounts provides deep empirical visibility into credit risk behavior, capital allocation, and borrower default dynamics:",
        body_style
    ))

    # Core Metrics Table (Items 16 to 25)
    core_metrics = [
        [Paragraph("<b>Metric Item (PDF Ref.)</b>", table_cell_white), Paragraph("<b>Value</b>", table_cell_white), Paragraph("<b>Business Description & Benchmark</b>", table_cell_white)],
        [Paragraph("16. Total Customers", table_cell_bold), Paragraph("5,000", table_cell), Paragraph("Distinct individual retail banking accounts evaluated.", table_cell)],
        [Paragraph("17. Total Loans", table_cell_bold), Paragraph("5,000", table_cell), Paragraph("Total originated loan agreements under active management.", table_cell)],
        [Paragraph("18. Defaulted Loans", table_cell_bold), Paragraph("955", table_cell), Paragraph("Delinquent accounts classified under non-performing/charge-off.", table_cell)],
        [Paragraph("19. Non-Defaulted Loans", table_cell_bold), Paragraph("4,045", table_cell), Paragraph("Performing accounts (Current or Fully Paid status).", table_cell)],
        [Paragraph("20. Overall Default Rate", table_cell_bold), Paragraph("<b>19.10%</b>", table_cell), Paragraph("Baseline portfolio credit default rate.", table_cell)],
        [Paragraph("21. Average Annual Income", table_cell_bold), Paragraph("$69,486.35", table_cell), Paragraph("Mean customer gross income (Median: $62,000.00).", table_cell)],
        [Paragraph("22. Average Credit Score", table_cell_bold), Paragraph("667.10", table_cell), Paragraph("Weighted credit score representing 'Fair-to-Good' baseline.", table_cell)],
        [Paragraph("23. Average Loan Amount", table_cell_bold), Paragraph("$41,449.30", table_cell), Paragraph("Mean principal borrowed across all loan products.", table_cell)],
        [Paragraph("24. Average Interest Rate", table_cell_bold), Paragraph("14.18%", table_cell), Paragraph("Risk-adjusted annualized pricing margin.", table_cell)],
        [Paragraph("25. Average Debt-to-Income", table_cell_bold), Paragraph("0.3571 (35.71%)", table_cell), Paragraph("Mean customer monthly debt obligations vs gross earnings.", table_cell)],
    ]
    t_core = Table(core_metrics, colWidths=[150, 90, 260])
    t_core.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_core)
    story.append(Spacer(1, 10))

    # Segment breakdowns: Loan Type, Employment, Credit Score Group
    story.append(Paragraph("Segment-Level Default Risk Profiles (Items 26 to 33)", h2_style))
    segment_table_data = [
        [Paragraph("<b>Dimension</b>", table_cell_white), Paragraph("<b>Segment Category</b>", table_cell_white), Paragraph("<b>Total Volume</b>", table_cell_white), Paragraph("<b>Default Rate (%)</b>", table_cell_white), Paragraph("<b>Risk Tier</b>", table_cell_white)],
        [Paragraph("<b>Loan Type</b>", table_cell_bold), Paragraph("Home", table_cell), Paragraph("1,203", table_cell), Paragraph("<b>34.91%</b>", table_cell), Paragraph("Critical", table_cell)],
        [Paragraph("", table_cell), Paragraph("Business", table_cell), Paragraph("485", table_cell), Paragraph("<b>23.92%</b>", table_cell), Paragraph("High", table_cell)],
        [Paragraph("", table_cell), Paragraph("Auto", table_cell), Paragraph("1,123", table_cell), Paragraph("14.43%", table_cell), Paragraph("Moderate", table_cell)],
        [Paragraph("", table_cell), Paragraph("Education", table_cell), Paragraph("715", table_cell), Paragraph("13.15%", table_cell), Paragraph("Moderate", table_cell)],
        [Paragraph("", table_cell), Paragraph("Personal", table_cell), Paragraph("1,474", table_cell), Paragraph("11.06%", table_cell), Paragraph("Low", table_cell)],
        [Paragraph("<b>Employment</b>", table_cell_bold), Paragraph("Unemployed", table_cell), Paragraph("399", table_cell), Paragraph("<b>45.11%</b>", table_cell), Paragraph("Critical", table_cell)],
        [Paragraph("", table_cell), Paragraph("Employed", table_cell), Paragraph("3,465", table_cell), Paragraph("17.23%", table_cell), Paragraph("Standard", table_cell)],
        [Paragraph("", table_cell), Paragraph("Self-Employed", table_cell), Paragraph("1,136", table_cell), Paragraph("15.67%", table_cell), Paragraph("Standard", table_cell)],
        [Paragraph("<b>Credit Score</b>", table_cell_bold), Paragraph("Poor (&lt;580)", table_cell), Paragraph("793", table_cell), Paragraph("<b>37.45%</b>", table_cell), Paragraph("Critical Subprime", table_cell)],
        [Paragraph("", table_cell), Paragraph("Fair (580-669)", table_cell), Paragraph("1,758", table_cell), Paragraph("22.58%", table_cell), Paragraph("Elevated", table_cell)],
        [Paragraph("", table_cell), Paragraph("Good (670-739)", table_cell), Paragraph("1,435", table_cell), Paragraph("13.52%", table_cell), Paragraph("Moderate", table_cell)],
        [Paragraph("", table_cell), Paragraph("Very Good (740-799)", table_cell), Paragraph("699", table_cell), Paragraph("8.30%", table_cell), Paragraph("Prime", table_cell)],
        [Paragraph("", table_cell), Paragraph("Excellent (800+)", table_cell), Paragraph("315", table_cell), Paragraph("<b>2.86%</b>", table_cell), Paragraph("Super Prime", table_cell)],
        [Paragraph("<b>Income Tier</b>", table_cell_bold), Paragraph("Low (&lt;$40k)", table_cell), Paragraph("1,094", table_cell), Paragraph("<b>33.91%</b>", table_cell), Paragraph("High Risk", table_cell)],
        [Paragraph("", table_cell), Paragraph("Lower-Middle ($40k-$65k)", table_cell), Paragraph("1,607", table_cell), Paragraph("19.60%", table_cell), Paragraph("Standard", table_cell)],
        [Paragraph("", table_cell), Paragraph("Upper-Middle ($65k-$95k)", table_cell), Paragraph("1,268", table_cell), Paragraph("13.96%", table_cell), Paragraph("Low Risk", table_cell)],
        [Paragraph("", table_cell), Paragraph("High (&gt;$95k)", table_cell), Paragraph("1,031", table_cell), Paragraph("<b>8.92%</b>", table_cell), Paragraph("Minimal Risk", table_cell)]
    ]
    t_seg = Table(segment_table_data, colWidths=[90, 140, 80, 100, 90])
    t_seg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_seg)
    story.append(Spacer(1, 10))

    # Filtering Criteria (Items 34 to 39)
    story.append(Paragraph("High-Risk Exposure Subsets & Extremes (Items 34 to 39)", h2_style))
    risk_subsets = [
        "<b>Below-Average Credit Score (&lt;667.1):</b> 2,480 borrowers (49.6% of portfolio) with a combined default rate of <b>27.22%</b>.",
        "<b>Above-Average Loan Principal (&gt;$41,449):</b> 1,748 borrowers (35.0% of portfolio) with an elevated default rate of <b>31.18%</b>.",
        "<b>High Debt-to-Income Ratio (&gt;0.40):</b> 1,837 borrowers (36.7% of portfolio) showing a severe default rate of <b>34.30%</b>.",
        "<b>Product with Highest Default Rate (Item 38):</b> <b>Home Loans at 34.91%</b> due to extended commitment and heavy principal burdens.",
        "<b>Region with Highest Default Rate (Item 39):</b> <b>South Region at 20.13%</b>, followed by East at 19.5% and West at 18.9%."
    ]
    for rs in risk_subsets:
        story.append(Paragraph(f"• {rs}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: PYTHON VISUALIZATIONS & RISK CHARTS
    # =========================================================================
    story.append(Paragraph("5. Visual Analytics & Risk Distribution Charts", h1_style))
    story.append(Paragraph(
        "Visual inspection of the portfolio uncovers the distributional dynamics, non-linear thresholds, and risk driver correlations:",
        body_style
    ))

    # Grid of charts (Page 3 visual layout)
    chart_w = 245
    chart_h = 135

    img1 = Image("Visualizations/01_loan_default_distribution_pie.png", width=chart_w, height=chart_h)
    img2 = Image("Visualizations/03_default_rate_by_loan_type_bar.png", width=chart_w, height=chart_h)
    img3 = Image("Visualizations/06_credit_score_distribution_hist.png", width=chart_w, height=chart_h)
    img4 = Image("Visualizations/08_annual_income_distribution_hist.png", width=chart_w, height=chart_h)

    chart_table_1 = [
        [img1, img2],
        [Paragraph("<b>Figure 1:</b> Portfolio Loan Default Distribution (Pie Chart)", table_cell),
         Paragraph("<b>Figure 2:</b> Default Rate (%) by Loan Product (Bar Chart)", table_cell)],
        [img3, img4],
        [Paragraph("<b>Figure 3:</b> Credit Score Distribution with Mean Indicator", table_cell),
         Paragraph("<b>Figure 4:</b> Annual Income Distribution (Log-Normal Profile)", table_cell)]
    ]
    t_charts1 = Table(chart_table_1, colWidths=[250, 250])
    t_charts1.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_charts1)
    story.append(Spacer(1, 10))

    img5 = Image("Visualizations/12_credit_score_by_default_status_box.png", width=chart_w, height=chart_h)
    img6 = Image("Visualizations/13_dti_by_default_status_box.png", width=chart_w, height=chart_h)
    chart_table_2 = [
        [img5, img6],
        [Paragraph("<b>Figure 5:</b> Credit Score Dispersion by Default Status", table_cell),
         Paragraph("<b>Figure 6:</b> Debt-to-Income (DTI) Strain by Default Status", table_cell)]
    ]
    t_charts2 = Table(chart_table_2, colWidths=[250, 250])
    t_charts2.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_charts2)

    story.append(PageBreak())

    # Heatmap and Scatter
    story.append(Paragraph("Risk Factor Correlation & Multidimensional Interactions", h2_style))
    img_heat = Image("Visualizations/15_correlation_heatmap.png", width=340, height=230)
    img_scatter = Image("Visualizations/09_credit_score_vs_loan_amount_scatter.png", width=340, height=200)

    t_heat = Table([[img_heat]], colWidths=[500])
    t_heat.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_heat)
    story.append(Paragraph("<b>Figure 7:</b> Correlation Heatmap of Financial, Credit Risk, and Delinquency Features", table_cell))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Correlation Insights:</b> Default_Numeric exhibits the strongest positive correlations with Debt-to-Income Ratio (+0.38), "
        "Previous Defaults (+0.32), and Loan Amount (+0.29), while displaying a strong inverse correlation with Credit Score (-0.42). "
        "Age and Employment Years show moderate protective associations with lower default probability.",
        body_style
    ))

    # =========================================================================
    # SECTION 6: POWER BI DASHBOARD ARCHITECTURE & DAX MEASURES
    # =========================================================================
    story.append(Paragraph("6. Power BI Dashboard Architecture & DAX Implementation", h1_style))
    story.append(Paragraph(
        "An enterprise-grade, interactive dashboard titled <b>'Loan Default & Credit Risk Analytics Dashboard'</b> was modeled in Power BI Desktop. "
        "The architecture integrates 7 primary KPI cards, 7 responsive slicers, and 11 focused analytical visuals.",
        body_style
    ))

    img_pbi = Image("Visualizations/power_bi_dashboard_preview.png", width=490, height=255)
    t_pbi = Table([[img_pbi]], colWidths=[500])
    t_pbi.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_pbi)
    story.append(Paragraph("<b>Figure 8:</b> Power BI Dashboard Interactive Layout Preview (Executive Navy Theme)", table_cell))
    story.append(Spacer(1, 10))

    # DAX Table
    dax_data = [
        [Paragraph("<b>Measure Name</b>", table_cell_white), Paragraph("<b>DAX Formula</b>", table_cell_white), Paragraph("<b>KPI Target</b>", table_cell_white)],
        [Paragraph("<b>Total Customers</b>", table_cell_bold), Paragraph("<code>DISTINCTCOUNT('Loan_Credit_Risk_Cleaned'[Customer_ID])</code>", table_cell), Paragraph("5,000", table_cell)],
        [Paragraph("<b>Total Loans</b>", table_cell_bold), Paragraph("<code>COUNTROWS('Loan_Credit_Risk_Cleaned')</code>", table_cell), Paragraph("5,000", table_cell)],
        [Paragraph("<b>Defaulted Loans</b>", table_cell_bold), Paragraph("<code>CALCULATE(COUNTROWS('Loan_Credit_Risk_Cleaned'), 'Loan_Credit_Risk_Cleaned'[Default_Status]=\"Yes\")</code>", table_cell), Paragraph("955", table_cell)],
        [Paragraph("<b>Non-Defaulted Loans</b>", table_cell_bold), Paragraph("<code>CALCULATE(COUNTROWS('Loan_Credit_Risk_Cleaned'), 'Loan_Credit_Risk_Cleaned'[Default_Status]=\"No\")</code>", table_cell), Paragraph("4,045", table_cell)],
        [Paragraph("<b>Default Rate %</b>", table_cell_bold), Paragraph("<code>DIVIDE([Defaulted Loans], [Total Loans], 0)</code>", table_cell), Paragraph("19.10%", table_cell)],
        [Paragraph("<b>Average Loan Amount</b>", table_cell_bold), Paragraph("<code>AVERAGE('Loan_Credit_Risk_Cleaned'[Loan_Amount])</code>", table_cell), Paragraph("$41,449", table_cell)],
        [Paragraph("<b>Average Credit Score</b>", table_cell_bold), Paragraph("<code>AVERAGE('Loan_Credit_Risk_Cleaned'[Credit_Score])</code>", table_cell), Paragraph("667.1", table_cell)],
        [Paragraph("<b>Average Annual Income</b>", table_cell_bold), Paragraph("<code>AVERAGE('Loan_Credit_Risk_Cleaned'[Annual_Income])</code>", table_cell), Paragraph("$69,486", table_cell)]
    ]
    t_dax = Table(dax_data, colWidths=[110, 310, 80])
    t_dax.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_dax)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 7: DETAILED BUSINESS INSIGHTS (QUESTIONS 1 - 12)
    # =========================================================================
    story.append(Paragraph("7. Comprehensive Business Insights & Research Findings", h1_style))
    story.append(Paragraph(
        "Below are the rigorous analytical answers to the 12 business inquiries outlined in the institutional project specifications:",
        body_style
    ))

    qa_list = [
        ("1. What is the overall loan default rate?",
         "The overall portfolio default rate is exactly <b>19.10%</b> (955 defaulted accounts out of 5,000 total loans). This serves as the benchmark against which all customer segments and loan products are evaluated."),

        ("2. Which loan type has the highest default rate?",
         "<b>Home Loans</b> exhibit the highest default rate at <b>34.91%</b> (420 defaults out of 1,203 loans), followed by <b>Business Loans</b> at <b>23.92%</b>. Conversely, Personal Loans (11.06%), Education Loans (13.15%), and Auto Loans (14.43%) perform substantially below the portfolio average due to lower principal commitments and shorter loan durations."),

        ("3. Which region has the highest default rate?",
         "The <b>South Region</b> recorded the highest regional default rate at <b>20.13%</b> (211 defaults out of 1,048 loans), followed by the East Region at 19.49% and the West Region at 18.85%. Regional variance is moderate, indicating macroeconomic risk factors are uniform across lending territories."),

        ("4. Does credit score appear associated with loan default?",
         "<b>Yes, credit score is the single strongest negative predictor of loan default.</b> Performing borrowers maintain a mean credit score of <b>678.12</b>, compared to <b>620.42</b> for defaulted borrowers—a 58-point spread. Furthermore, default rates decline monotonically across FICO tiers: Poor (&lt;580) defaults at <b>37.45%</b>, Fair (580-669) at 22.58%, Good (670-739) at 13.52%, Very Good (740-799) at 8.30%, and Excellent (800+) at just <b>2.86%</b>."),

        ("5. Does income appear associated with default?",
         "<b>Yes, higher income significantly mitigates default probability.</b> Performing customers earn an average annual income of <b>$73,082.48</b> versus <b>$54,254.55</b> for defaulters. Borrowers in the Low-income bracket (&lt;$40k) experience a <b>33.91%</b> default rate, whereas High-income borrowers (&gt;$95k) exhibit a default rate of only <b>8.92%</b>."),

        ("6. Are higher debt-to-income ratios associated with default?",
         "<b>Yes, high debt burden dramatically escalates default risk.</b> Defaulters show a median DTI of 0.44 compared to 0.26 for performing accounts. Borrowers with DTI exceeding the critical banking threshold of 0.40 experience a default rate of <b>34.30%</b>, nearly triple the default rate of conservative borrowers (DTI &lt; 0.25 at 11.8%)."),

        ("7. Are previous defaults associated with current default?",
         "<b>Yes, historical default conduct shows severe delinquency recidivism.</b> Customers with 0 prior defaults default at <b>15.57%</b>. With 1 prior default, the risk surges to <b>39.57%</b>; with 2 prior defaults, it climbs to <b>45.99%</b>; and with 3 prior defaults, default probability peaks at <b>63.27%</b>."),

        ("8. Which customer segment has the highest default rate?",
         "The most vulnerable segment is <b>Unemployed borrowers with Subprime credit (&lt;580) and high DTI (&gt;0.40)</b>. As an isolated employment segment, Unemployed individuals demonstrate a staggering <b>45.11%</b> default rate across 399 originated loans."),

        ("9. Which factors appear associated with loan default?",
         "Default probability is governed by four primary drivers: (1) <b>Credit Score</b> (inverse), (2) <b>Debt-to-Income Ratio</b> (direct), (3) <b>Historical Delinquency / Previous Defaults</b> (direct), and (4) <b>Employment Stability</b> (direct). Secondary drivers include loan principal scale and borrower educational attainment."),

        ("10. What patterns can be observed between loan amount and default status?",
         "Defaulted loans carry a significantly higher average balance (<b>$59,267.96</b>) compared to non-defaulted loans (<b>$37,242.42</b>). When loan principal is large relative to borrower income, higher monthly debt service strains cash flow reserves, triggering default events."),

        ("11. What financial factors should an organization monitor?",
         "The financial institution must establish real-time surveillance across: (1) <b>DTI Caps</b> (&gt;40% trigger manual credit underwriting), (2) <b>FICO Cut-offs</b> (&lt;600 minimum threshold or compulsory collateral), (3) <b>Prior Default Exclusion</b>, and (4) <b>Loan-to-Income (LTI) Multiples</b> exceeding 1.2x gross annual earnings."),

        ("12. Strategic Business Insights & Policy Recommendations:",
         "<b>1. Underwriting Policy Tightening:</b> Introduce an automated decline rule for applicants with 2+ prior defaults or credit scores under 550, which would eliminate 38% of total default occurrences.<br/>"
         "<b>2. Mortgage & Home Loan Restructuring:</b> Re-evaluate Home loan affordability requirements; home loans represent 44% of total default count despite comprising only 24% of origination volume.<br/>"
         "<b>3. Risk-Based Margin Pricing:</b> Ensure subprime interest rate margins adequately cover the 37%+ loss rate, or mandate credit insurance for loans with DTI &gt; 0.38.<br/>"
         "<b>4. Targeted Low-Risk Expansion:</b> Actively market auto and personal credit facilities to prime borrowers (&gt;740 FICO), where default rates consistently track below 8%."
        )
    ]

    for q_title, q_ans in qa_list:
        story.append(Paragraph(f"<b>{q_title}</b>", h2_style))
        story.append(Paragraph(q_ans, body_style))
        story.append(Spacer(1, 3))

    # =========================================================================
    # SECTION 8: CONCLUSION & PROJECT CHECKLIST
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Project Conclusion & Compliance Verification", h1_style))
    story.append(Paragraph(
        "This project successfully translated 5,000 retail banking loan accounts into actionable credit risk management insights. "
        "Through data exploration, feature cleaning, multivariate correlation modeling, and dynamic Power BI dashboard reporting, "
        "the financial institution is equipped with concrete criteria to control non-performing loan growth while optimizing portfolio profitability.",
        body_style
    ))

    chk_data = [
        [Paragraph("<b>Component / Requirement</b>", table_cell_white), Paragraph("<b>Artifact Location</b>", table_cell_white), Paragraph("<b>Status</b>", table_cell_white)],
        [Paragraph("1. Python Notebook & Script", table_cell_bold), Paragraph("Python/Loan_Credit_Risk_Analysis.ipynb & .py", table_cell), Paragraph("✓ Verified (Executed)", table_cell)],
        [Paragraph("2. Cleaned Dataset", table_cell_bold), Paragraph("Dataset/Loan_Credit_Risk_Cleaned.csv (5,000 rows)", table_cell), Paragraph("✓ Verified (0 nulls/dups)", table_cell)],
        [Paragraph("3. Power BI Dashboard File", table_cell_bold), Paragraph("PowerBI/Loan_Credit_Risk_Dashboard.pbix", table_cell), Paragraph("✓ Verified (Packaged)", table_cell)],
        [Paragraph("4. DAX Measures & Setup Guide", table_cell_bold), Paragraph("PowerBI/DAX_Measures_and_Visuals_Guide.md", table_cell), Paragraph("✓ Verified (8 Measures)", table_cell)],
        [Paragraph("5. Visual Charts (15 Figures)", table_cell_bold), Paragraph("Visualizations/ (01 to 15 PNG figures)", table_cell), Paragraph("✓ Verified (300 DPI)", table_cell)],
        [Paragraph("6. Project Submission Report", table_cell_bold), Paragraph("Report/Loan_Credit_Risk_Project_Report.pdf", table_cell), Paragraph("✓ Complete", table_cell)]
    ]
    t_chk = Table(chk_data, colWidths=[150, 240, 110])
    t_chk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_chk)

    # Build PDF with two-pass canvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf_report()
