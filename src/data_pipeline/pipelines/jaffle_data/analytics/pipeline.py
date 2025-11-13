from kedro.pipeline import Pipeline, node, pipeline
from .nodes import compute_order_metrics

def create_pipeline(**kwargs) -> Pipeline:
    """
        Create pipeline for data analytics.
        One metric table will be generated in this pipeline.
    """
    return pipeline([
        node(
            func=compute_order_metrics,
            inputs=["orders_enriched", "raw_items"],
            outputs="fact_order_metrics",
            name="compute_order_level_metrics"
        ),
    ])
