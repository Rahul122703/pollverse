from flask import Flask,render_template,redirect,url_for,request,send_file,jsonify
from flask_bootstrap import Bootstrap5
from forms import LoginForm,RegisterForm,CommentForm,DatabaseForm,EditProfileForm,SearchForm,ReplyForm,ContactForm,ChangePasswordForm
from flask_ckeditor import CKEditor

from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash


from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import relationship,DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String,Float,LargeBinary

import random
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import base64
import string
import os

logged_in = 0
not_registering = 1
current_user_id = 0
otp_send = 0
anonymous_mode = 0
current_user_pic = None
comment = None
random_username = None
current_user_email = None
user_otp = None
current_user = None
username = None
user_icon = None

current_page = "index"
from_email = "xieminiproject@gmail.com"
app_pass = "ibpp vdjr pukx fyek"
#  https://myaccount.google.com/apppasswords 
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

app.config['SECRET_KEY']="mrpvproject"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI',"sqlite:///posts.db")



database.init_app(app) 

bootstrap_app = Bootstrap5(app)
#abcde
def analyze_sentiment(comment):
    api_url = f'https://api.api-ninjas.com/v1/sentiment?text={comment}'
    response = requests.get(api_url, headers={'X-Api-Key': '9No6wnmZqzRC/NRH0VvxHA==QRYgA94Njvme77Wg'})
    
    if response.status_code == requests.codes.ok:
        data = response.json()
        polarity = data['score']
        return polarity 
    else:
        return None, None, None

def format_time_and_date(date_time):
    return date_time.strftime("%H:%M %d/%m/%Y")

def map_polarity_to_color(polarity):
    if polarity < -0.1:   # negative
        return f'#f21800'  
    elif polarity > 0.1:  # positive
        return f'#00f200'  
    else:                 # neutral
        return f'#596061' 

def b64encode_image(image_data):
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image
app.jinja_env.filters['b64encode_image'] = b64encode_image

def send_mail(from_user,to_user,body):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user="xieminiproject@gmail.com", password=app_pass)
    msg = MIMEMultipart()
    msg['From'] = from_user
    msg['To'] = to_user
    msg['Subject'] = "SUBJECT"

    msg.attach(MIMEText(body, 'html'))

    server.sendmail(from_user, to_user, msg.as_string())
    server.quit()

def is_logged(function):
    global logged_in  
    def wrapper_function():
        if logged_in:
            return function()  
        else:
            return '''<h1 style="color: #FF5733; font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #F2F2F2; border-radius: 10px;">You Are Not Logged In</h1>'''
    return wrapper_function


#Created tables
class User(UserMixin, database.Model):
    __tablename__ = "user"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    icon : Mapped[str]= mapped_column(String(500))
    uicon  = mapped_column(LargeBinary)
    username : Mapped[str]= mapped_column(String(50))
    email : Mapped[str]= mapped_column(String(50))
    password : Mapped[str]= mapped_column(String(50))
    created: Mapped[str] = mapped_column(String(50), nullable=True)
    phoneNo : Mapped[str] = mapped_column(String(15))
    poll: Mapped[int] = mapped_column(Integer)
    reply: Mapped[int] = mapped_column(Integer)
    admin : Mapped[int] = mapped_column(Integer, nullable=False)
    ApiKey :  Mapped[str]= mapped_column(String(50))
    
    comments = relationship("Comment",back_populates = "comment_author")
    subcomments = relationship("Subcomment",back_populates = "subcomment_author")

    
class Comment(database.Model):
    __tablename__ = "Comment"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    upvote : Mapped[int] = mapped_column(Integer, nullable=True) #make it false later
    downvote : Mapped[int] = mapped_column(Integer, nullable=True)
    body : Mapped[str] = mapped_column(String)
    head : Mapped[str] = mapped_column(String(150))
    bg_image : Mapped[str] = mapped_column(String(900), nullable=True) 
    date : Mapped[str] = mapped_column(String(150),nullable=True)
    anonymous : Mapped[int] = mapped_column(Integer, nullable=False) 
    
    userId : Mapped[int] = mapped_column(Integer, database.ForeignKey("user.id"))
    comment_author = relationship("User", back_populates="comments")
    replies = relationship("Subcomment", back_populates="comment")
    
