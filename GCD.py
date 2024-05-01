from DataImporter import *
import pandas as pd
import numpy as np

##### classes #####
class GCDExperimentSpecs:
    """
    Represents the specifications for a GCD (Galvanostatic Cycling and Discharging) experiment.

    Args:
        level_number (int): The number of levels in the experiment.
        level_current (list): A list of current values for each level.
        level_time (list): A list of time values for each level.
        cycle_seperated (bool, optional): Whether the cycles are separated. Defaults to False.
        level_seperated (bool, optional): Whether the levels are separated. Defaults to False.

    Raises:
        ValueError: If levels are separated but cycles are not.
        ValueError: If level_number is not a positive integer.
        ValueError: If level_current and level_time have different lengths than level_number.

    """

    def __init__(self,
                 level_number,
                 level_current,
                 level_time,
                 material_mass,
                 cycle_seperated=False,
                 level_seperated=False
                 ):
        self.cycle_seperated = cycle_seperated
        self.level_seperated = level_seperated
        self.level_number = level_number 
        self.level_current = level_current 
        self.level_time = level_time
        self.material_mass = material_mass
        self._double_check()

    def _double_check(self):
        if not self.cycle_seperated and self.level_seperated:
            raise ValueError("Levels cannot be separated if cycles are not.")
        if not (isinstance(self.level_number, int) and self.level_number > 0):
            raise ValueError("Level number must be a positive integer.")
        if not (isinstance(self.material_mass, (int, float)) and self.material_mass > 0):
            raise ValueError("Active material mass must be a positive.")
        if not (len(self.level_current) == len(self.level_time) == self.level_number):
            raise ValueError("Level current and time must have the same length as level number.")
        if not all(isinstance(x, (int, float)) for x in self.level_current):
            raise ValueError("Level current must be a number.")
        if not all(isinstance(x, (int, float)) for x in self.level_time):
            raise ValueError("Level time must be a number.")
              
class UnifiedDataGCD:
    def __init__(self, obj, specs):
        """
        Initializes UnifiedDataGCD object with given data object from DataImport at DataImporter.py.

        Args:
        - obj: Object from DataImport at DataImporter.py which is containing raw data.

        Attributes:
        - raw_data: Raw data DataFrame.
        - headers: List of dictionaries containing header information.
        - unified_data: DataFrame with converted units.
        """
        self.raw_data = obj.data
        self.headers = self.splitter(self.raw_data.columns.tolist())
        self.unified_data = self.Unification(
                                         self.SIConverter(self.raw_data),
                                         specs
                                        )
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
    
    def Unification(self, data, specs):
        if specs.cycle_seperated and specs.level_seperated:
            data_new = pd.DataFrame()
            for i in range(data.shape[1]//2): ## // kullanırsan hep integer sonuç gelir tek / sonucu float olur ##
                dummy = pd.DataFrame()
                dummy['Time / s'] = data.iloc[:, 2*i]
                dummy['Potential / V'] = data.iloc[:, 2*i+1]
                dummy['Current / A'] = specs.level_current[(i % specs.level_number)]
                data_new = pd.concat([data_new, dummy], axis=1)
        return data_new


##### Functions #####
##### Kapasite hesaplaması başka bir class içinde olmasın onu fonksiyon olarak tutalım #####
def CapacityCalculater(data_new, material_mass):
    """
    Calculates the capacity based on the given data and material mass.

    Args:
    - data_new: DataFrame with the unified data.
    - material_mass: Mass of the material in grams.

    Returns:
    - capacity: Calculated specific capacity in mA.h/g
    """
    total_charge = data_new['Current / A'].sum() * data_new['Time / s'].max()
    capacity = total_charge * 1000 / (material_mass * 3600)
    return capacity

##### Test #####
if __name__ == "__main__":
    # Example usage
    specs = GCDExperimentSpecs(
        level_number=2,
        level_current=[0.1, -0.1],
        level_time=[99999, 99999],
        material_mass=56.789e-9,
        cycle_seperated=True,
        level_seperated=True
    )

    test = DataImport('./GCD/0.1Ag-1.xlsx')
    print(test.data)
    test = UnifiedDataGCD(test, specs)
    print(test.unified_data)
