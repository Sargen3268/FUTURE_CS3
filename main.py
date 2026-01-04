from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import FileField , SubmitField
from werkzeug.utils import secure_filename
import os 
from wtforms.validators import InputRequired
from flask import send_from_directory
from flask import redirect, url_for
from flask import flash



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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('home'))

    upload_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])

    if not os.path.exists(upload_path):
        files = []
    else:
        files = os.listdir(upload_path)

    return render_template('index.html', form=form, files=files)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )



if __name__ == '__main__':
    app.run(debug=True) 