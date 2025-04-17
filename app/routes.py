from flask import Blueprint, request, render_template, redirect, current_app, send_from_directory
from .utils import get_username, is_authorized
import os
from datetime import datetime

bp = Blueprint('main', __name__)

# В памяти
messages = []  # [(имя, сообщение, тип)]

@bp.route('/')
def index():
    if not is_authorized():
        return "⛔ Доступ запрещён", 403
    return render_template('chat.html', username=get_username(), messages=messages)

@bp.route('/send', methods=['POST'])
def send_text():
    if not is_authorized():
        return "⛔ Доступ запрещён", 403
    msg = request.form.get('message', '').strip()
    if msg:
        messages.append((get_username(), msg, 'text'))
    return redirect('/')

@bp.route('/send_voice', methods=['POST'])
def send_voice():
    if not is_authorized():
        return "⛔", 403
    voice = request.files.get('voice')
    if voice:
        filename = f"{datetime.utcnow().timestamp()}_{get_username()}.webm"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        voice.save(path)
        messages.append((get_username(), filename, 'voice'))
    return '', 204


@bp.route('/static/voices/<filename>')
def voice_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

from flask import jsonify

@bp.route('/messages')
def get_messages():
    if not is_authorized():
        return "⛔", 403
    return jsonify([
        {'name': name, 'content': content, 'type': kind}
        for name, content, kind in messages
    ])
