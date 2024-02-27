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
from models import get_user, add_user, get_all_users, User, get_user_id, get_worker, add_worker

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


# class UpdateProfileForm(FlaskForm):
#     username = StringField('Username')
#     phone_number = StringField('Phone Number')
#     profile_picture = FileField('Profile Picture', validators=[
#         FileAllowed(photos, 'Images only!')
#     ])



login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    user = get_user_id(user_id)
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("Login to access this page", category="info")
    return redirect(url_for("login_for_user"))



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





# Token for email verification for user
@app.route('/token_user/<email>', methods=['GET', 'POST'])
def token_user(email):
    if request.method == 'POST':
        token = request.form.get('otp')
        stored_otp = session.get('otp', None)
        if token != str(stored_otp):
            print('token', stored_otp)
            print('stored otp', stored_otp)
            flash('Invalid token. Please try again.', 'danger')
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login_for_user'))
    return render_template('token_user.html', current_user=current_user)
            



# Token for email verification for user
@app.route('/token_worker/<email>', methods=['GET', 'POST'])
def token_worker(email):
    if request.method == 'POST':
        token = request.form.get('otp')
        stored_otp = session.get('otp', None)
        if token != str(stored_otp):
            print('token', stored_otp)
            print('stored otp', stored_otp)
            flash('Invalid token. Please try again.', 'danger')
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login_for_worker'))
    return render_template('token_worker.html', current_user=current_user)
            




@app.route("/signup_user", methods=['GET', 'POST'])
def signup_user():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            hashed_password = sha256_crypt.hash(password)
            profile_pic = request.files['profile_picture']
            phone_number = request.form['phone_number']
            country = request.form['country']
            state = request.form['state']
            local_govt = request.form['local_govt']
            address = request.form['address']

            print(name, email, hashed_password, profile_pic, phone_number, country, state, local_govt, address)

            if not name or not email or not password or not profile_pic or not phone_number or not country or not state or not local_govt or not address:
                flash('Please fill in all fields', 'danger')

            if get_user(email):
                flash('Email already exists', 'danger')
                return redirect(url_for('signup_user'))
            
            if profile_pic:
                filename = secure_filename(profile_pic.filename)
                response = cloudinary.uploader.upload(profile_pic, public_id=f"users/{filename}")
                profile_pic = response['secure_url']
            
            add_user(name, email, hashed_password, profile_pic, phone_number, country, state, local_govt, address)
            connection.commit()

            # Generate OTP and send verification email
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            send_otp(email, otp)
            print(email, otp)

            flash('Registration successful. Please check your email for verification token.', 'success')
            return redirect(url_for('token_user', email=email))
        get_all_users()
        return render_template("signup_user.html")
    except Exception as e:
        print(e)
        print(e)
        print(e)
        return render_template('signup_user.html', current_user=current_user)
    finally:
        cursor.close()
        connection.close()








@app.route("/signup_worker", methods=['GET', 'POST'])
def signup_worker():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            hashed_password = sha256_crypt.hash(password)
            profile_pic = request.files['profile_picture']
            phone_number = request.form['phone_number']
            country = request.form['country']
            state = request.form['state']
            local_govt = request.form['local_govt']
            address = request.form['address']
            company = request.form['company']
            service = request.form['service']
            description = request.form['description']
            rate = request.form['rate']
            work_pic1 = request.files['work_pic1']
            work_pic2 = request.files['work_pic2']
            work_pic3 = request.files['work_pic3']
            

            print(name, email, hashed_password, profile_pic, phone_number, country, state, local_govt, address, company, service, description, rate, work_pic1, work_pic2, work_pic3)

            if not name or not email or not password or not profile_pic or not phone_number or not country or not state or not local_govt or not address or not company or not service or not work_pic1 or not work_pic2 or not work_pic3 or not description or not rate:
                flash('Please fill in all fields', 'danger')

            if get_worker(email):
                flash('Email already exists', 'danger')
                return redirect(url_for('signup_worker'))
            
            if profile_pic:
                filename = secure_filename(profile_pic.filename)
                response = cloudinary.uploader.upload(profile_pic, public_id=f"workers/{filename}")
                profile_pic = response['secure_url']
            
            if work_pic1:
                filename = secure_filename(work_pic1.filename)
                response = cloudinary.uploader.upload(work_pic1, public_id=f"workers/{filename}")
                work_pic1 = response['secure_url']
            
            if work_pic2:
                filename = secure_filename(work_pic2.filename)
                response = cloudinary.uploader.upload(work_pic2, public_id=f"workers/{filename}")
                work_pic2 = response['secure_url']

            if work_pic3:
                filename = secure_filename(work_pic3.filename)
                response = cloudinary.uploader.upload(work_pic3, public_id=f"workers/{filename}")
                work_pic3 = response['secure_url']
            
            add_worker(name, email, hashed_password, profile_pic, phone_number, country, state, local_govt, address, company, service,  description, rate, work_pic1, work_pic2, work_pic3)
            connection.commit()

            # Generate OTP and send verification email
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            send_otp(email, otp)
            print(email, otp)

            flash('Registration successful. Please check your email for verification token.', 'success')
            return redirect(url_for('token_worker', email=email))
        get_all_users()
        return render_template("signup_worker.html")
    except Exception as e:
        print(e)
        print(e)
        print(e)
        return render_template('signup_worker.html', current_user=current_user)
    finally:
        cursor.close()
        connection.close()





