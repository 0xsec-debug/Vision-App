# 🤖 AI Vision App - ML Web Application

A **real-time ML-powered web application** for facial expression recognition and object counting built with **React + Flask + TensorFlow**!

Created by **Isparsh Tiwari**

---

## ✨ Features

### 🎭 **Facial Expression Recognition**
- Detects 7 emotions: Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral
- CNN model trained on FER2013 dataset
- Real-time detection from camera
- Returns emotion + confidence + motivational quote

### 🖐️ **Finger Counter**
- Counts raised fingers using MediaPipe
- Supports both hands simultaneously
- Shows which fingers are raised
- Real-time hand tracking

### 🔍 **Object Counter**
- Counts any countable objects in image
- Multiple detection methods (contour, blob)
- Works with various object types
- Annotated visualization

### 📹 **Multi-Input Support**
- ✅ Live camera (real-time)
- ✅ Upload images (JPG, PNG, GIF)
- ✅ Upload videos (MP4, AVI, MOV)

### 📱 **Responsive UI**
- Works on desktop & mobile
- Modern React interface
- Real-time results display

---

## 🏗️ Architecture

```
AI Vision App
│
├── Backend (Flask + Python)
│   ├── Emotion Detection (TensorFlow/Keras CNN)
│   ├── Finger Counting (MediaPipe Hands)
│   ├── Object Counting (OpenCV)
│   └── REST API
│
└── Frontend (React)
    ├── Camera Interface
    ├── File Upload
    └── Results Display
```

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **pip**

### Step 1: Clone/Download Project

```bash
# Create project structure
ai-vision-app/
├── backend/
└── frontend/
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Download & Prepare Dataset

**Option A: Kaggle (Recommended)**

1. Install Kaggle CLI:
```bash
pip install kaggle
```

2. Setup Kaggle API:
- Go to https://www.kaggle.com/account
- Create new API token
- Download `kaggle.json`
- Place in `~/.kaggle/` (Linux/Mac) or `C:\Users\<username>\.kaggle\` (Windows)

3. Download FER2013 dataset:
```bash
kaggle datasets download -d msambare/fer2013
unzip fer2013.zip
```

**Option B: Manual Download**

1. Go to: https://www.kaggle.com/datasets/msambare/fer2013
2. Download dataset
3. Organize as:

```
data/
  train/
    angry/
      img1.jpg
      img2.jpg
      ...
    disgust/
    fear/
    happy/
    sad/
    surprise/
    neutral/
  test/
    (same structure)
```

### Step 4: Train the Model

```bash
python train_model.py
```

**Training Info:**
- Time: 2-4 hours (CPU) or 30-60 min (GPU)
- Epochs: 50
- Expected Accuracy: 60-70% (FER2013 is challenging!)

**Skip Training (For Testing):**
The app will run without a trained model, but emotion detection won't work. You can:
1. Test with finger counting & object counting first
2. Train model later
3. Use pre-trained model (if available)

### Step 5: Start Backend Server

```bash
python app.py
```

Server runs on: `http://localhost:5000`

### Step 6: Frontend Setup

Open new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start React app
npm start
```

App opens at: `http://localhost:3000`

---

## 🚀 Usage

### 1. Choose Input Mode
- **Live Camera**: Real-time analysis
- **Upload Image**: Analyze static images
- **Upload Video**: Process video files

### 2. Select Analysis Type
- **All**: Emotion + Fingers + Objects
- **Emotion Only**: Face expression detection
- **Fingers Only**: Hand/finger counting
- **Objects Only**: General object counting

### 3. Analyze
- Click "Analyze" button
- Wait for processing
- View results with annotations

### 4. Results Include
- **Emotion**: Detected emotion, confidence, motivational quote
- **Fingers**: Count per hand, which fingers are raised
- **Objects**: Total count, detection method
- **Annotated Image**: Visual overlay with bounding boxes

---

## 📊 Model Training Details

### Dataset: FER2013
- **Images**: 35,887 grayscale images
- **Size**: 48x48 pixels
- **Classes**: 7 emotions
- **Train/Test Split**: 80/20

### Model Architecture
```
CNN Model:
- Conv2D (64) -> BatchNorm -> Conv2D (64) -> MaxPool -> Dropout
- Conv2D (128) -> BatchNorm -> Conv2D (128) -> MaxPool -> Dropout  
- Conv2D (256) -> BatchNorm -> Conv2D (256) -> MaxPool -> Dropout
- Dense (512) -> BatchNorm -> Dropout
- Dense (256) -> BatchNorm -> Dropout
- Dense (7, softmax)

Total Parameters: ~5M
Optimizer: Adam
Loss: Categorical Crossentropy
```

