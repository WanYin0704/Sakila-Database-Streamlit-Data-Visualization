import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import plotly.express as px 
import queries 
import altair as alt

# TASK 1: establish connection to MySQL
# You code starts here
conn = mysql.connector.connect(
    host='localhost',
    user='root', # put your username here
    password='W@nyin02', # put your password here
    database='sakila'
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

st.title('Sakila Data Exploration')
tab_overview, tab_sales, tab_film, tab_actor, tab_rentals = st.tabs(['Overview','Sales Dashboard','Film Dashboard','Actor Dashboard','Rental Dashboard'])

# ---------------------------------------------- Tab 1 ----------------------------------------------

with tab_overview:
    st.header('Overview')
    col11, col12, col13, col14,col15 = st.columns(5)
    
    with col11:
        st.metric('Total Customers (Active)',getOne_query(queries.query1, conn))
    with col12:
        st.metric('Total Store',getOne_query(queries.query2, conn))
    with col13:
        st.metric('Total Staff',getOne_query(queries.query3, conn))
    with col14:
        st.metric('Total Film',getOne_query(queries.query4, conn))
    with col15:
        st.metric('Total Actor',getOne_query(queries.query5, conn))
        
    col16,col17=st.columns(2)
    with col16:        
        st.subheader('Customer Counts by Store')
        customer_count_by_store=getMany_query(queries.query6, conn)
        # Check if 'store_id' column exists before displaying the data
        if not customer_count_by_store.empty:
            st.bar_chart(customer_count_by_store.set_index('store_id'))
        else:
            st.write('Error: Column "store_id" not found in the DataFrame.')
    
    with col17:
        st.subheader('Total Late Payment Customers by Film')
        total_late_cust=getMany_query(queries.query7, conn)
        if not total_late_cust.empty:
            st.bar_chart(total_late_cust, y='total_late_payment_cust', x='film_title', height=500)

    st.subheader('Total Late Payment Customer by Film Category')
    total_latepayment_cust=getMany_query(queries.query_total_late_cust, conn)
    if not total_latepayment_cust.empty:
        st.bar_chart(total_latepayment_cust, y='sum_late_payment_cust', x='category', height=500)
    
# ---------------------------------------------- Tab 2 ----------------------------------------------

with tab_sales:
    st.header('Sales Dashboard')
    
    col19,col20,col21= st.columns(3)
    
    with col19:
        total_sales = getOne_query(queries.query9, conn)
        st.metric('Total Sales', float(total_sales))
        
    with col20:
        late_payment_charge = getOne_query(queries.query8, conn)
        st.metric('Total Late Payment Charge Incurred', float(late_payment_charge))
    
    with col21:
        avg_sales = getOne_query(queries.query10, conn)
        st.metric('Average Daily Sales', float(avg_sales))
    
    col21,col22 = st.columns(2)
    
    with col21:
        st.subheader('Sales by Year')
        df = getMany_query(queries.query11, conn)
        df['annual_sales'] = pd.to_numeric(df['annual_sales'], errors='coerce')
        if not df.empty:
            st.bar_chart(df, y='annual_sales', x='year', height=500)

    with col22:
        st.subheader('Monthly Sales Distribution')
        df = getMany_query(queries.query21, conn)
        df['monthly_sales'] = pd.to_numeric(df['monthly_sales'], errors='coerce')
        if not df.empty:
            df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str)
            st.line_chart(df, y='monthly_sales', x='year_month', height=500)

           
    col23,col24=st.columns(2)
    
    with col23:
        st.subheader('Percentage of Sales by Category')
        df = getMany_query(queries.query31, conn)

        # Check if data is available
        if not df.empty:
            # Convert 'total_sales' to numeric
            df['total_sales_per_category'] = pd.to_numeric(df['total_sales_per_category'], errors='coerce')

            # Display pie chart
            fig = px.pie(df, names='name', values='total_sales_per_category')
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.write('No sales by category data available.')   
        
    with col24:
        st.subheader('Sales by Film Rating')

        df = getMany_query(queries.query41, conn)

        # Check if data is available
        if not df.empty:
            # Convert 'total_sales_by_rating' to numeric
            df['total_sales_by_rating'] = pd.to_numeric(df['total_sales_by_rating'], errors='coerce')

            # Create bar chart using Plotly Express
            fig = px.bar(df, x='rating', y='total_sales_by_rating')

            # Display bar chart
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No sales by film rating data available.')

    col33,col34=st.columns(2)
    
    with col33:
        st.subheader('Top 10 Sales by Country')
        df = getMany_query(queries.query42, conn)

        # Check if data is available
        if not df.empty:
            # Convert 'total_sales' to numeric
            df['total_sales_per_country'] = pd.to_numeric(df['total_sales_per_country'], errors='coerce')

            # Display pie chart
            fig = px.bar(df, x='total_sales_per_country', y='Country', color='Country')
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.write('No sales by Country data available.')   
   
        
    with col34:
        st.subheader('Sales by Country and City')
        df = getMany_query(queries.query43, conn)
        # Display filter for selecting a specific product
        selected_country = st.selectbox('Select Country:', df['country'].unique())

        # Filter the data based on the selected product
        filtered_data = df[df['country'] == selected_country]

        # Display line chart
        if not filtered_data.empty:
            st.subheader(f'Sales by Country and City for {selected_country}')
            filtered_data['total_sales_per_country'] = pd.to_numeric(filtered_data['total_sales_per_country'], errors='coerce')
            
            st.bar_chart(filtered_data.set_index('city')['total_sales_per_country'], use_container_width=True, color='#f77189')
        else:
            st.warning('No data available for the selected Country.') 

