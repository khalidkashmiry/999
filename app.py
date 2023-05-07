from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get uploaded file
    file = request.files['file']

    # Save uploaded file to original folder
    os.makedirs('original', exist_ok=True)
    file_path = os.path.join('original', file.filename)
    file.save(file_path)

    # Process image
    output_path = os.path.join('masked', file.filename)
    with open(output_path, 'wb') as f:
        input_data = open(file_path, 'rb').read()
        subject = remove(input_data, alpha_matting=True )
        f.write(subject)

    # Display masked image
    img = Image.open(BytesIO(subject))
    img_io = BytesIO()
    img.save(img_io, 'png', quality=70)
    img_io.seek(0)

    # Return masked image
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
