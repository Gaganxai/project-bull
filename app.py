from flask import Flask, request, jsonify
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CLIPS_FOLDER = 'clips'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLIPS_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "✅ Project Bull API is Running!"

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Auto-clip first 59 seconds
    clip_output = os.path.join(CLIPS_FOLDER, f"clip_{file.filename}")
    try:
        clip_video(filepath, 0, 59, clip_output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'message': 'Video uploaded and clipped',
        'clip_path': clip_output
    }), 200

def clip_video(input_path, start_sec, end_sec, output_path):
    video = VideoFileClip(input_path)
    clip = video.subclip(start_sec, end_sec)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

if __name__ == '__main__':
    app.run(debug=True)
