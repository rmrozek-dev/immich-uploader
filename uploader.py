import requests
import os
import json
from datetime import datetime
import argparse
from pathlib import Path

API_KEY = '' # put your api key here
BASE_URL = 'http://immich/api'  # replace as needed

def upload(file) -> dict:
    stats = os.stat(file)

    headers = {
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }

    data = {
        'deviceAssetId': f'{file}-{stats.st_mtime}',
        'deviceId': 'python',
        'fileCreatedAt': datetime.fromtimestamp(stats.st_mtime),
        'fileModifiedAt': datetime.fromtimestamp(stats.st_mtime),
        'isFavorite': 'false',
    }

    files = {
        'assetData': open(file, 'rb')
    }

    response = requests.post(f'{BASE_URL}/assets', headers=headers, data=data, files=files)

    # debug print
    # print(response.json())
    
    if response.json().get("status") != "created":
        print(f"[WARNING] found duplicated image {file}")
    
    return response.json().get("id")

def create_album(album_name,list_of_images):

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    
    payload = json.dumps({
        "albumName": album_name,
        "albumUsers": [
        ],
        "assetIds": list_of_images,
        "description": ""
    })
    
    # debug print
    # print(payload)
    
    response = requests.post(f'{BASE_URL}/albums', headers=headers, data=payload)
    
    # debug print
    # print(response.json())


def upload_all_in_dir(dirname) -> list:
    uploaded_images_list = []
    included_extensions = ['jpg','jpeg','JPG','JPEG']
    file_names_list = [fn for fn in os.scandir(dirname.path) if any(fn.name.endswith(ext) for ext in included_extensions)]
    
    # debug print
    # print("[DEBUG] list of file to upload:\n")
    # print(file_names_list)
    
    for image_file in file_names_list:
        result = upload(image_file.path) 
        uploaded_images_list.append(result)
    
    return uploaded_images_list



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=Path)
    start_path = parser.parse_args()
    
    # debug print
    # print(start_path.dir_path, type(start_path.dir_path), start_path.dir_path.exists())
        
    subfolders = [ f for f in os.scandir(start_path.dir_path) if f.is_dir() ]

    for dir in subfolders:
        print(f"[INFO] uploading: {dir.name}")
        uploaded_images = upload_all_in_dir(dir)
        print(f"[INFO] creating album: {dir.name}")
        create_album(dir.name,uploaded_images)
    

if __name__ == '__main__':
    main()

