"""
OBJECTIVES:
Create data import module for various data types to further process. The possible filetypes are xlsx, xls, csv, and dta.
    1. You need to import all the data without any problem. You can create a new class called "DataImport".
        a. Data import class should have "path, file_name, file_type, data" attributes.
        b. Class object should have only one input which is path. You need to crete functions or use other modules to retrieve
        file_name and file_type attributes. User should not enter file_name and file_type input.
        c. Assign proper error handling options. For example, you can use object.status attributes to assign status numbers
            like 200 for successfull and 400 for other. 
            More information: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    2. You need to create a new class called "UnifiedData".
        a. Further specs will be given later.

ADDITONAL NOTES:
- Try to added comment based explanations in your code as much as you can.
- Right now, you were assigned to work xlsx, xls, and csv files.
"""

##### Imports ######
import pandas as pd
import os

##### Classes #####
class DataImport:
    def __init__(self, path: str) -> None:
        '''
        Initializes DataImport object with given file path.

        Args:
        - path (str): Path to the data file.

        Attributes:
        - file_path (str): Path to the data file.
        - file_name (str): Name of the data file.
        - file_type (str): Extension of the data file.
        - data (DataFrame): Loaded data from the file.
        - status (int): Status code indicating success or failure of data loading.
        - status_message (str): Message corresponding to the status code.
        '''

        self.file_path = path
        self.file_name, self.file_type = self.path2name_extension(self.file_path)
        self.data, self.status, self.status_message = self.LoadData()
    
    def path2name_extension(self, path: str) -> list[str, str]:
        """
        Extracts file name and extension from the given file path.

        Args:
        - path (str): Path to the file.

        Returns:
        - list: [file_name (str), file_extension (str)]
        """

        name, extension = os.path.splitext(path)
        type = extension[1:] # Remove the dot from the extension
        return [name, type]

    def LoadData(self):
        """
        Loads data from the file based on its extension.

        Returns:
        - data (DataFrame): Loaded data from the file.
        - status (int): Status code indicating success or failure of data loading.
        - status_message (str): Message corresponding to the status code.
        """

        # Define status messages corresponding to different status codes
        status_messages = {
            200: "Success: Data loaded successfully.",
            204: "Warning: File is empty.",
            400: "Warning: File format is invalid.",
            404: "Warning: File was not found.",
            }
        
        try:
            # Load data based on file extension
            match self.file_type:
                case 'xlsx' | 'xls':
                    df = pd.read_excel(self.file_path)
                case 'csv':
                    df = pd.read_csv(self.file_path)
                case _:
                    # Invalid file format
                    status = 400
                    message = status_messages[status]
                    return None, status, message
                
            # Check if the loaded DataFrame is empty
            if len(df.columns) == 0 or len(df.index) == 0:
                status = 204  # Empty file
                message = status_messages[status]
            else:
                status = 200  # Success
                message = status_messages[status]

            return df, status, message
                
        except Exception:
            # File not found or other exceptions
            status = 404
            message = status_messages[status]
            return None, status, message

##### Functions #####
if __name__ == "__main__":
    ### Testing code ###
    # Test file paths
    path = ['0.1Ag-1.xls', '0.1Ag-1.xlsx', '0.1Ag-1.txt', '0.2Ag-1.txt', '0.1Ag-1.csv']
    
    # Create DataImport object and print results
    obj = DataImport(path=path[4])
    print(obj.data)
    print(obj.file_name, obj.file_type, obj.status, obj.status_message)