import tensorflow as tf
import numpy as np
from PIL import Image

# =========================
# LOAD MODEL
# =========================
model = tf.keras.models.load_model("model/waste_model.h5")

# =========================
# CLASS LABELS
# =========================
classes = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

# =========================
# PREDICT FUNCTION
# =========================
def predict_image(image_path):
    # Load image
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    # Convert to array
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)
    confidence = np.max(prediction)

    return {
        "class": classes[class_index],
        "confidence": float(confidence)
    }