import pandas as pd
from pathlib import Path

def export_to_reports(fact_order_metrics: pd.DataFrame) -> None:
    """Export analytics results to clean CSV and Excel files."""
    output_dir = Path("data/04_reporting")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export fact_order_metrics
    fact_order_metrics.to_csv(output_dir / "fact_order_metrics.csv", index=False)

    # Export product dimension
    # products_dim.to_csv(output_dir / "products_dim_report.csv", index=False)
    # products_dim.to_excel(output_dir / "products_dim_report.xlsx", index=False)

    print(f"Reports exported to {output_dir}")
