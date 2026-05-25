<div align="center">

# 🛍️ Omnichannel Retail Sales & Inventory Analytics Dashboard

**Developed by: Rohit Ranjan**
*Data Analyst & AI/ML Intern @ Infotact Solutions | B.Tech IT @ VBSPU*

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-MySQL-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github)](https://github.com/ranjannrohit)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=18&pause=1000&color=F59E0B&center=true&vCenter=true&width=600&lines=End-to-End+Retail+Analytics+Pipeline;641K%2B+Transactions+%7C+%2473M+Revenue+Analyzed;Python+%2B+SQL+%2B+Power+BI+%2B+Tableau;Infotact+Solutions+Internship+Project+%E2%9C%85"/>

> **Official Internship Project Submission** — An end-to-end data analytics pipeline transforming raw omnichannel retail data into strategic business insights.

![Data Analytics](https://user-images.githubusercontent.com/74038190/212749447-bfb7e725-6987-49d9-ae85-2015e3e7cc41.gif)

</div>

---

## 📌 Project Overview

This project builds a complete data analytics solution for a multi-channel retailer. It unifies **physical store** and **online** sales data, cleans and prepares the data, performs SQL aggregations and business metrics, and presents insights through an interactive **Power BI dashboard**.

**Problem Statement:**
In the rapidly digitizing retail landscape, offline businesses transitioning to digital models frequently encounter systemic bottlenecks due to fragmented data across multiple sales channels. This project solves that by creating a unified data analytics pipeline enabling inventory managers, store managers, and regional directors to make data-driven decisions.

**Key business questions answered:**
- 💰 What is our total revenue & average transaction value?
- 📊 How do sales compare across channels (Store, Website, MobileApp)?
- 🏆 Which product categories are top-performers?
- 📈 How do revenues trend month-to-month?
- 🌍 Which cities/regions drive the most sales?
- 👥 What are customer spending patterns and growth opportunities?

---

## 🏆 Key Results

<div align="center">

| 📊 Metric | 💡 Value | 🔍 Insight |
|-----------|---------|-----------|
| **Total Revenue** | $73,214,931 | 5-year cumulative across all channels |
| **Total Transactions** | 641,843 | High transaction volume reflects retail scale |
| **Avg Transaction Value** | $114.07 | Mid-to-premium product mix |
| **Unique Customers** | 5,001 | Concentrated base; growth opportunity |
| **Revenue/Customer** | $14,641 | High customer lifetime value |
| **Top Channel** | Store — 41.3% | Physical retail still dominant |
| **Top City** | Dubai — 56% | Geographic concentration risk |
| **Q4 Revenue %** | 18% of annual | Peak seasonal opportunity |

</div>

---

## 🏆 Project Progress

| Week | Task | Status | Key Outputs |
|------|------|--------|-------------|
| **Week 1** | Data Cleaning & EDA | ✅ Complete | Cleaned 6 CSV files; handled nulls, outliers, date formats |
| **Week 2** | SQL Database & Aggregations | ✅ Complete | MySQL database; 8 SQL queries; KPIs extracted |
| **Week 3** | Power BI Dashboard | ✅ Complete | Interactive dashboard with 6+ visualizations |
| **Week 4** | Final Report & Insights | ✅ Complete | Strategic recommendations; GitHub finalized |

---

## 📂 Repository Structure

```
retail-analytics-project/
├── README.md                          # Project overview & setup guide
├── FINAL_REPORT.md                    # Week 4: Business insights & recommendations
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Excludes raw data & credentials
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb        # Week 1: Data import, profiling, cleaning
│   └── 02_exploratory_analysis.ipynb # Week 1: EDA, visualizations, insights
│
├── sql/
│   ├── 01_create_schema.sql          # Week 2: Table creation & schema
│   ├── 02_load_data.sql              # Week 2: Data import into database
│   └── 03_analytics_queries.sql      # Week 2: Business metrics & aggregations
│
├── data/
│   ├── raw/                          # Original CSV files (in .gitignore)
│   └── cleaned/                      # Processed datasets ready for SQL
│
├── dashboard/
│   ├── retail_dashboard.pbix         # Week 3: Interactive Power BI dashboard
│   └── dashboard_screenshot.png      # High-resolution screenshot
│
└── LICENSE                           # MIT License
```

---

## 📊 Dataset Description

- **Files**: 6 CSV files (~2.5M rows total)
- **Time Period**: 2021–2025 (5 years)
- **Clean Records**: 641,843 transactions
- **Unique Customers**: 5,001

### Data Quality Issues Resolved

| Issue | Count | Action Taken |
|-------|-------|-------------|
| NULL values | 234 missing entries | Removed rows with critical NULL fields |
| Duplicates | 12 duplicate IDs | Removed exact duplicates |
| Date format issues | 156 malformed dates | Standardized to YYYY-MM-DD |
| Outlier prices | 8 prices > 10,000 | Verified as bulk orders; retained |
| Missing channel labels | 45 blank channels | Filled with "Unknown" |

**Final Data Completeness: 99.8%**

---

## 🔍 SQL Analytics — Core Queries

### Query 1: Revenue KPIs
```sql
SELECT 
  SUM(revenue) as total_revenue,
  COUNT(DISTINCT transaction_id) as total_transactions,
  COUNT(DISTINCT customer_id) as unique_customers,
  ROUND(AVG(revenue), 2) as avg_transaction_value
FROM transactions
WHERE date BETWEEN '2021-01-01' AND '2025-12-31';
```

### Query 2: Revenue by Sales Channel
```sql
SELECT 
  channel,
  SUM(revenue) as channel_revenue,
  ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM transactions), 2) as pct_of_total
FROM transactions
GROUP BY channel
ORDER BY channel_revenue DESC;
```

**Results:**
| Channel | Revenue | % of Total |
|---------|---------|-----------|
| Store | $30,231,970 | 41.3% |
| Website | $20,300,319 | 27.7% |
| MobileApp | $13,097,686 | 17.9% |
| Amazon | $6,470,766 | 8.8% |
| Noon | $3,114,189 | 4.3% |

### Query 3: Window Function — City Rankings
```sql
SELECT 
  city,
  SUM(revenue) as city_revenue,
  RANK() OVER (ORDER BY SUM(revenue) DESC) as revenue_rank
FROM transactions
GROUP BY city;
```

---

## 📊 Power BI Dashboard

### Key Visualizations
1. **Monthly Sales Trend** — Line chart showing 5-year revenue trajectory
2. **Revenue by Product Category** — Bar chart (Electronics dominates 65%)
3. **Sales by City** — Geographic performance comparison
4. **Sales by Day of Week** — Peak day identification
5. **Revenue by Channel** — Omnichannel distribution
6. **KPI Cards** — Total Revenue, AOV, Transactions, Customers

### Interactive Features
- 📅 Date Range Slider
- 🏙️ City Filter
- 📱 Channel Filter
- 🔍 Drill-through to transaction level

---

## 🎯 Key Business Insights

### Finding 1: Seasonal Patterns 📈
- Q4 = 18% of annual revenue ($13.1M)
- January & July are peak months
- **Recommendation:** Build inventory +25% before Q4

### Finding 2: Omnichannel Opportunity 🛒
- Online channels = 52.7% of revenue
- Only 5,001 unique customers
- **Recommendation:** Unified loyalty program across channels

### Finding 3: Geographic Risk 🌍
- Dubai = 56% of revenue
- **Recommendation:** Expand to Sharjah (+25% marketing spend)

### Finding 4: Product Mix 📦
- Electronics = 65% of revenue
- **Recommendation:** Bundle Electronics + Accessories for premium pricing

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Data Preparation | Python 3.10, Pandas, NumPy |
| Database & Querying | MySQL / SQL |
| Visualization | Power BI Desktop |
| Version Control | Git / GitHub |

---

## ✅ Evaluation Checklist

✅ 4 weeks of GitHub commits (consistent daily contributions)
✅ Data cleaning pipeline (NULL handling, outlier detection, date standardization)
✅ SQL database with complex queries (JOINs, GROUP BY, window functions)
✅ Interactive Power BI dashboard (6+ visualizations, dynamic filters)
✅ Final written report (strategic recommendations)
✅ README with complete documentation
✅ Data security (.gitignore for raw data, no credentials exposed)
✅ Semantic commits with feature branching

---

## 🚀 How to Run

```bash
# Clone repo
git clone https://github.com/ranjannrohit/retail-analytics-project.git
cd retail-analytics-project

# Setup Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run data cleaning
jupyter notebook notebooks/01_data_cleaning.ipynb

# Run SQL queries
mysql -u root -p < sql/01_create_schema.sql
mysql -u root -p < sql/02_load_data.sql
mysql -u root -p < sql/03_analytics_queries.sql

# Open Power BI Dashboard
# File → Open → dashboard/retail_dashboard.pbix
```

---

<div align="center">

### 💬 Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-10k%2B%20Followers-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-ranjannrohit-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ranjannrohit)
[![Email](https://img.shields.io/badge/Gmail-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rohitranjan09082002@gmail.com)

**Rohit Ranjan** — Data Analyst & AI/ML Intern @ Infotact Solutions
*B.Tech IT | VBSPU | Graduating June 2026*

![](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer)

</div>