@app.route('/login_for_user', methods=['GET', 'POST'])
def login_for_user():
    if request.method == 'POST':
        email = request.form['email']   
        password = request.form['password']
        connection  = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            print(user, '******************')
            if user is not None:
                user_id = user['id']
                name = user['name']
                email = user['email']
                stored_password = user['password']
                profile_pic = user['profile_pic']
                phone_number = user['phone_number']
                country = user['country']
                state = user['state']
                local_govt = user['local_govt']
                address = user['address']


                if sha256_crypt.verify(password,  stored_password):
                    user = User(id=user_id, email=email, name=name, password=stored_password, profile_pic=profile_pic, phone_number=phone_number, country=country, state=state, local_govt=local_govt, address=address)
                    login_user(user)
                    # flash('Login Successful', 'success')
                    return redirect(url_for('user_index', user_id=user_id))
                else:
                    flash('Invalid Email or Password', 'danger')
                    return render_template('login_for_user.html', current_user=current_user)
            else:
                flash('Email not found', 'danger')
                return render_template('login_for_user.html', current_user=current_user)
        except Exception as e:
            print('Error during login', e)
            flash('Error during login. Please try again.', 'danger')
        finally:
            cursor.close()
    return render_template('login_for_user.html', current_user=current_user)





@app.route('/login_for_worker', methods=['GET', 'POST'])
def login_for_worker():
    if request.method == 'POST':
        email = request.form['email']   
        password = request.form['password']
        connection  = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM workers WHERE email = %s', (email,))
            user = cursor.fetchone()
            print(user, '******************')
            if user is not None:
                user_id = user['id']
                name = user['name']
                email = user['email']
                stored_password = user['password']
                profile_pic = user['profile_pic']
                phone_number = user['phone_number']
                country = user['country']
                state = user['state']
                local_govt = user['local_govt']
                address = user['address']
                company = user['company']
                service = user['service']


                if sha256_crypt.verify(password,  stored_password):
                    user = User(id=user_id, email=email, name=name, password=stored_password, profile_pic=profile_pic, phone_number=phone_number, country=country, state=state, local_govt=local_govt, address=address, company=company, service=service)
                    login_user(user)
                    flash('Login Successful', 'success')
                    return redirect(url_for('user_index', user_id=user_id))
                else:
                    flash('Invalid Email or Password', 'danger')
                    return render_template('login_for_worker.html', current_user=current_user)
            else:
                flash('Email not found', 'danger')
                return render_template('login_for_worker.html', current_user=current_user)
        except Exception as e:
            print('Error during login', e)
            flash('Error during login. Please try again.', 'danger')
        finally:
            cursor.close()
    return render_template('login_for_worker.html', current_user=current_user)





@app.route('/edit_user_profile', methods=['GET', 'POST'])
@login_required
def edit_user_profile():
    return render_template("edit_user_profile.html", current_user=current_user)



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))




def user_profile(user_id):
    # try:
    connection  = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT name, email, profile_pic, phone_number, country, state, local_govt, address FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))

    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        # print(user, 'user')
        return {
            'name': user['name'],
            'email': user['email'],
            'profile_pic': user['profile_pic'],
            'phone_number': user['phone_number'],
            'country': user['country'],
            'state': user['state'],
            'local_govt': user['local_govt'],
            'address': user['address'],
        }
    
    else:
        return {}




def get_service(service):
    connection  = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM workers WHERE service = %s"
    cursor.execute(query, (service,))

    worker = cursor.fetchall()
    cursor.close()
    connection.close()

    if worker:
        # print(worker, 'worker')
        return worker
    else:
        print('no record found')
        return {}




