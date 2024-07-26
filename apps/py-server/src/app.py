import os
import logging
from flask import Flask, Response, request, render_template

import config
from capture import generate_frames

# Global state for streaming
streaming = True


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.logger.setLevel(logging.INFO)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.logger.info("loading config.py")
        app.config.from_object(config.Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(app, streaming), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/control')
    def control():
        global streaming
        action = request.args.get('action')
        if action == 'pause':
            streaming = False
        elif action == 'resume':
            streaming = True
        return f'Streaming is {"paused" if not streaming else "running"}'

    @app.route('/')
    def index():
        return render_template('index.html')

    app.config['STATIC_FOLDER'] = '.'

    return app


if __name__ == '__main__':
    app = create_app()
    port = os.getenv('PORT', 3000)
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host, port=port)