class Subcomment(database.Model):
    __tablename__ = "Subcomment"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    upvote : Mapped[int] = mapped_column(Integer, nullable=True) #make it false later
    downvote : Mapped[int] = mapped_column(Integer, nullable=True)
    body : Mapped[str] = mapped_column(String)
    anonymous : Mapped[int] = mapped_column(Integer, nullable=False)
    date : Mapped[str] = mapped_column(String(150),nullable=True)
    color: Mapped[str] = mapped_column(String(150), nullable=True)
    intensity: Mapped[float] = mapped_column(Float ,nullable=False)
    
    user_id : Mapped[str] = mapped_column(Integer, database.ForeignKey("user.id"))
    comment_id = mapped_column(Integer,database.ForeignKey("Comment.id"))
    
    subcomment_author = relationship("User", back_populates="subcomments")
    comment = relationship("Comment", back_populates="replies")
    
class icon(database.Model):
    __tablename__ = "icon"
    id : Mapped[int] = mapped_column(Integer,primary_key = True)
    link: Mapped[str] = mapped_column(String(500))


with app.app_context():
    database.create_all()

@app.context_processor
def common_variable():
    global logged_in, not_registering, current_user_id, otp_send, anonymous_mode,current_page,admin_flash,sorting,positive_replies,negative_replies,neutral_replies
    global current_user_email, user_otp, current_user, username, user_icon,random_username,current_user_pic,comment
    words_list = ["ShadowSeeker", "WhisperWanderer", "VeilVoyager", "EchoExplorer", "SilentSleuth", "ShadeShifter", "PhantomProwler", "IncognitoInquirer", "StealthStroller", "EnigmaRoamer"]
    random_username = random.choice(words_list)

    return dict(logged_in = logged_in,
                positive_replies = positive_replies,
                negative_replies = negative_replies,
                neutral_replies = neutral_replies,
                sorting  = sorting,
                admin_flash = admin_flash,
                current_user = current_user,
                current_page = current_page,
                login_form = LoginForm(),               
                search_form = SearchForm(),
                not_registering = not_registering,
                current_user_id = current_user_id,
                otp_send = otp_send,
                anonymous_mode = anonymous_mode,
                current_user_email = current_user_email,
                user_otp = user_otp,
                username = username,
                user_icon = user_icon,
                random_username = random_username,
                current_user_pic = current_user_pic,
                comment = comment)
     
@app.route('/register',methods = ['GET','POST'])
def register():#reg123
    global not_registering,current_user_id,current_user,logged_in,current_user_pic,anonymous_mode 
    not_registering = 0
    
    register_form_object = RegisterForm()
    if register_form_object.validate_on_submit():
        entred_email = request.form.get('email')
        user_email = database.session.execute(database.select(User).where(User.email == entred_email)).scalar()
        if user_email == None:
            hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256',salt_length=8)
            icons = [i for i in database.session.execute(database.select(icon)).scalars().all()]
            selected_icon = "https://cdn-icons-png.flaticon.com/512/3251/3251650.png" if len(icons) == 0 else random.choice(icons).link
            new_user = User(
                username = register_form_object.username.data,
                icon = selected_icon,
                email = register_form_object.email.data.lower(),
                password = hashed_password,
                created = datetime.now().strftime("%Y-%m-%d"),
                phoneNo = register_form_object.phoneNo.data,
                poll = 0,
                reply = 0,
                admin =0,
                ApiKey = 0
            )
            database.session.add(new_user)
            database.session.commit()
            current_user = new_user
            logged_in = 1
            current_user_id = current_user.id
            current_user_pic = None
            anonymous_mode = 0
            login_user(new_user)
            body = f'''
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f0f0f0;">
<div class="notification-container" style="width: 400px; margin: 100px auto; background-color: #f0f0f0; padding: 20px; border-radius: 20px; box-shadow: 20px 20px 50px #b9b9b9, -20px -20px 50px #ffffff;">
    <img src="https://img.freepik.com/free-vector/floral-welcome-lettering-concept_23-2147903882.jpg?size=626&ext=jpg&ga=GA1.1.658439437.1707051336&semt=ais" alt="Welcome Image" class="notification-image" style="display: block; margin: 0 auto; width: 200px; height: auto;">
    <h1 style="text-align: center; margin-top: 20px; color: #333;">Welcome to Our Community, {current_user.username}!</h1>
    <p style="text-align: center; color: #555;">Your account has been successfully created. We're excited to have you join us!</p>
    <div class="terms" style="margin-top: 20px; text-align: center; color: #777;">
        <p>By using our platform, you agree to the following terms and conditions:</p>
        <ul>
            <li>Users must adhere to the community guidelines and refrain from posting inappropriate content.</li>
            <li>Any abusive behavior towards other users will not be tolerated.</li>
            <li>The platform reserves the right to moderate discussions and remove any content that violates these terms.</li>
            <li>User data will be handled in accordance with our privacy policy.</li>
        </ul>
    </div>
</div>
</body>
'''
            send_mail("xieminiproject@gmail.com",current_user.email,body)
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
def login(): #login123
    global logged_in,current_user,current_user_id,current_user_email,current_user_pic,anonymous_mode
    form_instance = LoginForm()
    
    if form_instance.validate_on_submit():
        entred_email = request.form.get('email').lower()
        user = database.session.execute(database.select(User).where(User.email == entred_email)).scalar()
        if user != None:
            current_user = user
            entered_password = request.form.get('password')
            if check_password_hash(user.password, entered_password):
                login_user(user)
                logged_in = 1
                current_user_id = user.id
                current_user_pic = user.uicon
                current_user = user
                current_user_email = entred_email
                anonymous_mode = 0
                print(f">>>>>> {entred_email} has logged in <<<<<")
                return redirect(url_for('index'))
            else:
                current_user_email = entred_email
                error = "Forgot password? click to change"
                return render_template('index.html',error = error)
            
        else:
            error = "No account by this name"
            return render_template('index.html',error = error)    
    return redirect(url_for('index'))


