from google.cloud import bigquery
import pandas as pd

def load_to_bigquery(csv_file, table_name):
    client = bigquery.Client()
    df = pd.read_csv(csv_file)
    table_id = f"{client.project}.savannah_dataset.{table_name}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print(f"Loaded {csv_file} into {table_id}")

def run_loading():
    load_to_bigquery("clean_users.csv", "users_table")
    load_to_bigquery("clean_products.csv", "products_table")
    load_to_bigquery("clean_carts.csv", "carts_table")

if __name__ == "__main__":
    run_loading()
