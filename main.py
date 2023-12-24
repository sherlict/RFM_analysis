import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
df = pd.read_csv('Online_Retail_2.csv', sep=';', parse_dates=['InvoiceDate'], 
     dayfirst=True, dtype={'UnitPrice': float, 'CustomerID': str}, decimal=',')

# We select lines in which 'InvoiceNo' begins with 'C'
filtered_df = df[~df['InvoiceNo'].str.startswith('C')]

# We clean the data
df = df[(df['Quantity'] > 0) & (df['Quantity'] < 10000) & (df['UnitPrice'] > 0)]
df = df.dropna()
df['Sum'] = df['Quantity'] * df['UnitPrice']

# Calculation of the number of purchases per customer
# Counting the number of InvoiceNo for each CustomerID
purchase_frequency = df.groupby('CustomerID')['InvoiceDate'].count().reset_index()

# Filter only buyers who have made more than one purchase
filtered_customers = purchase_frequency[purchase_frequency['InvoiceDate'] > 1]

# Leave only rows corresponding to customers who made more than one purchase
df = df[df['CustomerID'].isin(filtered_customers['CustomerID'])]
purchase_frequency = df.groupby('CustomerID')['InvoiceDate'].count().reset_index()

# Breakdown of purchase_frequency into 10 segments
purchase_frequency['PurchaseSegment'] = pd.qcut(purchase_frequency['InvoiceDate'], q=10, labels=False, duplicates='drop')+1
sorted_purchase_frequency = purchase_frequency.sort_values(by='InvoiceDate')

# We group the data by segments and find the maximum number of purchases (purchase dates) in each segment
segment_counts = purchase_frequency.groupby('PurchaseSegment')['InvoiceDate'].max().reset_index()

# Creating a schedule
plt.figure(figsize=(10, 6))
plt.bar(segment_counts['PurchaseSegment'], segment_counts['InvoiceDate'], color='skyblue', edgecolor='black')

# We add annotations with the maximum number of days for each segment
for index, value in zip(segment_counts['PurchaseSegment'], segment_counts['InvoiceDate']):
    plt.text(index, value, str(value), ha='center', va='bottom')

# We add the median line
median_value = purchase_frequency['InvoiceDate'].median()
plt.axhline(y=median_value, color='red', linestyle='--', label=f'Median: {int(median_value)}')

# We add a line of average value
mean_value = purchase_frequency['InvoiceDate'].mean()
plt.axhline(y=mean_value, color='green', linestyle='--', label=f'Mean: {int(mean_value)}')
plt.legend()

# Adding captions and a title
plt.xlabel('Segments (in order of increasing number of purchases)')
plt.ylabel('Maximum number of purchases')
plt.title('Distribution of the number of purchases per customer by segment')
plt.show()

# We count the number of subscribers in each segment
customer_counts = purchase_frequency['PurchaseSegment'].value_counts().sort_index().reset_index()
customer_counts.columns = ['PurchaseSegment', 'CustomerCount']

# We display it on the graph
plt.figure(figsize=(10, 6))
bars = plt.bar(customer_counts['PurchaseSegment'], customer_counts['CustomerCount'], color='skyblue', edgecolor='black')

# We add the text with the number of buyers to each column
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, int(yval), ha='center', va='bottom')

# Adding captions and a title
plt.xlabel('Segments (in order of increasing number of purchases)')
plt.ylabel('Number of buyers')
plt.title('The number of buyers in each segment')
plt.show()

# We group data by segments and get unique buyers for each segment
segment_customers = last_purchase_date.groupby('DaysSegment')['CustomerID'].unique().reset_index()

# We display a list of buyers for each segment
for index, row in segment_customers.iterrows():
    segment = row['DaysSegment']
    customers = row['CustomerID']
    print(f"Сегмент {segment}: {customers}")

# Age of last purchase (Recency)

# We find for each buyer the last date of his purchase
last_purchase_date = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()

# We calculate the number of days without purchases until the end of the period
last_date = df['InvoiceDate'].max()
last_purchase_date['DaysWithoutPurchase'] = (last_date - last_purchase_date['InvoiceDate']).dt.days

# We divide the number of days without purchases into 10 segments in ascending order
last_purchase_date['DaysSegment'] = pd.qcut(last_purchase_date['DaysWithoutPurchase'], q=10, labels=False, duplicates='drop', retbins=False, precision=0)+1

# We group the data by segments and find the maximum number of days in each segment
segment_counts = last_purchase_date.groupby('DaysSegment')['DaysWithoutPurchase'].max().reset_index()

# We create a schedule
plt.figure(figsize=(10, 6))
plt.bar(segment_counts['DaysSegment'], segment_counts['DaysWithoutPurchase'], color='skyblue')

# We add annotations with the maximum number of days for each segment
for index, value in zip(segment_counts['DaysSegment'], segment_counts['DaysWithoutPurchase']):
    plt.text(index, value, str(value), ha='center', va='bottom')

