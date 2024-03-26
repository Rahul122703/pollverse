from flask import Flask,render_template,redirect,url_for,abort,request
from flask_bootstrap import Bootstrap5
from forms import LoginForm,RegisterForm,CommentForm,DatabaseForm,OtpForm,EditProfileForm,SearchForm
from flask_ckeditor import CKEditor

from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash


from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import relationship,DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String, Boolean,func

import random
import requests
from datetime import datetime
import os
from functools import wraps

logged_in = 0
not_registering = 1
current_user_id = 0
otp_send = 0
anonymous_mode = 0

random_username = None
current_user_email = None
user_otp = None
user_obj = None
username = None
user_icon = None
sidenav = 0
current_page = None

site_mail = "xieminiprojet@gmail.com"
site_pass  = "yerp yfnl htro eimm"

app =  Flask(__name__)

ckeditor = CKEditor(app)

class Base(DeclarativeBase):
    pass

database = SQLAlchemy(model_class=Base)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return database.session.get(User,user_id)

def admin_only(function):
    @wraps(function)
    def wrapper(*args,**kwargs):
        if current_user.id != 1:
            return abort(404,"You must be admin to access this page")
        return function(*args,**kwargs)
    return wrapper


app.config['SECRET_KEY']="mrpvproject"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///polling.db"

database.init_app(app) 

bootstrap_app = Bootstrap5(app)

#Creating tables
class User(UserMixin, database.Model):
    __tablename__ = "user"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    icon : Mapped[str]= mapped_column(String(500))
    username : Mapped[str]= mapped_column(String(50))
    email : Mapped[str]= mapped_column(String(50))
    password : Mapped[str]= mapped_column(String(50))
    created: Mapped[str] = mapped_column(String(50), nullable=True)
    phoneNo : Mapped[str] = mapped_column(String(15))
    
    comments = relationship("Comment",back_populates = "comment_author")
    subcomments = relationship("Subcomment",back_populates = "subcomment_author")

    
class Comment(database.Model):
    __tablename__ = "Comment"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    upvote : Mapped[int] = mapped_column(Integer, nullable=True) #make it false later
    downvote : Mapped[int] = mapped_column(Integer, nullable=True)
    body : Mapped[str] = mapped_column(String(5000))
    head : Mapped[str] = mapped_column(String(150))
    bg_image : Mapped[str] = mapped_column(String(900), nullable=True) 
    userId : Mapped[int] = mapped_column(Integer, database.ForeignKey("user.id"))
    anonymous : Mapped[int] = mapped_column(Integer, nullable=False) 
    comment_author = relationship("User", back_populates="comments")
    
class Subcomment(database.Model):
    __tablename__ = "Subcomment"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    body : Mapped[str] = mapped_column(String(5000))
    user_id : Mapped[str] = mapped_column(Integer, database.ForeignKey("user.id"))
    subcomment_author = relationship("User", back_populates="subcomments")
    
class icon(database.Model):
    __tablename__ = "icon"
    id : Mapped[int] = mapped_column(Integer,primary_key = True)
    link: Mapped[str] = mapped_column(String(500))


with app.app_context():
    database.create_all()

@app.context_processor
def common_variable():
    global logged_in, not_registering, current_user_id, otp_send, anonymous_mode,sidenav,current_page
    global current_user_email, user_otp, user_obj, username, user_icon,random_username
    words_list = ["ShadowSeeker", "WhisperWanderer", "VeilVoyager", "EchoExplorer", "SilentSleuth", "ShadeShifter", "PhantomProwler", "IncognitoInquirer", "StealthStroller", "EnigmaRoamer"]
    random_username = random.choice(words_list)
    return dict(logged_in = logged_in,
                current_page = current_page,
                login_form = LoginForm(),               
                search_form = SearchForm(),
                not_registering = not_registering,
                current_user_id = current_user_id,
                otp_send = otp_send,
                anonymous_mode = anonymous_mode,
                current_user_email = current_user_email,
                user_otp = user_otp,
                user_obj = user_obj,
                username = username,
                user_icon = user_icon,
                sidenav = sidenav,
                random_username = random_username,)

    

