from DataImporter import *
from CV import *

path = '0.1Ag-1.csv'
    
# Create DataImport object and print results
obj = DataImport(path=path)
print(obj.data)
print(obj.file_name, obj.file_type, obj.status, obj.status_message)
dummy = obj.data.columns.tolist()
print(obj.data.iloc[:, 0:])
obj2 = UnifiedDataCV(obj) # Combine multiple data objects

print(obj2.headers[0])