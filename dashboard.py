import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import plotly.express as px 
import queries 

# TASK 1: establish connection to MySQL
# You code starts here
conn = mysql.connector.connect(
    host='localhost',
    user='root', # put your username here
    password='W@nyin02', # put your password here
    database='bikestore'
)

# Use this function to get scalar values from MySQL
# To use the function, pass in the query variable and connection object.
def getOne_query(query,conn):
    if query != '':
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return list(result)[0]
    else:
        return '--'

# Use this function to get dataframe from MySQL for ploting OR display of lists
# To use the function, pass in the query variable and connection object.
def getMany_query(query, conn):
    if query != '':
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=cursor.column_names)
        cursor.close()
    else:
        result = pd.DataFrame()
    return result

st. set_page_config(layout="wide")

st.title('Bikestore Data Exploration')
tab_overview, tab_customers, tab_staff, tab_items, tab_orders = st.tabs(['Overview','Customers Dashboard','Staff Dashboard','Item Dashboard','Orders Dashboard'])

# ---------------------------------------------- Tab 1 ----------------------------------------------

with tab_overview:
    st.header('Overview')
    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.metric('Total Customers',getOne_query(queries.queryT1, conn))
    with col12:
        st.metric('Total Products', getOne_query(queries.queryT2, conn))
    with col13:
        st.metric('Total Stores', getOne_query(queries.queryT3, conn))
    with col14:
        st.metric('Total Orders', getOne_query(queries.queryT4, conn))

    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Total Orders by Year')
        df = getMany_query(queries.queryT5, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='no_of_orders', x='year', height=500)

    with col22:
        st.subheader('Distribution of Orders by Store')
        df = getMany_query(queries.queryT6, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='no_of_orders', x='store', height=500)

# ---------------------------------------------- Tab 2 ----------------------------------------------

with tab_customers:
    st.header('Customer Dashboard')

    # Total number of customers
    total_customers = getOne_query(queries.queryT1, conn)
    st.metric('Total Customers', total_customers)

    # Categorize customers into One-Time or Recurring
    df_customer_category = getMany_query(queries.query_customer_category, conn)
    st.subheader('Customer Counts by Customer Categories')

    if not df_customer_category.empty in df_customer_category.columns:
        st.bar_chart(df_customer_category, x='customer_category', y='customer_count', height=500)
    else:
        st.warning('No data available.')
        
    # List of recurring customers and their corresponding sales
    df_recurring_customers = getMany_query(queries.query_recurring_customers, conn)
    st.subheader('Recurring Customers and Sales')
    st.table(df_recurring_customers)

    # List of top 10 customers who spent the most
    df_top_spenders = getMany_query(queries.query_top_spenders, conn)
    st.subheader('Top 10 Customers by Spending')
    st.table(df_top_spenders)


    
    

# ---------------------------------------------- Tab 3 ----------------------------------------------

with tab_staff:
    st.header('Staff Dashboard')
    # your code starts here
    col11, col12= st.columns(2)
    with col11:
        df_staff_data = getMany_query(queries.queryO4, conn)

        # Check if the result is not empty
        if not df_staff_data.empty:
            # Display bar chart for total staff by store
            st.subheader('Total Staff by Store')

            # Bar chart for Total Staff
            st.bar_chart(df_staff_data.set_index('store_name'))

        else:
            st.write('No data available.')
    with col12:
        df_staff_data = getMany_query(queries.queryO5, conn)

        # Check if the result is not empty
        if not df_staff_data.empty:
            # Display total customers, total staff, and customer-to-staff ratio in a table
            st.subheader('Staff Metrics by Store')
            st.table(df_staff_data)
            
            fig = px.pie(df_staff_data, names='store_name', values='customer_staff_ratio', title='Pie Chart: Customer-Staff Ratio')
            # Create a pie chart for the customer-staff ratio
            st.subheader('Pie Chart: Customer-Staff Ratio')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available.')
            
    
    df_staff_data = getMany_query(queries.queryO6, conn)

    # Check if the result is not empty
    if not df_staff_data.empty:
        df_staff_data['order_year'] = pd.to_datetime(df_staff_data['YEAR(o.order_date)'], format='%Y').dt.year
        # Display total customers, total staff, and customer-to-staff ratio in a table
        st.subheader('Staff Metrics by Store and Year')
        st.table(df_staff_data)
        
        col1, col2, col3 = st.columns(3)
        grouped_by_year = df_staff_data.groupby('order_year')
        for year, group in grouped_by_year:
            fig = px.pie(group, names='store_name', values='customer_staff_ratio', title=f'Pie Chart for {year}: Customer-Staff Ratio')
            if year == 2016:
                col1.subheader(f'Pie Chart for {year}: Customer-Staff Ratio')
                col1.plotly_chart(fig, use_container_width=True)
            elif year == 2017:
                col2.subheader(f'Pie Chart for {year}: Customer-Staff Ratio')
                col2.plotly_chart(fig, use_container_width=True)
            elif year == 2018:
                col3.subheader(f'Pie Chart for {year}: Customer-Staff Ratio')
                col3.plotly_chart(fig, use_container_width=True)            
    else:
        st.write('No data available.')




