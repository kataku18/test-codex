from __future__ import annotations

import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from services.ai_writer import generate_caption
from services.instagram_bot import InstagramAutoPoster
from services.media import build_post_image

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/auto-post')
def auto_post():
    data = request.get_json(force=True)
    required = ['username', 'password', 'topic', 'audience', 'tone']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({'ok': False, 'error': f'Missing fields: {", ".join(missing)}'}), 400

    username = data['username']
    password = data['password']
    topic = data['topic']
    audience = data['audience']
    tone = data['tone']
    extra = data.get('extra_instructions', '')

    caption = generate_caption(topic=topic, audience=audience, tone=tone, extra_instructions=extra)

    with tempfile.TemporaryDirectory() as tmp:
        media_path = Path(tmp) / 'post.png'
        build_post_image(topic=topic, audience=audience, output_path=media_path)

        poster = InstagramAutoPoster(headless=os.getenv('HEADLESS', 'true').lower() == 'true')
        post_result = poster.login_and_post(
            username=username,
            password=password,
            caption=caption,
            image_path=media_path,
        )

    return jsonify({'ok': True, 'caption': caption, 'instagram_result': post_result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
