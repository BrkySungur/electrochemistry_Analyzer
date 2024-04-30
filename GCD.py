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

        return df


if __name__ == "__main__":
    path = './GCD/0.1Ag-1.csv'
    # Create DataImport object and print results
    obj = DataImport(path=path)
    obj2 = UnifiedDataGCD(obj)
    print(obj2.uni_data) 
