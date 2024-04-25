from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, EmailField, PasswordField, SubmitField,URLField,FileField
from wtforms.validators import DataRequired, Email, URL,Length

class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"}, label= False)
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Enter your password"}, label= False)
    submit = SubmitField('login',render_kw={"class": "btn btn-primary"})

class RegisterForm(FlaskForm):
    email = EmailField( validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"}, label= False)
    username = StringField( validators=[DataRequired()], render_kw={"placeholder": "Choose a username"}, label= False)
    password = PasswordField( validators=[DataRequired(),Length(min=1)], render_kw={"placeholder": "Choose a password"}, label= False)
    phoneNo = StringField( validators=[DataRequired()], render_kw={"placeholder": "Enter Working Phone number"}, label= False)
    submit = SubmitField('register',render_kw={"class": "btn btn-success"})

class CommentForm(FlaskForm):
    head = StringField( validators=[DataRequired()], render_kw={"placeholder": "Enter heading"})
    body = CKEditorField('Body', validators=[DataRequired()])
    bg_image = URLField('Enter background image URL',render_kw={"placeholder": "Enter background image URL (optional)"})
    submit = SubmitField('Post poll',render_kw={"class": "btn btn-success"})
    
class DatabaseForm(FlaskForm):
    icon_link = URLField(validators=[DataRequired()], render_kw={"placeholder": "Enter valid icon link"}, label= False)
    submit = SubmitField('Submit',render_kw={"class": "btn btn-primary"})
    
# class OtpForm(FlaskForm):
#     OTP = StringField( validators=[DataRequired()], render_kw={"placeholder": "Enter OTP sent at your mail"})
#     submit = SubmitField('Submit',render_kw={"class": "btn btn-primary"})
    
class ChangePasswordForm(FlaskForm):
    password1 = PasswordField( render_kw={"placeholder": "Choose a new password "}, label= False)
    password2 = PasswordField( render_kw={"placeholder": "Confirm password "}, label= False)
    submit = SubmitField('Change',render_kw={"class": "btn btn-primary"})
 
    
class EditProfileForm(FlaskForm):
    ProfilePic = URLField( render_kw={"placeholder": "Enter a valid Profile pic link (optional)"}, label= False)
    username = StringField( render_kw={"placeholder": "Choose new username (optional)"}, label= False)
    password = PasswordField( render_kw={"placeholder": "Create a new password (optional) "}, label= False)
    SelectPic = FileField( render_kw={"placeholder": "Select photo (optional) "}, label= False)
    submit = SubmitField('Submit',render_kw={"class ": "btn btn-primary"})

class ReplyForm(FlaskForm):
    body = CKEditorField(validators=[DataRequired()], label= False)
    submit = SubmitField('Submit',render_kw={"class": "btn btn-primary"})
    
class SearchForm(FlaskForm):
    text = StringField(validators=[DataRequired()], render_kw={"class": "form-control search-input me-2", "type": "search", "placeholder": "Search", "aria-label": "Search"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-outline-primary", "type": "submit"})
    
class ContactForm(FlaskForm):
    body = CKEditorField(validators=[DataRequired()], label= False)
    submit = SubmitField('Submit',render_kw={"class": "btn btn-primary"})
    
#contact us
#sentimant