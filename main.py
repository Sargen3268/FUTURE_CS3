from fileinput import filename
from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import FileField , SubmitField
from werkzeug.utils import secure_filename
import os 
import io
from wtforms.validators import InputRequired
from flask import send_from_directory
from flask import Flask, render_template, redirect, url_for, send_file
from flask import flash
from dotenv import load_dotenv
from aes_utils import encrypt_data, decrypt_data

load_dotenv()

AES_KEY = os.getenv("AES_KEY").encode()




app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'



class UploadFileForm(FlaskForm):
    file = FileField("File ", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        data = file.read()
        encrypted_data = encrypt_data(data, AES_KEY)

        with open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "wb") as f:
            f.write(encrypted_data)

        return redirect(url_for('home'))

    upload_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])

    if not os.path.exists(upload_path):
        files = []
    else:
        files = os.listdir(upload_path)

    return render_template('index.html', form=form, files=files)



@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    with open(filepath, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_data(encrypted_data, AES_KEY)

    return send_file(
        io.BytesIO(decrypted_data),
        as_attachment=True,
        download_name=filename
    )




if __name__ == "__main__":
    app.run(
        debug=True,
        ssl_context="adhoc"
    )
