# E-Commerce Clickstream & Conversion Funnel Analytics

## Executive Summary
This project analyzes multi-stage conversion funnel drop-offs for an e-commerce platform using high-volume clickstream event data (3.5M+ logs). Leveraging Python for chunked data batch ingestion, SQLite for CTE-based session aggregation, and Tableau for interactive visualization, this analysis isolates core friction points across product discovery, cart abandonment, and checkout completion.

## Architecture & Tech Stack
* **Data Ingestion & Hygiene:** Python (`pandas`, `sqlite3`, `logging`)
* **Data Processing & SQL Analytics:** SQLite (Common Table Expressions, Conditional Aggregations, Indexing)
* **Business Intelligence & Visualization:** Tableau

## Business Problem & Strategic Objectives
* **Core Problem:** Low end-to-end user purchase conversion driven by unquantified drop-offs across user navigation journeys.
* **Primary Objective:** Measure session-level conversion rates across key funnel milestones (`View Product` → `Add to Cart` → `Purchase`), isolate primary attrition stages, and establish baseline funnel metrics for UX optimization and retargeting workflows.

## Key Analytical Insights

* **Significant Initial Attrition (`View` → `Cart`):** Out of 794,416 product view sessions, only 130,124 sessions proceeded to add items to the cart, representing a **16.38% progression rate** and an **83.62% drop-off rate**. [Inference] This indicates potential friction in product page engagement, pricing clarity, or inventory display.

* **Cart Abandonment Velocity (`Cart` → `Purchase`):** Of the 130,124 sessions with cart additions, 19,819 successfully completed a purchase (**15.23% checkout conversion rate**), resulting in an **84.77% cart drop-off rate**. [Inference] This highlights an immediate opportunity for automated cart-recovery trigger campaigns and streamlined checkout payment options.

* **End-to-End Conversion Baseline:** The overall end-to-end session conversion rate from initial product view to completed transaction stands at **2.49%** (19,819 purchases from 794,416 view sessions).

## Dashboard Preview
<img width="2730" height="1534" alt="E-Commerce Conversion Funnel Dashboard" src="https://github.com/user-attachments/assets/9a8c2d9e-e7ee-497d-b4f4-068b8e2fb78c" />


**[View Interactive Tableau Dashboard](https://public.tableau.com/views/E-CommerceClickstreamConversionFunnelAnalysis/E-CommerceConversionFunnelAttritionDashboard_?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

## Data Source & Reproducibility
* **Raw Dataset Source:** [Kaggle - E-Commerce Events History in Cosmetics Shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop)
* **Data Engineering Best Practice:** Following Git production standards, large-scale raw event files (`event-history.csv`) and database binary files (`funnel_warehouse.db`) are excluded via `.gitignore`. The analytics pipeline can be fully reproduced locally using the execution instructions below.

## Execution Instructions
1. Download `event-history.csv` from [Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) and place it in the root project directory.
2. Execute `python3 prep_funnel_data.py` to clean and ingest raw clickstream logs into the local SQLite `funnel_warehouse.db`.
3. Execute `python3 funnel_analysis.py` to trigger SQL funnel aggregation CTEs and export `funnel_summary.csv`.
