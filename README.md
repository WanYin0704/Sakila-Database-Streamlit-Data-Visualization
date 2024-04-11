# Streamlit-Data-Visualization
Welcome to the World of Exploring Bikestore Database and Analyzing Sakila Database! **Streamlit**, a Python package designed for building interactive web applications, is utilised in this project to query data from both database and visualise them with appropriate visualisations. 

 ## Bikestore Database
The bikestore database includes records for customers, merchandise, employees, and sales orders, and it is designed to resemble a hypothetical bike shop. There are overall five main dashboards that we have created to provide comprehensive insights into various aspects of the bike store's operations. 

a) **Overview:**: Provides a general snapshot of the store's operations, covering key metrics related to customers, products, stores, and orders.

b) **Sales Order Dashboard:** This dashboard focuses on analyzing sales data, including total sales recorded, sales by year and by product, and identifying the top-selling products.

c) **Customer Dashboard:** Centered on customer analysis, this dashboard includes metrics such as total customer count, categorizing customers as One-Time or Recurring based on order frequency, and identifying top-spending customers.

d) **Item Dashboard:** Analyzing product data, this dashboard includes insights such as total products and brands, major brands and product distribution, sales by brand, and categorizing products based on price range.

e) **Staff Dashboard:** Focused on staff analysis, this dashboard includes metrics such as total staff count per store, customer-to-staff ratio for each store and by year.

## Sakila Database
The Sakila database includes a detailed set of tables representing a fictional DVD rental store, encompassing data related to films, customers, rentals, and staff. We explored the Sakila database, analyzed its data, and created interactive dashboards with our main focus on understanding the dynamics of a DVD rental business. Our analysis comprises:

a) **Overview:** Provides a summary of total customers, stores, staff, films, and actors, along with customer counts by store and total late payment customers by film.

b) **Sales Dashboard:** Analyzes total sales, late payment charges incurred, average daily sale, sales by year and month, percentage of sales by category, sales by film rating, and top 10 sales by country and city. This dashboard focusing on sales-related metrics delivers insightful information into the store's revenue generation and sales trends.

c) **Film Dashboard:** Presents information regarding the film catalog, including total films, average film length, film language, film release year, film counts by categories, the top 10 films by rental count, film counts by special features, and film counts by film ratings. This dashboard was presented with the major aim of understanding the film inventory and popularity among customers.

d) **Actor Dashboard:** highlights metrics connected to actors, such as total actors, top actors by film, top 10 actors by count, actor film counts by category, top 5 actors by count in 2006, top 10 actors by average duration of film, and the number of actors in each category of films. It provides information about the performers' contributions to the popularity of films and consumer preferences.

e)  **Rental Analysis:** Provides insights into rental-related metrics, including total rental counts, average rental duration, rentals by category, rental duration distribution by film category, average rental rate by category, top 10 loyal customers, distribution of rental counts by store, rental counts by language, renting films by rental rate, and rental revenue over time. This dashboard aids in understanding rental patterns and customer behavior.

### Files 
- [queries.py](queries.py): This Python script contains all the SQL queries used to extract data from the bikestore and Sakila databases.
- [dashboard.py](dashboard.py): This Python script is responsible for creating interactive Streamlit dashboards to visualize insights from the bikestore database.
- [dashboard_sakila.py](dashboard_sakila.py): This Python script creates Streamlit dashboards to analyze and visualize data from the Sakila database.