# ---------------------------------------------- Tab 3 ----------------------------------------------

with tab_film:
    st.header('Film Dashboard')
    # your code starts here
    col30,col31,col32,col33=st.columns(4)
    with col30:
        st.metric('Total Film Category',getOne_query(queries.queryF5, conn))
        
    with col31:    
        avg_length = getOne_query(queries.queryF4, conn)
        st.metric('Average Film Length', float(avg_length))
        
    with col32:
        st.metric('Film Language',getOne_query(queries.queryF6, conn))
        
        
    with col33:    
        st.metric('Film Release Year',getOne_query(queries.queryF9, conn))   
        
    col33,col34=st.columns(2)
    with col33:
        st.subheader('Film Counts by Film Category')
        df_category = getMany_query(queries.queryF7, conn)
        if not df_category.empty:
             st.bar_chart(df_category, y='num_film', x='category', height=500)
        else:
             st.write('No data, please insert query in queries.py')
        
    with col34:
        st.subheader('Top 10 Films by Rental Count')
        df_top_selling = getMany_query(queries.queryF8, conn)
        if not df_top_selling.empty:
            st.table(df_top_selling)
        else:
            st.write('No data, please insert query in queries.py')
    col35,col36=st.columns(2)  
    
    with col35:
        st.subheader('Film Counts by Special Features')
        df_special = getMany_query(queries.queryF11, conn)
        sort_order = st.selectbox("Sort the film _count", ["Ascending", "Descending"], index=1)

# Apply sorting based on user selection
        if sort_order == "Ascending":
            df_special=            df_special.sort_values(by='film_count', ascending=True)
        else:
            df_special = df_special.sort_values(by='film_count', ascending=False)
        
        if not df_special.empty:
            df_special
        else:
            st.write('No data, please insert query in queries.py')            
       
            
    with col36:
        st.subheader('Film Counts by Film Ratings')
        df_ratings = getMany_query(queries.queryF10, conn)
        if not df_ratings.empty:
            st.bar_chart(df_ratings, y='no_film', x='ratings', height=500)
        else:
            st.write('No data, please insert query in queries.py')            
            
        
        
        
# ---------------------------------------------- Tab 4 ----------------------------------------------

with tab_actor:
    st.header('Actor Dashboard')
    # your code starts here
    

    col11, col12 = st.columns(2)
    with col11:
        st.metric('Total Actors', getOne_query(queries.q2, conn))
    with col12:
        st.metric('Top Actor by Films', getOne_query(queries.q3, conn))
  
    
    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Top 10 Actor by Film Count')
        df = getMany_query(queries.q1, conn)
        if not df.empty:
            chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('film_count:Q', title='Number of Films'),
            y=alt.Y('actor_name:N', title='Actor Name', sort='-x')  # Sorting by film_count in descending order
            ).properties(width=600,height=400)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available")
            
    with col22:
        st.subheader('Actor Film Counts by Film Category') 
        df = getMany_query(queries.q4, conn)
        if not df.empty:
            chart = alt.Chart(df).mark_rect().encode(
            x='category_name:N',
            y='actor_name:N',
            color='film_count:Q'
            ).properties(width=600,height=400)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available")
            
    col2, col3 = st.columns(2)
    with col2:
        st.subheader('Top 5 Actors by Film Counts in Each Release Year')
        df = getMany_query(queries.q5, conn)
        if not df.empty:
            chart = alt.Chart(df).mark_point().encode(
            x='release_year:O',
            y='actor_name:N',
            size='film_count:Q',
            tooltip=['actor_name', 'release_year', 'film_count']
            ).properties(width=800,height=600)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available")
            
    with col3:
        st.subheader('Top 10 Actors by Average Film Length')
        df = getMany_query(queries.q6, conn) 
        if not df.empty:
            df.set_index('actor_name', inplace=True)
            st.bar_chart(df['avg_film_length'])
        else:
            st.write("No data available")

        
    st.subheader('Number of Actors per Film Category')
    df = getMany_query(queries.q7, conn)
    if not df.empty:
        st.bar_chart(data=df, x='category_name', y='actor_count')
    else:
        st.write("No data available")

            

