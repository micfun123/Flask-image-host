import os
from flask import Flask, flash, request, redirect, render_template,send_from_directory
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "q424234134245rwry45r24tqr3t23"
app.config['MAX_CONTENT_LENGTH'] = 16 * 2000 * 2000

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','mp4'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded at http://127.0.0.1:5000/uploads/' + filename)
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif, mp3, mp4')
            return redirect(request.url)

#get the files from the uploads folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
      return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000)