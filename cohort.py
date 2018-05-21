import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

pd.set_option('max_columns', 50)
mpl.rcParams['lines.linewidth'] = 2

%matplotlib inline

df = pd.read_csv('C:\\Users\\radhapavan\\Desktop\\cohort\\relay-foods-1.csv')
df.head()
# converting dateformat to y-m
# reatin proginal orderdate columns
df['OrderDat'] = pd.to_datetime(df.OrderDate)
df['OrderPeriod'] = df['OrderDat'].dt.strftime('%Y-%m')

# Replace $ and convert back to number
df['TotalCharges2'] = df['TotalCharges'].str.replace('$', '') # replace $sign
df['TotalCharges'] = pd.to_numeric(df['TotalCharges2'], errors='coerce')
##print(df.head(5))


#cohort group column
df.set_index('UserId', inplace=True)
df['CohortGroup'] = df.groupby(level=0)['OrderDat'].min().apply(lambda x: x.strftime('%Y-%m'))
df.reset_index(inplace=True)
#print(df.head(5))

'''
Since we're looking at monthly cohorts, we need to aggregate users, orders, and amount spent by the CohortGroup within the month (OrderPeriod).
'''
grouped = df.groupby(['CohortGroup', 'OrderPeriod'])
# count the unique users, orders, and total revenue per Group + Period
cohorts = grouped.agg({'UserId': pd.Series.nunique,
                       'OrderId': pd.Series.nunique,
                       'TotalCharges': np.sum})

# make the column names more meaningful
cohorts.rename(columns={'UserId': 'TotalUsers',
                        'OrderId': 'TotalOrders'}, inplace=True)
print(cohorts.head())