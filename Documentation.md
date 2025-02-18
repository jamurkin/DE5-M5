# Project objectives

1. Set up GitHub repo for project
2. Design an architectural diagram for the pipeline
3. Implement the Python application that does the data cleaning
4. Test the Python application
5. If there are no bugs, deploy pipeline (CI/CD)
6. Trigger the pipeline to write to a database
7. Use the written data to create a Power BI dashboard

# Architecture
![Architecture diagram](./architecture/library.png)


# Data Cleaning
## Books
To process Books data, use the following CLI command:
```
cd application
python clean_books.py --rel_path <path to CSV file>
```
This will load the cleaned dataframe to a SQL table in the Module5 database: Library.Books
### Options
#### Date columns
Date columns should be specified in for processing:
```
python clean_books.py --rel_path <path> --dates <date1> <date2> ...
```

#### Days on loan
To calculate number of days on loan for a book, first specify all date columns, then specify loan and return date columns:
```
python clean_books.py --rel_path <path> --dates <date1> <date2> ... --loan_date_col <loan_date> --return_date_col <return_date>
```
This will add the 'DaysOnLoan' column to the processed dataframe.

### Validity checks
By default, some validity checks will be applied to the final dataframe, resulting in an additional column (ValidRow):
#### 1. Check for nulls
If any null values exist in a row, then it will be flagged as invalid.

#### 2. Date check
If a loan date and return date are specified and exist in the final dataframe, then the code will check that the loan date is before the return date. If not, then the row will be flagged as invalid.

## Customers
To process Books data, use the following CLI command:
```
cd application
python clean_customers.py --rel_path <path to CSV file>
```
This will load the cleaned dataframe to a SQL table in the Module5 database: Library.Customers