import flask
from flask import Flask
from flask import request
from services.court_recognition_service import CourtRecognitionService
from services.image_service import ImageService
from services.pose_extraction.movenet_pose_extraction_service import MovenetPoseExtractionService
from services.video_analyzer import VideoAnalyzer
from services.stroke_recognition.stroke_recognition_manager_factory import DenseModelStrokeRecognitionManagerFactory
from flask_cors import cross_origin

court_recognition_service = CourtRecognitionService()
image_service = ImageService()
pose_extraction_service = MovenetPoseExtractionService()
stroke_recognition_manager_factory = DenseModelStrokeRecognitionManagerFactory()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/recognize_court', methods=['POST'])
@cross_origin()
def recognize_court():
    try:
        json = request.get_json()
        encoded_frame = json.get('frame')

        frame = image_service.load_image_from_base64(encoded_frame)
        court = court_recognition_service.get_court(frame)
    except Exception as e:
        print(e)
        court = None

    return flask.jsonify({
        'court': court
    })


@app.route('/analyze_video', methods=['POST'])
@cross_origin()
def analyze_video():
    try:
        json = request.get_json()

        encoded_video = json.get('video')
        court_coordinates = json.get('court')

        video_analyzer = VideoAnalyzer(
            pose_extraction_service,
            stroke_recognition_manager_factory,
            encoded_video,
            court_coordinates
        )
        analysis_output = video_analyzer.analyze_video()
        video_analyzer.teardown()
    except Exception as e:
        print(e)
        analysis_output = {
            'players_data': None,
            'fps': None
        }

    return flask.jsonify(analysis_output)
