# Main Flask Application - Original 3-Feature Version
# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2, numpy as np, base64, io, os
from PIL import Image
from werkzeug.utils import secure_filename

from services.emotion_detector import EmotionDetector
from services.finger_counter   import FingerCounter
from services.object_counter   import ObjectCounter
from utils.quotes              import get_quote, get_counting_message

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('models', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Init services
print("🚀 Initializing AI services...")
emotion_detector = EmotionDetector()
finger_counter   = FingerCounter()
object_counter   = ObjectCounter()

# Load emotion model
for name in ['models/emotion_model_best.h5', 'models/emotion_model_final.h5', 'models/emotion_model.h5']:
    if os.path.exists(name):
        emotion_detector.load_model(name)
        print(f"✅ Emotion model loaded: {name}")
        break
else:
    emotion_detector.build_model()
    print("⚠️  No trained model found. Please train first using train_model.py")

print("✅ All services initialized!")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def img_from_request():
    if 'file' in request.files:
        arr = np.array(Image.open(request.files['file']))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR) if arr.ndim == 3 else arr
    if request.json and 'image' in request.json:
        b64 = request.json['image']
        if ',' in b64: b64 = b64.split(',')[1]
        arr = np.array(Image.open(io.BytesIO(base64.b64decode(b64))))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR) if arr.ndim == 3 else arr
    return None


def to_b64(image):
    pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    pil.save(buf, format='JPEG')
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def annotate_flag():
    return (request.args.get('annotate') == 'true' or
            (request.json and request.json.get('annotate')))


@app.route('/')
def home():
    return jsonify({
        'message': 'AI Vision App API',
        'version': '1.0.0',
        'endpoints': [
            'GET  /api/health',
            'POST /api/detect-emotion',
            'POST /api/count-fingers',
            'POST /api/count-objects',
            'POST /api/analyze-all',
        ]
    })


@app.route('/api/health')
def health():
    return jsonify({
        'status' : 'healthy',
        'model'  : 'loaded' if emotion_detector.model else 'not loaded',
        'features': ['emotion', 'fingers', 'objects']
    })


@app.route('/api/detect-emotion', methods=['POST'])
def detect_emotion():
    try:
        img = img_from_request()
        if img is None: return jsonify({'error': 'No image provided'}), 400
        res = emotion_detector.predict_emotion(img)
        for e in res.get('emotions', []):
            e['quote'] = get_quote(e['emotion'])
        if annotate_flag():
            res['annotated_image'] = to_b64(emotion_detector.draw_results(img, res))
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/count-fingers', methods=['POST'])
def count_fingers():
    try:
        img = img_from_request()
        if img is None: return jsonify({'error': 'No image provided'}), 400
        res = finger_counter.count_fingers(img)
        res['message'] = get_counting_message(res['total_fingers'], 'fingers')
        if annotate_flag():
            res['annotated_image'] = to_b64(finger_counter.draw_results(img, res))
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/count-objects', methods=['POST'])
def count_objects():
    try:
        img = img_from_request()
        if img is None: return jsonify({'error': 'No image provided'}), 400
        res = object_counter.count_objects(img)
        res['message'] = get_counting_message(res['count'], 'objects')
        for o in res.get('objects', []):
            o.pop('contour', None)
        if annotate_flag():
            res['annotated_image'] = to_b64(object_counter.draw_results(img, res))
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-all', methods=['POST'])
def analyze_all():
    try:
        img = img_from_request()
        if img is None: return jsonify({'error': 'No image provided'}), 400

        em = emotion_detector.predict_emotion(img)
        for e in em.get('emotions', []): e['quote'] = get_quote(e['emotion'])

        fi = finger_counter.count_fingers(img)
        fi['message'] = get_counting_message(fi['total_fingers'], 'fingers')

        ob = object_counter.count_objects(img)
        ob['message'] = get_counting_message(ob['count'], 'objects')
        for o in ob.get('objects', []): o.pop('contour', None)

        res = {'emotion': em, 'fingers': fi, 'objects': ob}

        if annotate_flag():
            ann = emotion_detector.draw_results(img.copy(), em)
            ann = finger_counter.draw_results(ann, fi)
            ann = object_counter.draw_results(ann, ob)
            res['annotated_image'] = to_b64(ann)

        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI Vision App")
    print("=" * 60)
    print("Endpoints:")
    print("  GET  /api/health")
    print("  POST /api/detect-emotion")
    print("  POST /api/count-fingers")
    print("  POST /api/count-objects")
    print("  POST /api/analyze-all")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
