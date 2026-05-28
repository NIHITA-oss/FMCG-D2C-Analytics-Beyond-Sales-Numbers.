# FMCG-D2C-Analytics-Beyond-Sales-Numbers.
What Actually Drives Revenue, Profit, and Growth in Consumer Brands


---

## The Problem This Project Solves

Most D2C dashboards answer: **"How much did we sell?"**

This project answers: **"Why did sales move — and what should we do about it?"**

Inspired by the Open Secret founder's post on building an AI-native D2C brand, this analysis goes 10x deeper than top-line revenue to surface the metrics that actually drive business decisions.

---

## Key Findings from 18,240 FMCG Transactions (2023–2025)

| Insight | Finding | Business Action |
|---|---|---|
| **Best channel by margin** | Wholesale: 26.5% vs 19.9% avg | Double down on wholesale partnerships |
| **Promotion ROI gap** | No Promo (3.0x) vs Festival Campaign (1.2x) | Reallocate 30% of festival budget |
| **Discount sweet spot** | Margin peaks at 5–10% discount | Never go above 15% — margin collapses |
| **Top category** | Personal Care: 26.0% avg margin | Prioritise SKU expansion here |
| **Revenue CAGR** | $4.59M → $5.02M (+9.4% YoY) | Accelerating — Q4 consistently strongest |

---

## What's Inside

```
📊 4 Analysis Charts
├── chart1_executive_dashboard.png   — Full KPI overview (6 panels)
├── chart2_why_sales_move.png        — The "why" behind every metric (6 panels)
├── chart3_profitability_deep_dive.png — Where money is made and where it leaks
└── chart4_ai_insights.png          — AI-powered D2C execution insights

📁 fmcg_analysis.py                 — Complete Python analysis (run this)
📁 README.md                        — This file
```

---

## The 4 Analysis Layers

### Layer 1 — Executive Dashboard
Monthly revenue and profit trends, category performance, channel comparison, YoY growth, discount-margin scatter, brand profitability ranking.

### Layer 2 — Why Sales Move
- **Seasonality heatmap** — which category peaks in which month
- **Channel × Category margin matrix** — where the best margin combinations are
- **Promotion ROI bubble chart** — volume vs return vs margin simultaneously
- **B2C vs B2B deep dive** — different revenue and margin profiles by segment
- **Sales rep quadrant** — stars vs volume hunters vs underperformers
- **Price-volume elasticity** — demand curves by category

### Layer 3 — Profitability Deep Dive
- **Revenue waterfall** — Gross Sales → Discounts → COGS → Logistics → Marketing → Profit
- **Margin trends** — which categories are improving or declining over time
- **SKU-level pareto** — top 15 products by revenue with margin coding
- **Regional profitability map** — where geography creates margin differences

### Layer 4 — AI-Powered Insights
- **Discount sweet spot** — optimal discount band before margin collapse
- **Channel × Promotion ROI matrix** — best combination of where and how to promote
- **Quarterly category velocity** — momentum vs stagnation signals

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/[your-username]/fmcg-d2c-analytics

# Install dependencies
pip install pandas numpy matplotlib seaborn

# Add your dataset
# Place fmcg_sales_marketing_profitability_2023_2025.csv in the root folder

# Run the analysis
python fmcg_analysis.py
```

---

## Tech Stack

- **Python** — pandas, numpy, matplotlib, seaborn
- **Analysis** — cohort metrics, elasticity curves, ROI modelling, margin decomposition
- **Visualisation** — 20+ charts across 4 analysis modules

---

## About

Built by **Nihita Raj** — Economics & Mathematics graduate (Miranda House, DU). Interested in AI applied to consumer brands, D2C analytics, and data-driven business strategy.


---

*This project was built as a demonstration of applied analytics for D2C consumer brands — specifically exploring the metrics that explain why sales move, not just that they moved.*
