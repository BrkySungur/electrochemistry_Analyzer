"""
Documentation for GCD Experiment Code

This script defines classes and functions for analyzing data from Galvanostatic Cycling and Discharging (GCD) experiments.

Classes:
- GCDExperimentSpecs: Represents the specifications for a GCD experiment.
- UnifiedDataGCD: Processes raw data and converts units to create unified data for analysis.
Further Notes:
- Documentation will be added and fixed. !!!!
- Type hintings will be fixed. !!!!
- DataImporter.py will be updated. !!!!
- Delete all the existing documentation for codes and rewrite. !!!!!
- class objects could be merged
"""

from DataIO import DataImport, DataExporterGCD
import pandas as pd
from scipy.integrate import cumulative_trapezoid
from typing import List, Dict, Union


class GCDExperimentSpecs:
    def __init__(
        self,
        level_number: int,
        level_current: List[float],
        level_time: List[float],
        material_mass: float,
        cycle_separated: bool = False,
        level_separated: bool = False
    ) -> None:
        self.cycle_separated = cycle_separated
        self.level_separated = level_separated
        self.level_number = level_number 
        self.level_current = level_current 
        self.level_time = level_time
        self.material_mass = material_mass
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        if self.level_separated and not self.cycle_separated:
            raise ValueError("Levels cannot be separated if cycles are not.")
        if not isinstance(self.level_number, int) or self.level_number <= 0:
            raise ValueError("Level number must be a positive integer.")
        if not isinstance(self.material_mass, (int, float)) or self.material_mass <= 0:
            raise ValueError("Active material mass must be a positive number.")
        if len(self.level_current) != len(self.level_time) != self.level_number:
            raise ValueError("Level currents and times must have the same length as level number.")
        if not all(isinstance(x, (int, float)) for x in self.level_current):
            raise ValueError("All level currents must be numbers.")
        if not all(x > 0 for x in self.level_time):
            raise ValueError("All level times must be positive numbers.")


class UnifiedDataGCD:
    """
    Class for processing and unifying raw data for GCD (Galvanostatic Charge-Discharge) experiments.
    """

    def __init__(self, raw_data: pd.DataFrame, specs: 'GCDExperimentSpecs') -> None:
        """
        Initializes the UnifiedDataGCD object.

        Args:
            raw_data (pd.DataFrame): The raw data to be processed and unified.
            specs (GCDExperimentSpecs): The specifications for the GCD experiment.

        Returns:
            None
        """
        self.raw_data: pd.DataFrame = raw_data
        self.headers: List[Dict[str, Union[str, float, None]]] = self.split_headers(raw_data.columns.tolist())
        self.unified_data: pd.DataFrame = self.unify_data(
            self.convert_to_si_units(raw_data),
            specs
        )
        
    def split_headers(self, input_headers: List[str]) -> List[Dict[str, Union[str, float, None]]]:
        """
        Splits the input headers into title and unit, and converts the unit to a conversion multiplier.

        Args:
            input_headers (List[str]): The input headers to be split.

        Returns:
            List[Dict[str, Union[str, float, None]]]: The split headers with title, unit, and conversion multiplier.
        """
        unit_conversion_list: Dict[str, float] = {
            's' : 1E0,
            'ms': 1E-3,
            'us': 1E-6,
            'V' : 1E0,
            'mV': 1E-3,
            'uV': 1E-6,
        }

        headers_list: List[Dict[str, Union[str, float, None]]] = []
        for item in input_headers:
            if '.' in item:
                item = item.split('.')[0]  
            
            title, unit = item.rsplit(' /', 1)
            headers_list.append({
                'title': title,
                'unit': unit,
                'conversion_multiplier': unit_conversion_list.get(unit, None)
            })
        return headers_list
    
    def convert_to_si_units(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Converts the raw data to SI units based on the conversion multipliers.

        Args:
            raw_data (pd.DataFrame): The raw data to be converted.

        Returns:
            pd.DataFrame: The converted data in SI units.
        """
        unit_converted_data: pd.DataFrame = raw_data.copy()
        for i, col in enumerate(unit_converted_data.columns):
            multi = self.headers[i]['conversion_multiplier']
            if multi is not None:
                unit_converted_data[col] *= multi
            else:
                print("Warning! No matching units found.")
        unit_converted_data.columns = [item['title'] for item in self.headers]
        return unit_converted_data
    
    def unify_data(self, data: pd.DataFrame, specs: 'GCDExperimentSpecs') -> pd.DataFrame:
        """
        Unifies the data by combining the time, current, and potential columns.

        Args:
            data (pd.DataFrame): The data to be unified.
            specs (GCDExperimentSpecs): The specifications for the GCD experiment.

        Returns:
            pd.DataFrame: The unified data.
        """
        if specs.cycle_separated and specs.level_separated:
            dfs = []
            for i in range(data.shape[1] // 2):
                df = pd.DataFrame({
                    'Time / s': data.iloc[:, 2*i],
                    'Current / A': specs.level_current[(i % specs.level_number)],
                    'Potential / V': data.iloc[:, 2*i+1]
                })
                dfs.append(df)
            return pd.concat(dfs, axis=1)
        else:
            return pd.DataFrame()
    

def CalculaterForBattery(unified_data, specs):
    """
    Calculate battery properties based on unified data and specifications.

    Parameters:
    - unified_data: The unified data containing time, current, and potential values.
    - specs: The specifications of the battery.

    Returns:
    - dataframes: A list of dataframes containing calculated battery properties.
    - levels_info: A list of dictionaries containing information about each level of the battery.

    """
    mass = specs.material_mass
    data = unified_data.unified_data
    new_df = pd.DataFrame()
    levels_info = []
    dataframes = []
    for i in range(data.shape[1]//3):
        dummy = pd.DataFrame()
        dummy['Time / s']       = data.iloc[:,3*i]
        dummy['Current / A']    = data.iloc[:,3*i+1]
        dummy['Potential / V']  = data.iloc[:, 3*i+2]
        dummy['Specific Capacity / mAh/g'] = abs((dummy['Time / s'] / 3600) * (dummy['Current / A'] * 1000) 
                                                 / (mass))
        dummy['Energy Density / Wh/kg'] = abs(cumulative_trapezoid(
                                                               dummy['Specific Capacity / mAh/g'],
                                                               x=dummy['Potential / V'],
                                                               initial=0
                                                               ))
        dummy['Power Density / W/kg'] = dummy['Energy Density / Wh/kg'] / (dummy['Time / s'] / 3600)

        
        dummy = dummy.dropna()
        
        
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

        
        dataframes.append(dummy)
        
        levels_info.append(level_informations)
    
    
    return dataframes, levels_info


if __name__ == "__main__":
    
    specs = GCDExperimentSpecs(
        level_number=2,
        level_current=[0.0007038, -0.0007038],
        level_time=[99999, 99999],
        material_mass= 0.004116,
        cycle_separated=True,
        level_separated=True
    )

    imported_data = DataImport('./test.xlsx')
    data = UnifiedDataGCD(imported_data.data, specs)

    df , list = CalculaterForBattery(data, specs)
    DataExporterGCD(list, df, imported_data.file_name, number_of_rows=200)