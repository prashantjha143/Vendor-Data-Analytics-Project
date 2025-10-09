# Vendor-Data-Analytics-Project
<img width="1280" height="720" alt="Presentation1" src="https://github.com/user-attachments/assets/be3205a2-3278-4180-b22f-30d24c93d0c8" />

**Overview**
----------
This project involves a comprehensive analysis of Vendors sales data using Python,SQL and PowerBi. The goal is to extract valuable insights and answer various business questions based on the dataset. The following README provides a detailed account of the project's objectives, business problems, solutions, findings, and conclusions.

Here, I use sqlite3 in Python for loading data into database **inventory.db**.

## Objective
--------
**Tasks**
* Create the database using given '.csv' files.
*  Analyze the data
*  Data Preprocessing
*  Exploratory Data Analysis
*  Creating Visualizations for better understanding
*  Creating new columns like GrossProfit,ProfitMargin,StockTurnover and SalestoPurchaseRatio
*  Now convert the dataframe we created with new columns to '.csv' file
*  Create dashboard based on this '.csv' file
*  Create Report File based on analysis

--------------------------
## Dataset
Dataset link - [Link](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbks1NXFFZV9ULXY4Y0JyVVR6RVczcGRrWWh6Z3xBQ3Jtc0tuV3ZDVW80aG9rSEQxczdobmthZTN5N3pfRmhxT0VmbThwcUJVdnFNbDFFaEhTemFLZ19NeG4yTUlxUzF1dDJoM015MnZHUHdNV2ZmaUVSUkpLMkhVeWVYOXdkVm1WeTlmdDFYOG9WSlYxYVFObzg4TQ&q=https%3A%2F%2Ftopmate.io%2Fayushi_mishra%2F1557424&v=nmCfNHjfgEY)

### Step1 - Ingesting data from the datasets
```python
import pandas as pd
import os
from sqlalchemy import create_engine
import logging


logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s -%(levelname)s -%(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df,table_name,engine):
    '''This function will ingest the dataframe into database table'''
    df.to_sql(table_name,con = engine,if_exists = 'replace',index = 'False')
    
def load_raw_data():
    '''This function will load CSV into dataframe and ingest them into db'''
    start = time.time()
    for file in os.listdir('C:\\Users\\admin\\Documents\\study\\data anlytics\\end to end\\data'):
        if'.csv' in file:
            # print('---',file,'---')
            df = pd.read_csv('C:\\Users\\admin\\Documents\\study\\data anlytics\\end to end\\data\\'+file)
            logging.info(f'Ingesting {file} in db' )
            ingest_db(df,file[:-4],engine)
    end = time.time()
    total_time = (end -start)/60
    logging.info('--------Ingestion complete---------')
    logging.info(f'Total Time Taken: {total_time} ,minutes')

if __name__=='__main__':
    load_raw_data()
```
### Step2- Exploratory Data Analysis

