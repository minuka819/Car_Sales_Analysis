import pandas as pd
import warnings

pd.set_option('display.max_columns', None)

warnings.filterwarnings("ignore")
'''
DATA CLEANING

Through manual viewing in excel, I noticed blank cell spaces. To investigate further the csv file is imported 
as a dataframe in the pandas package.  

To clean the car_sales data set for SQL database integration we have two goals:

(1) Remove null characters
    - Replace NAN with 0 for integer types
    - Replace NAN with 'unknown' for string types 
(2) Type cast data types of columns to appropriate data types
    - Headers including year, condition, odometer, mmr and selling price are type casted to int
    - Date column needs to be split into date and time column
    - All other headers are converted to string types 
    
CSV file is output and ready for SQL integration
'''
#setting default values for data frame visualization

df = pd.read_csv("D:\\Data_science\\Projects\\My_Car_Sales\\car_prices.csv")

#inspect the first 80 rows, through visual insepction row#74 had an empty cell case

#print(df.head(80))

#I imported csv but most of the strings are objects , will this be a problem in the future

#making a copy of the data frame so that original data frame is a reference point for cleaning stages
df_copy = df.copy(deep=True)

#Data removal of some rows
#Noticed that subsection of jettas with trim SE PZEV w/connectivity are incomplete , thus decided to remove these rows
jettas = df_copy[df_copy['trim'] == 'SE PZEV w/Connectivity']
#print(jettas)
df_copy = df_copy.drop( df_copy[df_copy['trim']=='SE PZEV w/Connectivity'].index)
#There is a seller called kfl llc that has provided no entries on mmr, sellingprice and date so we remove them
df_copy = df_copy.dropna(subset='saledate')

#For loop for converting column types to what is required
for column in df_copy:
    if (column == 'year') or (column == 'condition') or (column == 'odometer') or (column == 'mmr') or (column == 'sellingprice'):
        df_copy[column].fillna(0,inplace=True)
        df_copy[column] = df_copy[column].astype('int')
    else:
        df_copy[column].fillna("unknown",inplace=True)
        df_copy[column] = df_copy[column].astype('string')

#using regex to extract the day date and time values
df_copy[['Day', 'Date', 'Time']] = df_copy['saledate'].str.extract(
    r'(\w+)\s+(\w+\s+\d+\s+\d+)\s+([\d:]+)'
)
df_copy['Date'] = df_copy['Date'].str.replace(' ','-', regex=True)
#now we do not need selling date so we can drop it from the df

df_copy = df_copy.drop('saledate', axis=1)

print(df_copy.dtypes)
#print(df_copy)
#print(df_copy.info)

#print('Any null values for original?\n',df.isnull().values.any(),'\n Null report for original:\n', df[df.columns[df.isnull().any()]].isnull().sum(),'\n')

#print('Any null values for new?\n',df_copy.isnull().values.any(),'\n Null report for new:\n', df_copy[df_copy.columns[df_copy.isnull().any()]].isnull().sum())

#checking for nulls
#rows_with_nulls = df_copy[df_copy.isnull().any(axis=1)]
#print(rows_with_nulls)

df_copy['Date'] = pd.to_datetime(df_copy['Date'], format='%b-%d-%Y')
df_copy['Time'] = pd.to_datetime(df_copy['Time'])

print('After changing date type : \n',df_copy.dtypes)


'''



df_copy['Date'].fillna(0,inplace=True)

#change Date string to dateype
print(df_copy['Date'])
df_copy['Date'] = pd.to_datetime(df_copy['Date'], format='%b-%d-%Y')
#print(df_copy['Date'])
#print(df_copy.info())
'''

'''

print(df_copy.info())

print(df_copy)

#checking for null values

print('Any null values for original?\n',df.isnull().values.any(),'\n Null report for original:\n', df[df.columns[df.isnull().any()]].isnull().sum(),'\n')

print('Any null values for new?\n',df_copy.isnull().values.any(),'\n Null report for original:\n', df_copy[df.columns[df.isnull().any()]].isnull().sum())



In this project we want to test whether the condition of the car,the year and the odomoter has an effect on the
selling price and mmr

Correlation testing in Pandas 

'''


