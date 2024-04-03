from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class ImageForm(FlaskForm):
    imageInput = FileField('Select Image', validators=[DataRequired()])
    submit = SubmitField('Upload Image')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        # Handle form submission
        image_data = form.imageInput.data.read()  # Read image data
        # You can now save image_data to a file or do other processing

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
