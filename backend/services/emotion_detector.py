# Emotion Detection Service
# services/emotion_detector.py

import cv2
import numpy as np
import os

class EmotionDetector:
    def __init__(self):
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.model = None
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def build_model(self):
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import (
            Conv2D, MaxPooling2D, Flatten, Dense,
            Dropout, BatchNormalization
        )
        model = Sequential([
            Conv2D(64, (3,3), activation='relu', padding='same', input_shape=(48,48,1)),
            BatchNormalization(),
            Conv2D(64, (3,3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2,2), Dropout(0.25),

            Conv2D(128, (3,3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(128, (3,3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2,2), Dropout(0.25),

            Conv2D(256, (3,3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(256, (3,3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2,2), Dropout(0.25),

            Flatten(),
            Dense(512, activation='relu'), BatchNormalization(), Dropout(0.5),
            Dense(256, activation='relu'), BatchNormalization(), Dropout(0.5),
            Dense(7, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model = model
        return model

    def load_model(self, model_path):
        import tensorflow as tf
        if os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
            print(f"✅ Emotion model loaded: {model_path}")
        else:
            print(f"⚠️  Model not found at {model_path}")
            self.build_model()

    def save_model(self, model_path):
        if self.model:
            self.model.save(model_path)

    def detect_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Equalize histogram for better detection in different lighting
        gray_eq = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(
            gray_eq,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces, gray

    def preprocess_face(self, face_image):
        # Resize to 48x48
        face_resized = cv2.resize(face_image, (48, 48))
        # Equalize histogram — matches training preprocessing
        face_eq = cv2.equalizeHist(face_resized)
        # Normalize to [0, 1]
        face_normalized = face_eq / 255.0
        return face_normalized.reshape(1, 48, 48, 1)

    def predict_emotion(self, image):
        if self.model is None:
            return {"error": "Model not loaded", "faces_detected": 0, "emotions": []}

        faces, gray = self.detect_faces(image)

        if len(faces) == 0:
            return {"faces_detected": 0, "emotions": []}

        results = []
        for (x, y, w, h) in faces:
            # Add padding around face for better detection
            padding = 10
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x + w + padding)
            y2 = min(image.shape[0], y + h + padding)

            face_roi       = gray[y1:y2, x1:x2]
            face_processed = self.preprocess_face(face_roi)
            predictions    = self.model.predict(face_processed, verbose=0)

            emotion_idx = np.argmax(predictions[0])
            confidence  = float(predictions[0][emotion_idx])
            emotion     = self.emotion_labels[emotion_idx]

            results.append({
                'emotion'          : emotion,
                'confidence'       : round(confidence * 100, 2),
                'bbox'             : {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                'all_probabilities': {
                    label: round(float(prob) * 100, 2)
                    for label, prob in zip(self.emotion_labels, predictions[0])
                }
            })

        return {'faces_detected': len(faces), 'emotions': results}

    def draw_results(self, image, results):
        if results.get('faces_detected', 0) == 0:
            return image

        image_copy = image.copy()
        img_h, img_w = image_copy.shape[:2]

        for ed in results['emotions']:
            b = ed['bbox']
            x  = b['x']
            y  = b['y']
            x2 = x + b['width']
            y2 = y + b['height']

            # Clamp to image bounds
            x  = max(0, x)
            y  = max(0, y)
            x2 = min(img_w, x2)
            y2 = min(img_h, y2)

            # Draw face bounding box
            cv2.rectangle(image_copy, (x, y), (x2, y2), (0, 255, 0), 2)

            # Draw corner accents
            corner_len = 16
            thickness  = 3
            color      = (0, 255, 0)
            # Top-left
            cv2.line(image_copy, (x, y), (x + corner_len, y), color, thickness)
            cv2.line(image_copy, (x, y), (x, y + corner_len), color, thickness)
            # Top-right
            cv2.line(image_copy, (x2, y), (x2 - corner_len, y), color, thickness)
            cv2.line(image_copy, (x2, y), (x2, y + corner_len), color, thickness)
            # Bottom-left
            cv2.line(image_copy, (x, y2), (x + corner_len, y2), color, thickness)
            cv2.line(image_copy, (x, y2), (x, y2 - corner_len), color, thickness)
            # Bottom-right
            cv2.line(image_copy, (x2, y2), (x2 - corner_len, y2), color, thickness)
            cv2.line(image_copy, (x2, y2), (x2, y2 - corner_len), color, thickness)

            # Label text
            label      = f"{ed['emotion'].upper()}  {ed['confidence']}%"
            font       = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.65
            thickness_txt = 2

            (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, thickness_txt)

            # Place label ABOVE box, but clamp so it never goes off-screen
            label_y = y - 10
            label_x = x

            # If too close to top, place INSIDE box at top
            if label_y - text_h - baseline < 0:
                label_y = y + text_h + 8

            # If label overflows right edge
            if label_x + text_w > img_w:
                label_x = max(0, img_w - text_w - 4)

            # Draw filled background rectangle for label
            pad = 4
            cv2.rectangle(
                image_copy,
                (label_x - pad, label_y - text_h - pad),
                (label_x + text_w + pad, label_y + baseline + pad),
                (0, 0, 0), -1
            )
            cv2.rectangle(
                image_copy,
                (label_x - pad, label_y - text_h - pad),
                (label_x + text_w + pad, label_y + baseline + pad),
                (0, 255, 0), 1
            )

            # Draw label text
            cv2.putText(image_copy, label,
                        (label_x, label_y),
                        font, font_scale, (0, 255, 0), thickness_txt)

        return image_copy


# Training function
def train_emotion_model(train_data_path, epochs=50, batch_size=64, resume_model_path=None):
    import tensorflow as tf
    from pathlib import Path
    from sklearn.model_selection import train_test_split

    print("Loading dataset...")
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    images, labels = [], []

    for idx, emotion in enumerate(emotion_labels):
        folder = Path(train_data_path) / emotion
        if not folder.exists():
            continue
        files = list(folder.glob('*.jpg')) + list(folder.glob('*.png')) + list(folder.glob('*.jpeg'))
        print(f"  {emotion}: {len(files)} images")
        for img_path in files:
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, (48, 48))
            # Apply histogram equalization during training too!
            img = cv2.equalizeHist(img)
            images.append(img)
            labels.append(idx)

    if len(images) == 0:
        raise ValueError("No images loaded!")

    X = np.array(images, dtype='float32') / 255.0
    X = X.reshape(-1, 48, 48, 1)
    y = tf.keras.utils.to_categorical(labels, num_classes=7)

    print(f"\nTotal: {len(X)} images")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=np.argmax(y, axis=1)
    )

    print(f"Training: {len(X_train)} | Validation: {len(X_val)}")

    # Build or resume model
    detector = EmotionDetector()
    if resume_model_path and os.path.exists(resume_model_path):
        print(f"\n✅ Resuming from: {resume_model_path}")
        model = tf.keras.models.load_model(resume_model_path)
        detector.model = model
    else:
        print("\n🆕 Building new model...")
        model = detector.build_model()

    # Augmentation
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.RandomTranslation(0.1, 0.1),
    ])

    train_ds = (
        tf.data.Dataset.from_tensor_slices((X_train, y_train))
        .shuffle(1000)
        .batch(batch_size)
        .map(lambda x, y: (data_augmentation(x, training=True), y),
             num_parallel_calls=tf.data.AUTOTUNE)
        .prefetch(tf.data.AUTOTUNE)
    )

    val_ds = (
        tf.data.Dataset.from_tensor_slices((X_val, y_val))
        .batch(batch_size)
        .prefetch(tf.data.AUTOTUNE)
    )

    os.makedirs('models', exist_ok=True)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            'models/emotion_model_best.h5',
            monitor='val_accuracy', save_best_only=True, mode='max', verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True, verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001, verbose=1
        )
    ]

    history = model.fit(
        train_ds, epochs=epochs,
        validation_data=val_ds,
        callbacks=callbacks, verbose=1
    )

    model.save('models/emotion_model_final.h5')
    return history, model
