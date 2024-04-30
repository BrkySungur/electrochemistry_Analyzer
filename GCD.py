from DataImporter import *
import pandas as pd
import numpy as np


class UnifiedDataGCD:
    def __init__(self, obj):
        """
        Initializes UnifiedDataGCD object with given data object from DataImport at DataImporter.py.

        Args:
        - obj: Object from DataImport at DataImporter.py which is containing raw data.

        Attributes:
        - raw_data: Raw data DataFrame.
        - headers: List of dictionaries containing header information.
        - uni_data: DataFrame with converted units.
        """
        self.raw_data = obj.data
        self.headers = self.splitter(self.raw_data.columns.tolist())
        self.uni_data = self.SIConverter(self.raw_data)

    def splitter(self, input):
        """
        Splits headers into title, unit, and find SI-conversion multiplier.

        Args:
        - input: List of header names.

        Returns:
        - headers_list: List of dictionaries containing header information with SI-conversion multiplier.
        """
        unitConverisonList = {
            's' : 1E0,
            'ms': 1E-3,
            'us': 1E-6,
            'V' : 1E0,
            'mV': 1E-3,
            'uV': 1E-6,
        }

        headers_list = []
        for items in input:
            if '.' in items:
                items = items.split('.')[0]
            
            dummy = {
                'title'             : items.split(' /')[0],
                'unit'              : items.split(' /')[1],
                'conversionMulti'   : unitConverisonList.get(items.split(' /')[1], None)
            }
            headers_list.append(dummy)
        return headers_list
    
    def SIConverter(self, RawData):
        """
        Converts data units to SI units based on SI-conversion multipliers.

        Args:
        - RawData: DataFrame with raw data.

        Returns:
        - df: DataFrame with converted units.
        """
        df = RawData
        for i in range(len(df.columns)):
            dummy = df.iloc[:, i]
            multi = self.headers[i]['conversionMulti']
            if not multi is None:
                df.iloc[:, i] = dummy * multi
            else:
                print("Warning! No matching units found.")
        df.columns = [item['title'] for item in self.headers]   

        # Duplicate the first column and insert it after every other column
        first_column_name = df.columns[0]
        first_column = df.iloc[:, 0].values[:, np.newaxis]
        for i in range(2, len(df.columns) * 2, 2):
            df.insert(i, first_column_name, first_column, allow_duplicates=True)

        return df
   
    def adjust_duplicated_columns(self, df):

        # Get duplicated columns
        duplicated_columns = df.columns[df.columns.duplicated(keep=False)]
        for i in range(0, len(duplicated_columns), 2):
            col1 = duplicated_columns[i]
            col2 = duplicated_columns[i+1]

            df[col1] = df[col1].where(df[col1].notnull(), None)
            df[col2] = df[col2].where(df[col2].notnull(), None)
                              
        return df


if __name__ == "__main__":
    path = './GCD/0.1Ag-1.csv'
    # Create DataImport object and print results
    obj = DataImport(path=path)
    obj2 = UnifiedDataGCD(obj)
    print(obj2.uni_data) 
