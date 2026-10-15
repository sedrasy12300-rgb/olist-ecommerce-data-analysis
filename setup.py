import pandas as pd
import sqlite3 as sql
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "olist.db")

print("⏳ البدء في بناء قاعدة البيانات والجداول من ملفات CSV الحية...")

try:
    # 1. فتح اتصال مباشر لبناء ملف olist.db نظيف ومليء بالبيانات
    conn = sql.connect(db_path)
    
    # 2. قراءة ملفات الـ CSV المرفوعة في مستودع GitHub الخاص بكِ
    # تأكدي أن هذه الملفات مرفوعة بالفعل على حسابك بنفس هذه الأسماء تماماً
    orders_df = pd.read_csv(os.path.join(BASE_DIR, "olist_orders_dataset.csv"))
    payments_df = pd.read_csv(os.path.join(BASE_DIR, "olist_order_payments_dataset.csv"))
    products_df = pd.read_csv(os.path.join(BASE_DIR, "olist_products_dataset.csv"))
    order_items_df = pd.read_csv(os.path.join(BASE_DIR, "olist_order_items_dataset.csv"))
    translation_df = pd.read_csv(os.path.join(BASE_DIR, "product_category_name_translation.csv"))
    
    # 3. ضخ البيانات وإنشاء الجداول بالأسماء الصحيحة والمطابقة تماماً لكود app.py
    orders_df.to_sql("olist_orders_dataset", conn, if_exists="replace", index=False)
    payments_df.to_sql("olist_order_payments_dataset", conn, if_exists="replace", index=False)
    products_df.to_sql("olist_products_dataset", conn, if_exists="replace", index=False)
    order_items_df.to_sql("olist_order_items_dataset", conn, if_exists="replace", index=False)
    translation_df.to_sql("product_category_name_translation", conn, if_exists="replace", index=False)
    
    conn.close()
    print("✅ تم بناء قاعدة البيانات والجداول بنجاح 100%!")

except Exception as e:
    print(f"❌ حدث خطأ أثناء قراءة الـ CSV أو بناء الجداول: {e}")
