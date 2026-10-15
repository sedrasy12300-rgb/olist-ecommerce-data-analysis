import zipfile
import os

if os.path.exists("olist.zip") and not os.path.exists("olist.db"):
    with zipfile.ZipFile("olist.zip", 'r') as zip_ref:
        zip_ref.extractall()
