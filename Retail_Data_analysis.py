#import libraries and Load data
import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\JATIN\OneDrive\Desktop\Retail_Data_Analysis_Pandas\Online Retail.csv')
print(df.head())
print(df.info())

#Handling Missing Values

print(df.isnull().sum())
df['Description'] = df['Description'].fillna('unknown product')
df['CustomerID'] = df['CustomerID'].fillna(-1).astype(int)
print(df.isnull().sum())

#convert Invoice Date to Date-time
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

#Checking Return Order
returns_df = df[df['Quantity'] < 0]

sales_df = df[df["Quantity"]>0].copy()

returns_df = returns_df[returns_df['Description'] != 'Discount']
sales_df['Revenue'] = sales_df['Quantity']*sales_df['UnitPrice']

#Calculate the total revenue

total_revenue = sales_df['Revenue'].sum()
print("Total Revenue:", total_revenue)

#Monthly Revenue
sales_df['Month'] = sales_df['InvoiceDate'].dt.month
monthly_revenue = sales_df.groupby('Month')['Revenue'].sum()
print(monthly_revenue)

#Top 10 Products

top_products = sales_df.groupby('Description')['Revenue']\
.sum()\
.sort_values(ascending=False)\
.head(10)

print(top_products)

#Country Wise Revenue

country_wise_revenue = sales_df.groupby('Country')['Revenue'].sum()\
.sort_values(ascending=False)
print(country_wise_revenue)

#Customer Analysis : Top Unique Customers(excluding -1)

unique_customers = sales_df[sales_df['CustomerID'] != -1]['CustomerID'].nunique()
print("Total Unique Customers:", unique_customers)

#Top 10 High Value Customers

high_value_customers = sales_df[sales_df['CustomerID'] != -1]\
.groupby('CustomerID')['Revenue']\
.sum()\
.sort_values(ascending=False)\
.head(10)
print(high_value_customers)

#Repeat Customers 
repeat_customers = sales_df[sales_df['CustomerID'] != -1]['CustomerID']\
.value_counts()\
.head(10)
print(repeat_customers)


#------------------------------------------Order Level Insights------------------------------
#average order value

average_order_value = sales_df.groupby('InvoiceNo')['Revenue'].mean().mean()
print("Average Order Value", average_order_value)

#average products per order
average_products_per_order = sales_df.groupby('InvoiceNo')['Quantity'].sum().mean()
print("Average Products Per order", average_products_per_order)

#Most Returned Products
Most_return = returns_df.groupby('Description')['Quantity']\
.sum()\
.sort_values(ascending=False)
print('Most Returned Products', Most_return.head(10))

#-------------------------------Time Based Insights----------------------------------------

sales_df['weekday'] = sales_df['InvoiceDate'].dt.weekday
# Best Sales Day
weekday_revenue = sales_df.groupby('weekday')['Revenue'].sum()\
.sort_values(ascending=False)

weekday_map = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
weekday_revenue.index = weekday_revenue.index.map(weekday_map)
print(weekday_revenue)

# Highest Revenue Day
HRD = sales_df.groupby('weekday')['Revenue'].sum()
print("Highest Revenue Day",HRD.idxmax(), "Revenue:", HRD.max())

# Best Sales Hour
sales_df['hour'] = sales_df['InvoiceDate'].dt.hour

Best_sales_hour = sales_df.groupby('hour')['Revenue'].sum()
print("Best Sales Hour", Best_sales_hour)
print("Best Sales Hour", Best_sales_hour.idxmax(), "Revenue", Best_sales_hour.max())


