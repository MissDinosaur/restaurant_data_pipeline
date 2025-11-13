from kedro.pipeline import Pipeline, node, pipeline
from .nodes import combine_raw_sources

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=combine_raw_sources,
            inputs=[
                "raw_customers",
                "raw_orders",
                "raw_items",
                "raw_products",
                "raw_stores",
                "raw_supplies"
            ],
            outputs="all_raw_data",
            name="combine_all_raw_sources"
        ),
    ])
