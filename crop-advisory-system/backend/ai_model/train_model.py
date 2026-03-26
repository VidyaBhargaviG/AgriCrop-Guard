"""
CNN Model Training Script for Crop Disease Detection
Uses Transfer Learning with MobileNetV2 on PlantVillage dataset.

Usage:
    1. Download PlantVillage dataset and place in backend/ai_model/dataset/
       Structure: dataset/train/<class_name>/*.jpg
                  dataset/val/<class_name>/*.jpg
    2. Run: python backend/ai_model/train_model.py
    3. Model will be saved as backend/ai_model/crop_disease_model.h5

Dataset source: https://www.kaggle.com/datasets/emmarex/plantdisease
"""

import os
import json

# Suppress TF warnings for cleaner output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# ---------- Configuration ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
VAL_DIR = os.path.join(DATASET_DIR, 'val')
MODEL_PATH = os.path.join(BASE_DIR, 'crop_disease_model.h5')
LABELS_PATH = os.path.join(BASE_DIR, 'class_labels.json')

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 25
LEARNING_RATE = 0.0001


def create_model(num_classes):
    """Create a CNN model using MobileNetV2 transfer learning."""
    # Load pre-trained MobileNetV2 (without top classification layer)
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )

    # Freeze base model layers (use pre-trained features)
    base_model.trainable = False

    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model, base_model


def train():
    """Train the CNN model on crop disease dataset."""

    if not os.path.exists(TRAIN_DIR):
        print(f"Error: Training dataset not found at {TRAIN_DIR}")
        print("\nTo train the model:")
        print("1. Download PlantVillage dataset from:")
        print("   https://www.kaggle.com/datasets/emmarex/plantdisease")
        print(f"2. Extract and organize into: {DATASET_DIR}/train/<class_name>/")
        print(f"   and: {DATASET_DIR}/val/<class_name>/")
        print("\nExpected folder structure:")
        print("   dataset/train/Paddy_Blast/")
        print("   dataset/train/Paddy_BacterialLeafBlight/")
        print("   dataset/train/Paddy_BrownSpot/")
        print("   dataset/train/Chilli_Anthracnose/")
        print("   dataset/train/Chilli_LeafCurl/")
        print("   dataset/train/Coffee_LeafRust/")
        print("   dataset/train/Coffee_BerryDisease/")
        print("   dataset/train/Healthy/")
        print("   (same structure for val/)")
        return

    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1.0 / 255)

    print("Loading training data...")
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )

    print("Loading validation data...")
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    num_classes = train_generator.num_classes
    class_labels = {v: k for k, v in train_generator.class_indices.items()}

    print(f"\nFound {num_classes} classes: {list(train_generator.class_indices.keys())}")
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {val_generator.samples}")

    # Save class labels
    with open(LABELS_PATH, 'w') as f:
        json.dump(class_labels, f, indent=2)
    print(f"Class labels saved to {LABELS_PATH}")

    # Create model
    print("\nCreating MobileNetV2 model...")
    model, base_model = create_model(num_classes)

    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.summary()

    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)
    ]

    # Phase 1: Train with frozen base
    print("\n--- Phase 1: Training classification head (base frozen) ---")
    history1 = model.fit(
        train_generator,
        epochs=10,
        validation_data=val_generator,
        callbacks=callbacks
    )

    # Phase 2: Fine-tune top layers of base model
    print("\n--- Phase 2: Fine-tuning top layers ---")
    base_model.trainable = True
    # Freeze all layers except last 30
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE / 10),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    history2 = model.fit(
        train_generator,
        epochs=EPOCHS,
        initial_epoch=len(history1.history['loss']),
        validation_data=val_generator,
        callbacks=callbacks
    )

    # Final evaluation
    print("\n--- Final Evaluation ---")
    loss, accuracy = model.evaluate(val_generator)
    print(f"Validation Loss: {loss:.4f}")
    print(f"Validation Accuracy: {accuracy:.4f}")
    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Class labels saved to: {LABELS_PATH}")


if __name__ == '__main__':
    train()
