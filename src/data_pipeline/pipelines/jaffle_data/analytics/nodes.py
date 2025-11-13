import pandas as pd
from pathlib import Path

def compute_order_metrics(orders_enriched: pd.DataFrame, raw_items: pd.DataFrame) -> pd.DataFrame:
    """Compute order-level KPIs: total value and number of items."""
    order_items = raw_items.groupby("order_id")["sku"].count().reset_index()
    order_items.rename(columns={"sku": "num_items"}, inplace=True)

    df = orders_enriched.merge(order_items, left_on="id", right_on="order_id", how="left")
    # Average order value 
    df["avg_order_value"] = round(df["order_total"].mean(), 2)

    metrics = df[["id", "customer", "order_total", "num_items", "avg_order_value"]]
    metrics.rename(columns={"id": "order_id"}, inplace=True)
    metrics["num_items"] = metrics["num_items"].astype("Int64")

    return metrics