@app.route('/register',methods = ['GET','POST'])
def register():
    global not_registering,current_user_id,user_obj,logged_in
    not_registering = 0
    register_form_object = RegisterForm()
    if register_form_object.validate_on_submit():
        entred_email = request.form.get('email')
        user_email = database.session.execute(database.select(User).where(User.email == entred_email)).scalar()
        if user_email == None:
            hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256',salt_length=8)
            icons = [i for i in database.session.execute(database.select(icon)).scalars().all()]
            selected_icon = "https://cdn-icons-png.flaticon.com/512/3251/3251650.png" if len(icons) == 0 else random.choice(icons).link
            print(selected_icon)
            new_user = User(
                username = register_form_object.username.data,
                icon = selected_icon,
                email = register_form_object.email.data.lower(),
                password = hashed_password,
                created = datetime.now().strftime("%Y-%m-%d"),
                phoneNo = register_form_object.phoneNo.data
            )
            user_obj = new_user
            logged_in = 1
            current_user_id = user_obj.id
            database.session.add(new_user)
            database.session.commit()
            login_user(new_user)
            print("user added sucessfully")
            
            return redirect(url_for("index"))
        else:
            error = "This account already exists, Please try another one"
            return render_template('register.html',
                                   register_form = register_form_object,
                                   error = error)
    return render_template('register.html', 
                        register_form = register_form_object, 
                        not_registering = not_registering)


@app.route('/login_user',methods = ['GET','POST'])
def login():
    global logged_in,user_obj,current_user_id,current_user_email
    form_instance = LoginForm()
    if form_instance.validate_on_submit():
        entred_email = request.form.get('email').lower()
        user = database.session.execute(database.select(User).where(User.email == entred_email)).scalar()
        if user != None:
            entered_password = request.form.get('password')
            if check_password_hash(user.password, entered_password):
                login_user(user)
                logged_in = 1
                current_user_id = user.id
                print(f"here!!!!!!!!! {current_user_id}")
                user_obj = user
                current_user_email = entred_email
                return redirect(url_for('index'))
            else:
                print("wrong pass")
                error = "Wrong password click to change"
                return render_template('index.html',error = error)
            
        else:
            print("no account")
            error = "No account by this name"
            print(current_user_id)
            return render_template('index.html',error = error)    
    return redirect(url_for('index'))

@app.route('/') 
def index():
    global current_user_id,user_obj,login_form,current_page,sidenav
    current_page = 'index'
    if user_obj != None:
        print(user_obj.username,user_obj.icon)
    login_form = LoginForm()
    all_comments = database.session.execute(database.select(Comment)).scalars().all()
    api_url = 'https://api.api-ninjas.com/v1/quotes?category=success'
    QUOTE_API_KEY = 'oBCu1eDCEZdDYk6oHgIokQ==kjmShcGj3Tcbu34B'
    quote = requests.get(api_url, headers={'X-Api-Key': QUOTE_API_KEY}).json()[0]
    quote_text = f"'{quote['quote']}' - {quote['author']}"
    print(f"current user id is ---> {current_user_id}")
    print(f"side nav is ---> {sidenav}")
    return render_template('index.html',
                           quote = quote_text,
                           comments = all_comments)

@app.route('/logout')
def logout():
    global logged_in, current_user_id
    logged_in = 0
    current_user_id = 0
    logout_user()
    return redirect(url_for('index'))


    
@app.route('/profile',methods = ['GET','POST'])
def profile():
    global current_page
    current_page = 'profile'
    user_obj = database.session.execute(database.select(User).where(User.id == current_user_id)).scalar()
    profile_form = EditProfileForm()
    if profile_form.validate_on_submit():
        user_obj.icon = profile_form.ProfilePic.data
        user_obj.username = profile_form.username.data
        user_obj.password =  generate_password_hash( profile_form.password.data, method='pbkdf2:sha256',salt_length=8)
        database.session.commit()
        
        return redirect(url_for('profile'))
    return render_template('profile.html',
                           profile_form = profile_form,
                           current_user_id = current_user_id)
    
