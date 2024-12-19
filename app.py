from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from keras.applications.vgg16 import preprocess_input

app = Flask(__name__)

# Load the trained model
model = load_model('model.h5')

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Prediction function
def model_predict(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    img_data = preprocess_input(x)

    classes = model.predict(img_data)
    result = int(classes[0][0])

    if result == 1:
        return "Person is affected by Covid-19"
    else:
        return "Result is normal"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file to the uploads folder
        file.save(file_path)
        
        # Get the prediction result
        result = model_predict(file_path)
        
        return result
    else:
        return "Invalid file format"

if __name__ == '__main__':
    app.run(debug=True)
