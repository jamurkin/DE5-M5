import pandas as pd
import argparse
from datetime import datetime
from clean_books import save_to_sql

def clean_customers(path: str, index: str):
    customers_raw = pd.read_csv(path)

    customers_raw = customers_raw.dropna(subset=[index])

    customers = customers_raw.set_index(index)
    return customers


if __name__ == "__main__":
    print(f"{datetime.now()} | Beginning data processing.")
    parser = argparse.ArgumentParser()
    parser.add_argument('--rel_path', type=str, required=True, help='Relative path to data CSV file.')
    parser.add_argument('--index', type=str, required=True, help='Specify index column.')

    args = parser.parse_args()

    customers = clean_customers(args.rel_path, index=args.index)
    print(f"{datetime.now()} | Completed data processing.")
    print(customers)

    print(f"{datetime.now()} | Beginning SQL load")
    save_to_sql(customers, 'Library', 'Customers', 'localhost', 'Module5')
    print(f"{datetime.now()} | Completed SQL load. Loaded {len(customers.index)} rows.")