import pandas as pd
import sqlite3 as sq
import matplotlib.pyplot as plt


orders_df =pd.read_csv("olist_orders_dataset.csv")
order_items_df =pd.read_csv("olist_order_items_dataset.csv")
products_df=pd.read_csv("olist_products_dataset.csv")
payments_df=pd.read_csv("olist_order_payments_dataset.csv")
reviews_df=pd.read_csv("olist_order_reviews_dataset.csv")
translation_df=pd.read_csv("product_category_name_translation.csv")
customers_df =pd.read_csv("olist_customers_dataset.csv")

# Load datasets

conn =sq.connect("olist.db")

# Database Connection

customers_df.to_sql("olist_customers_dataset",conn,if_exists="replace",index=False)
orders_df.to_sql("olist_orders_dataset",conn,if_exists="replace",index=False)
payments_df.to_sql("olist_order_payments_dataset",conn,if_exists="replace",index=False)
products_df.to_sql("olist_products_dataset",conn,if_exists="replace",index=False)
order_items_df.to_sql("olist_order_items_dataset",conn,if_exists="replace",index=False)
translation_df.to_sql("product_category_name_translation",conn,if_exists="replace",index=False)
reviews_df.to_sql("olist_order_reviews_dataset",conn,if_exists="replace",index=False)



print(pd.read_sql_query("""SELECT order_status ,COUNT(*) AS order_count, COUNT(*) *100.0 /(SELECT COUNT(*)
  FROM olist_orders_dataset) AS percentage FROM olist_orders_dataset GROUP BY order_status""",conn ))

print(pd.read_sql_query("""SELECT payment_type,SUM(payment_value) AS total_payment
FROM olist_order_payments_dataset GROUP BY payment_type""",conn))

print(pd.read_sql_query(""" SELECT payment_type ,AVG(payment_value) AS avg_payment 
FROM olist_order_payments_dataset GROUP BY payment_type""",conn))

print(pd.read_sql_query(""" SELECT AVG(sum_payment) AS avg_order_value 
FROM (
SELECT order_id ,SUM(payment_value) AS sum_payment FROM olist_order_payments_dataset
GROUP BY order_id ) AS order_totals

 """,conn))
print(pd.read_sql_query(""" SELECT payment_type, AVG(sum_payment_value) AS avg_order_value
 FROM (
SELECT order_id ,payment_type ,SUM(payment_value) AS sum_payment_value
FROM olist_order_payments_dataset 
GROUP BY order_id , payment_type ) AS totals
GROUP BY payment_type  """,conn))

print(pd.read_sql_query("""SELECT customer_unique_id , MAX(order_count)
FROM (
SELECT olist_customers_dataset.customer_unique_id , COUNT(*) AS order_count
FROM olist_orders_dataset 
JOIN olist_customers_dataset 
ON olist_orders_dataset.customer_id = olist_customers_dataset.customer_id 
GROUP BY  olist_customers_dataset.customer_unique_id 

) AS totals

""",conn))

print(pd.read_sql_query("""
SELECT olist_customers_dataset.customer_unique_id , COUNT(*) 
FROM olist_orders_dataset 
JOIN olist_customers_dataset 
ON olist_orders_dataset.customer_id = olist_customers_dataset.customer_id 
GROUP BY  olist_customers_dataset.customer_unique_id 
HAVING COUNT(*) >16
""",conn))

print(pd.read_sql_query("""SELECT ROUND( COUNT(*) *100.0 /( SELECT COUNT(DISTINCT customer_unique_id) 
FROM olist_customers_dataset) ,2)  AS repeat_customer_percentage
FROM (SELECT olist_customers_dataset.customer_unique_id , COUNT(*) 
FROM olist_orders_dataset 
JOIN  olist_customers_dataset
ON olist_orders_dataset.customer_id = olist_customers_dataset.customer_id 
GROUP BY customer_unique_id
HAVING COUNT(*) >1
) AS repeat_customers

 """,conn))

