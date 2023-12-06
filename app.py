import os
import numpy as np
from PIL import Image
from keras.models import load_model
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'disease_selected_100.h5'
model = load_model(MODEL_PATH)

# List of disease labels
DISEASE_LABELS = {
    0:  'potato late blight',
    1:  'potato healthy',
    2:  'tomato late blight',
    3:  'tomato mosaic virus',
    4:  'tomato bacterial spot',
    5:  'tomato early blight',
    6:  'tomato healthy',
    7:  'tomato leaf mold',
    8:  'tomato septoria leaf spot',
    9:  'tomato two spotted spider mites ',
}

def model_predict(img_path, model):
    img = Image.open(img_path)
    img = img.resize((64, 64))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    pred_class = np.argmax(preds, axis=1)
    result = DISEASE_LABELS[pred_class[0]]

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def pload():
    if request.method == 'POST':
        try:
            file = request.files['file']

            # Check if the file is selected
            if file.filename == '':
                return jsonify(error='No file selected.')

            # Save the file
            basepath = os.path.dirname(__file__)
            uploads_dir = os.path.join(basepath, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)  # Create the 'uploads' directory if it doesn't exist
            file_path = os.path.join(uploads_dir, secure_filename(file.filename))
            file.save(file_path)

            result = model_predict(file_path, model)

            return jsonify(result=result, file_path=file_path)

        except Exception as e:
            return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
