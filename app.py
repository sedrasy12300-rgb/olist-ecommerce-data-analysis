import streamlit as st
import pandas as pd
import sqlite3 as sql
import os
import kagglehub

dataset_path = kagglehub.dataset_download(
    "olistbr/brazilian-ecommerce"
)


st.write("Dataset files:")
st.write(os.listdir(dataset_path))

st.title("Olist E-Commerce Data Analysis")
st.write("""This application provides insights into Olist e-commerce data
, including orders, sales, customers, products, payments, and reviews.""")

conn =sql.connect("olist.db")
query ="""SELECT COUNT(*) AS total_orders FROM olist_orders_dataset """
result =pd.read_sql_query(query,conn)

total_sales =(pd.read_sql_query("""SELECT SUM(payment_value) AS total_sales
FROM olist_order_payments_dataset """,conn))

payment_data =(pd.read_sql_query("""SELECT payment_type,SUM(payment_value) AS total_payment
FROM olist_order_payments_dataset GROUP BY payment_type""",conn))

unique_customers =pd.read_sql_query(""" SELECT COUNT(DISTINCT customer_unique_id) AS unique_customers  FROM olist_customers_dataset
""",conn)


st.subheader("Key Metrics")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric( "Total Orders",
    result["total_orders"].iloc[0])
with col2:
    st.metric("total Sales".title(),
      f"""{total_sales["total_sales"].iloc[0]:,.2f}""")
with col3:
    st.metric("Unique Customers",
     unique_customers["unique_customers"].iloc[0])


order_status =pd.read_sql_query("""SELECT order_status , COUNT(*) AS order_count
FROM olist_orders_dataset  
GROUP BY order_status""",conn)


monthly_sales =pd.read_sql_query("""SELECT strftime('%Y-%m', order_purchase_timestamp) AS month_order ,SUM(payment_value) AS total_sales
FROM  olist_orders_dataset
JOIN olist_order_payments_dataset
ON olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
GROUP BY month_order ORDER BY month_order ASC""",conn)

product =pd.read_sql_query("""SELECT  
product_category_name_translation.product_category_name_english 
,SUM(price) AS total_sales
FROM olist_order_items_dataset
JOIN olist_products_dataset
ON olist_order_items_dataset.product_id =olist_products_dataset.product_id 
JOIN product_category_name_translation
ON olist_products_dataset.product_category_name = product_category_name_translation.product_category_name
GROUP BY product_category_name_translation.product_category_name_english  ORDER BY total_sales DESC 
LIMIT 10""",conn)


payment_usage_analysis =pd.read_sql_query("""SELECT payment_type, COUNT(*) AS payment_total 
FROM olist_order_payments_dataset
GROUP BY  payment_type""",conn)

selected_analysis =st.selectbox("what data do you want ? ".title(),["Order Status","monthly sales".title(),"Product","Payment Analysis","payment usage analysis".title()])

if selected_analysis =="Order Status":
     
    st.subheader("Order Status Analysis")
    st.dataframe(order_status)
    st.bar_chart(order_status, x="order_status",y="order_count")
elif selected_analysis == "monthly sales".title():
     
    st.subheader("Monthly Sales Analysis")

    st.dataframe(monthly_sales)

    st.line_chart(monthly_sales,x="month_order",y="total_sales")
    st.warning("""Note: Sales data for September 2016 and October 2018 may be incomplete
        because the dataset starts and ends during these months.
        Interpret the sales figures for these periods with caution.""")
elif selected_analysis == "Product": 
    st.subheader("Top 10 Product Categories by Sales")
    st.dataframe(product)
    st.bar_chart(product,x="product_category_name_english",y="total_sales")
elif selected_analysis == "Payment Analysis":
     st.subheader("Payment Analysis")
     st.dataframe(payment_data)
     st.bar_chart(payment_data, x="payment_type",y="total_payment")
elif selected_analysis =="payment usage analysis".title():
     st.subheader("Payment Usage Analysis")
     st.dataframe(payment_usage_analysis)
     st.bar_chart(payment_usage_analysis,x="payment_type",y="payment_total")



