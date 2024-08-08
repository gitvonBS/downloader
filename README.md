# Downloader

## Description

Downloader is a Flask web application that connects to Google Drive, allowing users to select a specific screen, list available videos for that screen, and download selected videos. The application uses OAuth 2.0 for authentication with Google Drive and manages user sessions to secure video access.

## Features

- **Password Authentication**: Each screen is protected by a specific password.
- **Video Selection**: Displays available videos for the selected screen with checkboxes for selection.
- **Video Download**: Downloads selected videos to a local directory.
- **Manual Refresh**: Option to manually refresh the video list.
- **Sensitive Information Protection**: Sensitive information such as credentials and passwords are stored in a protected configuration file.

## Requirements

- Python 3.6 or higher
- Google account with Google Drive access

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/downloader.git
    cd downloader
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure OAuth 2.0 credentials**:

    - Go to the Google Cloud Console and create a project.
    - Enable the Google Drive API.
    - Configure the OAuth consent screen.
    - Create OAuth 2.0 credentials for a web application and download the `client_secrets.json` file.
    - Place the `client_secrets.json` file in the project's root directory.

5. **Set up sensitive information**:

    - Create a `config.json` file in the root directory with the necessary configurations.

6. **Create the download directory**:

    ```bash
    mkdir -p downloaded
    ```

## Usage

1. **Run the application**:

    ```bash
    python run.py
    ```

2. **Access the web interface**:

    - Open a web browser and go to `http://127.0.0.1:5000`.

3. **Select a screen and log in**:

    - Select a screen (1 to 5).
    - Enter the corresponding password.
    - Click "Login".

4. **List and download videos**:

    - The list of available videos for the selected screen will be displayed.
    - Select videos using checkboxes and click "Download".