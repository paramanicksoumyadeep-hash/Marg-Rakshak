import zipfile
import os

zip_path = r"E:\flipkarttrafficapp\datasets\number plate recognition of riders without helmet.yolov11.zip"
extract_path = r"\\?\E:\flipkarttrafficapp\datasets\riders_without_helmet"

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Unzip successful!")
except Exception as e:
    print(f"Error unzipping: {e}")
