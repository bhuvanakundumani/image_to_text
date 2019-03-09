import os
from flask import Flask, render_template, request


# importing the ocr function
from script import ocr_core

# folder to store the images

UPLOAD_FOLDER = '/static/uploads/'

# allowed files of specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)


# function to check the file extension

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page

@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload image

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # checking to see if a file exists in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')

        file = request.files['file']

        #if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            # call the ocr function
            extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('upload.html',
                                    msg = 'Successfully processed',
                                    extracted_text = extracted_text,
                                    img_src = UPLOAD_FOLDER + file.filename)


    elif request.method == 'GET':
        return render_template('upload.html')




if __name__ == '__main__':
    app.run()