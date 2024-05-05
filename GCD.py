"""
Documentation for GCD Experiment Code

This script defines classes and functions for analyzing data from Galvanostatic Cycling and Discharging (GCD) experiments.

Classes:
- GCDExperimentSpecs: Represents the specifications for a GCD experiment.
- UnifiedDataGCD: Processes raw data and converts units to create unified data for analysis.

Functions:
- CalculaterForBattery: Calculates specific capacity for a battery based on provided data and specifications.

Further Notes:
- Documentation will be added and fixed. !!!!
"""

from DataImporter import *
import pandas as pd
from scipy.integrate import cumulative_trapezoid

##### classes #####
class GCDExperimentSpecs:
    """
    Represents the specifications for a GCD (Galvanostatic Cycling and Discharging) experiment.

    Args:
        level_number (int): The number of levels in the experiment.
        level_current (list of float): A list of current values for each level.
        level_time (list of float): A list of time values for each level.
        material_mass (float): Mass of the active material in grams.
        cycle_separated (bool, optional): Whether the cycles are separated. Defaults to False.
        level_separated (bool, optional): Whether the levels are separated. Defaults to False.

    Raises:
        ValueError: If levels are separated but cycles are not.
        ValueError: If level_number is not a positive integer.
        ValueError: If material_mass is not a positive number.
        ValueError: If level_current and level_time have different lengths than level_number.
        ValueError: If any element in level_current is not a number.
        ValueError: If any element in level_time is not a positive number.

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
            raise ValueError("Level currents must be a number.")
        if not all((isinstance(x, (int, float)) and x > 0) for x in self.level_time):
            raise ValueError("Level times must be positive numbers.")
              
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
            new_df = pd.DataFrame()
            for i in range(data.shape[1]//2):
                dummy = pd.DataFrame()
                dummy['Time / s']       = data.iloc[:, 2*i]
                dummy['Current / A']    = specs.level_current[(i % specs.level_number)]
                dummy['Potential / V']  = data.iloc[:, 2*i+1]
                new_df = pd.concat([new_df, dummy], axis=1)
        return new_df


##### Functions #####
def DataExporterGCD(levels_info, levels_details, file_path, number_of_rows=100):
    file_path = file_path + ' Results.xlsx'
    # Convert JSON data to DataFrame
    df_summary = pd.DataFrame(levels_info)
    
    # Create an Excel writer
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # Write summary DataFrame to the Summary sheet
        df_summary.to_excel(writer, index=False, sheet_name='Summary')
        # Get the workbook object
        workbook = writer.book
        # Write details DataFrames to the Details sheets
        for index, items in enumerate(levels_details):
            # Calculate the step size
            if not len(items) <= number_of_rows:
                step_size = max(len(items) // number_of_rows, 1)
                items = items.iloc[::step_size]
            # Ensure that the compressed data has the desired number of rows
            items = items.head(number_of_rows)
            # Write the details DataFrame to the Details sheet
            items.to_excel(writer, index=False, sheet_name='Details', startcol=7*index, startrow=1)
            # Access the Details sheet in the workbook
            sheet = workbook['Details']
            # Add string to specific cell
            sheet.cell(row=1, column=7*index + 1, value='Level ID')
            sheet.cell(row=1, column=7*index + 2, value=index+1)
    return
    

def CalculaterForBattery(unified_data, specs):
    """
    Calculate specific capacity for a battery based on provided data and specifications.

    Parameters:
        unified_data (pandas DataFrame): DataFrame from unified_data of UnifiedDataGCD.
        # # # mass (float, int): Mass of the active material. Mass should be unit of gram.

    Returns:
        tuple: A tuple containing:
            - new_df (pandas DataFrame): DataFrame with calculated specific capacity.
            - levels_info (list of dicts): Information about each level containing:
                - Level: Level number.
                - Current / A: Final current value for the level.
                - Time / s: Final time value for the level.
                - Specific Capacity / mAh/g: Calculated specific capacity for the level.

    Example:
        data:
            Time / s  |  Current / A  |  Potential / V
            ------------------------------------------
            10        |  0.01         |  3.5
            20        |  0.01         |  3.6
            ...
        
        specs:
            material_mass: 0.05

        CalculaterForBattery(data, specs) returns:
            (new_df, levels_info)

        new_df:
            Time / s  |  Current / A  |  Potential / V  |  Specific Capacity / mAh/g
            -------------------------------------------------------------------------
            10        |  0.01         |  3.5            |  0.0005555555555556
            20        |  0.01         |  3.6            |  0.0011111111111111
            ...

        levels_info:
            [
                {'Level': 0, 'Current / A': 2, 'Time / s': 10, 'Specific Capacity / mAh/g': 0.0005555555555556},
                {'Level': 1, 'Current / A': 3, 'Time / s': 20, 'Specific Capacity / mAh/g': 0.0011111111111111},
                ...
            ]
    """
    mass = specs.material_mass
    data = unified_data.unified_data
    # Initialize an empty DataFrame to store the calculated data
    new_df = pd.DataFrame()
    # Initialize an empty list to store level information
    levels_info = []
    dataframes = []
    # Iterate through each set of three columns in the unified_data DataFrame
    for i in range(data.shape[1]//3):
        # Initialize a temporary DataFrame to store data for the current level
        dummy = pd.DataFrame()
        # Extract data for the current level
        # Calculate specific capacity for the current level
        # Calculate energy density and power density for the each row of current level
        # Calculate power density from energy density and time for the each row of current level
        dummy['Time / s']       = data.iloc[:,3*i]
        dummy['Current / A']    = data.iloc[:,3*i+1]
        dummy['Potential / V']  = data.iloc[:, 3*i+2]
        dummy['Specific Capacity / mAh/g'] = abs((dummy['Time / s'] / 3600) * dummy['Current / A'] 
                                                 / (mass))
        dummy['Energy Density / Wh/kg'] = abs(cumulative_trapezoid(
                                                               dummy['Specific Capacity / mAh/g'],
                                                               x=dummy['Potential / V'],
                                                               initial=0
                                                               ))
        dummy['Power Density / W/kg'] = dummy['Energy Density / Wh/kg'] / (dummy['Time / s'] / 3600)

        # Drop rows with NaN values
        dummy = dummy.dropna()
        
        # Store information about the current level
        level_informations = {
            'ID'                        : i+1,
            'Cycle'                     : i//specs.level_number + 1,
            'Level'                     : i % specs.level_number + 1,
            'Current / A'               : dummy['Current / A'].iloc[-1],
            'Time / s'                  : dummy['Time / s'].iloc[-1],
            'Specific Capacity / mAh/g' : dummy['Specific Capacity / mAh/g'].iloc[-1],
            'Energy Density / Wh/kg'    : dummy['Energy Density / Wh/kg'].iloc[-1],
            'Power Density / W/kg'      : dummy['Power Density / W/kg'].iloc[-1]
        }

        # Concatenate the current level's data with the overall DataFrame
        dataframes.append(dummy)
        # Append the information about the current level to the list
        levels_info.append(level_informations)
    
    # Return the DataFrame and the list of level information
    return dataframes, levels_info

##### Test #####
if __name__ == "__main__":
    # Example usage
    specs = GCDExperimentSpecs(
        level_number=2,
        level_current=[0.7038, -0.7038],
        level_time=[99999, 99999],
        material_mass= 0.004116,
        cycle_seperated=True,
        level_seperated=True
    )

    imported_data = DataImport('./test.xlsx')
    data = UnifiedDataGCD(imported_data, specs)

    df , list = CalculaterForBattery(data, specs)
    DataExporterGCD(list, df,  imported_data.file_name)