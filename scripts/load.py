import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")


def load_csv_to_postgres(csv_path, table_name):
    df = pd.read_csv(csv_path)
    if df.empty:
        print(f"{csv_path} is empty. Skipping.")
        return

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Standardize column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        # Dynamically create table columns
        columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                {columns}
            );
        ''')

        # Prepare data for insertion
        values = [tuple(row) for row in df.astype(str).values]
        quoted_cols = ', '.join([f'"{col}"' for col in df.columns])
        insert_query = f'INSERT INTO "{table_name}" ({quoted_cols}) VALUES %s'
        execute_values(cur, insert_query, values)

        conn.commit()
        print(f"Inserted {len(df)} rows into {table_name}")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Failed to load {csv_path}: {e}")


def main():
    processed_dir = "../data/processed"
    for file in os.listdir(processed_dir):
        if file.endswith("_combined.csv"):
            path = os.path.join(processed_dir, file)
            table_name = os.path.splitext(file)[0].lower()
            load_csv_to_postgres(path, table_name)


if __name__ == "__main__":
    main()
