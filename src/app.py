import os

from flask import Flask, redirect, render_template, Response, url_for

from main import Faces

BASE_DIR = os.path.dirname(__file__)
ROOT = os.path.dirname(BASE_DIR)
TEMPLATE_PATH = os.path.join(ROOT, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_PATH)

face = Faces()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video_feed():
    return Response(face.blur_and_anon_faces(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/set_mode/<new_mode>')
def set_mode(new_mode):
    if new_mode in ['blur', 'pixelate', 'both', 'none']:
        face.mode = new_mode
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
