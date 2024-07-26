import cv2
import base64
import logging
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*') # TODO: CORS
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return ':)'

@socketio.on('connect')
def connect(sid):
    print('Client connected:', sid)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected:')


@socketio.on('frame')
def handle_frame(data):
    print(f"Received data size: {len(data)} bytes")
    print(f"Received data (hex): {data[:50]}...")  # Print first 50 bytes for inspection

    try:
        logger.info('handle_frame')
        np_data = np.frombuffer(data, dtype=np.uint8)
        print(f"Received data (hex): {np_data[:50]}...")  # Print first 50 bytes for inspection
        logger.info('read from buffer')
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        logger.info('buffer decoded into image')

        if frame is not None:
            # Process frame with OpenCV
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            logger.info('image processed')

            # Encode processed frame and send back if needed
            _, buffer = cv2.imencode('.jpg', gray)
            logger.info('image encoded')
            emit('response_frame', buffer.tobytes())
            logger.info('response_frame sent')
        else:
            print('Frame is None. Data might be corrupted.')
    except Exception as e:
        print(f"Error processing frame: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    socketio.run(app, host='0.0.0.0', port=5000)
