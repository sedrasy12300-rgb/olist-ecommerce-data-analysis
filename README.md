Olist E-Commerce Data Analysis

Project Overview

This project explores e-commerce data from Olist using Python, SQL, and data visualization tools.

The project uses SQLite to store and query the datasets, Pandas to process the data, Matplotlib to create visualizations,
and Streamlit to build an interactive dashboard.

Tools and Technologies

Python

SQL

SQLite

Pandas

Matplotlib

Streamlit

Project Structure

olist-ecommerce-analysis/

│
├── app.py                  # Streamlit dashboard

├── analysis.py             # Data preparation, SQL queries, and visualizations

├── olist.db                # SQLite database

├── requirements.txt        # Python dependencies

├── .streamlit/

│   └── config.toml         # Streamlit theme configuration

└── README.md               # Project documentation

Data Analysis

The project includes exploratory data analysis using SQL queries and Python.

The analysis covers:

Order Analysis: Examining order statuses and their distribution.

Sales Analysis: Analyzing monthly and yearly sales using payment data.

Payment Analysis: Comparing payment types and their total and average values.

Customer Analysis: Exploring repeat customers and order frequency.

Product Analysis: Identifying product categories with high total sales and examining average prices.

Review Analysis: Exploring average review scores across product categories.

Interactive Dashboard

The Streamlit dashboard presents key metrics and interactive analyses.

Key Metrics

Total Orders

Total Sales

Unique Customers

Dashboard Sections

Order Status Analysis

Monthly Sales Analysis

Top 10 Product Categories by Sales

Payment Analysis

Payment Usage Analysis

The dashboard uses tables and charts to make the results easier to explore.

It also includes a warning about potentially incomplete data for September 2016 and October 2018,
as the dataset starts and ends during these months.

Database

The project uses SQLite to store the Olist datasets in a database named olist.db.

The database contains tables for:

Orders
Customers
Payments
Products
Order Items
Product Category Translations
Reviews
Installation and Setup
1. Install the Dependencies
2. 
Open a terminal in the project directory and run:
pip install -r requirements.txt
3. Prepare the Database
4. 
Make sure olist.db is available in the project directory.
If you need to recreate the database,
place the original CSV datasets in the appropriate location and run the data preparation script.
6. Run the Dashboard
7. 
Run the following command:

streamlit run app.py

Then open the local URL displayed in the terminal.

Project Goal

The goal of this project is to practice SQL-based data analysis,
work with a relational database, explore e-commerce data,
and present the results through an interactive dashboard.
Notes
The dashboard requires olist.db to run.
The original CSV datasets are needed to recreate the database from the source data.
The data preparation and exploratory analysis script is separate from the Streamlit dashboard.
