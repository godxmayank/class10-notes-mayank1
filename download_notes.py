import os
import json
import requests
from zipfile import ZipFile

def safe_filename(name):
    return "".join(c if c.isalnum() or c in " _-" else "_" for c in name)

def download_file(url, filepath):
    try:
        response = requests.get(url, stream=True, timeout=20)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"✅ Downloaded: {filepath}")
    except Exception as e:
        print(f"❌ Failed: {url} ({e})")

def zip_directory(folder_path, zip_name):
    with ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), folder_path))
    print(f"\n📦 Created ZIP: {zip_name}")

def main():
    with open('sources.json', 'r') as f:
        sources = json.load(f)

    base_dir = "Class 10 Notes - Mayank Board Prep"
    os.makedirs(base_dir, exist_ok=True)

    for subject, chapters in sources.items():
        print(f"\n📘 Subject: {subject}")
        subject_dir = os.path.join(base_dir, safe_filename(subject))
        os.makedirs(subject_dir, exist_ok=True)

        for chapter_name, pdf_url in chapters.items():
            filename = safe_filename(chapter_name) + ".pdf"
            filepath = os.path.join(subject_dir, filename)
            if not os.path.exists(filepath):
                download_file(pdf_url, filepath)
            else:
                print(f"⏭️ Skipping (already exists): {filename}")

    zip_directory(base_dir, f"{base_dir}.zip")

if __name__ == "__main__":
    main()