global_comments = None
start = 1
sorting = "Oldest"
@app.route('/sort_comment/<int:value>',methods = ['GET','POST'])
def sort_comment(value):
    global global_comments,start,sorting
    
    start = 0
    
    if value == 3: 
        sorting = "Recent"
        global_comments.reverse()  
    elif value == 2: #most active
        sorting = "Most Active"
        global_comments.reverse()
        active_comment = []
        sorted_comments = sorted(global_comments, key=lambda comment: len(database.session.execute(database.select(Subcomment).where(Subcomment.comment_id == comment.id)).scalars().all()), reverse=True)
        active_comment.extend(sorted_comments)
        global_comments = active_comment
    elif value == 1: #oldest
        sorting = "Oldest"
        start = 1
    return redirect(url_for('index'))


@app.route('/') 
def index(): #index123
    global current_user_id,current_user,login_form,logged_in,current_page,global_comments,start
    current_page = "index"
    all_comments = database.session.execute(database.select(Comment)).scalars().all()
    if start:
        comments = [comment for comment in all_comments]
        global_comments = comments
    login_form = LoginForm()

    api_url = 'https://api.api-ninjas.com/v1/quotes?category=success'
    QUOTE_API_KEY = '9No6wnmZqzRC/NRH0VvxHA==QRYgA94Njvme77Wg'
    quote = requests.get(api_url, headers={'X-Api-Key': QUOTE_API_KEY}).json()[0]
    quote_text = f"'{quote['quote']}' - {quote['author']}"
    print(f"current user id is ---> {current_user_id}")
    return render_template('index.html',
                           quote = quote_text,
                           comments = global_comments)

