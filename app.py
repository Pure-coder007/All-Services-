from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from mysql.connector import Error
from email_validator import validate_email, EmailNotValidError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import random
from flask_mail import Mail, Message
from db_setup import setup_database, config
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256_crypt
from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, configure_uploads, IMAGES
import calendar
from datetime import datetime
# from models import get_user_id

import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name = "duyoxldib",
    api_key = "778871683257166", 
  api_secret = "NM2WHVuvMytyfnVziuzRScXrrNk"
)






app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/assets/img'
configure_uploads(app, photos)


class UpdateProfileForm(FlaskForm):
    username = StringField('Username')
    phone_number = StringField('Phone Number')
    profile_picture = FileField('Profile Picture', validators=[
        FileAllowed(photos, 'Images only!')
    ])



# login_manager = LoginManager(app)
# # login_manager.init_app(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'


# @login_manager.user_loader
# def load_user(user_id):
#     user = get_user_id(user_id)
#     return user



app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'assets', 'img')
# flask mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'kingsleydike318@gmail.com'
app.config['MAIL_PASSWORD'] = ' pblfcvwhfwnujtll'
MAIL_USE_TLS = False
SECRET_KEY = 'language007'



# Flask Mail Configuration
mail = Mail(app)


# Otp function
def send_otp(email, otp):
    msg = Message('Verification Token', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your verification token is {otp}'
    print('otp : ', otp)
    mail.send(msg)





@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/services", methods=['GET', 'POST'])
def services():
    return render_template("services.html")


@app.route("/signup_user", methods=['GET', 'POST'])
def signup_user():
    return render_template("signup_user.html")



@app.route("/signup_worker", methods=['GET', 'POST'])
def signup_worker():
    return render_template("signup_worker.html")




if __name__ == "__main__":
    app.run(debug=True)