import zipfile
import os
import shutil

# 1. تحديد المسارات المطلقة بدقة على السيرفر
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(BASE_DIR, "olist.zip")

# المسار المطلق والمسار المحلي المتوقع لكود app.py الأصلي
db_absolute_path = os.path.join(BASE_DIR, "olist.db")
db_local_path = "olist.db"

print("⏳ جاري تهيئة قاعدة البيانات وفك الضغط الجذري...")

# 2. فك ضغط ملف olist.zip إذا كان موجوداً
if os.path.exists(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(BASE_DIR)
        print("✅ تم فك الملف بنجاح في المسار المطلق.")
        
        # 3. الخدعة السحرية: نسخ الملف المفكوك إلى المسار المحلي الذي يبحث عنه كود app.py
        if os.path.exists(db_absolute_path):
            shutil.copy(db_absolute_path, db_local_path)
            print("🎯 تم تأمين قاعدة البيانات وتطابق المسارات بنجاح!")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")
else:
    print("🔔 ملف olist.zip غير متوفر في المستودع.")
