from kedro.pipeline import Pipeline
from data_pipeline.pipelines.jaffle_data.ingestion.pipeline import create_pipeline as jaffle_ingestion_pipeline
from data_pipeline.pipelines.jaffle_data.transformation.pipeline import create_pipeline as jaffle_transformation_pipeline
from data_pipeline.pipelines.jaffle_data.analytics.pipeline import create_pipeline as jaffle_analytics_pipeline
from data_pipeline.pipelines.jaffle_data.reporting.pipeline import create_pipeline as jaffle_reporting_pipeline
from data_pipeline.pipelines.support_tickets import pipeline as s_pipe

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": jaffle_ingestion_pipeline() + jaffle_transformation_pipeline() + jaffle_analytics_pipeline() + jaffle_reporting_pipeline() \
                    + s_pipe.create_pipeline(),
        "jaffle_ingestion": jaffle_ingestion_pipeline(),
        "jaffle_transformation": jaffle_transformation_pipeline(),
        "jaffle_analytics": jaffle_analytics_pipeline(),
        "jaffle_reporting": jaffle_reporting_pipeline(),
        "support_tickets": s_pipe.create_pipeline(),
    }
