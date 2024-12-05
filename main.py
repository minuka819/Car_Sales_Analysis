import  pandas as pd
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
    - date type is converted to date
    - All other headers are converted to string types 
    
CSV file is output and ready for SQL integration
'''



#setting default values for data frame visualization

df = pd.read_csv("D:\\Data_science\\Projects\\My_Car_Sales\\car_prices.csv")

#inspect the first 80 rows, through visual insepction row#74 had an empty cell case
#print(df.info())

#print(df.head(80))
#I imported csv but most of the strings are objects , will this be a problem in the future

#print(df.to_string(pd))

#change object to string

#df['make'] = df['make'].astype("object")

#making a copy of the data frame so that original data frame is a reference point for cleaning stages
df_copy = df.copy(deep=True)

print(df_copy.info())

#for loop for converting column types to what is required
for column in df_copy:
    if (column == 'year') or (column == 'condition') or (column == 'odometer') or (column == 'mmr') or (column == 'sellingprice'):
        df_copy[column].fillna(0,inplace=True)
        df_copy[column] = df_copy[column].astype('int')
    else:
        df_copy[column].fillna("unknown",inplace=True)
        df_copy[column] = df_copy[column].astype('string')

jettas = df_copy[df_copy['trim'] == 'SE PZEV w/Connectivity']

#print(jettas)

#print(df_copy.info())

df_copy.drop(df_copy[df_copy.trim == 'SE PZEV w/Connectivity'].index)

#we found 26 Volkswaggen jettas with no VIN , incorrect sales date and no mmmr value so we decided to remove these from the dataset
#print(df_copy.info())

print(df_copy.info())

#checking for null values

print('Any null values?\n',df.isnull().values.any(),'\n Null report:\n', df[df.columns[df.isnull().any()]].isnull().sum())

print('\nNull Report for new:\n',df_copy.isnull().values.any())
'''
In this project we want to test whether the condition of the car,the year and the odomoter has an effect on the
selling price and mmr

Correlation testing in Pandas 
'''

