from kedro.pipeline import Pipeline, node
from .nodes import load_data_from_azure_blob, clean_support_tickets, extract_sentiment, calculate_avg_score, tickets_per_order, export_to_reports


# Using ELT approach. Extract --> Load --> Transform
def create_pipeline(**kwargs):
    return Pipeline([
        # Extract + Load
        node(
            func=load_data_from_azure_blob,
            inputs="params:support_tickets_sas_url",
            outputs="raw_support_tickets",
            name="load_support_tickets_node"
        ),
        # Transform: cleaning data and flattening nested fields to generate intermediate tables
        node(
            func=clean_support_tickets,
            inputs="raw_support_tickets",
            outputs="clean_support_tickets",
            name="clean_support_tickets_node"
        ),
        node(
            func=extract_sentiment,
            inputs="clean_support_tickets",
            outputs="sentiment_table",
            name="extract_sentiment_node"
        ),
        # Analytics: 
        # 1. Analyzing the average sentiment score in each order.
        # 2. Analyzing the number of tickets per order
        node(
            func=calculate_avg_score,
            inputs="sentiment_table",
            outputs="avg_score_per_order",
            name="calculate_avg_score_node"
        ),
        node(
            func=tickets_per_order,
            inputs="clean_support_tickets",
            outputs="tickets_per_order",
            name="tickets_per_order_node"
        ),
        # Export anlytic results to the csv file for a better check
        node(
            func=export_to_reports,
            inputs=["avg_score_per_order", "params:avg_score_filename"],  # from analytics outputs
            outputs=None,  # no dataset needed; we’re exporting directly
            name="export_avg_score"
        ),
        node(
            func=export_to_reports,
            inputs=["tickets_per_order", "params:tickets_per_order_filename"],
            outputs=None,
            name="export_tickets_count"
        ),
    ])
