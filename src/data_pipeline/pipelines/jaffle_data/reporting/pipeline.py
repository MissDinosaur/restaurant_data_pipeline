# src/data_pipeline/pipelines/reporting/pipeline.py
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import export_to_reports

def create_pipeline(**kwargs) -> Pipeline:
    """
        Create pipeline for analytic results export.
        One csv file will be generated in this pipeline.
    """
    return pipeline([
        node(
            func=export_to_reports,
            inputs=["fact_order_metrics"],  # from analytics outputs
            outputs=None,  # no dataset needed; we’re exporting directly
            name="export_reporting_files"
        ),
    ])
