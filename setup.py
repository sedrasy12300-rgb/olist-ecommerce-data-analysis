import zipfile
import os
import shutil
import sqlite3 as sql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(BASE_DIR, "olist.zip")
db_final_name = "olist.db"
db_target_path = os.path.join(BASE_DIR, db_final_name)

print("⏳ جاري فك الضغط وفحص بنية الجداول...")

# 1. فك الضغط وتأمين المسارات
if os.path.exists(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(BASE_DIR)
            
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                if file.lower() == db_final_name.lower():
                    current_file_path = os.path.join(root, file)
                    if current_file_path != db_target_path:
                        shutil.move(current_file_path, db_target_path)

        if os.path.exists(db_target_path):
            shutil.copy(db_target_path, db_final_name)
            
            # 2. الخدعة السحرية: فحص أسماء الجداول وإصلاحها تلقائياً!
            conn = sql.connect(db_final_name)
            cursor = conn.cursor()
            
            # جلب أسماء كل الجداول الموجودة داخل ملفكِ حالياً
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 الجداول الموجودة في ملفكِ هي: {tables}")
            
            # إذا وجدتِ جدول المبيعات باسم مختلف أو بدون dataset، نقوم بنسخه للاسم الصحيح فوراً
            for t in tables:
                if "order" in t.lower() and t != "olist_orders_dataset":
                    try:
                        cursor.execute(f"CREATE TABLE IF NOT EXISTS olist_orders_dataset AS SELECT * FROM {t};")
                        conn.commit()
                        print(f"🔄 تم استنساخ الجدول {t} إلى الاسم الصحيح olist_orders_dataset ✅")
                    except Exception as e:
                        print(f"⚠️ فشل استنساخ الجدول: {e}")
            
            conn.close()
            print("🎯 تم الانتهاء من فحص وتأمين بنية الجداول بنجاح!")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء فك ومعالجة البيانات: {e}")
