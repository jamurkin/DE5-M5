import pandas as pd
import numpy as np
from datetime import datetime
import argparse
from sqlalchemy import create_engine


def date_parser(date_str: str):
    # Function that attempts to parse date columns from given list of formats
    formats = [
        '"%d/%m/%Y"',
        "%d/%m/%Y",
    ]

    # If not able to parse, then return NaT - allows successive calculations to work as expected
    dt = np.datetime64('NaT')

    for format in formats:
        try:
            dt = datetime.strptime(date_str, format)
            # If successfully parsed, then exit loop and return
            break
        except ValueError:
            # If unable to parse, then try next format
            continue
    return dt

def days_on_loan(loan_date, return_date):
    return (return_date - loan_date)/np.timedelta64(1, "D")


def clean_books(path: str, index: str, date_cols: list = [], loan_date_col: str = None, return_date_col: str = None):
    # Load csv file into dataframe
    books_raw = pd.read_csv(path)

    # Drop items with blank Id value
    books_raw = books_raw.dropna(subset=[index])

    # Create separate dataframe to hold invalid records
    books_drop = books_raw[books_raw.isna().any(axis=1)]
    books = books_raw[~books_raw.isna().any(axis=1)]

    # Set Id column as data frame index
    books = books.set_index(index)

    # Parse given date columns
    if date_cols:
        for col in date_cols:
            books[col] = books.apply(lambda row: date_parser(row[col]), axis=1)

        if loan_date_col and return_date_col:      
            # Add calculated column - loaned days
            books['DaysOnLoan'] = books.apply(lambda row: days_on_loan(row[loan_date_col], row[return_date_col]), axis=1)

    # Check if row is valid
    def valid_check(row):
        if row.isnull().any():
            # Check if there are any null values
            return False
        if 'DaysOnLoan' in row.index and row['DaysOnLoan'] < 0:
            # Ensure that return date is after loan date
            return False
        else:
            return True
        
    books["ValidRow"] = books.apply(valid_check, axis=1)

    return books, books_drop


def save_to_sql(df, schema, name, server, db):
    engine = create_engine(f"mssql+pyodbc://{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
    df.to_sql(name=name, schema=schema, con=engine, if_exists='replace')



if __name__ == "__main__":
    print(f"{datetime.now()} | Beginning data processing.")
    parser = argparse.ArgumentParser()
    parser.add_argument('--rel_path', type=str, required=True, help='Relative path to data CSV file.')
    parser.add_argument('--index', type=str, required=True, help='Specify index column.')
    parser.add_argument('--date_cols', nargs='*', type=str, help='(Optional) Specify date columns in CSV file.')
    parser.add_argument('--loan_date_col', type=str, help="(Optional) Specify column that indicates when book was loaned out. If also specifying return_date_col, then calculates DaysLoaned column.")
    parser.add_argument('--return_date_col', type=str, help="(Optional) Specify column that indicates when book was returned. If also specifying loan_date_col, then calculates DaysLoaned column.")

    args = parser.parse_args()

    books, drop = clean_books(
        path=args.rel_path,
        index=args.index,
        date_cols=args.date_cols,
        loan_date_col=args.loan_date_col,
        return_date_col=args.return_date_col
    )
    print(f"{datetime.now()} | Completed data processing.")

    print(books)
    print(drop)
    print(f"{datetime.now()} | Beginning SQL load")
    save_to_sql(books, 'Library', 'Books', 'localhost', 'Module5')
    print(f"{datetime.now()} | Completed SQL load. Loaded {len(books.index)} rows.")