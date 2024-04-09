from flask import Flask,render_template,redirect,url_for,abort,request,send_file
from flask_bootstrap import Bootstrap5
from forms import LoginForm,RegisterForm,CommentForm,DatabaseForm,OtpForm,EditProfileForm,SearchForm,ReplyForm,ContactForm
from flask_ckeditor import CKEditor

from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash


from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import relationship,DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String, Boolean,func,Float,LargeBinary

import random
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from functools import wraps
import base64

logged_in = 0
not_registering = 1
current_user_id = 0
otp_send = 0
anonymous_mode = 0

random_username = None
current_user_email = None
user_otp = None
current_user = None
username = None
user_icon = None
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

app.config['SECRET_KEY']="mrpvproject"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///polling.db"


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


#Creating tables
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
    global logged_in, not_registering, current_user_id, otp_send, anonymous_mode,current_page,admin_flash
    global current_user_email, user_otp, current_user, username, user_icon,random_username
    words_list = ["ShadowSeeker", "WhisperWanderer", "VeilVoyager", "EchoExplorer", "SilentSleuth", "ShadeShifter", "PhantomProwler", "IncognitoInquirer", "StealthStroller", "EnigmaRoamer"]
    random_username = random.choice(words_list)

    return dict(logged_in = logged_in,
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
                random_username = random_username)
    
@app.route('/register',methods = ['GET','POST'])
def register():
    global not_registering,current_user_id,current_user,logged_in
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
                phoneNo = register_form_object.phoneNo.data,
                poll = 0,
                reply = 0
            )
            database.session.add(new_user)
            database.session.commit()
            current_user = new_user
            logged_in = 1
            current_user_id = current_user.id
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
    global logged_in,current_user,current_user_id,current_user_email
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
                print(f"here!!!!!!!!! {current_user_id}")
                current_user = user
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
    global current_user_id,current_user,login_form,current_page
    if current_user != None:
        print(current_user.username,current_user.icon)
    login_form = LoginForm()
    all_comments = database.session.execute(database.select(Comment)).scalars().all()

    api_url = 'https://api.api-ninjas.com/v1/quotes?category=success'
    QUOTE_API_KEY = '9No6wnmZqzRC/NRH0VvxHA==QRYgA94Njvme77Wg'
    quote = requests.get(api_url, headers={'X-Api-Key': QUOTE_API_KEY}).json()[0]
    quote_text = f"'{quote['quote']}' - {quote['author']}"
    print(f"current user id is ---> {current_user_id}")
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
    current_user = database.session.execute(database.select(User).where(User.id == current_user_id)).scalar()
    profile_form = EditProfileForm()
    if profile_form.validate_on_submit():
        if len(profile_form.ProfilePic.data)!=0:
            current_user.icon = profile_form.ProfilePic.data 
        if  len(profile_form.username.data)!=0:    
            current_user.username = profile_form.username.data
        if len(profile_form.password.data)!=0:    
            current_user.password =  generate_password_hash( profile_form.password.data, method='pbkdf2:sha256',salt_length=8)  
        if profile_form.SelectPic.data is not None:   
            print("done!!") 
            current_user.uicon = profile_form.SelectPic.data.read()
            print(profile_form.SelectPic.data.read())
            print("this is being printed and this is here")
        database.session.commit()   
        return redirect(url_for('profile'))
    
    
    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == current_user_id)).scalars().all()

    comments = database.session.execute(database.select(Comment).where(Comment.userId == current_user_id)).scalars().all()

    all_replies = database.session.execute(database.select(Subcomment).where(Subcomment.user_id == current_user.id)).scalars().all()
    intensities = [i.intensity for i in all_replies]

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
                           all_replies = all_replies)
    
    return render_template('profile.html',
                           length = len(intensities),
                           all_replies  = all_replies ,
                           comments = comments,
                           profile_form = profile_form)
 
@app.route('/comment_profile/<int:user_id>',methods = ['GET','POST'])
def comment_profile(user_id):
    print(f"the user id is {user_id}")
    global current_page
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
            print("done!!") 
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

    if comment_form.validate_on_submit():
        new_comment = Comment(
            head = comment_form.head.data,
            body = comment_form.body.data,
            bg_image = comment_form.bg_image.data,
            date = format_time_and_date(datetime.now()),
            userId = current_user.id ,
            anonymous = anonymous_mode if anonymous_mode else anonymous_mode
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
@app.route('/comment/<int:comment_id>',methods = ['GET','POST'])
def show_comment(comment_id):
    global current_page,anonymous_mode,current_user,percent_gt_01,percent_lt_minus01,percent_between_minus01_to_01
    chosen_comment = database.session.execute(database.select(Comment).where(Comment.id == comment_id)).scalar()
    reply_form = ReplyForm()
    body = str(reply_form.body.data)
    polarity = analyze_sentiment(body)
    if reply_form.validate_on_submit():
        print(f"THE POLARITY IS {polarity} and the color is { map_polarity_to_color(polarity)}")
        parent_user = database.session.execute(database.select(User).where(User.id == chosen_comment.userId)).scalar()
        date = format_time_and_date(datetime.now())
        print(polarity)
        new_reply = Subcomment(
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
                    <a href="pollverse-fqol.onrender.com" style="text-decoration: none; color: inherit;">
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
    global otp_send,current_user_email,current_user_id,user_otp,current_user,logged_in,from_email,app_pass
    otp_form = OtpForm()
    random_otp = ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for i in range(6))
    print(f"value of otp sent is {otp_send}")
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
        send_mail(from_email,current_user.email,body)

        return render_template('index.html', otp_form=otp_form, error=1)
    print(current_user_email)
    print(f"USER ENTERED OTP = {otp_form.OTP.data}")
    print(f"OTP = {user_otp}")
    if otp_form.OTP.data == user_otp:
        otp_send = 0
        logged_in = 1
        
        print(f"this is the user {current_user}")
        login_user(current_user)
        current_user_id = current_user.id
        return redirect(url_for('index'))
    else:
        error = "Entered Wrong OTP"
        otp_send = 0
        return render_template('index.html',error = error) 
   
@app.route('/anonymous')  
def anonymous():
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
    database_form = DatabaseForm()
    if database_form.validate_on_submit():
        new_icon = icon(link = database_form.icon_link.data)
        database.session.add(new_icon)
        database.session.commit()
    users = database.session.execute(database.select(User)).scalars().all()
    print(users)
    return render_template('database_control.html',database_form = database_form,users = users)

mail_flash = None
@app.route('/contact/<int:user_id>',methods = ['POST','GET'])
def contact(user_id): 
    global current_page,from_email,current_user_id,mail_flash
    current_page = "contact"
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        user = database.get_or_404(User,user_id)
        mail_flash = "Email sent sucessfully"
        body = contact_form.body.data
        send_mail(user.email,from_email,body)
        print("here !!")
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
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)