# We add the median line
median_value = segment_counts['DaysWithoutPurchase'].median()
plt.axhline(y=median_value, color='red', linestyle='--', label=f'Median: {median_value}')

# We add a line of average value
mean_value = segment_counts['DaysWithoutPurchase'].mean()
plt.axhline(y=mean_value, color='green', linestyle='--', label=f'Mean: {mean_value}')

plt.xlabel('Segments (in ascending order of the number of days)')
plt.ylabel('Maximum number of days without purchase')
plt.title('Distribution of the number of days without a purchase by segments')
plt.legend()
plt.show()

# We count the number of subscribers in each segment
customer_counts = last_purchase_date['DaysSegment'].value_counts().sort_index()

# We display it on the graph
plt.figure(figsize=(10, 4))
bars = plt.bar(customer_counts.index, customer_counts.values)

plt.xlabel('Segments by day')
plt.ylabel('Number of customers')
plt.title('Distribution of customers by days without purchase')

# We add the text with the number of buyers to each column
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, round(yval), ha='center', va='bottom')

plt.show()

segment_customers = last_purchase_date.groupby('DaysSegment')['CustomerID'].agg(list).reset_index()
segment_customers.head(10)

# Purchase amount (Monetary)

# Calculation of Sum for each CustomerID and InvoiceNo
sum_per_purchase = df.groupby(['CustomerID', 'InvoiceNo'])['Sum'].sum().reset_index()

# We divide the number of purchases into 10 segments in ascending order
sum_per_purchase['SumPerPurchase'] = pd.qcut(sum_per_purchase['Sum'], q=10, labels=False, duplicates='drop') + 1

# We create a schedule
plt.figure(figsize=(10, 6))
plt.bar(segment_stats['SumPerPurchase'], segment_stats['max'], color='skyblue', label='Максимальна сума')

# We add the median and mean lines
plt.plot(segment_stats['SumPerPurchase'], segment_stats['median'], color='red', linestyle='--', label='Median line')
plt.plot(segment_stats['SumPerPurchase'], segment_stats['mean'], color='purple', linestyle='--', label='The middle line')

# We add annotations with the maximum amount for each segment
for index, max_val in zip(segment_stats['SumPerPurchase'], segment_stats['max']):
    plt.text(index, max_val, f"{round(max_val)}", ha='center', va='bottom')

# We add the text for the legend with the average value
median_legend_text = f"Median: {round(segment_stats['median'].mean())}"
mean_legend_text = f"Middle line: {round(segment_stats['mean'].mean())}"
plt.legend([median_legend_text, mean_legend_text])

plt.xlabel('Segments (in ascending order of amount)')
plt.ylabel('The value of the amount of purchases')
plt.title('Distribution of the median and average purchase amounts by segment')
plt.show()

# Calculation of buyer rank

# We find for each buyer the last date of his purchase
last_purchase_date = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()

# We calculate the number of days without purchases until the end of the period
last_date = df['InvoiceDate'].max()
last_purchase_date['DaysWithoutPurchase'] = (last_date - last_purchase_date['InvoiceDate']).dt.days

# We determine the value of X by condition
last_purchase_date['X'] = pd.cut(last_purchase_date['DaysWithoutPurchase'], bins=[-np.inf, 21, 105, np.inf], labels=[1, 2, 3])

#  We find the number of purchases for each customer
purchase_frequency = df.groupby('CustomerID')['InvoiceDate'].count().reset_index()

# We determine the value of Y according to the condition
purchase_frequency['Y'] = np.where(purchase_frequency['InvoiceDate'] > 93, 1, 2)

# Calculation of Sum for each CustomerID and InvoiceNo
sum_per_purchase = df.groupby(['CustomerID', 'InvoiceNo'])['Sum'].sum().reset_index()

# We determine the value of Z according to the condition
sum_per_purchase['Z'] = np.where(sum_per_purchase['Sum'] > 418, 1, 2)
# We combine data from different variables into a separate dataframe
rank_df = pd.merge(last_purchase_date[['CustomerID', 'X']], purchase_frequency[['CustomerID', 'Y']], on='CustomerID')
rank_df = pd.merge(rank_df, sum_per_purchase[['CustomerID', 'Z']], on='CustomerID')

# We find unique CustomerIDs and assign them a rank
rank_df = rank_df.drop_duplicates(subset='CustomerID').reset_index(drop=True)
# We combine the values of variables X, Y, Z into one number
rank_df['Rank'] = rank_df.apply(lambda row: int(f"{row['X']}{row['Y']}{row['Z']}"), axis=1)

print(rank_df[['CustomerID', 'Rank']])

# Calculation of the number in % of each Rank
rank_counts = rank_df['Rank'].value_counts()
rank_percentages = round(rank_counts / rank_counts.sum() * 100, 1)

rank_percentages_sorted = rank_percentages.sort_index(ascending=True)
print(rank_percentages_sorted)
