import google_auth_oauthlib.flow
import googleapiclient.discovery
import json
import os
import io
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = 'client_secrets.json'

def get_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8081)
    service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
    return service

def get_folder_id():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
            return config['drive_folder_id']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config.json: {e}")
        return None

def list_videos_for_screen(screen_number):
    service = get_service()
    folder_id = get_folder_id()
    if folder_id is None:
        return []

    query = f"'{folder_id}' in parents and mimeType='video/mp4' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = results.get('files', [])
    
    videos_for_screen = []
    screen_str = f"screen_{screen_number}"
    for file in files:
        if screen_str in file['name']:
            videos_for_screen.append(file['name'])
    
    return videos_for_screen

def download_videos(screen_number, video_names):
    service = get_service()
    folder_id = get_folder_id()
    if folder_id is None:
        return []

    downloaded_files = []
    query = f"'{folder_id}' in parents and mimeType='video/mp4' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = results.get('files', [])

    for file in files:
        if file['name'] in video_names:
            request = service.files().get_media(fileId=file['id'])
            fh = io.FileIO(os.path.join('downloaded', file['name']), 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            fh.close()
            downloaded_files.append(file['name'])

    return downloaded_files