@app.route('/user_index/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_index(user_id):
    user = user_profile(user_id)
    # print(user)

    all_workers = []

    if request.method == 'POST':
        services = ['ac_gas_filling', 'ac_repair_and_installation', 'refrigerator_repair', 'auto_repair', 'car_ac_repair', 'car_rewire', 'barber', 'hair_stylist', 'human_hair', 'nail_technician', 'pedicure_manicure', 'catering_service', 'plumber', 'laundry_service', 'dispatch_rider', 'electrical', 'generator', 'haulage', 'painter', 'photographer', 'event', 'cosmetic', 'taxi_service', 'personal_trainer', 'elderly_care', 'dstv', 'welder']

        service_results = []

        for service in services:
            if request.form.get(service):
                workers = get_service(service)
                service_results.extend(workers)

        all_workers = list({worker['id']: worker for worker in service_results}.values())
        print(all_workers, 'all workerssssssssssssssssssss')
        session['all_workers'] = all_workers
        return redirect(url_for('services'))




    return render_template("user_index.html", current_user=current_user, user=user, user_id=user_id)








@app.route('/services', methods=['GET'])
def services():
    workers = session.get('all_workers')
    print(workers, '3333333333333333333333333333333333333')
    # Render the results
    return render_template('services.html', workers=workers)






# View Worker profile
def get_worker_id(worker_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        query = "SELECT id, name, email, password, profile_pic, phone_number, country, state, local_govt, address, company, service, description, rate, work_pic1, work_pic2, work_pic3 FROM workers WHERE id = %s"
        cursor.execute(query, (worker_id,))

        worker = cursor.fetchone()

        cursor.close()
        connection.close()

        if worker:
            return{
                'id': worker[0],
                'name': worker[1],
                'email': worker[2],
                'password': worker[3],
                'profile_pic': worker[4],
                'phone_number': worker[5],
                'country': worker[6],
                'state': worker[7],
                'local_govt': worker[8],
                'address': worker[9],
                'company': worker[10],
                'service': worker[11],
                'description': worker[12],
                'rate': worker[13],
                'work_pic1': worker[14],
                'work_pic2': worker[15],
                'work_pic3': worker[16]
            }
        else:
            return {}
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {}
    

@app.route('/item_profile/<int:worker_id>')
@login_required
def item_profile(worker_id):
    worker = get_worker_id(worker_id)
    print(worker)
    return render_template('item_profile.html', worker_id=worker_id, worker=worker)






# Reviews 


from datetime import datetime  # Import datetime module
from datetime import datetime  # Import datetime module

@app.route('/reviews/<int:worker_id>', methods=['GET', 'POST'])
@login_required
def reviews(worker_id):
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        satisfy = request.form.get('satisfy')
        suggestions = request.form.get('msg')

        # Get the current user ID
        user_id = current_user.id

        # Convert 'yes' and 'no' to boolean values
        enjoy_service = 1 if satisfy == 'yes' else 0

        # Save the data to the database
        try:
            connection = mysql.connector.connect(**config)
            with connection.cursor() as cursor:
                # Insert the data into the worker_reviews table
                sql = """INSERT INTO worker_reviews (user_id, worker_id, name, email, phone_number, enjoy_service, suggestions, created_at)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

                cursor.execute(sql, (user_id, worker_id, name, email, phone_number, enjoy_service, suggestions, datetime.now()))
                connection.commit()

                flash('Review submitted successfully', 'success')
                return redirect(url_for('view_reviews', worker_id=worker_id)) 

        except Exception as e:
            print(f"Error: {e}")
            flash('An error occurred while submitting the review', 'danger')

        finally:
            connection.close()
        return redirect(url_for('reviews', worker_id=worker_id))

    return render_template('reviews.html', current_user=current_user)








from datetime import datetime


# View Reviews
@app.route('/view_reviews/<int:worker_id>', methods=['GET', 'POST'])
@login_required
def view_reviews(worker_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "SELECT name, enjoy_service, suggestions, created_at FROM worker_reviews WHERE worker_id = %s ORDER BY created_at DESC"
    cursor.execute(query, (worker_id,))

    reviews = cursor.fetchall()
    cursor.close()
    connection.close()

    # Convert the creatd format before passing it to the template
    formatted_reviews = [(name, enjoy_service, suggestions, created_at.strftime('%Y %b %d') if created_at is not None else None) for name, enjoy_service, suggestions, created_at in reviews]
    print(formatted_reviews)


    return render_template('view_reviews.html', reviews=formatted_reviews, worker_id=worker_id)




if __name__ == "__main__":
    app.run(debug=True)