@app.route('/logout')
def logout():
    global logged_in, current_user_id
    logged_in = 0
    current_user_id = 0
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile',methods = ['GET','POST'])
def profile():#profile123
    global current_page,current_user,comment,current_user_pic
    current_page = 'profile'
    changed_user = database.session.execute(database.select(User).where(User.id == current_user_id)).scalar()
    profile_form = EditProfileForm()
    if profile_form.validate_on_submit():
        if len(profile_form.ProfilePic.data)!=0:
            changed_user.icon = profile_form.ProfilePic.data 
        if  len(profile_form.username.data)!=0:    
            changed_user.username = profile_form.username.data
        if len(profile_form.password.data)!=0:    
            changed_user.password =  generate_password_hash( profile_form.password.data, method='pbkdf2:sha256',salt_length=8)  
        if profile_form.SelectPic.data is not None:   
            changed_user.uicon = profile_form.SelectPic.data.read()
        database.session.commit() 
        
        return redirect(url_for('profile'))
    
    
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == current_user_id)).scalars().all()

    comments = database.session.execute(database.select(Comment).where(Comment.userId == current_user_id)).scalars().all()
    print(f'comments = {comments} and current_userId = {current_user_id}')
    # comment  = len(comments)!=0 if comments[0] else None
    
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == current_user.id)).scalars().all()
    intensities = [i.intensity for i in all_replies]
    current_user_pic = changed_user.uicon
    if len(intensities):
        gt_01_count = sum(1 for num in intensities if num > 0.1)
        lt_minus01_count = sum(1 for num in intensities if num < -0.1)
        between_minus01_to_01_count = sum(1 for num in intensities if -0.1 <= num <= 0.1)
        
        total_numbers = len(intensities)
        percent_gt_01 = (gt_01_count / total_numbers) * 100
        percent_lt_minus01 = (lt_minus01_count / total_numbers) * 100
        percent_between_minus01_to_01 = (between_minus01_to_01_count / total_numbers) * 100
        return render_template('profile.html',
                           comments = comments,
                           profile_form = profile_form,
                           length = len(intensities),
                           plus = percent_gt_01,
                           minus = percent_lt_minus01 ,
                           neutral = percent_between_minus01_to_01,
                           all_replies = all_replies,
                           current_user_pic = current_user_pic)
    return render_template('profile.html',
                           length = len(intensities),
                           all_replies  = all_replies ,
                           comments = comments,
                           profile_form = profile_form,
                           current_user_pic = current_user_pic)
 
@app.route('/comment_profile/<int:user_id>',methods = ['GET','POST'])
def comment_profile(user_id):
    comment_user = database.get_or_404(User,user_id)
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == user_id)).scalars().all()

    comments = database.session.execute(database.select(Comment).where(Comment.userId == user_id)).scalars().all()

    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == user_id)).scalars().all()
    intensities = [i.intensity for i in all_replies]
    
    profile_form = EditProfileForm()
    if profile_form.validate_on_submit():
        if len(profile_form.ProfilePic.data)!=0:
            comment_user.icon = profile_form.ProfilePic.data 
        if  len(profile_form.username.data)!=0:    
            comment_user.username = profile_form.username.data
        if len(profile_form.password.data)!=0:    
            comment_user.password =  generate_password_hash( profile_form.password.data, method='pbkdf2:sha256',salt_length=8)  
        if profile_form.SelectPic.data is not None:   
            comment_user.uicon = profile_form.SelectPic.data.read()
        database.session.commit()  
        return redirect(url_for('comment_profile', user_id=user_id)) 
    if len(intensities):
        gt_01_count = sum(1 for num in intensities if num > 0.1)
        lt_minus01_count = sum(1 for num in intensities if num < -0.1)
        between_minus01_to_01_count = sum(1 for num in intensities if -0.1 <= num <= 0.1)
        total_numbers = len(intensities)
        percent_gt_01 = (gt_01_count / total_numbers) * 100
        percent_lt_minus01 = (lt_minus01_count / total_numbers) * 100
        percent_between_minus01_to_01 = (between_minus01_to_01_count / total_numbers) * 100
        return render_template('comment_profile.html',
                           comment_user = comment_user,
                           comments = comments,
                           length = len(intensities),
                           plus = percent_gt_01,
                           minus = percent_lt_minus01 ,
                           neutral = percent_between_minus01_to_01,
                           all_replies = all_replies,
                           profile_form = profile_form)
    
    return render_template('comment_profile.html',
                           length = len(intensities),
                           comment_user = comment_user,
                           all_replies  = all_replies ,
                           comments = comments,
                           profile_form = profile_form) 
 
    
@app.route('/new_comment',methods = ['GET','POST'])
def new_comment():
    global current_page,anonymous_mode
    comment_form = CommentForm()
    print("you are here")
    if comment_form.validate_on_submit():
        new_comment = Comment(
            head = comment_form.head.data,
            body = comment_form.body.data,
            bg_image = comment_form.bg_image.data,
            date = format_time_and_date(datetime.now()),
            userId = current_user.id ,
            anonymous = anonymous_mode if anonymous_mode else anonymous_mode,
            upvote = 0,
            downvote = 0
        )
        current_user.poll += 1
        database.session.add(new_comment)
        database.session.commit()
        return redirect(url_for("index"))
    current_page = 'new_comment'
    return render_template('new_comment.html',comment_form = comment_form) 


