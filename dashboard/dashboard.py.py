import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
all_data_df = pd.read_csv("all_data.csv")

# Ensure 'order_purchase_timestamp' is in datetime format
all_data_df['order_purchase_timestamp'] = pd.to_datetime(all_data_df['order_purchase_timestamp'])

# Extract month names for easier selection
all_data_df['month'] = all_data_df['order_purchase_timestamp'].dt.month_name()

# App title
st.title("Sales Data Visualization")

# Sidebar filter for selecting year
selected_year = st.sidebar.selectbox('Select Year', all_data_df['order_purchase_timestamp'].dt.year.unique())

# Sidebar filter for selecting month or 'All'
month_option = st.sidebar.radio('Select Month or View All', ['All Months'] + all_data_df['month'].unique().tolist())

# Filter data based on year and month selection
if month_option == 'All Months':
    filtered_data = all_data_df[all_data_df['order_purchase_timestamp'].dt.year == selected_year]
else:
    filtered_data = all_data_df[
        (all_data_df['order_purchase_timestamp'].dt.year == selected_year) & 
        (all_data_df['month'] == month_option)
    ]

# Business Question 1: Most and Least Sold Product Categories
category_sales = filtered_data.groupby('product_category_name_english')['order_id'].count()
most_sold_category = category_sales.idxmax()
most_sold_sales = category_sales.max()
least_sold_category = category_sales.idxmin()
least_sold_sales = category_sales.min()

# Display the results
st.subheader("Most and Least Sold Product Categories")
st.write("Most Sold Category:")
st.write(f"{most_sold_category} with {most_sold_sales} sales")
st.write("Least Sold Category:")
st.write(f"{least_sold_category} with {least_sold_sales} sales")

# Visualizing most and least sold categories
sales_data = pd.DataFrame({
    'Category': [most_sold_category, least_sold_category],
    'Sales': [most_sold_sales, least_sold_sales]
})

# Bar plot for most and least sold categories
plt.figure(figsize=(10, 5))
sns.barplot(x='Category', y='Sales', data=sales_data, palette='viridis')
plt.title('Most and Least Sold Product Categories')
plt.xlabel('Product Category')
plt.ylabel('Number of Sales')
plt.xticks(rotation=45)  # Rotate labels for better readability
st.pyplot(plt)

st.subheader(f"Top Three Selling Categories {selected_year}")
# Monthly sales count per category
monthly_category_sales = filtered_data.groupby(['month', 'product_category_name_english'])['order_id'].count().reset_index()

# Finding top three selling categories per month
top_selling_categories = monthly_category_sales.groupby('month').apply(lambda x: x.nlargest(3, 'order_id')).reset_index(drop=True)

# Visualize top categories per month
plt.figure(figsize=(12, 6))
sns.barplot(data=top_selling_categories, x='month', y='order_id', hue='product_category_name_english', palette='Set2')
plt.xlabel('Month')
plt.ylabel('Number of Sales')
plt.xticks(rotation=45)
plt.legend(title='Product Category')
st.pyplot(plt)

# Additional: Display raw data for more insights
if st.checkbox('Show Raw Data'):
    st.write(filtered_data)
