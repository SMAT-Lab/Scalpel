import pandas as pd
import dill
import numpy
df = pd.read_csv("orders.csv", parse_dates=["created_at_date"])
df.head()
df.keys()
max_revenue = df[['customer_id', 'revenue']].groupby('customer_id', as_index=True).max()['revenue']
df[['customer_id', 'order_id']].groupby(['customer_id']).order_id.nunique().to_frame()
max_items = df[['customer_id', 'num_items']].groupby('customer_id', as_index=True).max()['num_items']
total_revenue = df[['customer_id', 'revenue']].groupby('customer_id', as_index=True).sum()['revenue']
days_since_last_order = pd.Timestamp.strptime('2017-10-17', '%Y-%m-%d') - df[['customer_id', 'created_at_date']].groupby('customer_id', as_index=True).max()['created_at_date']
result = pd.DataFrame({'Max revenue': max_revenue, 'Order count': order_count, 'Max items': max_items, 'Total revenue': total_revenue, 'Days since last order': days_since_last_order})
model = dill.load(open("model.dill", 'rb'))
array = numpy.array([[2, 5, 6, 7, 9, 10], [3, 6, 7, 8, 11, 12]])
model.predict(array)
df['revenue'].plot()
result
customers_orders = df.groupby(['customer_id', 'order_id'])
def max_items():
    return df.groupby(['customer_id', 'order_id'])['customer_id', 'order_id', 'num_items'].sum().groupby(['customer_id']).max()
df.head()
lol = df[['customer_id', 'created_at_date']].groupby('customer_id').max()['created_at_date'].subtract(pd.Timestamp(datetime(2017, 10, 17))).abs().to_frame()
lol.dtypes