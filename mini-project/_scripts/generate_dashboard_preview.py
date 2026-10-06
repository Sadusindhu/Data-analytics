"""
Script: generate_dashboard_preview.py
Generates a realistic 16:9 composite Power BI dashboard layout preview image.
Embeds this into the Visualizations folder and PDF report.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

def create_powerbi_dashboard_image():
    df = pd.read_csv("Dataset/Loan_Credit_Risk_Cleaned.csv")
    
    # Setup 16:9 canvas
    fig = plt.figure(figsize=(16, 9), facecolor='#F4F6F9')
    
    # 1. Dashboard Header Banner
    header_ax = fig.add_axes([0.02, 0.91, 0.96, 0.07], facecolor='#1A365D')
    header_ax.axis('off')
    header_ax.text(0.02, 0.55, "LOAN DEFAULT & CREDIT RISK ANALYTICS DASHBOARD", color='white',
                   fontsize=18, fontweight='bold', va='center')
    header_ax.text(0.02, 0.22, "Executive Credit Risk Monitoring & Portfolio Quality Overview | Retail Lending Division",
                   color='#CBD5E1', fontsize=9.5, va='center')
    header_ax.text(0.98, 0.5, "POWER BI DESKTOP REPORT", color='#E2E8F0',
                   fontsize=11, fontweight='bold', ha='right', va='center')

    # 2. KPI Cards Row (Top)
    kpis = [
        ("Total Customers", f"{df['Customer_ID'].nunique():,}", "#1E293B"),
        ("Total Loans", f"{df['Loan_ID'].nunique():,}", "#1E293B"),
        ("Defaulted Loans", f"{(df['Default_Status']=='Yes').sum():,}", "#DC2626"),
        ("Default Rate %", f"{(df['Default_Status']=='Yes').mean()*100:.1f}%", "#DC2626"),
        ("Avg Loan Amount", f"${df['Loan_Amount'].mean():,.0f}", "#0369A1"),
        ("Avg Credit Score", f"{df['Credit_Score'].mean():.1f}", "#0D9488"),
        ("Avg Annual Income", f"${df['Annual_Income'].mean():,.0f}", "#4338CA")
    ]
    
    kpi_width = 0.96 / len(kpis) - 0.008
    for i, (title, val, col) in enumerate(kpis):
        x = 0.02 + i * (kpi_width + 0.0093)
        ax_kpi = fig.add_axes([x, 0.81, kpi_width, 0.085], facecolor='white')
        ax_kpi.axis('off')
        # border rect
        rect = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03,rounding_size=0.05",
                                      linewidth=1, edgecolor='#E2E8F0', facecolor='white', transform=ax_kpi.transAxes)
        ax_kpi.add_patch(rect)
        ax_kpi.text(0.5, 0.70, title.upper(), fontsize=7.5, fontweight='bold', color='#64748B', ha='center', va='center')
        ax_kpi.text(0.5, 0.28, val, fontsize=14, fontweight='bold', color=col, ha='center', va='center')

    # 3. Left Slicer Panel
    ax_slicer = fig.add_axes([0.02, 0.03, 0.16, 0.76], facecolor='#FFFFFF')
    ax_slicer.axis('off')
    rect_slicer = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                        linewidth=1, edgecolor='#E2E8F0', facecolor='#FFFFFF', transform=ax_slicer.transAxes)
    ax_slicer.add_patch(rect_slicer)
    
    ax_slicer.text(0.08, 0.96, "PORTFOLIO SLICERS", fontsize=10, fontweight='bold', color='#1E293B')
    
    slicers = [
        ("Gender", "All (Male, Female)"),
        ("Education", "All (Bachelor, Master, PhD...)"),
        ("Employment Status", "All (Employed, Self, Unemp)"),
        ("Loan Type", "All (Personal, Home, Auto...)"),
        ("Region", "All (North, South, East...)"),
        ("Default Status", "All (No, Yes)"),
        ("Credit Score Group", "All (Poor, Fair, Good...)")
    ]
    for idx, (s_name, s_val) in enumerate(slicers):
        y = 0.88 - idx * 0.125
        ax_slicer.text(0.08, y, s_name, fontsize=8, fontweight='bold', color='#475569')
        # Slicer input box representation
        box = patches.FancyBboxPatch((0.08, y - 0.055), 0.84, 0.045, boxstyle="round,pad=0.01,rounding_size=0.02",
                                     linewidth=0.8, edgecolor='#CBD5E1', facecolor='#F8FAFC', transform=ax_slicer.transAxes)
        ax_slicer.add_patch(box)
        ax_slicer.text(0.12, y - 0.032, s_val, fontsize=7.5, color='#64748B')
        ax_slicer.text(0.86, y - 0.032, "▼", fontsize=6.5, color='#94A3B8')

    # 4. Visual 1: Donut Chart - Default Distribution
    ax_v1 = fig.add_axes([0.20, 0.44, 0.24, 0.35], facecolor='white')
    ax_v1.set_title("1. Loan Default Distribution", fontsize=9.5, fontweight='bold', color='#1E293B', pad=10)
    counts = df['Default_Status'].value_counts()
    wedges, texts, autotexts = ax_v1.pie(counts, labels=['Non-Default', 'Default'], autopct='%1.1f%%',
                                        colors=['#10B981', '#EF4444'], startangle=140,
                                        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
                                        textprops=dict(fontsize=8, fontweight='bold'))
    for autotext in autotexts:
        autotext.set_fontsize(8.5)
        autotext.set_color('white')

    # 5. Visual 2: Default Rate by Loan Type (Bar Chart)
    ax_v2 = fig.add_axes([0.47, 0.44, 0.25, 0.35], facecolor='white')
    ax_v2.set_title("2. Default Rate by Loan Type", fontsize=9.5, fontweight='bold', color='#1E293B')
    lt_def = (df.groupby('Loan_Type')['Default_Numeric'].mean() * 100).sort_values()
    bars = ax_v2.barh(lt_def.index, lt_def.values, color='#F97316', edgecolor='#EA580C', height=0.55)
    ax_v2.set_xlabel("Default Rate (%)", fontsize=8, fontweight='bold')
    ax_v2.tick_params(labelsize=8)
    for bar in bars:
        w = bar.get_width()
        ax_v2.text(w + 0.6, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center', fontsize=7.5, fontweight='bold')
    ax_v2.set_xlim(0, 42)

    # 6. Visual 3: Default Rate by Credit Score Group (Column Chart)
    ax_v3 = fig.add_axes([0.75, 0.44, 0.23, 0.35], facecolor='white')
    ax_v3.set_title("3. Default Rate by Credit Score Group", fontsize=9.5, fontweight='bold', color='#1E293B')
    cs_def = (df.groupby('Credit_Score_Group', observed=False)['Default_Numeric'].mean() * 100)
    bars_cs = ax_v3.bar(range(len(cs_def)), cs_def.values, color='#3B82F6', edgecolor='#1D4ED8', width=0.55)
    ax_v3.set_xticks(range(len(cs_def)))
    ax_v3.set_xticklabels(['<580', '580-669', '670-739', '740-799', '800+'], fontsize=7.5, rotation=15)
    ax_v3.set_ylabel("Default Rate (%)", fontsize=8, fontweight='bold')
    ax_v3.tick_params(labelsize=8)
    for bar in bars_cs:
        h = bar.get_height()
        ax_v3.text(bar.get_x() + bar.get_width()/2, h + 0.8, f"{h:.1f}%", ha='center', fontsize=7.5, fontweight='bold')
    ax_v3.set_ylim(0, 45)

    # 7. Visual 4: Default Rate by Employment Status (Bar Chart)
    ax_v4 = fig.add_axes([0.20, 0.05, 0.24, 0.34], facecolor='white')
    ax_v4.set_title("4. Default Rate by Employment Status", fontsize=9.5, fontweight='bold', color='#1E293B')
    emp_def = (df.groupby('Employment_Status')['Default_Numeric'].mean() * 100).sort_values()
    bars_emp = ax_v4.barh(emp_def.index, emp_def.values, color='#8B5CF6', edgecolor='#6D28D9', height=0.55)
    ax_v4.set_xlabel("Default Rate (%)", fontsize=8, fontweight='bold')
    ax_v4.tick_params(labelsize=8)
    for bar in bars_emp:
        w = bar.get_width()
        ax_v4.text(w + 0.8, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center', fontsize=7.5, fontweight='bold')
    ax_v4.set_xlim(0, 52)

    # 8. Visual 5: Total Loan Volume by Loan Type
    ax_v5 = fig.add_axes([0.47, 0.05, 0.25, 0.34], facecolor='white')
    ax_v5.set_title("5. Total Capital Exposure by Loan Type", fontsize=9.5, fontweight='bold', color='#1E293B')
    vol = (df.groupby('Loan_Type')['Loan_Amount'].sum() / 1e6).sort_values(ascending=False)
    bars_vol = ax_v5.bar(vol.index, vol.values, color='#0EA5E9', edgecolor='#0284C7', width=0.55)
    ax_v5.set_ylabel("Total Amount ($ Millions)", fontsize=8, fontweight='bold')
    ax_v5.tick_params(labelsize=8)
    for bar in bars_vol:
        h = bar.get_height()
        ax_v5.text(bar.get_x() + bar.get_width()/2, h + 1, f"${h:.1f}M", ha='center', fontsize=7.5, fontweight='bold')
    ax_v5.set_ylim(0, max(vol.values) * 1.18)

    # 9. Visual 6: DTI vs Default Status (Box/Violin preview)
    ax_v6 = fig.add_axes([0.75, 0.05, 0.23, 0.34], facecolor='white')
    ax_v6.set_title("6. Debt-to-Income (DTI) by Default Status", fontsize=9.5, fontweight='bold', color='#1E293B')
    dti_no = df[df['Default_Status'] == 'No']['Debt_to_Income_Ratio']
    dti_yes = df[df['Default_Status'] == 'Yes']['Debt_to_Income_Ratio']
    bp = ax_v6.boxplot([dti_no, dti_yes], patch_artist=True, tick_labels=['Non-Default', 'Default'],
                       medianprops=dict(color='black', linewidth=1.5))
    colors = ['#A7F3D0', '#FECACA']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    ax_v6.set_ylabel("Debt-to-Income Ratio", fontsize=8, fontweight='bold')
    ax_v6.tick_params(labelsize=8)

    preview_path = "Visualizations/power_bi_dashboard_preview.png"
    plt.savefig(preview_path, dpi=300)
    plt.close()
    print(f"Generated Power BI Dashboard composite preview at: {preview_path}")

if __name__ == "__main__":
    create_powerbi_dashboard_image()
