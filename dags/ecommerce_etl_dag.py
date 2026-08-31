from datetime import datetime, timedelta
from pathlib import Path
import subprocess

from airflow import DAG
from airflow.operators.python import PythonOperator


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_VENV_PYTHON = PROJECT_ROOT / "venv" / "bin" / "python"


def run_command(script_path):
    """
    Run a project Python script using the main project virtual environment.
    """
    command = [
        str(MAIN_VENV_PYTHON),
        str(PROJECT_ROOT / script_path),
    ]

    subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        check=True,
    )


def run_data_quality():
    run_command("src/data_quality.py")


def run_etl_pipeline():
    run_command("src/pipeline.py")


def run_spark_transformation():
    run_command("spark/transform_orders.py")


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="ecommerce_data_pipeline",
    description="End-to-end e-commerce ETL pipeline with PostgreSQL and PySpark",
    default_args=default_args,
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    tags=["ecommerce", "etl", "postgresql", "pyspark"],
) as dag:

    data_quality_task = PythonOperator(
        task_id="validate_raw_data",
        python_callable=run_data_quality,
    )

    etl_pipeline_task = PythonOperator(
        task_id="run_etl_pipeline",
        python_callable=run_etl_pipeline,
    )

    spark_transformation_task = PythonOperator(
        task_id="run_pyspark_transformation",
        python_callable=run_spark_transformation,
    )

    (
        data_quality_task
        >> etl_pipeline_task
        >> spark_transformation_task
    )
