# Training Script for Emotion Detection Model
# train_model.py

"""
This script trains the emotion detection model on FER2013 dataset from Kaggle.

Dataset: https://www.kaggle.com/datasets/msambare/fer2013
OR: https://www.kaggle.com/datasets/deadskull7/fer2013

Download and organize as:
data/
  train/
    angry/
    disgust/
    fear/
    happy/
    sad/
    surprise/
    neutral/
  test/
    angry/
    ...

Then run: python train_model.py
"""

import os
import sys
import numpy as np
import pandas as pd
from services.emotion_detector import EmotionDetector, train_emotion_model
import matplotlib.pyplot as plt

def plot_training_history(history):
    """Plot training history"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Accuracy
    axes[0].plot(history.history['accuracy'], label='Training Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True)
    
    # Loss
    axes[1].plot(history.history['loss'], label='Training Loss')
    axes[1].plot(history.history['val_loss'], label='Validation Loss')
    axes[1].set_title('Model Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    print("📊 Training history saved to training_history.png")


def main():
    print("="*60)
    print("🎭 EMOTION DETECTION MODEL TRAINING")
    print("="*60)
    
    # Check if data directory exists
    data_path = 'data/train'
    
    if not os.path.exists(data_path):
        print("\n❌ Error: Training data not found!")
        print("\n📥 Please download FER2013 dataset from Kaggle:")
        print("   https://www.kaggle.com/datasets/msambare/fer2013")
        print("\n📁 Organize data as:")
        print("   data/")
        print("     train/")
        print("       angry/")
        print("       disgust/")
        print("       fear/")
        print("       happy/")
        print("       sad/")
        print("       surprise/")
        print("       neutral/")
        print("\n💡 Alternative: Use this script to download from Kaggle API:")
        print("   1. Install kaggle: pip install kaggle")
        print("   2. Setup API key: https://www.kaggle.com/docs/api")
        print("   3. Run: kaggle datasets download -d msambare/fer2013")
        print("   4. Unzip and organize as shown above")
        sys.exit(1)
    
    # Count images
    print(f"\n📊 Counting training images...")
    total_images = 0
    class_counts = {}
    
    for emotion in os.listdir(data_path):
        emotion_path = os.path.join(data_path, emotion)
        if os.path.isdir(emotion_path):
            count = len([f for f in os.listdir(emotion_path) if f.endswith(('.jpg', '.png', '.jpeg'))])
            class_counts[emotion] = count
            total_images += count
            print(f"   {emotion}: {count} images")
    
    print(f"\n✅ Total training images: {total_images}")
    
    if total_images == 0:
        print("\n❌ No images found! Please check your data directory.")
        sys.exit(1)
    
    # Training parameters
    print("\n🔧 Training Configuration:")
    epochs = 50
    batch_size = 64
    print(f"   Epochs: {epochs}")
    print(f"   Batch Size: {batch_size}")
    print(f"   Optimizer: Adam")
    print(f"   Loss: Categorical Crossentropy")
    
    # Confirm
    response = input("\n❓ Start training? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Training cancelled.")
        sys.exit(0)
    
    print("\n🚀 Starting training...")
    print("⏱️  This may take several hours depending on your hardware!")
    print("💡 Tip: Use GPU for faster training (CUDA required)")
    print("-"*60)
    
    # Train model
    try:
        history, model = train_emotion_model(
            train_data_path=data_path,
            epochs=epochs,
            batch_size=batch_size
        )
        
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETED!")
        print("="*60)
        
        # Final metrics
        final_train_acc = history.history['accuracy'][-1]
        final_val_acc = history.history['val_accuracy'][-1]
        final_train_loss = history.history['loss'][-1]
        final_val_loss = history.history['val_loss'][-1]
        
        print(f"\n📊 Final Metrics:")
        print(f"   Training Accuracy: {final_train_acc:.4f}")
        print(f"   Validation Accuracy: {final_val_acc:.4f}")
        print(f"   Training Loss: {final_train_loss:.4f}")
        print(f"   Validation Loss: {final_val_loss:.4f}")
        
        # Plot history
        plot_training_history(history)
        
        print("\n💾 Model saved to:")
        print("   - models/emotion_model_best.h5 (best checkpoint)")
        print("   - models/emotion_model_final.h5 (final model)")
        
        print("\n🎉 You can now use the model in the Flask app!")
        print("   Just run: python app.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user!")
        print("💾 Partial model may have been saved as checkpoint.")
    except Exception as e:
        print(f"\n\n❌ Training failed with error:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
