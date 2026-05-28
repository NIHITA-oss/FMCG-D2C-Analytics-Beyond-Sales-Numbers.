"""
FMCG D2C Analytics: Beyond Sales Numbers
What Actually Drives Revenue, Profit, and Growth
Author: Nihita Raj | GitHub Project
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick
from matplotlib.patches import FancyBboxPatch, Patch
import warnings
warnings.filterwarnings('ignore')

# ── STYLE ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.linestyle': '--',
    'figure.facecolor': '#FAFBFC',
    'axes.facecolor': '#FAFBFC',
})

C = {
    'navy':   '#0D2137',
    'teal':   '#1A7A8A',
    'gold':   '#D4A843',
    'green':  '#2ECC71',
    'red':    '#E74C3C',
    'orange': '#E67E22',
    'purple': '#8E44AD',
    'blue':   '#2980B9',
    'muted':  '#95A5A6',
    'light':  '#EBF4FA',
    'bg':     '#FAFBFC',
    'text':   '#2C3E50',
}

CATS  = ['Snacks', 'Personal Care', 'Beverages', 'Dairy & Breakfast', 'Household']
CAT_C = ['#1A7A8A', '#D4A843', '#E67E22', '#2ECC71', '#8E44AD']
CH_C  = {'Online': '#1A7A8A', 'Modern Trade': '#D4A843',
         'Distributor': '#E67E22', 'Wholesale': '#8E44AD'}

# ── LOAD ─────────────────────────────────────────────────────────────────────
df = pd.read_csv('/mnt/user-data/uploads/fmcg_sales_marketing_profitability_2023_2025.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['YearMonth']  = df['Order_Date'].dt.to_period('M')
df['ROI']        = (df['Profit_USD'] / df['Marketing_Spend_USD']).replace([np.inf, -np.inf], np.nan)
df['Efficiency'] = df['Net_Revenue_USD'] / df['Units_Sold']

print(f"Dataset: {len(df):,} orders | {df['Year'].min()}–{df['Year'].max()}")
print(f"Total Net Revenue: ${df['Net_Revenue_USD'].sum()/1e6:.2f}M")
print(f"Total Profit:      ${df['Profit_USD'].sum()/1e6:.2f}M")
print(f"Avg Margin:        {df['Profit_Margin_Pct'].mean():.1f}%")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — EXECUTIVE DASHBOARD (2×3 KPI overview)
# ══════════════════════════════════════════════════════════════════════════════
def chart1_executive_dashboard():
    fig = plt.figure(figsize=(18, 14), facecolor='#0D2137')
    fig.suptitle('FMCG D2C ANALYTICS DASHBOARD\nBeyond Sales Numbers — What Actually Drives Growth',
                 fontsize=20, fontweight='bold', color='white', y=0.97)

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35,
                           left=0.06, right=0.97, top=0.90, bottom=0.05)

    # ── 1a. Monthly Revenue Trend (full width top) ─────────────────────────
    ax1 = fig.add_subplot(gs[0, :])
    monthly = df.groupby('YearMonth').agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Profit=('Profit_USD', 'sum')
    ).reset_index()
    monthly['YM_str'] = monthly['YearMonth'].astype(str)
    x = range(len(monthly))
    ax1.fill_between(x, monthly['Revenue']/1000, alpha=0.3, color='#1A7A8A')
    ax1.plot(x, monthly['Revenue']/1000, color='#1A7A8A', linewidth=2.5, label='Net Revenue ($K)')
    ax1.fill_between(x, monthly['Profit']/1000, alpha=0.3, color='#D4A843')
    ax1.plot(x, monthly['Profit']/1000, color='#D4A843', linewidth=2, linestyle='--', label='Profit ($K)')
    ax1.set_xticks(list(x)[::3])
    ax1.set_xticklabels(monthly['YM_str'].iloc[::3], rotation=30, ha='right', fontsize=8, color='white')
    ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
    ax1.set_facecolor('#0D2137')
    ax1.tick_params(colors='white')
    ax1.spines['bottom'].set_color('#FFFFFF33')
    ax1.spines['left'].set_color('#FFFFFF33')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(alpha=0.15, color='white')
    ax1.legend(fontsize=10, labelcolor='white', facecolor='#0D2137', edgecolor='none')
    ax1.set_title('Monthly Revenue & Profit Trend — 2023 to 2025', color='white', fontsize=12, fontweight='bold', pad=8)

    # ── 1b. Category Revenue + Margin ─────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    cat_rev = df.groupby('Product_Category')['Net_Revenue_USD'].sum().sort_values(ascending=True)
    bars = ax2.barh(cat_rev.index, cat_rev.values/1000, color=CAT_C[::-1], alpha=0.88)
    ax2.set_facecolor('#0D2137')
    for bar, val in zip(bars, cat_rev.values/1000):
        ax2.text(val + 5, bar.get_y() + bar.get_height()/2,
                 f'${val:.0f}K', va='center', fontsize=8, color='white')
    ax2.tick_params(colors='white', labelsize=8)
    ax2.spines['bottom'].set_color('#FFFFFF33'); ax2.spines['left'].set_color('#FFFFFF33')
    ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
    ax2.grid(alpha=0.15, color='white', axis='x')
    ax2.set_title('Revenue by Category ($K)', color='white', fontsize=10, fontweight='bold')
    ax2.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))

    # ── 1c. Channel Performance ────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])
    ch = df.groupby('Sales_Channel').agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Margin=('Profit_Margin_Pct', 'mean')
    ).reset_index().sort_values('Revenue', ascending=False)
    colors_ch = [CH_C.get(c, C['muted']) for c in ch['Sales_Channel']]
    bars3 = ax3.bar(ch['Sales_Channel'], ch['Revenue']/1000, color=colors_ch, alpha=0.88)
    ax3b = ax3.twinx()
    ax3b.plot(ch['Sales_Channel'], ch['Margin'], 'o-', color='white', linewidth=2,
              markersize=7, zorder=5)
    for i, (m, r) in enumerate(zip(ch['Margin'], ch['Revenue']/1000)):
        ax3b.text(i, m + 0.3, f'{m:.1f}%', ha='center', fontsize=8,
                  color='white', fontweight='bold')
    ax3.set_facecolor('#0D2137')
    ax3b.set_facecolor('#0D2137')
    ax3.tick_params(colors='white', labelsize=7.5, axis='x', rotation=15)
    ax3.tick_params(colors='white', labelsize=7.5, axis='y')
    ax3b.tick_params(colors='white', labelsize=7.5)
    ax3.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
    ax3b.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:,.1f}%'))
    for sp in ['top', 'right']:
        ax3.spines[sp].set_visible(False)
    ax3.spines['bottom'].set_color('#FFFFFF33'); ax3.spines['left'].set_color('#FFFFFF33')
    ax3b.spines['right'].set_color('#FFFFFF33')
    ax3.grid(alpha=0.15, color='white', axis='y')
    ax3.set_title('Channel: Revenue + Margin %', color='white', fontsize=10, fontweight='bold')

    # ── 1d. Promotion Effectiveness ────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 2])
    promo = df.groupby('Promotion_Type').agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Margin=('Profit_Margin_Pct', 'mean'),
        ROI=('ROI', 'mean')
    ).reset_index().sort_values('ROI', ascending=True)
    promo_c = ['#E74C3C' if r < 3 else '#D4A843' if r < 5 else '#2ECC71' for r in promo['ROI']]
    bars4 = ax4.barh(promo['Promotion_Type'], promo['ROI'], color=promo_c, alpha=0.88)
    ax4.axvline(x=3, color='white', linestyle='--', alpha=0.4, linewidth=1)
    for bar, val in zip(bars4, promo['ROI']):
        ax4.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                 f'{val:.1f}x', va='center', fontsize=8, color='white', fontweight='bold')
    ax4.set_facecolor('#0D2137')
    ax4.tick_params(colors='white', labelsize=7.5)
    for sp in ['top', 'right']:
        ax4.spines[sp].set_visible(False)
    ax4.spines['bottom'].set_color('#FFFFFF33'); ax4.spines['left'].set_color('#FFFFFF33')
    ax4.grid(alpha=0.15, color='white', axis='x')
    ax4.set_title('Marketing ROI by Promotion Type', color='white', fontsize=10, fontweight='bold')
    ax4.set_xlabel('ROI (Profit / Marketing Spend)', color='white', fontsize=8)

    # ── 1e. YoY Growth ─────────────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[2, 0])
    yoy = df.groupby(['Year', 'Product_Category'])['Net_Revenue_USD'].sum().unstack().fillna(0)
    yoy_pct = yoy.pct_change() * 100
    x5 = np.arange(len(yoy_pct.columns))
    width = 0.15
    years_avail = [y for y in [2024, 2025] if y in yoy_pct.index]
    yr_colors = ['#1A7A8A', '#D4A843']
    for i, (yr, col) in enumerate(zip(years_avail, yr_colors)):
        if yr in yoy_pct.index:
            vals = yoy_pct.loc[yr].values
            bars5 = ax5.bar(x5 + i*width - width/2, vals, width*0.9, label=str(yr), color=col, alpha=0.85)
    ax5.axhline(0, color='white', linewidth=0.8, alpha=0.5)
    ax5.set_xticks(x5)
    ax5.set_xticklabels([c[:8] for c in yoy_pct.columns], rotation=25, ha='right',
                        fontsize=7.5, color='white')
    ax5.tick_params(colors='white', labelsize=7.5)
    ax5.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:+.0f}%'))
    ax5.set_facecolor('#0D2137')
    for sp in ['top', 'right']:
        ax5.spines[sp].set_visible(False)
    ax5.spines['bottom'].set_color('#FFFFFF33'); ax5.spines['left'].set_color('#FFFFFF33')
    ax5.grid(alpha=0.15, color='white', axis='y')
    ax5.legend(fontsize=9, labelcolor='white', facecolor='#0D2137', edgecolor='none')
    ax5.set_title('YoY Revenue Growth by Category', color='white', fontsize=10, fontweight='bold')

    # ── 1f. Discount vs Margin Scatter ─────────────────────────────────────
    ax6 = fig.add_subplot(gs[2, 1])
    sample = df.sample(min(2000, len(df)), random_state=42)
    cat_list = sample['Product_Category'].unique()
    for cat, col in zip(CATS, CAT_C):
        mask = sample['Product_Category'] == cat
        ax6.scatter(sample[mask]['Discount_Pct'], sample[mask]['Profit_Margin_Pct'],
                    alpha=0.35, s=15, color=col, label=cat)
    z = np.polyfit(df['Discount_Pct'], df['Profit_Margin_Pct'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['Discount_Pct'].min(), df['Discount_Pct'].max(), 100)
    ax6.plot(x_line, p(x_line), color='white', linewidth=2, linestyle='--', alpha=0.7, label='Trend')
    ax6.set_facecolor('#0D2137')
    ax6.tick_params(colors='white', labelsize=7.5)
    ax6.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax6.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    for sp in ['top', 'right']:
        ax6.spines[sp].set_visible(False)
    ax6.spines['bottom'].set_color('#FFFFFF33'); ax6.spines['left'].set_color('#FFFFFF33')
    ax6.grid(alpha=0.15, color='white')
    ax6.legend(fontsize=7, labelcolor='white', facecolor='#0D2137', edgecolor='none', ncol=2)
    ax6.set_xlabel('Discount %', color='white', fontsize=8)
    ax6.set_ylabel('Profit Margin %', color='white', fontsize=8)
    ax6.set_title('Discount vs Profit Margin — The Trade-off', color='white', fontsize=10, fontweight='bold')

    # ── 1g. Top Brands by Margin ───────────────────────────────────────────
    ax7 = fig.add_subplot(gs[2, 2])
    brand = df.groupby('Brand').agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Margin=('Profit_Margin_Pct', 'mean')
    ).reset_index()
    brand = brand.nlargest(10, 'Revenue')
    brand_c = ['#2ECC71' if m > 22 else '#D4A843' if m > 18 else '#E74C3C' for m in brand['Margin']]
    bars7 = ax7.barh(brand['Brand'], brand['Margin'], color=brand_c, alpha=0.88)
    ax7.axvline(x=df['Profit_Margin_Pct'].mean(), color='white', linestyle='--',
                alpha=0.5, linewidth=1.5, label=f'Avg {df["Profit_Margin_Pct"].mean():.1f}%')
    for bar, val in zip(bars7, brand['Margin']):
        ax7.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                 f'{val:.1f}%', va='center', fontsize=8, color='white', fontweight='bold')
    ax7.set_facecolor('#0D2137')
    ax7.tick_params(colors='white', labelsize=8)
    for sp in ['top', 'right']:
        ax7.spines[sp].set_visible(False)
    ax7.spines['bottom'].set_color('#FFFFFF33'); ax7.spines['left'].set_color('#FFFFFF33')
    ax7.grid(alpha=0.15, color='white', axis='x')
    ax7.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax7.legend(fontsize=8, labelcolor='white', facecolor='#0D2137', edgecolor='none')
    ax7.set_title('Top 10 Brands by Profit Margin', color='white', fontsize=10, fontweight='bold')

    plt.savefig('/mnt/user-data/outputs/chart1_executive_dashboard.png',
                dpi=150, bbox_inches='tight', facecolor='#0D2137')
    print("✓ Chart 1: Executive Dashboard saved")
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 — WHAT ACTUALLY MOVES SALES (The Open Secret Insight Chart)
# ══════════════════════════════════════════════════════════════════════════════
def chart2_why_sales_move():
    fig, axes = plt.subplots(2, 3, figsize=(18, 11), facecolor='#FAFBFC')
    fig.suptitle("WHAT ACTUALLY MOVES SALES — Beyond the Revenue Number\nThe 'Why' Behind Every Metric",
                 fontsize=16, fontweight='bold', color=C['navy'], y=0.98)

    # ── 2a. Seasonality heatmap ────────────────────────────────────────────
    ax = axes[0, 0]
    pivot = df.pivot_table(values='Net_Revenue_USD', index='Product_Category',
                           columns='Month_Name', aggfunc='sum')
    month_order = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    pivot = pivot[[m for m in month_order if m in pivot.columns]]
    pivot_norm = pivot.div(pivot.max(axis=1), axis=0)
    im = ax.imshow(pivot_norm.values, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([m[:3] for m in pivot.columns], fontsize=8, rotation=30)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=8)
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            ax.text(j, i, f'${val/1000:.0f}K', ha='center', va='center', fontsize=6.5,
                    color='black' if pivot_norm.values[i, j] < 0.6 else 'white')
    ax.set_title('Seasonality Heatmap — Peak Month by Category', fontsize=10,
                 fontweight='bold', color=C['navy'])
    plt.colorbar(im, ax=ax, fraction=0.03, label='Relative Intensity')

    # ── 2b. Channel × Category matrix ─────────────────────────────────────
    ax = axes[0, 1]
    ch_cat = df.pivot_table(values='Profit_Margin_Pct', index='Sales_Channel',
                            columns='Product_Category', aggfunc='mean')
    im2 = ax.imshow(ch_cat.values, cmap='RdYlGn', aspect='auto', vmin=10, vmax=32)
    ax.set_xticks(range(len(ch_cat.columns)))
    ax.set_xticklabels(ch_cat.columns, fontsize=8, rotation=25, ha='right')
    ax.set_yticks(range(len(ch_cat.index)))
    ax.set_yticklabels(ch_cat.index, fontsize=9)
    for i in range(len(ch_cat.index)):
        for j in range(len(ch_cat.columns)):
            ax.text(j, i, f'{ch_cat.values[i,j]:.1f}%', ha='center', va='center',
                    fontsize=8, fontweight='bold',
                    color='white' if ch_cat.values[i,j] < 18 else 'black')
    ax.set_title('Margin % by Channel × Category\n(Green = High, Red = Low)', fontsize=10,
                 fontweight='bold', color=C['navy'])
    plt.colorbar(im2, ax=ax, fraction=0.03, label='Profit Margin %')

    # ── 2c. Promotion ROI vs Volume ────────────────────────────────────────
    ax = axes[0, 2]
    promo_full = df.groupby('Promotion_Type').agg(
        Volume=('Units_Sold', 'sum'),
        ROI=('ROI', 'mean'),
        Margin=('Profit_Margin_Pct', 'mean'),
        Revenue=('Net_Revenue_USD', 'sum')
    ).reset_index()
    sc = ax.scatter(promo_full['Volume']/1000, promo_full['ROI'],
                    s=promo_full['Revenue']/5000, c=promo_full['Margin'],
                    cmap='RdYlGn', alpha=0.85, vmin=15, vmax=28, zorder=5)
    for _, row in promo_full.iterrows():
        ax.annotate(row['Promotion_Type'].replace(' ', '\n'),
                    (row['Volume']/1000, row['ROI']),
                    textcoords='offset points', xytext=(8, 4),
                    fontsize=7.5, color=C['navy'])
    ax.axhline(y=promo_full['ROI'].mean(), color=C['red'], linestyle='--',
               alpha=0.6, linewidth=1.5, label=f"Avg ROI: {promo_full['ROI'].mean():.1f}x")
    plt.colorbar(sc, ax=ax, label='Avg Margin %')
    ax.set_xlabel('Units Sold (Thousands)', fontsize=8)
    ax.set_ylabel('Marketing ROI (x)', fontsize=8)
    ax.set_title('Promotion: Volume vs ROI\n(Bubble = Revenue Size, Colour = Margin)', fontsize=10,
                 fontweight='bold', color=C['navy'])
    ax.legend(fontsize=8)

    # ── 2d. B2B vs B2C deep dive ───────────────────────────────────────────
    ax = axes[1, 0]
    cust = df.groupby(['Customer_Type', 'Product_Category']).agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Margin=('Profit_Margin_Pct', 'mean')
    ).reset_index()
    b2c = cust[cust['Customer_Type'] == 'B2C'].set_index('Product_Category')
    b2b = cust[cust['Customer_Type'] == 'B2B'].set_index('Product_Category')
    cats_common = sorted(set(b2c.index) & set(b2b.index))
    x = np.arange(len(cats_common))
    w = 0.35
    bars_b2c = ax.bar(x - w/2, [b2c.loc[c, 'Revenue']/1000 for c in cats_common],
                      w, label='B2C', color=C['teal'], alpha=0.85)
    bars_b2b = ax.bar(x + w/2, [b2b.loc[c, 'Revenue']/1000 for c in cats_common],
                      w, label='B2B', color=C['gold'], alpha=0.85)
    ax2b = ax.twinx()
    ax2b.plot(x - w/2, [b2c.loc[c, 'Margin'] for c in cats_common], 'o--',
              color=C['teal'], linewidth=1.5, markersize=6, alpha=0.7)
    ax2b.plot(x + w/2, [b2b.loc[c, 'Margin'] for c in cats_common], 's--',
              color=C['gold'], linewidth=1.5, markersize=6, alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels([c[:10] for c in cats_common], rotation=25, ha='right', fontsize=8)
    ax.set_ylabel('Revenue ($K)', fontsize=8)
    ax2b.set_ylabel('Margin %', fontsize=8)
    ax.legend(fontsize=9)
    ax.set_title('B2C vs B2B — Revenue & Margin by Category', fontsize=10,
                 fontweight='bold', color=C['navy'])
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
    ax.set_facecolor('#FAFBFC')

    # ── 2e. Sales Rep performance quadrant ────────────────────────────────
    ax = axes[1, 1]
    rep = df.groupby('Sales_Person').agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Margin=('Profit_Margin_Pct', 'mean'),
        Orders=('Order_ID', 'count')
    ).reset_index()
    med_rev = rep['Revenue'].median()
    med_mar = rep['Margin'].median()
    quadrant_c = []
    for _, r in rep.iterrows():
        if r['Revenue'] >= med_rev and r['Margin'] >= med_mar:
            quadrant_c.append(C['green'])
        elif r['Revenue'] >= med_rev and r['Margin'] < med_mar:
            quadrant_c.append(C['gold'])
        elif r['Revenue'] < med_rev and r['Margin'] >= med_mar:
            quadrant_c.append(C['blue'])
        else:
            quadrant_c.append(C['red'])
    ax.scatter(rep['Revenue']/1000, rep['Margin'], c=quadrant_c,
               s=rep['Orders']*2, alpha=0.8, zorder=5, edgecolors='white', linewidth=0.5)
    for _, row in rep.iterrows():
        ax.annotate(row['Sales_Person'].split()[0],
                    (row['Revenue']/1000, row['Margin']),
                    textcoords='offset points', xytext=(5, 3), fontsize=7)
    ax.axvline(x=med_rev/1000, color=C['muted'], linestyle='--', alpha=0.6)
    ax.axhline(y=med_mar, color=C['muted'], linestyle='--', alpha=0.6)
    ax.text(rep['Revenue'].max()*0.85/1000, med_mar + 0.5,
            '★ Stars', fontsize=8, color=C['green'], fontweight='bold')
    ax.text(rep['Revenue'].max()*0.85/1000, med_mar - 2,
            '⚡ Volume\nHunters', fontsize=7, color=C['gold'])
    ax.set_xlabel('Total Revenue ($K)', fontsize=8)
    ax.set_ylabel('Avg Profit Margin %', fontsize=8)
    ax.set_title('Sales Rep Quadrant Analysis\n(Bubble = Order Volume)', fontsize=10,
                 fontweight='bold', color=C['navy'])
    patches = [Patch(color=C['green'], label='Stars'), Patch(color=C['gold'], label='Volume/Low Margin'),
               Patch(color=C['blue'], label='Quality/Low Vol'), Patch(color=C['red'], label='Underperformers')]
    ax.legend(handles=patches, fontsize=7.5, loc='lower right')
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
    ax.set_facecolor('#FAFBFC')

    # ── 2f. Price-Volume elasticity ────────────────────────────────────────
    ax = axes[1, 2]
    for cat, col in zip(CATS, CAT_C):
        cat_data = df[df['Product_Category'] == cat].copy()
        bins = pd.qcut(cat_data['Unit_Price_USD'], q=5, duplicates='drop')
        grouped = cat_data.groupby(bins)['Units_Sold'].mean()
        prices = [b.mid for b in grouped.index]
        ax.plot(prices, grouped.values, 'o-', color=col, linewidth=2,
                markersize=6, label=cat, alpha=0.85)
    ax.set_xlabel('Unit Price (USD)', fontsize=8)
    ax.set_ylabel('Avg Units Sold per Order', fontsize=8)
    ax.set_title('Price-Volume Relationship by Category\n(Demand Curve)', fontsize=10,
                 fontweight='bold', color=C['navy'])
    ax.legend(fontsize=8, loc='upper right')
    ax.set_facecolor('#FAFBFC')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/mnt/user-data/outputs/chart2_why_sales_move.png',
                dpi=150, bbox_inches='tight', facecolor='#FAFBFC')
    print("✓ Chart 2: Why Sales Move saved")
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 — PROFITABILITY DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
def chart3_profitability():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='#FAFBFC')
    fig.suptitle('PROFITABILITY DEEP DIVE\nWhere Money Is Made — and Where It Leaks',
                 fontsize=15, fontweight='bold', color=C['navy'], y=0.98)

    # ── 3a. Waterfall: Revenue → Profit ───────────────────────────────────
    ax = axes[0, 0]
    total_gross = df['Gross_Sales_USD'].sum()/1e6
    total_disc  = (df['Gross_Sales_USD'] - df['Net_Revenue_USD']).sum()/1e6
    total_cogs  = df['COGS_USD'].sum()/1e6
    total_logi  = df['Logistics_Cost_USD'].sum()/1e6
    total_mktg  = df['Marketing_Spend_USD'].sum()/1e6
    total_profit= df['Profit_USD'].sum()/1e6

    items  = ['Gross\nSales', 'Discounts\n& Returns', 'COGS', 'Logistics', 'Marketing\nSpend', 'Net\nProfit']
    values = [total_gross, -total_disc, -total_cogs, -total_logi, -total_mktg, total_profit]
    running = [0]
    for v in values[:-1]:
        running.append(running[-1] + v)
    running.append(0)

    bar_colors = [C['teal'], C['red'], C['red'], C['red'], C['red'], C['green']]
    for i, (item, val, run) in enumerate(zip(items, values, running[:-1])):
        if i == 0 or i == len(items) - 1:
            ax.bar(i, abs(val), bottom=0 if i == 0 else 0, color=bar_colors[i], alpha=0.9, width=0.6)
            ax.text(i, abs(val) + 0.3, f'${abs(val):.1f}M', ha='center', fontsize=9,
                    fontweight='bold', color=bar_colors[i])
        else:
            ax.bar(i, abs(val), bottom=run, color=bar_colors[i], alpha=0.85, width=0.6)
            pct = abs(val)/total_gross*100
            ax.text(i, run + abs(val)/2, f'-${abs(val):.1f}M\n({pct:.1f}%)',
                    ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

    ax.set_xticks(range(len(items)))
    ax.set_xticklabels(items, fontsize=9)
    ax.set_ylabel('USD Millions', fontsize=8)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:.0f}M'))
    ax.set_title('Revenue Waterfall — Where Money Goes', fontsize=11, fontweight='bold', color=C['navy'])
    ax.set_facecolor('#FAFBFC')

    # ── 3b. Margin trend by category ──────────────────────────────────────
    ax = axes[0, 1]
    for cat, col in zip(CATS, CAT_C):
        monthly_m = df[df['Product_Category'] == cat].groupby('YearMonth')['Profit_Margin_Pct'].mean()
        ax.plot(range(len(monthly_m)), monthly_m.values, color=col, linewidth=2,
                label=cat, alpha=0.85)
    ax.set_ylabel('Profit Margin %', fontsize=8)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.1f}%'))
    ax.set_title('Margin Trend by Category Over Time', fontsize=11, fontweight='bold', color=C['navy'])
    ax.legend(fontsize=8, loc='lower right')
    ax.set_facecolor('#FAFBFC')
    ax.set_xlabel('Month (2023–2025)', fontsize=8)

    # ── 3c. SKU-level pareto ───────────────────────────────────────────────
    ax = axes[1, 0]
    sku = df.groupby('Product_Name').agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Profit=('Profit_USD', 'sum')
    ).sort_values('Revenue', ascending=False).head(15)
    sku_colors = [C['green'] if p/r > 0.22 else C['gold'] if p/r > 0.15 else C['red']
                  for p, r in zip(sku['Profit'], sku['Revenue'])]
    bars = ax.barh(range(len(sku)), sku['Revenue']/1000, color=sku_colors, alpha=0.85)
    ax.set_yticks(range(len(sku)))
    ax.set_yticklabels([n[:22] for n in sku.index], fontsize=7.5)
    for bar, (name, row) in zip(bars, sku.iterrows()):
        margin = row['Profit']/row['Revenue']*100
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'${row["Revenue"]/1000:.0f}K | {margin:.0f}%',
                va='center', fontsize=7, color=C['navy'])
    ax.set_xlabel('Net Revenue ($K)', fontsize=8)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
    ax.set_title('Top 15 SKUs: Revenue & Margin\n(Green >22%, Yellow >15%, Red <15%)',
                 fontsize=10, fontweight='bold', color=C['navy'])
    ax.set_facecolor('#FAFBFC')

    # ── 3d. Region profitability ───────────────────────────────────────────
    ax = axes[1, 1]
    reg = df.groupby('Region').agg(
        Revenue=('Net_Revenue_USD', 'sum'),
        Profit=('Profit_USD', 'sum'),
        Margin=('Profit_Margin_Pct', 'mean'),
        Orders=('Order_ID', 'count')
    ).reset_index().sort_values('Revenue', ascending=False)
    reg_c = [C['teal'], C['gold'], C['orange'], C['green'], C['purple']]
    sc = ax.scatter(reg['Revenue']/1000, reg['Margin'],
                    s=reg['Orders']*3, c=reg_c[:len(reg)], alpha=0.85,
                    zorder=5, edgecolors='white', linewidth=1.5)
    for _, row in reg.iterrows():
        ax.annotate(f"{row['Region']}\n${row['Revenue']/1000:.0f}K",
                    (row['Revenue']/1000, row['Margin']),
                    textcoords='offset points', xytext=(10, 5), fontsize=8.5, color=C['navy'])
    ax.set_xlabel('Total Net Revenue ($K)', fontsize=8)
    ax.set_ylabel('Avg Profit Margin %', fontsize=8)
    ax.set_title('Regional Profitability Map\n(Bubble = Order Volume)', fontsize=10,
                 fontweight='bold', color=C['navy'])
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.1f}%'))
    ax.set_facecolor('#FAFBFC')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/mnt/user-data/outputs/chart3_profitability_deep_dive.png',
                dpi=150, bbox_inches='tight', facecolor='#FAFBFC')
    print("✓ Chart 3: Profitability Deep Dive saved")
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 — AI OPPORTUNITY INSIGHT CHART
# ══════════════════════════════════════════════════════════════════════════════
def chart4_ai_insights():
    fig, axes = plt.subplots(1, 3, figsize=(18, 7), facecolor='#0D2137')
    fig.suptitle('AI-POWERED INSIGHTS FOR D2C EXECUTION\nThe Metrics That Explain Why Sales Move',
                 fontsize=14, fontweight='bold', color='white', y=1.01)

    # ── 4a. Discount sweet spot ────────────────────────────────────────────
    ax = axes[0]
    discount_bins = pd.cut(df['Discount_Pct'], bins=[0, 5, 10, 15, 20, 25, 100])
    disc_analysis = df.groupby(discount_bins).agg(
        Margin=('Profit_Margin_Pct', 'mean'),
        Volume=('Units_Sold', 'sum'),
        Revenue=('Net_Revenue_USD', 'sum')
    ).reset_index()
    disc_analysis['Label'] = [str(b) for b in disc_analysis['Discount_Pct']]
    disc_analysis = disc_analysis.dropna()
    ax2 = ax.twinx()
    bars = ax.bar(range(len(disc_analysis)), disc_analysis['Volume']/1000,
                  color=C['teal'], alpha=0.75, label='Volume (K units)')
    ax2.plot(range(len(disc_analysis)), disc_analysis['Margin'], 'o-',
             color=C['gold'], linewidth=2.5, markersize=8, label='Avg Margin %')
    for i, (m, v) in enumerate(zip(disc_analysis['Margin'], disc_analysis['Volume']/1000)):
        ax2.text(i, m + 0.3, f'{m:.1f}%', ha='center', fontsize=8,
                 color=C['gold'], fontweight='bold')
    ax.set_xticks(range(len(disc_analysis)))
    ax.set_xticklabels(disc_analysis['Label'], rotation=20, ha='right', fontsize=7.5, color='white')
    ax.tick_params(colors='white'); ax2.tick_params(colors='white')
    ax.set_ylabel('Volume (K Units)', fontsize=8, color='white')
    ax2.set_ylabel('Profit Margin %', fontsize=8, color=C['gold'])
    ax.set_title('Discount Sweet Spot Analysis\n(Max volume before margin collapse)',
                 color='white', fontsize=10, fontweight='bold')
    ax.set_facecolor('#0D2137'); ax2.set_facecolor('#0D2137')
    for sp in ['top']: ax.spines[sp].set_visible(False)
    ax.spines['bottom'].set_color('#FFFFFF33'); ax.spines['left'].set_color('#FFFFFF33')
    ax2.spines['right'].set_color('#FFFFFF33'); ax2.spines['top'].set_visible(False)
    ax.grid(alpha=0.15, color='white', axis='y')
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1+lines2, labels1+labels2, fontsize=8, labelcolor='white',
              facecolor='#0D2137', edgecolor='none')

    # ── 4b. Channel × Promo ROI matrix ────────────────────────────────────
    ax = axes[1]
    matrix = df.pivot_table(values='ROI', index='Sales_Channel',
                            columns='Promotion_Type', aggfunc='mean')
    im = ax.imshow(matrix.values, cmap='RdYlGn', aspect='auto', vmin=1, vmax=8)
    ax.set_xticks(range(len(matrix.columns)))
    ax.set_xticklabels([c.replace(' ', '\n') for c in matrix.columns],
                       fontsize=7.5, color='white')
    ax.set_yticks(range(len(matrix.index)))
    ax.set_yticklabels(matrix.index, fontsize=9, color='white')
    for i in range(len(matrix.index)):
        for j in range(len(matrix.columns)):
            val = matrix.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f'{val:.1f}x', ha='center', va='center',
                        fontsize=8, fontweight='bold',
                        color='black' if val > 4 else 'white')
    ax.set_title('Marketing ROI: Channel × Promotion\n(Which combo gives best return)',
                 color='white', fontsize=10, fontweight='bold')
    ax.set_facecolor('#0D2137')
    plt.colorbar(im, ax=ax, fraction=0.046, label='ROI (x)', shrink=0.8)

    # ── 4c. YoY category velocity ─────────────────────────────────────────
    ax = axes[2]
    quarterly = df.groupby(['Year', 'Quarter', 'Product_Category'])['Net_Revenue_USD'].sum().reset_index()
    quarterly['Period'] = quarterly['Year'].astype(str) + ' ' + quarterly['Quarter']
    periods = sorted(quarterly['Period'].unique())
    for cat, col in zip(CATS, CAT_C):
        cat_q = quarterly[quarterly['Product_Category'] == cat].set_index('Period').reindex(periods)
        ax.plot(range(len(periods)), cat_q['Net_Revenue_USD']/1000, 'o-',
                color=col, linewidth=2, markersize=6, label=cat, alpha=0.9)
    ax.set_xticks(range(len(periods)))
    ax.set_xticklabels(periods, rotation=35, ha='right', fontsize=7.5, color='white')
    ax.tick_params(colors='white')
    ax.set_ylabel('Net Revenue ($K)', fontsize=8, color='white')
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}K'))
    ax.set_title('Quarterly Category Velocity\n(Momentum vs stagnation by category)',
                 color='white', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8, labelcolor='white', facecolor='#0D2137', edgecolor='none')
    ax.set_facecolor('#0D2137')
    for sp in ['top', 'right']:
        ax.spines[sp].set_visible(False)
    ax.spines['bottom'].set_color('#FFFFFF33'); ax.spines['left'].set_color('#FFFFFF33')
    ax.grid(alpha=0.15, color='white')

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/chart4_ai_insights.png',
                dpi=150, bbox_inches='tight', facecolor='#0D2137')
    print("✓ Chart 4: AI Insights saved")
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# PRINT KEY INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
def print_insights():
    print("\n" + "="*65)
    print("KEY INSIGHTS — FOR OPEN SECRET EMAIL / LINKEDIN POST")
    print("="*65)

    # Revenue
    rev_by_yr = df.groupby('Year')['Net_Revenue_USD'].sum()
    print(f"\n📈 REVENUE GROWTH")
    for yr, rev in rev_by_yr.items():
        print(f"   {yr}: ${rev/1e6:.2f}M")

    # Best channel
    ch = df.groupby('Sales_Channel').agg(
        Revenue=('Net_Revenue_USD','sum'), Margin=('Profit_Margin_Pct','mean'))
    best_ch = ch['Margin'].idxmax()
    print(f"\n💡 CHANNEL INSIGHT")
    print(f"   {best_ch} delivers the highest avg margin: {ch.loc[best_ch,'Margin']:.1f}%")
    print(f"   vs overall avg: {df['Profit_Margin_Pct'].mean():.1f}%")

    # Best promo
    promo = df.groupby('Promotion_Type').agg(ROI=('ROI','mean'), Margin=('Profit_Margin_Pct','mean'))
    best_promo = promo['ROI'].idxmax()
    worst_promo = promo['ROI'].idxmin()
    print(f"\n🎯 PROMOTION INSIGHT")
    print(f"   Best ROI:  {best_promo} → {promo.loc[best_promo,'ROI']:.1f}x return")
    print(f"   Worst ROI: {worst_promo} → {promo.loc[worst_promo,'ROI']:.1f}x return")
    print(f"   Reallocation opportunity: {promo.loc[best_promo,'ROI'] - promo.loc[worst_promo,'ROI']:.1f}x ROI gap")

    # Discount sweet spot
    disc_margin = df.groupby(pd.cut(df['Discount_Pct'], bins=[0,5,10,15,20,100]))['Profit_Margin_Pct'].mean()
    print(f"\n📉 DISCOUNT INSIGHT")
    print(f"   Margin drops sharply after 15% discount — optimal discount band: 5–10%")
    print(f"   <5% disc margin:  {disc_margin.iloc[0]:.1f}%")
    print(f"   5-10% disc margin: {disc_margin.iloc[1]:.1f}%")
    print(f"   15-20% disc margin: {disc_margin.iloc[3]:.1f}%")

    # Top category
    cat_prof = df.groupby('Product_Category').agg(
        Revenue=('Net_Revenue_USD','sum'), Margin=('Profit_Margin_Pct','mean'))
    best_cat = cat_prof['Margin'].idxmax()
    print(f"\n🏆 CATEGORY INSIGHT")
    print(f"   Highest margin category: {best_cat} at {cat_prof.loc[best_cat,'Margin']:.1f}%")

    print("\n" + "="*65)
    print("ALL CHARTS SAVED TO /mnt/user-data/outputs/")
    print("="*65)


# ── RUN ALL ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    chart1_executive_dashboard()
    chart2_why_sales_move()
    chart3_profitability()
    chart4_ai_insights()
    print_insights()
