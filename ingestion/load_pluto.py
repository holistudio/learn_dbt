import os
import pandas as pd
from sodapy import Socrata
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

BQ_DATASET="pluto_raw"

load_dotenv()

# --- Credentials ---
credentials = service_account.Credentials.from_service_account_file(
    os.environ["GCP_CREDENTIALS"]
)
GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]

# --- Extract ---
APP_TOKEN = os.environ["SOCRATA_APP_TOKEN"]
client = Socrata("data.cityofnewyork.us", APP_TOKEN)

DATASET_ID = "64uk-42ks"
CHUNK_SIZE = 100_000
all_records = []
offset = 0

print("Fetching from NYC Open Data...")
while True:
    chunk = client.get(DATASET_ID, limit=CHUNK_SIZE, offset=offset)
    if not chunk:
        break
    all_records.extend(chunk)
    offset += CHUNK_SIZE
    print(f"Fetched {offset} rows so far...")

df = pd.DataFrame.from_records(all_records)
print(f"Total rows fetched: {len(df)}")

# --- Governance metadata ---
df["_loaded_at"] = pd.Timestamp.now(tz="UTC")
df["_source"] = f"NYC OpenData PLUTO {DATASET_ID}"

# --- Load ---
print("Loading into BigQuery...")
bq_client = bigquery.Client(project=GCP_PROJECT_ID, credentials=credentials)
table_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}.pluto"

job = bq_client.load_table_from_dataframe(df, table_id)
job.result()

print(f"Loaded {len(df)} rows into {table_id}")