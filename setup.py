import zipfile
import os
import pandas as pd
import sqlite3 as sql

# 1. تحديد المسارات المطلقة بدقة على السيرفر لمنع التضارب
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(BASE_DIR, "olist.zip")
db_path = os.path.join(BASE_DIR, "olist.db")

print("⏳ جاري تهيئة قاعدة البيانات على السيرفر...")

# --- الجزء الأول: فك الضغط إذا كان ملف الـ zip موجوداً ---
if os.path.exists(zip_path) and not os.path.exists(db_path):
    print("📦 تم العثور على ملف olist.zip، جاري فك الضغط الآن...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(BASE_DIR)
        print("✅ تم فك ضغط ملف olist.db بنجاح!")
    except Exception as e:
        print(f"❌ فشل فك الضغط: {e}")

# --- الجزء الثاني: الحل الاحتياطي (إذا لم يجد الـ zip أو فشل فك الضغط، يبني من الـ CSV) ---
if not os.path.exists(db_path):
    print("⏳ ملف الـ zip غير موجود أو تالف، جاري بناء الجداول من ملفات CSV الحية...")
    try:
        conn = sql.connect(db_path)
        
        # قراءة الـ CSV
        orders_df = pd.read_csv(os.path.join(BASE_DIR, "olist_orders_dataset.csv"))
        payments_df = pd.read_csv(os.path.join(BASE_DIR, "olist_order_payments_dataset.csv"))
        products_df = pd.read_csv(os.path.join(BASE_DIR, "olist_products_dataset.csv"))
        order_items_df = pd.read_csv(os.path.join(BASE_DIR, "olist_order_items_dataset.csv"))
        translation_df = pd.read_csv(os.path.join(BASE_DIR, "product_category_name_translation.csv"))
        
        # ضخ الجداول بالأسماء الصحيحة المطابقة لكود app.py
        orders_df.to_sql("olist_orders_dataset", conn, if_exists="replace", index=False)
        payments_df.to_sql("olist_order_payments_dataset", conn, if_exists="replace", index=False)
        products_df.to_sql("olist_products_dataset", conn, if_exists="replace", index=False)
        order_items_df.to_sql("olist_order_items_dataset", conn, if_exists="replace", index=False)
        translation_df.to_sql("product_category_name_translation", conn, if_exists="replace", index=False)
        
        conn.close()
        print("✅ تم بناء قاعدة البيانات من ملفات CSV بنجاح 100%!")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء قراءة الـ CSV أو بناء الجداول: {e}")
else:
    print("🎯 قاعدة البيانات olist.db جاهزة ومليئة بالجداول الآن!")
