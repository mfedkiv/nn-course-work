import cv2
import dlib
import numpy as np

NOSE_TIP_IDX = 33
MAX_ERROR_COUNT = 100
LETTERS = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z']


def extract_frames(video_route, fps):
    frames = []

    cap = cv2.VideoCapture(video_route)

    if not cap.isOpened():
        print(f"Could not open video. Skipping this video.")
        return frames

    video_fps = cap.get(cv2.CAP_PROP_FPS)

    frame_interval = int(video_fps / fps) if video_fps >= fps else 1

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            frames.append(frame)

        frame_count += 1

    cap.release()

    return [cv2.resize(im, (128, 64), interpolation=cv2.INTER_LANCZOS4) for im in frames]


def arr2txt(arr, start):
    txt = []
    for n in arr:
        if n >= start:
            txt.append(LETTERS[n - start])
    return ''.join(txt).strip()


def ctc_decode(y):
    y = y.argmax(-1)
    return [arr2txt(y[_], start=1) for _ in range(y.size(0))]


def extract_mouth_images(frames):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('../data/shape_predictor_68_face_landmarks.dat')

    mouth_frames = []
    error_counter = 0

    for frame in frames:
        faces = detector(frame)
        if len(faces) > 0:
            face = faces[0]
            shape = predictor(frame, face)
            shape_np = np.array([(p.x, p.y) for p in shape.parts()])
            nose_tip = shape_np[NOSE_TIP_IDX]
            roi_width = 200
            roi_height = 200
            start_x = max(0, nose_tip[0] - roi_width // 2)
            start_y = nose_tip[1]
            end_x = min(frame.shape[1], start_x + roi_width)
            end_y = min(frame.shape[0], start_y + roi_height)
            roi = frame[start_y:end_y, start_x:end_x]

            mouth_frames.append(roi)
        else:
            error_counter += 1
            mouth_frames.append(frame)

    if error_counter >= MAX_ERROR_COUNT:
        return {
            'error': True,
            'message': 'Not enough mouth images were detected'
        }

    return {
        'error': False,
        'frames': [cv2.resize(frame, (128, 64), interpolation=cv2.INTER_LANCZOS4) for frame in mouth_frames]
    }


def preprocess_frames(frames):
    frames = frames.astype('float32')
    frames /= 255.0
    frames -= 0.5
    frames *= 2.0
    return frames
