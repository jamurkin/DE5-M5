import pandas as pd
import numpy as np
from datetime import datetime
import argparse
from sqlalchemy import create_engine

class DataCleaner:
    def __init__(self, rel_path: str, index: str):
        self.rel_path = self.set_file_path(rel_path)
        self.index = self.set_index(index)
        self.raw_df = self.get_raw_data()
        self.clean_df = None
        self.drop_df = None
        self.date_cols = []
        self.init_dt = datetime.now()
        self.complete_dt = None

    
    def set_file_path(self, path: str):
        try:
            pd.read_csv(path)
            self.rel_path = path
        except FileNotFoundError:
            print(f"File not found. Please ensure that the file exists.")
        return path
    
    def set_index(self, index: str):
        self.index = index
        return index
    
    def get_raw_data(self):
        self.raw_df = pd.read_csv(self.rel_path)
        print(self.raw_df)
        return self.raw_df
        
    def index_clean(self):
        try:
            drop_df = self.raw_df.dropna(subset=[self.index])
            self.clean_df = drop_df.set_index(self.index)
            return self.clean_df
        except KeyError:
            print(f"Invalid index column specified. Please select from {[col for col in self.raw_df.columns]}")
    
    def drop_nas(self):
        self.drop_df = self.clean_df[self.clean_df.isna().any(axis=1)]
        self.clean_df = self.clean_df[~self.clean_df.isna().any(axis=1)]
        return self.clean_df
    
    def parse_dates(self, date_cols: list[str], formats: list[str]):
        def parser(date_str: str):
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

        for col in date_cols:
            self.clean_df[col] = self.clean_df.apply(lambda row: parser(row[col]), axis=1)

        return self.clean_df

    def date_difference(self, start_date: datetime, end_date: datetime):
        return (end_date - start_date)/np.timedelta64(1, "D")
    
    def calculate_loan_duration(self, loan_date: str, return_date: str):
        self.clean_df['DaysOnLoan'] = self.clean_df.apply(lambda row: self.date_difference(row[loan_date], row[return_date]), axis=1)
        return self.clean_df
    
    def validate_df(self):
        def valid_check(row: pd.Series):
            if row.isnull().any():
                # Check if there are any null values
                return False
            if 'DaysOnLoan' in row.index and row['DaysOnLoan'] < 0:
                # Ensure that return date is after loan date
                return False
            else:
                return True
            
        self.clean_df['ValidRow'] = self.clean_df.apply(valid_check, axis=1)
        return self.clean_df

    def save_to_sql(self, schema: str, name: str, server: str, db: str):
        # Save cleaned and dropped data to SQL
        engine = create_engine(f"mssql+pyodbc://{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
        self.clean_df.to_sql(name=name, schema=schema, con=engine, if_exists='replace')
        self.drop_df.to_sql(name=f"{name}_dropped", schema=schema, con=engine, if_exists='replace')

        # Log process duration in SQL table
        self.complete_dt = datetime.now()
        etl_df = pd.DataFrame(
            {
                "Table": [name],
                "StartDate": [self.init_dt],
                "CompleteDate": [self.complete_dt],
                "DurationSeconds": [(self.complete_dt - self.init_dt).total_seconds()],
                "RowsLoaded": [len(self.clean_df.index)],
                "RowsDropped": [len(self.drop_df.index)]
            }
        )
        etl_df.to_sql(name="EtlLog", schema='Library', con=engine, if_exists='append')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help='Path to data CSV file.')
    parser.add_argument('--index', type=str, required=True, help='Specify index column.')
    parser.add_argument('--table_name', type=str, help='(Optional) Specify name of SQL table.')
    parser.add_argument('--date_cols', nargs='*', type=str, help='(Optional) Specify date columns in CSV file.')
    parser.add_argument('--date_formats', nargs='*', type=str, help='(Optional) Specify date formats in CSV file.')
    parser.add_argument('--loan_date_col', type=str, help="(Optional) Specify column that indicates when book was loaned out. If also specifying return_date_col, then calculates DaysOnLoan column.")
    parser.add_argument('--return_date_col', type=str, help="(Optional) Specify column that indicates when book was returned. If also specifying loan_date_col, then calculates DaysOnLoan column.")

    args = parser.parse_args()
    print(f"{datetime.now()} | Begin data cleaning process.")
    pd.set_option("display.width", 300)

    d = DataCleaner(args.path, args.index)
    print(f"{datetime.now()} | Data loaded from file.")

    d.index_clean()
    print(f"{datetime.now()} | Index cleaned.")

    d.drop_nas()
    print(f"{datetime.now()} | NA values dropped.")

    if args.date_cols and args.date_formats:
        d.parse_dates(args.date_cols, args.date_formats)
        print(f"{datetime.now()} | Date columns parsed.")

        if args.loan_date_col and args.return_date_col:
            d.calculate_loan_duration(args.loan_date_col, args.return_date_col)
            print(f"{datetime.now()} | Calculated loan duration.")

    d.validate_df()
    print(f"{datetime.now()} | Validated data.")

    print(f"{datetime.now()} | Completed data processing. Printing to console.")
    print(d.clean_df)
    print(d.drop_df)

    if args.table_name:
        d.save_to_sql(schema='Library', name=args.table_name, server='localhost', db='Module5')
        print(f"{datetime.now()} | Saved clean and dropped tables to SQL: Module5.Library.{args.table_name}")

    print(f"{datetime.now()} | Process complete.")
