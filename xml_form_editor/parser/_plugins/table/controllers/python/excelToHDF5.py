import sys
from xlrd import open_workbook
from argparse import ArgumentError
from cgi import FieldStorage

# Redirecting error output into the standard output
sys.stderr = sys.stdout

# Checking the number of attributes
if len(sys.argv)!=2:
    raise Exception('Invalid number of arguments: 1 expected, '+str(len(sys.argv)-1)+' given '+str(sys.argv))

excelFile = str(sys.argv[1])
#print ">Opening "+excelFile

book = open_workbook(excelFile)
sheetCount = book.nsheets

#print ">The book contains "+str(sheetCount)+" sheet(s)"

dataFromFile = ""
columnName = []
columnType = []

for s in book.sheets():
    #print '>Sheet:',s.name
    for row in range(s.nrows):
        
        values = []
        if row<=1: types = []
        
        for col in range(s.ncols):
            cellValue=s.cell(row,col).value
            
            # Converting Unicode strings to regular string
            if isinstance(cellValue, unicode):
                cellValue = str(cellValue)
            
            # If the variable is a string and not a header name (row 0), we need to surround the element with "
            if isinstance(cellValue, str) and row != 0:
                cellValue = '"' + cellValue + '"'
                
            if row <= 1:
                cellValueType = type(cellValue)
                
                types.append(str(cellValueType)[7:-2])
                values.append(str(cellValue))
            else:
                if columnType[col]==str(type(cellValue))[7:-2]:
                    values.append(str(cellValue))
                else:
                    values.append('##Incoherent type of value ('+str(columnType[col])+' & '+str(type(cellValue))+')##')
        
        if row == 1:
            columnType = types
        
        if row == 0: # Storing column names separately from the values
            columnName = values
        else:
            dataFromFile = dataFromFile + ' '.join(values)
            # dataFromFile = dataFromFile + '\n'


hdf5XmlCode = '<hDF5-File><hdf5:RootGroup OBJ-XID="xid_96" H5Path="/">'
hdf5XmlCode += '<hdf5:Group Name="Data" OBJ-XID="xid_800" H5Path="/Data" Parents="xid_96" H5ParentPaths="/" >'
hdf5XmlCode += '<hdf5:Dataset Name="'+ 'excelFile' +'" OBJ-XID="xid_1832" H5Path= "/Data/table" Parents="xid_800" H5ParentPaths="/Data">'
hdf5XmlCode += '<hdf5:StorageLayout><hdf5:ChunkedLayout Ndims="1"><hdf5:ChunkDimension DimSize="2" /><hdf5:RequiredFilter></hdf5:RequiredFilter></hdf5:ChunkedLayout></hdf5:StorageLayout>'
hdf5XmlCode += '<hdf5:FillValueInfo FillTime="FillIfSet" AllocationTime="Incremental"><hdf5:FillValue><hdf5:NoFill/></hdf5:FillValue></hdf5:FillValueInfo>'
hdf5XmlCode += '<hdf5:Dataspace><hdf5:SimpleDataspace Ndims="1"><hdf5:Dimension  DimSize="2" MaxDimSize="UNLIMITED"/></hdf5:SimpleDataspace></hdf5:Dataspace>'
hdf5XmlCode += '<hdf5:DataType><hdf5:CompoundType>'

hdf5UnitCode = ''

for i in range(len(columnName)):
    # Setting the unit of data in the colums
    indexStart = columnName[i].index('(')
    indexEnd = -1
    
    hdf5UnitCode += '<columnUnit><unitOfMeasureType><name>' + columnName[i][indexStart + 1:indexEnd] + '</name></unitOfMeasureType>'
    
    columnName[i] = columnName[i][:indexStart]
    
    # Setting the type of data in the columns
    if columnType[i] == 'str':
        fieldCode = '<hdf5:Field FieldName="'+columnName[i]+'"><hdf5:DataType><hdf5:AtomicType><hdf5:StringType Cset="H5T_CSET_ASCII" StrSize="64" StrPad="H5T_STR_NULLTERM"/>'
        fieldCode += '</hdf5:AtomicType></hdf5:DataType></hdf5:Field>'
    elif columnType[i] == 'float':
        fieldCode = '<hdf5:Field FieldName="'+columnName[i]+'"><hdf5:DataType><hdf5:AtomicType>'
        fieldCode += '<hdf5:FloatType ByteOrder="LE" Size="4" SignBitLocation="31" ExponentBits="8" ExponentLocation="23" MantissaBits="23" MantissaLocation="0" />'
        fieldCode += '</hdf5:AtomicType></hdf5:DataType></hdf5:Field>'
    else:
        ##Unknown data type##
        fieldCode = ''
    
    hdf5XmlCode = hdf5XmlCode + fieldCode
    hdf5UnitCode = hdf5UnitCode + fieldCode + '</columnUnit>'
    
    
hdf5XmlCode = hdf5XmlCode + '</hdf5:CompoundType></hdf5:DataType><hdf5:Data><hdf5:DataFromFile>' + dataFromFile + '</hdf5:DataFromFile></hdf5:Data>'
hdf5XmlCode += '</hdf5:Dataset></hdf5:Group></hdf5:RootGroup></hDF5-File>'

print hdf5UnitCode + hdf5XmlCode

