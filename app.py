import flask
from flask import Flask
from flask import request
from services.court_recognition_service import CourtRecognitionService
from services.image_service import ImageService
from flask_cors import CORS, cross_origin

court_recognition_service = CourtRecognitionService()
image_service = ImageService()

app = Flask(__name__)
CORS(app)


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
