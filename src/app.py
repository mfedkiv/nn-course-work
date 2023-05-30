import os
import torch
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS

from src.models.lipnet import LipNet
from video_helper import extract_frames, ctc_decode, extract_mouth_images, preprocess_frames

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify('Error: No video uploaded'), 400

    video = request.files['video']

    os.makedirs('temp', exist_ok=True)
    video_path = os.path.join('temp', video.filename)
    video.save(video_path)

    frames = extract_frames(video_path, 25)
    extraction_result = extract_mouth_images(frames)

    if extraction_result['error']:
        return jsonify(f"Error: {extraction_result['message']}"), 400

    mouth_frames = extraction_result['frames']
    mouth_frames = preprocess_frames(np.stack(mouth_frames, axis=0).astype(np.float32))

    mouth_frames = torch.FloatTensor(mouth_frames.transpose(3, 0, 1, 2)).unsqueeze(0)

    model = LipNet()
    state_dict = torch.load('./weights/lipnet-weights.pth', map_location=torch.device('cpu'))
    model.load_state_dict(state_dict)

    model.eval()
    prediction = model(mouth_frames)

    os.remove(video_path)

    return jsonify(ctc_decode(prediction)), 200


if __name__ == '__main__':
    app.run()
