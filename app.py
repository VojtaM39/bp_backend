import flask
from flask import Flask
from flask import request
from services.court_recognition_service import CourtRecognitionService
from services.image_service import ImageService
from services.openpose_service import OpenPoseService
from services.video_analyzer import VideoAnalyzer
from flask_cors import CORS, cross_origin

court_recognition_service = CourtRecognitionService()
image_service = ImageService()
openpose_service = OpenPoseService()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/recognize_court', methods=['POST'])
@cross_origin()
def recognize_court():
    json = request.get_json()
    encoded_frame = json.get('frame')

    frame = image_service.load_image_from_base64(encoded_frame)
    court = court_recognition_service.get_court(frame)

    return flask.jsonify({
        'court': court
    })


@app.route('/analyze_video', methods=['POST'])
@cross_origin()
def analyze_video():
    json = request.get_json()
    encoded_video = json.get('video')
    court_coordinates = json.get('court')

    video_analyzer = VideoAnalyzer(openpose_service, encoded_video, court_coordinates)
    analysis_output = video_analyzer.analyze_video()

    return flask.jsonify({
        'something': 'yes'
    })