percent_gt_01 = 0
percent_lt_minus01 = 0
percent_between_minus01_to_01 = 0
positive_replies = None
negative_replies = None
neutral_replies = None
@app.route('/comment/<int:comment_id>',methods = ['GET','POST'])
def show_comment(comment_id): #show123
    global current_page,anonymous_mode,current_user,percent_gt_01,percent_lt_minus01,percent_between_minus01_to_01,positive_replies,negative_replies,neutral_replies
    chosen_comment = database.session.execute(database.select(Comment).where(Comment.id == comment_id)).scalar()
    reply_form = ReplyForm()
    body = str(reply_form.body.data)
    polarity = analyze_sentiment(body)
    if reply_form.validate_on_submit():
        parent_user = database.session.execute(database.select(User).where(User.id == chosen_comment.userId)).scalar()
        date = format_time_and_date(datetime.now())
        new_reply = Subcomment(
            upvote = 0,
            downvote = 0,
            body = body,
            user_id = current_user_id,
            comment_id = comment_id,
            date = date,
            anonymous = anonymous_mode if anonymous_mode else anonymous_mode,
            color =  map_polarity_to_color(polarity),
            intensity = polarity
        )
        current_user.reply += 1
        database.session.add(new_reply)
        database.session.commit()
    
        email_body = f'''<!DOCTYPE html>
                    <html lang="en">
                    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                    <p style="font-size: 20px; color: #444;">{current_user.username} replied on your poll click to have a look</p><br/>
                    <hr>
                    <a href="pollverse-w0d9.onrender.com" style="text-decoration: none; color: inherit;">
                        <div style="border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #fff;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center;">
                                    <img src="{current_user.icon}" alt="User Icon" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
                                    <span style="font-weight: bold; margin-right: 10px;">{current_user.username}</span>
                                </div>
                                <span style="color: #666;">        {date}</span>
                            </div>
                            <div style="font-size: 16px; line-height: 1.5; margin-bottom: 20px;">
                                <p>{body}</p>
                            </div>
                        </div>
                    </a>
                    <hr>
                    </body>
                    </html>
                    '''
        send_mail("xieminiproject@gmail.com",parent_user.email,email_body)
        return redirect(url_for('show_comment',comment_id = comment_id))
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.comment_id == comment_id)).scalars().all()
    
    positive_replies = [reply for reply in all_replies if reply.color == "#f21800"]
    negative_replies = [reply for reply in all_replies if reply.color == "#00f200"]
    neutral_replies = [reply for reply in all_replies if reply.color == "#596061"]
    
    
    intensities = [i.intensity for i in all_replies]
    if len(intensities):
        gt_01_count = sum(1 for num in intensities if num > 0.1)
        lt_minus01_count = sum(1 for num in intensities if num < -0.1)
        between_minus01_to_01_count = sum(1 for num in intensities if -0.1 <= num <= 0.1)
        total_numbers = len(intensities)
        
        percent_gt_01 = (gt_01_count / total_numbers) * 100
        percent_lt_minus01 = (lt_minus01_count / total_numbers) * 100
        percent_between_minus01_to_01 = (between_minus01_to_01_count / total_numbers) * 100
        
        return render_template('show_comment.html',
                           length = len(intensities),
                           plus = percent_gt_01,
                           minus = percent_lt_minus01 ,
                           neutral = percent_between_minus01_to_01,
                           comment = chosen_comment,
                           reply_form = reply_form,
                           all_replies = all_replies)
    return render_template('show_comment.html',
                           length = len(intensities),
                           comment = chosen_comment,
                           reply_form = reply_form,
                           all_replies = all_replies)


@app.route('/change_password',methods = ['GET','POST'])
def change_password():
    global logged_in,current_user_id,current_user,current_user_email
    error = 2
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        password1 = change_password_form.password1.data
        password2 = change_password_form.password2.data  
        if password2 == password1:
            logged_in = 1
            login_user(current_user)
            current_user1 = database.session.execute(database.select(User).where(User.email == current_user.email)).scalar()
            current_user1.password = generate_password_hash(password1,method='pbkdf2:sha256',salt_length=8)
            database.session.commit()
            current_user_id = current_user.id
            return redirect(url_for('index'))
        else:
            error2 = "passwords don't match"
            return render_template('index.html',error2 = error2,change_password_form = change_password_form,error = 2) 
    return render_template('index.html',error = error,change_password_form = change_password_form) 


