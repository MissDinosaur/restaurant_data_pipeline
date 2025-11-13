from kedro.pipeline import Pipeline, node, pipeline
from .nodes import enrich_orders, prepare_products

def create_pipeline(**kwargs) -> Pipeline:
    """
        Create pipeline for data transformation.
        Two intermediate tables will be generated in this pipeline.
    """
    return pipeline([
        node(
            func=enrich_orders,
            inputs=["raw_orders", "raw_stores"],
            outputs="orders_enriched",
            name="clean_and_enrich_orders"
        ),
        node(
            func=prepare_products,
            inputs=["raw_products", "raw_supplies"],
            outputs="products_dim",
            name="prepare_product_dimension"
        ),
    ])
