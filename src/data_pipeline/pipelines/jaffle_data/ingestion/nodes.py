import pandas as pd

def load_csv(filepath: str) -> pd.DataFrame:
    """Generic loader for CSV files."""
    return pd.read_csv(filepath)

def combine_raw_sources(customers, orders, items, products, stores, supplies):
    """Return a dict of all raw dataframes for traceability."""
    return {
        "customers": customers,
        "orders": orders,
        "items": items,
        "products": products,
        "stores": stores,
        "supplies": supplies
    }