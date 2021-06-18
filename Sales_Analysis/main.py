import pandas as pd
import os
import matplotlib.pyplot as plt

# get all csv files in an array
files = os.listdir("./Sales_Data")

# empty dataframe to merge all csv files into one csv file
merged_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("./Sales_Data/" + file)
    merged_data = pd.concat([merged_data, df])


# cleaning up the data

# dropping rows with NaN
nan_df = merged_data[merged_data.isna().any(axis=1)]
merged_data = merged_data.dropna(how='all')

# dropping some duplicated title rows
merged_data = merged_data[merged_data['Order Date'].str[0:2] != 'Or']

# converting the Quantity Ordered & Price Each to int or float
merged_data['Quantity Ordered'] = pd.to_numeric(merged_data['Quantity Ordered'])
merged_data['Price Each'] = pd.to_numeric(merged_data['Price Each'])


# add month column
merged_data['Month'] = merged_data['Order Date'].str[0:2]
merged_data['Month'] = merged_data['Month'].astype('int32')

# add a sales column
merged_data['Sales'] = merged_data['Quantity Ordered'] * merged_data['Price Each']


# add a city column
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

merged_data['City'] = merged_data['Purchase Address'].apply(lambda x: f"{get_city(x)}, {get_state(x)}")


# Q1. What was the month with the best sales?
results = merged_data.groupby('Month').sum()
results.to_csv('Monthly_data.csv')

months = range(1, 13)
plt.bar(months, results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in 1M $ USD')
plt.xlabel('Month Number')
plt.show()

# Q2 Which city had the best sales?
results = merged_data.groupby('City').sum()
results.to_csv('City_Sales_data.csv')

cities = [city for city, df in merged_data.groupby('City')]

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation='vertical')
plt.ylabel('Sales in 1M $ USD')
plt.xlabel('City')
plt.show()

# converting Order date of the merged data in a date time object
merged_data['Order Date'] = pd.to_datetime(merged_data['Order Date'])

# adding an hour column
merged_data['Hour'] = merged_data['Order Date'].dt.hour
merged_data.to_csv("merged_data.csv", index=False)

# Q3 What is the best time to display advertises to increase likelihood of purchases
results = merged_data.groupby('Hour').sum()

hours = [hour for hour, df in merged_data.groupby('Hour')]

plt.plot(hours, merged_data.groupby('Hour').count())
plt.xticks(hours)
plt.yticks(rotation='vertical')
plt.xlabel('Hour')
plt.ylabel('Purchases made')
plt.grid()
plt.show()

# Q4 What product sold the most
results = merged_data.groupby('Product').sum()
results.to_csv('most_sold.csv')

prices = merged_data.groupby('Product').mean()['Price Each']

products = [product for product, df in results.groupby('Product')]

plt.bar(products, results['Quantity Ordered'])
plt.xticks(products, rotation='vertical')
plt.yticks(rotation='vertical')
plt.xlabel('Product')
plt.ylabel('Purchase frequency')
plt.show()
