import zipfile
import os
import shutil

# 1. تحديد المسارات المطلقة بدقة على السيرفر لضمان المزامنة
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(BASE_DIR, "olist.zip")
db_final_name = "olist.db"
db_target_path = os.path.join(BASE_DIR, db_final_name)

print("⏳ جاري تنفيذ المعالجة الجذرية لملف قاعدة البيانات...")

# 2. فك الضغط وفحص المحتويات بالكامل
if os.path.exists(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # فك الضغط مباشرة في المجلد الرئيسي
            zip_ref.extractall(BASE_DIR)
            
            # فحص إذا كان الملف قد فُك داخل مجلد فرعي بالخطأ ونقله للمسار الرئيسي
            for root, dirs, files in os.walk(BASE_DIR):
                for file in files:
                    if file.lower() == db_final_name.lower():
                        current_file_path = os.path.join(root, file)
                        if current_file_path != db_target_path:
                            shutil.move(current_file_path, db_target_path)

        # 3. الخدعة السحرية: نسخ الملف إلى المجلد الحالي النسبي الذي يبحث عنه كود app.py الأصلي
        if os.path.exists(db_target_path):
            shutil.copy(db_target_path, db_final_name)
            print("🎯 تم تأمين وتطابق مسارات قاعدة البيانات بنجاح 100%!")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء فك ومعالجة البيانات: {e}")
else:
    print("🔔 ملف olist.zip غير متوفر في المستودع حالياً.")
