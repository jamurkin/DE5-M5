import unittest
import pandas as pd
from datetime import datetime

from ..application import DataCleaner

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.d = DataCleaner('unit_testing/tests_data/books_1.csv', 'Id')

    def test_date_difference(self):
        self.assertEqual(self.d.date_difference(datetime(2024,1,1), datetime(2024,1,6)), 5, "Date calculation incorrect.")
    
    # def test_load(self):
    #     check_df = pd.DataFrame(
    #         {
    #             'Id': [1,2,3,4],
    #             'Books': ['Catcher in the Rye', 'Lord of the rings the two towers', 'Lord of the rings the return of the kind', 'The hobbit'],
    #             'Book checkout': ['"20/02/2023"', '"24/03/2023"', '"29/03/2023"', '"02/04/2023"'],
    #             'Book Returned': ['25/02/2023', '21/03/2023', '25/03/2023', '25/03/2023'],
    #             'Days allowed to borrow': ['2 weeks', '2 weeks', '2 weeks', '2 weeks'],
    #             'Customer ID': [1,2,3,4]
    #         }
    #     )
    #     self.assertEqual(self.d.raw_df, check_df, "Test failed")


if __name__ == "__main__":
    unittest.main()
