import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

def extract_mel_data(audio_file, sr=22050, n_mels=128, fmax=8000):
    """Load an audio file and convert it to a Mel spectrogram"""
    try:
        y, sr = librosa.load(audio_file, sr=sr)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, fmax=fmax) + 1e-9
        return librosa.power_to_db(S, ref=np.max)
    except Exception as e:
        print(f"Error processing {audio_file}: {str(e)}")
        return None

def save_spectrogram_image(S_DB, output_path, sr=22050, fmax=8000):
    """Save a Mel spectrogram as an image file"""
    plt.figure(figsize=(4, 4), dpi=100)
    plt.gca().set_facecolor('black')
    librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel', fmax=fmax, cmap='viridis')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()

def convert_audio_dataset_to_images(audio_dataset_dir, image_dataset_dir):
    """Convert audio files to spectrogram images"""
    os.makedirs(image_dataset_dir, exist_ok=True)
    
    if not os.path.exists(audio_dataset_dir):
        raise FileNotFoundError(f"Audio dataset directory not found: {audio_dataset_dir}")
    
    for language in os.listdir(audio_dataset_dir):
        lang_audio_path = os.path.join(audio_dataset_dir, language)
        if not os.path.isdir(lang_audio_path):
            continue
        
        lang_image_path = os.path.join(image_dataset_dir, language)
        os.makedirs(lang_image_path, exist_ok=True)
        print(f"Processing {language} audio files...")
        
        for file in os.listdir(lang_audio_path):
            if file.lower().endswith('.wav'):
                audio_file_path = os.path.join(lang_audio_path, file)
                image_file_path = os.path.join(lang_image_path, os.path.splitext(file)[0] + '.png')
                
                try:
                    S_DB = extract_mel_data(audio_file_path)
                    if S_DB is not None:
                        save_spectrogram_image(S_DB, image_file_path)
                        print(f"Converted {audio_file_path} to {image_file_path}")
                except Exception as e:
                    print(f"Error converting {audio_file_path}: {str(e)}")

# Main execution
audio_dataset_path = "dataset_audio"         
spectrogram_dataset_path = "dataset_spectrograms" 

# Convert audio to spectrograms
convert_audio_dataset_to_images(audio_dataset_path, spectrogram_dataset_path)

# Data augmentation for better generalization
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
])

# Prepare datasets with optimization
batch_size = 32
img_size = (128, 128)

train_ds = image_dataset_from_directory(
    spectrogram_dataset_path,
    image_size=img_size,
    batch_size=batch_size,
    validation_split=0.2,
    subset="training",
    seed=42
)

val_ds = image_dataset_from_directory(
    spectrogram_dataset_path,
    image_size=img_size,
    batch_size=batch_size,
    validation_split=0.2,
    subset="validation",
    seed=42
)

# Apply augmentation and performance optimizations
train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y),
    num_parallel_calls=tf.data.AUTOTUNE
).cache().shuffle(1000).prefetch(tf.data.AUTOTUNE)

val_ds = val_ds.cache().prefetch(tf.data.AUTOTUNE)

num_classes = len(train_ds.class_names)
print("Detected classes:", train_ds.class_names)

# Create improved model architecture
base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(128, 128, 3))
base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(128, activation="relu")(x)
x = Dropout(0.3)(x)
output = Dense(num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Add callbacks to prevent overfitting
callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
]

# Train with callbacks
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    callbacks=callbacks
)

# Save the model
model.save("language_detector_resnet.h5")
print("Model trained and saved successfully!")
