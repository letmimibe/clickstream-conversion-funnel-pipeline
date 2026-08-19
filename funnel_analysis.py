import pandas as pd
import sqlite3
import logging

# Configure enterprise logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_PATH = 'funnel_warehouse.db'
SUMMARY_OUTPUT_CSV = 'funnel_summary.csv'

def execute_funnel_analytics(db_path: str) -> pd.DataFrame:
    """
    Executes CTE-driven conversion funnel aggregation and exports metrics summary.
    """
    conn = sqlite3.connect(db_path)

    sql_query = """
    WITH SessionStages AS (
        SELECT 
            user_session,
            MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS viewed,
            MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS added_to_cart,
            MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased
        FROM events
        GROUP BY user_session
    ),
    FunnelCounts AS (
        SELECT 
            SUM(viewed) AS total_views,
            SUM(CASE WHEN viewed = 1 AND added_to_cart = 1 THEN 1 ELSE 0 END) AS total_carts,
            SUM(CASE WHEN viewed = 1 AND added_to_cart = 1 AND purchased = 1 THEN 1 ELSE 0 END) AS total_purchases
        FROM SessionStages
    )
    SELECT 
        '1. View Product' AS stage, 
        total_views AS session_count, 
        100.0 AS conversion_rate_pct, 
        0.0 AS drop_off_rate_pct 
    FROM FunnelCounts

    UNION ALL

    SELECT 
        '2. Add to Cart' AS stage, 
        total_carts AS session_count,
        ROUND((CAST(total_carts AS FLOAT) / total_views) * 100, 2) AS conversion_rate_pct,
        ROUND((1.0 - (CAST(total_carts AS FLOAT) / total_views)) * 100, 2) AS drop_off_rate_pct 
    FROM FunnelCounts

    UNION ALL

    SELECT 
        '3. Purchase' AS stage, 
        total_purchases AS session_count,
        ROUND((CAST(total_purchases AS FLOAT) / total_carts) * 100, 2) AS conversion_rate_pct,
        ROUND((1.0 - (CAST(total_purchases AS FLOAT) / total_carts)) * 100, 2) AS drop_off_rate_pct 
    FROM FunnelCounts;
    """

    df_funnel = pd.read_sql_query(sql_query, conn)
    conn.close()

    df_funnel.to_csv(SUMMARY_OUTPUT_CSV, index=False)
    return df_funnel

if __name__ == "__main__":
    logging.info("Executing conversion funnel SQL analytics pipeline...")
    df_results = execute_funnel_analytics(DATABASE_PATH)
    print("\n=== CONVERSION FUNNEL SUMMARY ===")
    print(df_results.to_string(index=False))
    logging.info(f"Summary exported to '{SUMMARY_OUTPUT_CSV}'.")