# ---------------------------------------------- Tab 5 ----------------------------------------------
with tab_rentals:
    st.header('Rental Dashboard')

    # Data Exploration 1: Total Rental Counts
    col40, col41 = st.columns(2)
    with col40:
        total_rental = getOne_query(queries.queryR1, conn)
        st.metric('Total Rental Counts', float(total_rental))

    # Data Exploration 2: Average Rental Duration
    with col41:
        avg_rental_duration = getOne_query(queries.queryR2, conn)
        st.metric('Average Rental Duration', float(avg_rental_duration))

    # Data Exploration 3: Rentals by Category
    col42, col43 = st.columns(2)
    with col42:
        st.subheader('Rentals by Category')
        df_rental = getMany_query(queries.queryR3, conn)
        if not df_rental.empty:
             st.bar_chart(df_rental, y='rental_count', x='category', height=500, color='category')
    
    # Data Exploration 4: Rental Duration Distribution (Histogram)
    with col43:
        rental_duration_category_result = getMany_query(queries.rental_duration_category_query, conn)
        if not rental_duration_category_result.empty:
            df_rental_duration_category = pd.DataFrame(rental_duration_category_result)
            st.subheader('Rental Duration Distribution by Film Category')
            fig = px.bar(
            df_rental_duration_category, 
            x='category', 
            y='total_rental_duration',  
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data, please check your query or there is no data in the result.')
            

    # Data Exploration 5: Average Rental Rate by Category
    col44, col45 = st.columns(2)
    with col44:
        df_avg_rental = getMany_query(queries.queryR4, conn)
        if not df_avg_rental.empty:
            st.subheader('Average Rental Rate by Category')
            fig = px.line(df_avg_rental, x='category', y='avg_rental_rate')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data, please insert query in queries.py')

    # Data Exploration 6: Loyal Customers
    with col45:
        repeat_rental_customers_with_names = getMany_query(queries.queryR5, conn)
        if not repeat_rental_customers_with_names.empty:
            st.subheader('Top 10 Loyal Customers')
            st.table(repeat_rental_customers_with_names)

   
    col46, col47 = st.columns(2)
    # Data Exploration 7: Distribution of Rental Counts by Store
    with col46:
        st.subheader('Distribution of Rental Counts by Store')
        df_rental_store = getMany_query(queries.queryR6, conn)
        if not df_rental_store.empty:
            fig = px.pie(df_rental_store, names='store', values='rental_count')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data, please insert query in queries.py')
      
     # Data Exploration 8:Rental Counts by Language    
    with col47:
        df_rental_by_language = getMany_query(queries.queryR7, conn)
        st.subheader('Rental Counts by Language')
        if not df_rental_by_language.empty:
            st.bar_chart(df_rental_by_language, x='language', y='rental_count', height=500)
        else:
            st.write('No data, please check your query or there is no data in the result.')
            
    col48, col49 = st.columns(2)
    
    # Data Exploration 9: Renting Films by Rental Rate
    with col48:
        df_top_rented_films_by_rate = getMany_query(queries.queryR8, conn)
        st.subheader('Renting Films by Rental Rate')
        if not df_top_rented_films_by_rate.empty:
            fig = px.line(df_top_rented_films_by_rate, x='film_title', y='avg_rental_rate')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data, please insert query in queries.py')
   
     #Data Exploration 10: Rental Revenue Over Time
    with col49:
        df_rental_revenue = getMany_query(queries.queryR9, conn)
        st.subheader('Rental Revenue Over Time')
        if not df_rental_revenue.empty:
            df_rental_revenue['rental_date'] = pd.to_datetime(df_rental_revenue['rental_date'])
            fig = px.line(df_rental_revenue, x='rental_date', y='revenue')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data, please check your query or there is no data in the result.')

