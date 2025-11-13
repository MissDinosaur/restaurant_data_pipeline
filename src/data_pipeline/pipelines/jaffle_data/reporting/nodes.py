import pandas as pd
from pathlib import Path

def export_to_reports(fact_order_metrics: pd.DataFrame) -> None:
    """Export analytics results to clean CSV files."""
    output_dir = Path("data/04_reporting")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export fact_order_metrics
    fact_order_metrics.to_csv(output_dir / "fact_order_metrics.csv", index=False)

    print(f"Reports fact_order_metrics is exported to {output_dir}")
