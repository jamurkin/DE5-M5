import pandas as pd
import argparse
from sqlalchemy import create_engine
from datetime import datetime

def clean_customers(path: str):
    customers_raw = pd.read_csv(path)

    customers_raw = customers_raw.dropna(subset=['Customer ID'])

    customers = customers_raw.astype({'Customer ID': int})
    customers = customers.set_index("Customer ID")
    return customers


if __name__ == "__main__":
    print(f"{datetime.now()} | Beginning data processing.")
    parser = argparse.ArgumentParser()
    parser.add_argument('--rel_path', type=str, required=True, help='Relative path to data CSV file.')

    args = parser.parse_args()

    customers = clean_customers(args.rel_path)
    print(f"{datetime.now()} | Completed data processing.")
    print(customers)

    print(f"{datetime.now()} | Beginning SQL load")
    engine = create_engine("mssql+pyodbc://localhost/Module5?driver=ODBC+Driver+17+for+SQL+Server")
    customers.to_sql(name='Customers', schema='Library', con=engine, if_exists='replace')
    print(f"{datetime.now()} | Completed SQL load. Loaded {len(customers.index)} rows.")