from flask import Flask,render_template,redirect,url_for,abort,request
from flask_bootstrap import Bootstrap5
from forms import LoginForm,RegisterForm,CommentForm,DatabaseForm,OtpForm,EditProfileForm,SearchForm,ReplyForm
from flask_ckeditor import CKEditor

from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash


from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import relationship,DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String, Boolean,func,Float

import random
import requests
from datetime import datetime
import os
from functools import wraps
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from textblob import TextBlob


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

from_email = "xieminiproject@gmail.com"
app_pass = "omni tvxy oelb dctl"

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

# Functions
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
        return f'#f77878'  
    elif polarity > 0.1:  # positive
        return f'#bef7be'  
    else:                 # neautral
        return f'#808080' 



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
            database.session.add(new_user)
            database.session.commit()
            user_obj = new_user
            logged_in = 1
            current_user_id = user_obj.id
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
            user_obj = user
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
    QUOTE_API_KEY = '9No6wnmZqzRC/NRH0VvxHA==QRYgA94Njvme77Wg'
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
        if len(profile_form.ProfilePic.data)!=0:
            user_obj.icon = profile_form.ProfilePic.data 
        if  len(profile_form.username.data)!=0:    
            user_obj.username = profile_form.username.data
        if len(profile_form.password.data)!=0:    
            user_obj.password =  generate_password_hash( profile_form.password.data, method='pbkdf2:sha256',salt_length=8)
        database.session.commit()   
        return redirect(url_for('profile'))
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == current_user_id)).scalars().all()
    print(all_replies)
    comments = database.session.execute(database.select(Comment).where(Comment.userId == current_user_id)).scalars().all()
    print(comments)
    return render_template('profile.html',
                           all_replies  = all_replies ,
                           comments = comments,
                           profile_form = profile_form,
                           current_user_id = current_user_id)
 
@app.route('/comment_profile/<int:user_id>',methods = ['GET','POST'])
def comment_profile(user_id):
    print(f"the user id is {user_id}")
    global current_page
    current_page = 'comment_profile'
    comment_user = database.get_or_404(User,user_id)
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == user_id)).scalars().all()
    print(all_replies)
    comments = database.session.execute(database.select(Comment).where(Comment.userId == user_id)).scalars().all()
    print(comments)
    return render_template('comment_profile.html',
                           comment_user = comment_user,
                           all_replies  = all_replies ,
                           comments = comments) 
 
    
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
            date = format_time_and_date(datetime.now()),
            userId = current_user.id ,
            anonymous = anonymous_mode if anonymous_mode else anonymous_mode
        )
        database.session.add(new_comment)
        database.session.commit()
        return redirect(url_for("index"))
    current_page = 'new_comment'
    return render_template('new_comment.html',comment_form = comment_form) 

@app.route('/comment/<int:comment_id>',methods = ['GET','POST'])
def show_comment(comment_id):
    global current_page,anonymous_mode
    chosen_comment = database.session.execute(database.select(Comment).where(Comment.id == comment_id)).scalar()
    reply_form = ReplyForm()
    body = str(reply_form.body.data)
    polarity = analyze_sentiment(body)
    if reply_form.validate_on_submit():
        print(f"THE POLARITY IS {polarity} and the color is { map_polarity_to_color(polarity)}")
        new_reply = Subcomment(
        body = body,
        user_id = current_user_id,
        comment_id = comment_id,
        date = format_time_and_date(datetime.now()),
        anonymous = anonymous_mode if anonymous_mode else anonymous_mode,
        color =  map_polarity_to_color(polarity),
        intensity = polarity
        )
        
        database.session.add(new_reply)
        database.session.commit()
        return redirect(url_for('show_comment',comment_id = comment_id))
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.comment_id == comment_id)).scalars().all()
    
    intensities = [i.intensity for i in all_replies]
    print(intensities)
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
    global otp_send,current_user_email,current_user_id,user_otp,user_obj,logged_in,from_email,app_pass
    otp_form = OtpForm()
    random_otp = ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for i in range(6))
    print(f"value of otp sent is {otp_send}")
    if otp_send == 0:
        import smtplib
        otp_send = 1
        user_otp = random_otp
        body = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>OTP Email</title>
            </head>
            <body style="font-family: Arial, sans-serif; background-image: linear-gradient(to bottom right, #ffffcc, #ffcc66); padding: 20px;">
                <div style="max-width: 600px; margin: auto; background-image: linear-gradient(to bottom right, #FFD700, #FFFF00); border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                    <p style="font-size: 18px; color: #666;">NOTE: This OTP is valid for only one time.</p>
                    <h1 style="font-size: 36px; color: #333; text-shadow: 2px 2px 2px rgba(0, 0, 0, 0.2);">YOUR OTP: <span style="color: #009688;">{random_otp}</span></h1>
                    <img src="https://img.freepik.com/premium-vector/secure-email-otp-authentication-verification-method_258153-468.jpg" alt="OTP Image" style="display: block; margin: 20px auto; max-width: 100%; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                </div>
            </body>
            </html>
            """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user=from_email, password=app_pass)

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = user_obj.email
        msg['Subject'] = "Your OTP"

        msg.attach(MIMEText(body, 'html'))

        server.sendmail(from_email, user_obj.email, msg.as_string())
        server.quit()

        # Render template with OTP form and error flag
        return render_template('index.html', otp_form=otp_form, error=1)
    print(current_user_email)
    print(f"USER ENTERED OTP = {otp_form.OTP.data}")
    print(f"OTP = {user_otp}")
    if otp_form.OTP.data == user_otp:
        otp_send = 0
        logged_in = 1
        
        print(f"this is the user {user_obj}")
        login_user(user_obj)
        current_user_id = user_obj.id
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
    return redirect(url_for(f'{current_page}'))


@app.route('/search',methods = ['POST','GET'])
def search():
    search_form = SearchForm()
    searched = search_form.text.data
    comments = Comment.query
    comments = comments.filter(Comment.head.like('%' + searched +'%'))
    users = User.query
    users = users.filter(User.username.like('%' + searched +'%'))
    return render_template('search.html',comments = comments,users = users)


@app.route('/sidenav',methods = ['POST','GET'])
def sidenav():
    global sidenav,current_page
    if sidenav == 0:
        sidenav = 1
    else:
        sidenav = 0
    return redirect(url_for(f'{current_page}'))
 
@app.route('/delete_reply/<int:reply_id>',methods = ['POST','GET'])   
def delete_reply(reply_id):
    global current_page
    reply_to_delete = database.get_or_404(Subcomment,reply_id)
    comment_id = reply_to_delete.comment_id
    database.session.delete(reply_to_delete)
    database.session.commit()
    if current_page == "profile":
        return redirect(url_for('profile'))
    return redirect(url_for('show_comment',comment_id = comment_id))
    


@app.route('/admin_panel',methods = ['POST','GET'])   
@admin_only
def for_admin():
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