```python
import pandas as pd
import sqlite3
import logging
from ingestion_db import ingest_db
logging.basicConfig(
    filename = 'logs/get_vendor_summary.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

conn = sqlite3.connect('inventory.db')

tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type = 'table'",conn)

tables

for table in tables['name']:
    print('-'*50 ,f'{table}','-'*50 )
    print('Count of records : ' ,pd.read_sql(f"select count(*) as count from {table}",conn)['count'].values[0])
    display(pd.read_sql(f"select * from {table} limit 5",conn))

purchases = pd.read_sql('''select * from purchases
                           where VendorNumber = 4466 ''',conn)
purchases

purchase_prices = pd.read_sql('''select * from purchase_prices
                           where VendorNumber = 4466 ''',conn)
purchase_prices

vendor_invoice = pd.read_sql('''select * from vendor_invoice
                           where VendorNumber = 4466 ''',conn)
vendor_invoice

sales = pd.read_sql('''select * from sales 
                       where VendorNo = 4466 ''',conn)
sales

purchases.groupby(['Brand','PurchasePrice'])[['Quantity','Dollars']].sum()

sales.groupby('Brand')[['SalesDollars','SalesPrice', 'SalesQuantity']].sum()

purchase_prices

vendor_invoice['PONumber'].nunique()

* The purchase table contains actual purchase data, including the date of purchase, products(brands) purchased by vendors, the amount paid( in dollars) , and the quantity purchased.
* The purchased price column is derived from the purchase_prices table, which provides product-wise actual and purchase prices. The combination of vendor and brand is unique in this table.
* The vendor_invoice table aggregates data from the purchases table, summarizing quantity and dollars amount, along with an additional column for freight. This table maintains the uniqueness based on vendor and PO number.
* The sales table captures actual sales transactions, detailing the brands purchased by vendors, the quantity sold, the selling price, and the revenue earned.
***
As the data that we need for analysis is distributed in different tables , we need to create a summary table containing:
* purchase transactions made by vendors
* sales transaction data
* freight costs for each vendor
* actual product prices from vendors

vendor_invoice.columns

freight_summary = pd.read_sql('''select VendorNumber,sum(Freight) from vendor_invoice
                                 group by VendorNumber ''',conn)

freight_summary

pd.read_sql('''SELECT * FROM purchases ''',conn )

pd.read_sql('''SELECT 
    *
    FROM purchase_prices ''',conn )

# pd.read_sql('''SELECT 
#                 p.VendorNumber,
#                 p.VendorName,
#                 p.Brand,
#                 pp.Volume,
#                 pp.Price AS ActualPrice,
#                 pp.PurchasePrice,
#                 SUM(p.Quantity) AS TotalQuantityPurchased,
#                 SUM(p.Dollars) AS TotalPurchaseDollar
#                 FROM purchases AS p
#                 JOIN purchase_prices AS pp
#                 ON
#                 p.VendorNumber = pp.VendorNumber
#                 GROUP BY p.VendorNumber,p.VendorName,p.brand
#          ''',conn )

pd.read_sql('''SELECT
    p.VendorNumber,
    p.VendorName,
    p.Brand,
    p.PurchasePrice,
    pp.Volume,
    pp.Price AS ActualPrice,
    SUM(p.Quantity) AS TotalPuchaseQuantity,
    SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases AS p
    JOIN purchase_prices AS pp
    ON 
    p.brand = pp.brand
    WHERE p.PurchasePrice >0
    GROUP BY p.VendorNumber,p.VendorName,p.Brand
    ORDER BY TotalPurchaseDollars''',conn)

import time
start = time.time()
vendor_sales_summary = pd.read_sql_query(''' WITH FreightSummary AS (
    SELECT 
        VendorNumber,
        SUM(Freight) AS FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
),
PurchaseSummary AS (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price AS ActualPrice,
        pp.Volume,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases AS p
    JOIN purchase_prices AS pp
    ON
    p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY p.VendorNumber,p.VendorName,p.Brand,p.Description,p.PurchasePrice, pp.Price,pp.Volume
),

SalesSummary AS (
    SELECT
        VendorNo,
        Brand,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo,Brand
)
SELECT 
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary AS ps 
LEFT JOIN SalesSummary AS ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary AS fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC
''',conn)
end = time.time()
totaltimetaken = (end - start)/60
print(f'total {totaltimetaken} minutes')

vendor_sales_summary

This query 👆 generates a vendor-wise sales and purchase summary, which is valuable for:

**Performance Optimization**
* The query involves heavy joins and aggregations on large datassets like sales and purchases.
* Storing the pre-aggregated results avoids repeated expensive computations.
* Helps in analyzing sales, purchases, and pricing for different vendors and brands.
* Future benefits of Storing this data for faster Dashboarding & Reporting.
* Instead of running expensive queries each time, dashboards can fetch data quickly from vendor_sales_summary.

vendor_sales_summary.dtypes

vendor_sales_summary.isnull().sum()

vendor_sales_summary['VendorName'].unique()

vendor_sales_summary['Description'].unique()

vendor_sales_summary['Volume'] = vendor_sales_summary['Volume'].astype('float64')
vendor_sales_summary.fillna(0,inplace = True)

vendor_sales_summary['VendorName'] = vendor_sales_summary['VendorName'].str.strip()

vendor_sales_summary['GrossProfit'] = vendor_sales_summary['TotalSalesDollars'] - vendor_sales_summary['TotalPurchaseDollars']
vendor_sales_summary['ProfitMargin'] = (vendor_sales_summary['GrossProfit']/vendor_sales_summary['TotalSalesDollars']) * 100
vendor_sales_summary['StockTurnover'] = vendor_sales_summary['TotalSalesQuantity']/vendor_sales_summary['TotalPurchaseQuantity']
vendor_sales_summary['SalestoPurchaseRatio'] = vendor_sales_summary['TotalSalesDollars']/vendor_sales_summary['TotalPurchaseDollars']

cursor = conn.cursor()

cursor.execute(''' 
CREATE TABLE vendor_sales_summary(
    VendorNumber INT,
    VendorName VARCHAR(100),
    Brand VARCHAR(100),
    PurchasePrice DECIMAL(10,2),
    ActualPrice DECIMAL(10,2),
    Volume,
    TotalPurchaseQuantity INT,
    TotalPurchaseDollars DECIMAL(15,2),
    TotalSalesQuantity INT,
    TotalSalesDollars DECIMAL(15,2),
    TotalSalesPrice DECIMAL(15,2),
    TotalExciseTax DECIMAL(15,2),
    FreightCost DECIMAL(15,2),
    GrossProfit DECIMAL(15,2),
    ProfitMargin DECIMAL(15,2),
    StockTurnover DECIMAL(15,2),
    SalesToPurchaseRatio DECIMAL(15,2),
    PRIMARY KEY(VendorNumber , Brand)
);
''')

pd.read_sql('select*from vendor_sales_summary',conn)

vendor_sales_summary.to_sql('vendor_sales_summary',conn,if_exists = 'replace',index = False)

pd.read_sql('select*from vendor_sales_summary',conn)
```
### Step3 - Creating function for creating final Data(table)
```python
def create_vendor_summary(conn):
    start = time.time()
    vendor_sales_summary = pd.read_sql_query(''' WITH FreightSummary AS (
        SELECT 
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases AS p
        JOIN purchase_prices AS pp
        ON
        p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber,p.VendorName,p.Brand,p.Description,p.PurchasePrice, pp.Price,pp.Volume
    ),
    
    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo,Brand
    )
    SELECT 
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary AS ps 
    LEFT JOIN SalesSummary AS ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary AS fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    ''',conn)
    
    return vendor_sales_summary

def clean_data(df):
    df['Volume'] = df['Volume'].astype('float64')
    df.fillna(0,inplace = True)
    
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit']/df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity']/df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars']/df['TotalPurchaseDollars']

    return df

if __name__=='__main__' :
    conn = sqlite3.connect('inventory.db')

    logging.info('Creating Vendor Summary Table....')
    summary_df = create_vendor_summary1(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data...')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting data....')
    ingest_db(clean_df,'vendor_sales_summary',conn)
    logging.info('Completed')

```
## PowerBi Dashboard
<img width="1430" height="803" alt="Screenshot 2025-10-06 160820" src="https://github.com/user-attachments/assets/a3ead882-45bb-47bc-a20e-eadf10d998e3" />

---------
### Description of file added in this repository
* ingesting.ipynb - In this jupyter notebook, Data load, then convert them into SQL tables
* ingesting.log - It is a log file which stores information everytime when we run the script
* EDA.ipynb - In this jupyter notebook, we have gained meaningful insights, visualize data with different plots , creating new tables which catries only useful information
* get_vendor_summary.log - It stores the information of every summary created on data by calling create_vendor_summary function
* ingesting.py, get_vendor_summary.py - These are nothing but scripts that are used without using notebooks everytime when new data is added to the database
* Exploratory Data Analysis Insights.docx - This is my report file of the whole project
---------------

Feel free to connect - [LinkedIn](https://github.com/prashantjha143)

If you have any suggestions related to this project, please let me know.