# ---------------------------------------------- Tab 4 ----------------------------------------------

with tab_items:
    st.header('Item Dashboard')
    # your code starts here
    total_products_brands = getMany_query(queries.queryP1, conn)

    # Task 1: Total number of products and brands
    if not total_products_brands.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric('Total Products',total_products_brands['total_products'].iloc[0])
            
        with col2:
            st.metric('Total Brands',total_products_brands['total_brands'].iloc[0])

    else:
        st.warning('Error retrieving total products and brands.')
        
    col32, col33 = st.columns(2)
    with col32:
        st.subheader('Distribution of Products by Brands')
        major_brands = getMany_query(queries.queryP2, conn)
        if not major_brands.empty:
            st.bar_chart(major_brands, y='product_count', x='brand_name', height=500)
        else:
            st.warning('No data available.')
            
    with col33:
        st.subheader('Item Price Categorization')
        price_category= getMany_query(queries.queryP4, conn)
        if not price_category.empty:
            st.dataframe(price_category) 
        else:
            st.warning('No data available.')

    col33,col34, col35 = st.columns(3)  
    with col33:
        df_product_count = getMany_query(queries.query_no_item_category, conn)
        # Display the pie chart
        st.subheader('Product Counts by Price Category')
        if not df_product_count.empty:
            fig = px.pie(df_product_count, values='product_count', names='price_category')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning('No data available.')
            
    with col34:
        st.subheader('Brands with the Most Sales and Top-Selling Product')
        brands_most_sales = getMany_query(queries.queryP3, conn)
        if not brands_most_sales.empty:
            st.dataframe(brands_most_sales)
        else:
            st.warning('No data available.')
    
    with col35:
        st.subheader('Top 5 Highest Sales Items by Price Category')
        low_priced_items = getMany_query(queries.queryLow, conn)
        medium_priced_items = getMany_query(queries.queryMed, conn)
        high_priced_items = getMany_query(queries.queryHigh, conn)

            # Display filter cards for each category
        category_filter = st.selectbox('Select Price Category', ['Low-priced', 'Medium-priced', 'High-priced'])

        if category_filter == 'Low-priced':
            st.dataframe(low_priced_items)
        elif category_filter == 'Medium-priced':
            st.dataframe(medium_priced_items)
        elif category_filter == 'High-priced':
            st.dataframe(high_priced_items)

# ---------------------------------------------- Tab 5 ----------------------------------------------

with tab_orders:
    st.header('Sales Order Dashboard')
    # your code starts here
    # Assuming getOne_query returns a decimal
    
    total_sales_decimal = getOne_query(queries.queryO1, conn)

    # Format the decimal as a string with a specific number of decimal places
    formatted_total_sales = f"{total_sales_decimal:.2f}"

    # Display the formatted total sales in the st.metric widget
    st.metric('Total Sales', formatted_total_sales)

    # Task 2: Display Sales by Product and Year
    col21, col22 = st.columns(2)
    with col21:    
        st.subheader('Sales by Year and Product')
        df = getMany_query(queries.queryS2, conn)
        # Display filter for selecting a specific product
        selected_product = st.selectbox('Select Product:', df['product_name'].unique())

        # Filter the data based on the selected product
        filtered_data = df[df['product_name'] == selected_product]

        # Display line chart
        if not filtered_data.empty:
            st.subheader(f'Sales by Year and Product for {selected_product}')
            filtered_data['product_sales'] = pd.to_numeric(filtered_data['product_sales'], errors='coerce')
            st.bar_chart(filtered_data.set_index('year')['product_sales'])
        else:
            st.warning('No data available for the selected product. Please choose another product.')

    # Task 2: Display Sales by Year
    with col22:
        st.subheader('Sales by Year')
        df_sales_by_year = getMany_query(queries.query_sale_by_year, conn)
        if not df_sales_by_year.empty:
            fig = px.line(df_sales_by_year, x='year', y='total_sales')
            st.plotly_chart(fig, use_container_width=True)   
        else:
            st.write('No data available.')
        
    # Task 3: Display Product with the Highest Sales
    st.subheader('Product with the Highest Sales')
    highest_sales_product_data = getMany_query(queries.queryO3, conn)

    if not highest_sales_product_data.empty:
        # Display the information in a table
        st.table(highest_sales_product_data)
    else:
        st.write('No data available.')