@app.route('/send_otp',methods = ['GET','POST'])
def send_otp():
    global otp_send,current_user_email,current_user_id,user_otp,current_user,logged_in,from_email,app_pass
    # otp_form = OtpForm()
    random_otp = ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for i in range(6))
    if otp_send == 0:
        otp_send = 1
        user_otp = random_otp
        body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>OTP Email</title>
            </head>
            <body style="font-family: Arial, sans-serif; background-image: linear-gradient(to bottom right, #ffffcc, #ffcc66); padding: 20px; margin: 0;">
                <div style="max-width: 600px; margin: auto; background-image: linear-gradient(to bottom right, #FFD700, #FFFF00); border-radius: 10px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); padding: 40px; text-align: center;">
                    <p style="font-size: 18px; color: #666; margin-bottom: 20px;">Dear User,</p>
                    <p style="font-size: 20px;">Your One-Time Password (OTP) is:</p>
                    <h1 style="font-size: 36px; color: #333; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); margin-bottom: 30px;"><span style="color: #009688; font-weight: bold;">{random_otp}</span></h1>
                    <p style="font-size: 20px; color: #444;">Please use this OTP to proceed with your action. Remember, this OTP is valid for a single use only.</p>
                    <div style="position: relative; display: inline-block; overflow: hidden; border-radius: 10px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); margin-top: 40px;">
                        <img src="https://media.istockphoto.com/id/1314193433/vector/envelope-with-approved-document-email-confirmation-document-with-check-mark-in-open-letter.jpg?s=612x612&w=0&k=20&c=yWcI4GIf9brTe5RtCZNPjkKggd7bsDpBNcQfP6vTUtk=" alt="OTP Image" style="display: block; width: 100%; transition: transform 0.5s ease-in-out;">
                    
                    </div>
                </div>
            </body>
            </html>
            """
        send_mail(from_email,current_user_email,body)

        return render_template('index.html', error=1)

    entred_otp = ""
    for i in range(1,7):
        entred_otp += request.form.get(f"{i}")
    
    if entred_otp == user_otp:
        otp_send = 0
        return redirect(url_for('change_password'))
    else:
        error = "Entered Wrong OTP click to send"
        otp_send = 0
        return render_template('index.html',error = error) 
   
@app.route('/anonymous')  
def anonymous():#ana123
    global username,user_icon,current_user,anonymous_mode,random_username
    if anonymous_mode == 0:
        username = current_user.username
        user_icon = current_user.icon
        current_user.username = random_username
        current_user.icon= "https://cdn-icons-png.flaticon.com/512/4123/4123763.png"
        anonymous_mode = 1
    else:
        current_user.username = username
        current_user.icon = user_icon
        anonymous_mode = 0
    return redirect(url_for(f'{current_page}'))


@app.route('/search',methods = ['POST','GET'])
def search():
    global current_page
    search_form = SearchForm()
    searched = search_form.text.data
    comments = Comment.query
    users = User.query
    comments = comments.filter(Comment.head.like('%' + searched +'%'))
    users = users.filter(User.username.like('%' + searched +'%'))
    comment_count = comments.filter(Comment.head.like('%' + searched +'%')).count()
    user_count = users.filter(User.username.like('%' + searched +'%')).count()
    return render_template('search.html',comments = comments,users = users,comment_count = comment_count,user_count = user_count)

@app.route('/delete_reply/<int:reply_id>',methods = ['POST','GET'])   
def delete_reply(reply_id):
    global current_page,current_user
    reply_to_delete = database.get_or_404(Subcomment,reply_id)
    comment_id = reply_to_delete.comment_id
    current_user.reply -= 1
    database.session.delete(reply_to_delete)
    database.session.commit()
    if current_page == "profile":
        return redirect(url_for('profile'))
    return redirect(url_for('show_comment',comment_id = comment_id))
    

@app.route('/admin_panel',methods = ['POST','GET'])   
def for_admin(): 
    global current_page
    current_page = "for_admin"
    database_form = DatabaseForm()
    if database_form.validate_on_submit():
        new_icon = icon(link = database_form.icon_link.data)
        database.session.add(new_icon)
        database.session.commit()
    users = database.session.execute(database.select(User)).scalars().all()
    return render_template('database_control.html',database_form = database_form,users = users)

mail_flash = None
@app.route('/contact/<int:user_id>',methods = ['POST','GET'])
def contact(user_id): 
    global current_page,from_email,current_user_id,mail_flash
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        user = database.get_or_404(User,user_id)
        mail_flash = "Email sent sucessfully"
        body = contact_form.body.data
        send_mail(user.email,from_email,body)
        return render_template('contact.html',contact_form = contact_form,mail_flash = mail_flash)
    mail_flash = None
    return render_template('contact.html',contact_form = contact_form,mail_flash = mail_flash)

admin_flash = None
@app.route('/addremove/<int:user_id>',methods = ['POST','GET'])
def addremove(user_id): 
    global current_page,admin_flash
    user = database.get_or_404(User,user_id)
    if user.admin == 1:
        user.admin = 0
        admin_flash = f"{user.username} is not subadmin"
    else:
        admin_flash = f"{user.username} is now subadmin"
        user.admin = 1
    database.session.commit()
    return redirect(url_for('comment_profile', user_id=user_id))


@app.route('/download/<int:comment_id>', methods=['GET'])
def download(comment_id):
    global percent_gt_01,percent_lt_minus01,percent_between_minus01_to_01
    labels = ['> 0.1', '< -0.1', '-0.1 to 0.1']
    sizes = [percent_gt_01, percent_lt_minus01, percent_between_minus01_to_01]
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Numbers')
    plt.savefig(f'pie-data-{comment_id}.pdf', format='pdf')

    file_path = f"pie-data-{comment_id}.pdf" 
    try:
        # Send the file to the client for download
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/about')
def about():
    global current_page
    current_page = "about"
    return render_template('about.html')

user_data = None
def generate_api_key(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/developer', methods=['POST', 'GET'])
def developer():    
    global user_data,current_user_id,current_page
    current_page = "developer"
    user = database.get_or_404(User,current_user_id)
    if request.method == 'POST':     
        user.ApiKey = generate_api_key(length = 32)
        database.session.commit()
    return render_template('developer.html',user = user)


#CREATING API
@app.route('/all_users')
@is_logged
def get_all_users():
    all_data = database.session.execute(database.select(User).order_by(User.id)).scalars().all()
    users = {"Users" : []}
    
    user = database.get_or_404(User,current_user_id)
    if user.ApiKey:
        for data in all_data:
            users['Users'].append({
            "id" : data.id,
            "username" : data.username,
            "icon_link" : data.icon,
            "email" : data.email,
            "created_on" : data.created,
            "total_polls" : data.poll,
            "total_replies" : data.reply
            })
        return jsonify(users) 
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    
    
@is_logged    
@app.route('/all_polls')
def get_all_polls():
    all_data = database.session.execute(database.select(Comment).order_by(Comment.id)).scalars().all()
    poll= {"polls" : []}
    user = database.get_or_404(User,current_user_id)
    if user.ApiKey:
        for data in all_data:
            poll['polls'].append({
            "id" : data.id,
            "upvote" : data.upvote,
            "downvote" : data.downvote,
            "head" : data.head,
            "created_on" : data.date,
            "body" : data.body,
            "is_anonymous" : data.anonymous
            })
        return jsonify(poll) 
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


@app.route('/add_reply',methods=['POST'])
def add_reply():
    user = database.get_or_404(User,current_user_id)

    if user.ApiKey:
        new_reply = Subcomment(
        body = request.form.get('body'),
        upvote = request.form.get('upvote'),
        downvote = request.form.get('downvote'),
        user_id = request.form.get('user_id'),
        comment_id = request.form.get('comment_id'),
        date = request.form.get('date'),
        anonymous = request.form.get('anonymous'),
        color =  request.form.get('color'),
        intensity = request.form.get('intensity')
    )
        database.session.add(new_reply)
        database.session.commit()
        return jsonify(response={"success": "All the replies have been added to the desired poll"})
    
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    
if __name__ == "__main__":
    app.run(debug=True)