### Training Tips
1. **Use GPU**: Much faster (CUDA required)
2. **Data Augmentation**: Enabled by default
3. **Early Stopping**: Prevents overfitting
4. **Checkpoints**: Best model saved automatically

### Expected Results
- Training Accuracy: 70-75%
- Validation Accuracy: 60-65%
- Note: FER2013 is challenging due to image quality

---

## 🔧 API Endpoints

### Health Check
```bash
GET /api/health
```

### Detect Emotion
```bash
POST /api/detect-emotion
Body: { "image": "base64_string", "annotate": true }
# OR
Body: FormData with 'file'
```

### Count Fingers
```bash
POST /api/count-fingers
Body: { "image": "base64_string", "annotate": true }
```

### Count Objects
```bash
POST /api/count-objects?method=contour
Body: { "image": "base64_string", "annotate": true }
```

### Analyze All
```bash
POST /api/analyze-all
Body: { "image": "base64_string", "annotate": true }
```

---

## 📁 Project Structure

```
ai-vision-app/
├── backend/
│   ├── app.py                    # Flask server
│   ├── train_model.py            # Training script
│   ├── requirements.txt          # Python dependencies
│   ├── services/
│   │   ├── emotion_detector.py   # CNN emotion model
│   │   ├── finger_counter.py     # MediaPipe hands
│   │   └── object_counter.py     # OpenCV counting
│   ├── utils/
│   │   └── quotes.py             # Motivational quotes
│   ├── models/                   # Trained models (created after training)
│   └── uploads/                  # Temp file storage
│
├── frontend/
│   ├── package.json              # npm dependencies
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js                # Main React component
│       ├── App.css               # Styles
│       └── index.js              # React entry
│
├── data/                         # Training data (not included)
│   ├── train/
│   └── test/
│
└── README.md                     # This file
```

---

## 🎨 Customization

### Add More Emotions
Edit `emotion_detector.py`:
```python
self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral', 'YOUR_EMOTION']
```

### Change Quotes
Edit `utils/quotes.py`:
```python
EMOTION_QUOTES = {
    'happy': ["Your custom quote!", ...],
    ...
}
```

### Adjust Detection Sensitivity
Edit `finger_counter.py`:
```python
self.hands = self.mp_hands.Hands(
    min_detection_confidence=0.7,  # Adjust 0-1
    min_tracking_confidence=0.5    # Adjust 0-1
)
```

---

## 🐛 Troubleshooting

### Backend Issues

**ModuleNotFoundError:**
```bash
pip install -r requirements.txt
```

**Model not loading:**
- Train model first: `python train_model.py`
- Or download pre-trained model

**Port 5000 already in use:**
```python
# In app.py, change:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

**npm install fails:**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**CORS errors:**
- Ensure Flask-CORS is installed
- Check `CORS(app)` in app.py

**Camera not working:**
- Allow camera permissions in browser
- Use HTTPS for production

---

## 🌐 Deployment

### Backend (Flask)

**Heroku:**
```bash
# Add Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

**Railway/Render:**
- Connect GitHub repo
- Set build command: `pip install -r requirements.txt`
- Set start command: `python app.py`

### Frontend (React)

**Vercel:**
```bash
npm run build
vercel --prod
```

**Netlify:**
```bash
npm run build
# Upload build/ folder
```

**Update API URL:**
```javascript
// In App.js:
const API_URL = 'https://your-backend-url.com/api';
```

---

## 📈 Performance

- **Emotion Detection**: ~100-200ms per image
- **Finger Counting**: ~50-100ms per image
- **Object Counting**: ~100-300ms per image
- **Combined Analysis**: ~300-500ms per image

*Times vary based on hardware and image size*

---

## 🤝 Contributing

Want to improve this project?

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Test thoroughly
5. Submit pull request

Ideas:
- More emotions
- Better UI/UX
- Video processing optimization
- Mobile app version
- Real-time video stream

---

## 📄 License

MIT License - Free to use and modify!

---

## 🙏 Acknowledgments

- **FER2013 Dataset**: Emotion recognition dataset
- **MediaPipe**: Hand tracking
- **OpenCV**: Computer vision
- **TensorFlow/Keras**: Deep learning
- **React**: Frontend framework
- **Flask**: Backend framework

---

## 👨‍💻 Author

**Isparsh Tiwari**
- Full Stack Developer
- ML Engineer
- Ethical Hacker

---

## 🎯 Next Steps

After setup:
1. ✅ Test with camera
2. ✅ Upload sample images
3. ✅ Train your model
4. ✅ Customize quotes
5. ✅ Deploy online
6. ✅ Share with friends!

---

**Made with ❤️ and lots of ☕**

Need help? Check issues or create new one!

🚀 **Happy Coding!**
