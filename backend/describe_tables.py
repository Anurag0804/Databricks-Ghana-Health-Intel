"""Quick script to DESCRIBE all tables used by the app."""
import os
import sys

# Manual .env parsing
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

import databricks.sql as dbsql

conn = dbsql.connect(
    server_hostname=os.getenv("DATABRICKS_HOST", "").replace("https://", "").replace("http://", "").rstrip("/"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH", ""),
    access_token=os.getenv("DATABRICKS_TOKEN", ""),
)

TABLES = [
    "virtue_foundation.ghana.gold_facilities_enriched",
    "virtue_foundation.ghana.gold_anomaly_flags",
    "virtue_foundation.ghana.gold_medical_desert_scores",
    "virtue_foundation.ghana.gold_regional_summary",
    "virtue_foundation.ghana.gold_regional_priority",
    "virtue_foundation.ghana.gold_idp_enriched",
]

cursor = conn.cursor()
for table in TABLES:
    print(f"\n{'='*80}")
    print(f"TABLE: {table}")
    print(f"{'='*80}")
    try:
        cursor.execute(f"DESCRIBE TABLE {table}")
        rows = cursor.fetchall()
        for row in rows:
            print(f"  {row[0]:50s} {row[1]}")
    except Exception as e:
        print(f"  ERROR: {e}")

cursor.close()
conn.close()
