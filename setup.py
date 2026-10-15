import zipfile
import os

# 1. تحديد المسارات المطلقة لمنع أخطاء السيرفر في التوجيه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(BASE_DIR, "olist.zip")
db_path = os.path.join(BASE_DIR, "olist.db")

print("⏳ جاري التحقق من ملف قاعدة البيانات المضغوط على السيرفر...")

# 2. فك الضغط تلقائياً إذا كان ملف الـ zip موجوداً وملف الـ db غير موجود
if os.path.exists(zip_path) and not os.path.exists(db_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # فك الملف مباشرة في المجلد الرئيسي للمشروع
            zip_ref.extractall(BASE_DIR)
        print("✅ تم فك ضغط ملف olist.db بنجاح على السيرفر!")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء فك الضغط: {e}")
else:
    print("🔔 ملف olist.db جاهز وموجود بالفعل، أو ملف olist.zip غير متوفر.")