@app.route('/new_comment',methods = ['GET','POST'])
def new_comment():
    global current_page,anonymous_mode
    comment_form = CommentForm()
    print(user_obj.username,user_obj.icon)
    if comment_form.validate_on_submit():
        new_comment = Comment(
            head = comment_form.head.data,
            body = comment_form.body.data,
            bg_image = comment_form.bg_image.data,
            userId = current_user.id ,
            anonymous = anonymous_mode if anonymous_mode else anonymous_mode
        )
        database.session.add(new_comment)
        database.session.commit()
        return redirect(url_for("index"))
    current_page = 'new_comment'
    return render_template('new_comment.html',comment_form = comment_form) 

@app.route('/comment/<int:comment_id>')
def show_comment(comment_id):
    global current_page,user_obj
    current_page = 'index'
    chosen_comment = database.session.execute(database.select(Comment).where(Comment.id == comment_id)).scalar()
    print(chosen_comment.bg_image)
    return render_template('show_comment.html',comment = chosen_comment,user_obj = user_obj)
  

@app.route('/change_password',methods = ['GET','POST'])
def change_password():
    global otp_send,current_user_email,current_user_id,user_otp,user_obj,logged_in
    otp_form = OtpForm()
    random_otp = ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for i in range(6))
    if otp_send == 0:
        otp_send = 1
        user_otp = random_otp
        msg = f"NOTE THIS TOP IS VALID FOR ONLY ONE TIME ....YOUR OTP ---->{random_otp}"
        from twilio.rest import Client
        AuthToken  = "363fc7c36532b1ac2c0b863b8208782c"
        account_sid = 'AC1f76444ae72a4365665fb95d3157bd29'
        auth_token = f'{AuthToken}'
        client = Client(account_sid, auth_token)
        message = client.messages.create(body = msg,from_= "+16237772097",to='+918291147114')
        return render_template('index.html',otp_form = otp_form,error = 1)
    
    print(f"USER ENTERED OTP = {otp_form.OTP.data}")
    print(f"OTP = {user_otp}")
    if otp_form.OTP.data == user_otp:
        otp_send = 0
        logged_in = 1
        user = database.session.execute(database.select(User).where(User.email == current_user_email)).scalar()
        user_obj = user
        print(f"this is the user {user}")
        login_user(user)
        current_user_id = user.id
        return redirect(url_for('index'))
    else:
        error = "Entered Wrong OTP"
        otp_send = 0
        return render_template('index.html',                       
                           error = error) 
   
@app.route('/anonymous')  
def anonymous():
    global username,user_icon,user_obj,anonymous_mode,random_username
    if anonymous_mode == 0:
        username = user_obj.username
        user_icon = user_obj.icon
        user_obj.username = random_username
        user_obj.icon= "https://cdn-icons-png.flaticon.com/512/4123/4123763.png"
        anonymous_mode = 1
    else:
        user_obj.username = username
        user_obj.icon = user_icon
        anonymous_mode = 0
    return redirect(url_for('index'))


@app.route('/search',methods = ['POST','GET'])
def search():
    search_form = SearchForm()
    searched = search_form.text.data
    comments = database.session.execute(database.select(Comment).where(func.ilike(Comment.head, searched + '%'))).scalar()
    print(comments)
    return render_template('search.html',comments = comments)


@app.route('/sidenav',methods = ['POST','GET'])
def sidenav():
    global sidenav,current_page
    if sidenav == 0:
        sidenav = 1
    else:
        sidenav = 0
    return redirect(url_for(f'{current_page}'))
    

@app.route('/db',methods = ['POST','GET'])
@admin_only
def database_control():
    database_form = DatabaseForm()
    if database_form.validate_on_submit():
        new_icon = icon(link = database_form.icon_link.data)
        database.session.add(new_icon)
        database.session.commit()
    return render_template('database_control.html',database_form = database_form)

@app.route('/contact')
def contact(): 
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)