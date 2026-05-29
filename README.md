# Financial Analysis & Intelligent Forecasting
### End-to-End Business Intelligence + Machine Learning Project

> An integrated system that bridges the gap between **descriptive analysis** and **predictive forecasting** — transforming 16 months of raw financial data into a fully interactive dashboard with a 6-month forward-looking forecast engine.

---

## Project Overview

| Attribute | Details |
|---|---|
| **Historical Data** | September 2021 → December 2022 (16 months) |
| **Forecast Horizon** | January 2023 → June 2023 (6 months) |
| **Financial KPIs** | Net Sales, Units Sold, Profit, Discounts |
| **Analysis Dimensions** | Customer Segment, Country, Product |
| **BI Tool** | Power BI |
| **ML Language** | Python |

---

## Part 1 — Power BI Dashboard

### 1.1 Analysis Scope
- **Overall Performance** — Total sales & profit trends across time periods, identifying growth and decline patterns
- **Geographical Analysis** — Country-level performance to surface the most profitable markets
- **Segmental Analysis** — Customer segment breakdown to guide targeted strategic decisions
- **Product Analysis** — Top-selling and highest-margin products, including discount impact on volume

---

### 1.2 Dashboard Backend & UX Engineering

> This is where the real engineering lives — most dashboards stop at visuals. This one was architected from the backend.

**Optimized Bookmarks & Selections**
- The dashboard eliminates page-load friction entirely by using **Bookmarks + Selections** to create dynamic visual layers
- Elements show/hide instantly based on user context — no new pages, no reload delays
- Each analysis view is a state, not a page — resulting in a significantly faster, cleaner experience

**Automated Toggle Buttons (Historical ↔ Forecasting)**
- Every analysis dimension — Products, Countries, Segments, and Time Periods — has a **dedicated toggle button**
- Clicking switches seamlessly between the **Historical Analysis view** and the **Forecasting Dashboard view** for that exact dimension
- Buttons use **dynamic formatting** (Active / Inactive states) so the user always knows which mode they're in at a glance

**Custom Tooltip Pages**
- Hovering over key data points triggers **custom-designed tooltip pages** — not default tooltips
- Surfaces granular detail (exact discount breakdowns, precise profit margins per month) without cluttering the main canvas
- Keeps the interface minimal while maximizing the depth of available insight

**Result:** Zero page reloads · Minimal click-paths · Maximum analytical depth

---

## Part 2 — ML Forecasting Engine (Python)

### 2.1 Methodology

**Algorithm — Exponential Smoothing (ETS)**
- Selected for its proven robustness on short time-series datasets (16 months)
- Significantly outperforms complex ML models on small data, which are prone to overfitting

**Auto-Optimization**
- A custom algorithm automatically iterates through **all possible configurations** of Trend and Seasonality parameters
- Guarantees the absolute best-performing model is selected independently for each financial metric

**Top-Down Distribution**
- The model forecasts **macro-level company totals** first
- Then distributes figures down to the micro-level (Product × Country × Segment) based on precise historical weighting
- Ensures full logical consistency across every dimension of the dashboard

---

### 2.2 Model Accuracy

Evaluated on unseen holdout data:

| Metric | Accuracy | Notes |
|---|---|---|
| Discounts | **80.86%** | Highly stable — reflects a predictable discount policy |
| Units Sold | **72.87%** | High confidence for demand & supply chain planning |
| Sales | **69.40%** | Reliable outlook for cash flow & revenue forecasting |
| Profit | **59.03%** | Realistic baseline — profit is inherently the most volatile metric |

---

## Part 3 — System Integration

The ML module outputs a **structured CSV** containing granular forecasts mapped to every combination of:

```
Date × Segment × Country × Product
```

This file is loaded directly into the **Power BI data model**. Combined with the Bookmark architecture, Line Charts plot historical actuals and forecasted projections **within the same visual** — a seamless analytical transition between past and future.

---

## Business Value

| Use Case | Impact |
|---|---|
| **Inventory Management** | Units Sold forecasts prevent overstocking and stockouts |
| **Financial Planning** | Sales & Profit projections support data-driven budget drafting |
| **Executive UX** | Backend engineering minimizes click-paths and saves management time |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Power BI** | Interactive dashboard & UX engineering |
| **Python** | ML forecasting engine |
| **Pandas** | Data manipulation & preprocessing |
| **Statsmodels** | ETS model implementation |

---

> *This project goes beyond traditional reporting — it delivers an enterprise-grade solution where descriptive BI and predictive ML coexist in a single, technically optimized, decision-ready interface.*
