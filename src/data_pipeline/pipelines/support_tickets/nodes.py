from azure.storage.blob import ContainerClient
import pandas as pd
from io import StringIO

"""
    One sample of support_tickets data.

"""

def load_data_from_azure_blob(sas_url: str) -> pd.DataFrame:
    """
    Load support_tickets dataset from an Azure Blob container using SAS URL.
    The container contains a single JSONL file.
    """
    # Connect to the container
    container = ContainerClient.from_container_url(sas_url)
    
    # List all blobs in the container
    blobs = list(container.list_blobs())
    if not blobs:
        raise ValueError("No blobs found in the container!")
    
    blob_name = blobs[0].name # there is only one JSONL file
    print(f"Found blob: {blob_name}")
    
    # Download the blob content
    blob_client = container.get_blob_client(blob_name)
    text_data = blob_client.download_blob().content_as_text()
    
    # Read JSONL into pandas DataFrame
    df = pd.read_json(StringIO(text_data), lines=True)
    
    print(f"Loaded {len(df)} rows from {blob_name}")
    return df


def load_support_tickets(filepath: str) -> pd.DataFrame:
    """
    Load data from given jsonl file
    Returns: DataFrame
    """
    return pd.read_json(filepath, lines=True)

def clean_support_tickets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove null values and convert data type 
    Returns: DataFrame
    """
    # Remove rows missing order_id or ticket_id
    df = df.dropna(subset=["ticket_id", "order_id"])
    df["ingested_at"] = pd.to_datetime(df["ingested_at"], errors="coerce")
    return df

def extract_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts sentiment information (model, score) from the nested sentiment column, creating a new domain data model.
    Returns:
        pd.DataFrame: A new DataFrame with columns: ticket_id, order_id, model, score.
    """
    # Drop rows where sentiment is missing
    df = df.copy()

    # Convert nested dict in 'sentiment' column into separate columns
    sentiment_df = pd.json_normalize(df["sentiment"])

    # Merge with ticket_id and order_id
    sentiment_df["ticket_id"] = df["ticket_id"].values
    sentiment_df["order_id"] = df["order_id"].values

    # Reorder columns
    sentiment_df = sentiment_df[["ticket_id", "order_id", "model", "score"]]

    return sentiment_df

def calculate_avg_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates average sentiment score per order_id.
    Returns:
        DataFrame with columns:
            - order_id
            - avg_score (average sentiment score for each order)
    """
    result = (
        df.groupby("order_id", as_index=False)["score"]
          .mean()
          .rename(columns={"score": "avg_score"})
          .round(2)
    )

    return result

def tickets_per_order(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate input table to count how many tickets belong to each order.
    Returns:
        DataFrame with columns:
            - order_id
            - num_tickets (count of tickets for each order)
    """
    # Group and count the number of tickets
    result = (
        df.groupby("order_id")["ticket_id"]
          .count()
          .reset_index()
          .rename(columns={"ticket_id": "num_tickets"})
    )

    return result

# Reporting
from pathlib import Path

def export_to_reports(df: pd.DataFrame, file_name: str) -> None:
    """Export analytics results to clean CSV and Excel files."""
    output_dir = Path("data/04_reporting")
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_dir / f"{file_name}.csv", index=False)
    print(f"Reports {file_name}.csv is exported to {output_dir}")
