from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from app.google_drive import list_videos_for_screen, download_videos
import json
import os

bp = Blueprint('routes', __name__)

def load_passwords():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path) as config_file:
        config = json.load(config_file)
        return config['passwords']

PASSWORDS = load_passwords()

@bp.route('/')
def index():
    return render_template('select_screen.html')

@bp.route('/login', methods=['POST'])
def login():
    screen_number = request.form.get('screen')
    password = request.form.get('password')
    
    if PASSWORDS.get(screen_number) == password:
        session['authenticated'] = True
        session['screen_number'] = screen_number
        return redirect(url_for('routes.list_videos'))
    else:
        return "Invalid password. Please try again.", 401

@bp.route('/list_videos')
def list_videos():
    if not session.get('authenticated'):
        return redirect(url_for('routes.index'))
    
    screen_number = session.get('screen_number')
    return render_template('list_videos.html', screen_number=screen_number)

@bp.route('/api/videos/<int:screen_number>', methods=['GET'])
def api_list_videos(screen_number):
    videos = list_videos_for_screen(screen_number)
    return jsonify(videos)

@bp.route('/download', methods=['POST'])
def download():
    if not session.get('authenticated'):
        return redirect(url_for('routes.index'))

    screen_number = request.form.get('screen_number')
    selected_videos = request.form.getlist('videos')

    if not selected_videos:
        return "Please select at least one video to download.", 400

    downloaded_files = download_videos(screen_number, selected_videos)
    return send_from_directory(directory='downloaded', filename=downloaded_files, as_attachment=True)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.index'))