print(pd.read_sql_query(""" SELECT order_status , AVG(sum_payment_value) AS avg_order_value
 FROM (
SELECT  order_status , olist_order_payments_dataset.order_id , SUM(payment_value) AS sum_payment_value
FROM olist_orders_dataset
JOIN olist_order_payments_dataset
ON  olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
GROUP BY olist_order_payments_dataset.order_id , order_status

) AS total
GROUP BY order_status
 """,conn))


monthly_sales =pd.read_sql_query("""SELECT strftime('%Y-%m', order_purchase_timestamp) AS month_order ,SUM(payment_value) AS total_sales
FROM  olist_orders_dataset
JOIN olist_order_payments_dataset
ON olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
GROUP BY month_order ORDER BY month_order ASC""",conn)


print(pd.read_sql_query("""SELECT strftime('%Y', order_purchase_timestamp) AS year_order ,SUM(payment_value)
FROM  olist_orders_dataset
JOIN olist_order_payments_dataset
ON olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
GROUP BY year_order ORDER BY SUM(payment_value) DESC""",conn))


print(pd.read_sql_query("""SELECT olist_products_dataset.product_category_name 
,product_category_name_translation.product_category_name_english
,SUM(price) AS total_sales
FROM olist_products_dataset
JOIN olist_order_items_dataset
ON olist_products_dataset.product_id = olist_order_items_dataset.product_id
JOIN product_category_name_translation
ON olist_products_dataset.product_category_name = product_category_name_translation.product_category_name
GROUP BY  olist_products_dataset.product_category_name ORDER BY total_sales DESC""",conn))


print(pd.read_sql_query("""SELECT olist_products_dataset.product_category_name ,
product_category_name_translation.product_category_name_english
,AVG(price) AS avg_price
FROM olist_products_dataset
JOIN olist_order_items_dataset
ON olist_products_dataset.product_id = olist_order_items_dataset.product_id
JOIN product_category_name_translation
ON olist_products_dataset.product_category_name = product_category_name_translation.product_category_name
GROUP BY  olist_products_dataset.product_category_name ORDER BY avg_price DESC""",conn))


print(pd.read_sql_query("""SELECT product_category_name , AVG(review_score) AS avg_review_score
FROM olist_order_reviews_dataset 
JOIN  olist_orders_dataset 
ON olist_order_reviews_dataset.order_id = olist_orders_dataset.order_id 
JOIN olist_order_items_dataset
ON olist_orders_dataset.order_id  =  olist_order_items_dataset.order_id 
JOIN olist_products_dataset
ON olist_order_items_dataset.product_id = olist_products_dataset.product_id
GROUP BY product_category_name """,conn))

# Visualizations

plt.plot(monthly_sales["month_order"],monthly_sales["total_sales"])
plt.xticks(rotation=45)
plt.xlabel("Month")

plt.ylabel("Sales")
plt.title("Monthly sales")
plt.show()

order_status =pd.read_sql_query("""SELECT order_status , COUNT(*) AS order_count
FROM olist_orders_dataset  
GROUP BY order_status""",conn)



plt.bar(order_status["order_status"],order_status["order_count"])
plt.xlabel("Order Status")
plt.ylabel("Order Count")
plt.title("Order Status Distribution")
plt.show()

product =pd.read_sql_query("""SELECT product_category_name ,SUM(price) AS total_sales
FROM olist_order_items_dataset
JOIN olist_products_dataset
ON olist_order_items_dataset.product_id =olist_products_dataset.product_id 
GROUP BY product_category_name ORDER BY total_sales DESC 
LIMIT 10""",conn)



plt.bar(product["product_category_name"],product["total_sales"])
plt.xticks(rotation=45)
plt.xlabel("product_category_name")
plt.ylabel("total_sales")
plt.title("Top 10 Product Categories by Sales")
plt.show()

