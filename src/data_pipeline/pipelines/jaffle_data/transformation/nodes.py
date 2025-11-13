import pandas as pd


def enrich_orders(raw_orders: pd.DataFrame, raw_stores: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich orders with store-level tax data."""
    df = raw_orders.copy()
    df['ordered_at'] = pd.to_datetime(df['ordered_at'])
    # df left join raw_stores on store_id = id
    df = df.merge(raw_stores, left_on='store_id', right_on='id', suffixes=('', '_store'))
    df['tax_difference'] = df['tax_paid'] - (df['subtotal'] * df['tax_rate'])
    return df

def prepare_products(raw_products: pd.DataFrame, raw_supplies: pd.DataFrame) -> pd.DataFrame:
    """Join product info with supplies for enrichment."""
    # df left join raw_products on sku=sku
    df = raw_products.merge(raw_supplies, on='sku', how='left', suffixes=('', '_supply'))
    df['is_perishable'] = df['perishable'].fillna(False)
    return df