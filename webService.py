from flask import Flask, request, send_file, render_template
import os
from werkzeug.utils import secure_filename
from Hachoir import Hachoir


app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
PROCESSED_FOLDER = '/tmp/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Hachoir d'image pour l'écran géant</title>
    <h1>Upload une image de 807x180</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    # Run the Hachoir processing script
    output_filename = os.path.splitext(filename)[0] + ".jpg"
    output_path = os.path.join(PROCESSED_FOLDER, f"processed_{output_filename}")     
    Hachoir(input_path, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5368,debug=True)
