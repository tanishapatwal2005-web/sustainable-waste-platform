import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model("model/waste_model.h5")

labels = ['Organic', 'Recyclable']

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0) / 255.0

    pred = model.predict(img)
    class_index = np.argmax(pred)
    confidence = round(np.max(pred) * 100, 2)

    return labels[class_index], confidence