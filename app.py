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
# from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
# from flask_uploads import UploadSet, configure_uploads, IMAGES
import calendar
from datetime import datetime
from models import get_user, add_user, get_all_users, User, get_user_id, get_worker, add_worker, contact_me, update_user_profile, Worker, get_worker_id, gen_ran_string, Admin, add_admin, get_admin_id, update_worker_profile

import cloudinary
import cloudinary.uploader
import string

cloudinary.config(
    cloud_name = "duyoxldib",
    api_key = "778871683257166", 
  api_secret = "NM2WHVuvMytyfnVziuzRScXrrNk"
)






app = Flask(__name__)
# photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/assets/img'
# configure_uploads(app, photos)


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
    print(user, 'user')
    if not user:
        worker_dict = get_worker_id(user_id)
        # print(worker_dict, 'worker_dict')
        if worker_dict:
            user = Worker(**worker_dict)
        else:
            user = get_admin_id(user_id)
            
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
    # hashed = sha256_crypt.hash('password')
    # add_admin(555, "kingsley", 'kingsleydike318@gmail.com', hashed )
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
            return redirect(url_for('token_user', email=email))
        # flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login_for_user'))
    return render_template('token_user.html', current_user=current_user)
            



# Token for email verification for user
@app.route('/token_worker/<email>/<worker_id>', methods=['GET', 'POST'])
def token_worker(email, worker_id):
    if request.method == 'POST':
        token = request.form.get('otp')
        stored_otp = session.get('otp', None)
        if token != str(stored_otp):
            print('token', stored_otp)
            print('stored otp', stored_otp)
            flash('Invalid token. Please try again.', 'danger')
            return redirect(url_for('token_worker', email=email, worker_id=worker_id))
        # flash('Registration successful. Please login.', 'success')
        return redirect(url_for('payment', worker_id=worker_id))
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
        # get_all_users()
        return render_template("signup_user.html")
    except KeyError as e:
        print(e, 'key error')
    except Exception as e:
        print(e)
        print(e)
        print(e)
        return render_template('signup_user.html', current_user=current_user)
    finally:
        cursor.close()
        connection.close()













def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))










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
            
            # special_characters = "!@#$%^&*()_+[]{}|;:,.<>?/~`"
            # if len(password) < 8 or not any(char.isupper() for char in password) or not any(char in special_characters for char in password):
            #     flash('Password must be at least 8 characters long, contain at least one uppercase letter, and include a special character', 'danger')
                # return redirect(url_for('signup_worker'))

            # print(name, email, hashed_password, profile_pic, phone_number, country, state, local_govt, address, company, service, description, rate, work_pic1, work_pic2, work_pic3)

            if not name or not email or not password or not profile_pic or not phone_number or not country or not state or not local_govt or not address or not company or not service or not work_pic1 or not work_pic2 or not work_pic3 or not description or not rate:
                flash('Please fill in all fields', 'danger')
                print(name, email, hashed_password, profile_pic, phone_number, country, state, local_govt, address, company, service, description, rate, work_pic1, work_pic2, work_pic3, "alllllllllllllllllllllllllllllllllllllllll")

            if get_worker(email):
                flash('Email already exists', 'danger')
                return redirect(url_for('signup_worker'))
            
            if profile_pic:
                response = cloudinary.uploader.upload(profile_pic, public_id=f"workers/{generate_random_id()}")
                profile_pic = response['secure_url']
            
            if work_pic1:
                response = cloudinary.uploader.upload(work_pic1, public_id=f"workers/{generate_random_id()}")
                work_pic1 = response['secure_url']
            
            if work_pic2:
                response = cloudinary.uploader.upload(work_pic2, public_id=f"workers/{generate_random_id()}")
                work_pic2 = response['secure_url']

            if work_pic3:
                response = cloudinary.uploader.upload(work_pic3, public_id=f"workers/{generate_random_id()}")
                work_pic3 = response['secure_url']
            
            worker = add_worker(name, email, hashed_password, profile_pic, phone_number, country, state, local_govt, address, company, service,  description, rate, work_pic1, work_pic2, work_pic3)
            worker_id = worker[0]
            connection.commit()

            # Generate OTP and send verification email
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            send_otp(email, otp)
            print(email, otp)

            flash('Registration successful. Please check your email for verification token.', 'success')
            return redirect(url_for('token_worker', email=email, worker_id=worker_id))
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

                if email == 'kingsleydike318@gmail.com' and password == 'password':
                    return redirect(url_for('admin'))


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
        print(email, '00000000333333333333333333333333')
        connection  = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM workers WHERE email = %s', (email,))
            worker = cursor.fetchone()
            # print(worker, '99999999999999999')
            if worker is not None:
                user_id = worker['id']
                name = worker['name']
                email = worker['email']
                stored_password = worker['password']
                profile_pic = worker['profile_pic']
                phone_number = worker['phone_number']
                country = worker['country']
                state = worker['state']
                local_govt = worker['local_govt']
                address = worker['address']
                company = worker['company']
                service = worker['service']


                if sha256_crypt.verify(password,  stored_password):
                    worker = Worker(id=user_id, name=name, email=email, password=stored_password, profile_pic=profile_pic, phone_number=phone_number, country=country, state=state, local_govt=local_govt, address=address, company=company, service=service)
                    login_user(worker)
                    # flash('Login Successful', 'success')
                    print(user_id, 'user id', current_user.id, 'current user id', current_user, 'current user', name, 'email', email, 'password', password, 'profile_pic', profile_pic, 'phone_number', phone_number, 'country', country, 'state', state, 'local_govt', local_govt, 'address', address, '0000000000000000000000000')
                    return redirect(url_for('worker_index', user_id=user_id))
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




@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']   
        password = request.form['password']
        print(email, '00000000333333333333333333333333')
        connection  = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM admin WHERE email = %s', (email,))
            admin = cursor.fetchone()
            print(admin, '99999999999999999')
            if admin is not None:
                user_id = admin['id']
                name = admin['name']
                email = admin['email']
                stored_password = admin['password']
                print(admin, )

                if sha256_crypt.verify(password,  stored_password):
                    admin = Admin(id=user_id, name=name, email=email, password=stored_password)
                    login_user(admin)
                    return redirect(url_for('admin'))
                else:
                    flash('Invalid Email or Password', 'danger')
                    return render_template('admin_login.html', current_user=current_user)

        except Exception as e:
            print('Error during login', e)
            flash('Error during login. Please try again.', 'danger')
        finally:
            cursor.close()
    return render_template('admin_login.html', current_user=current_user)










@app.route('/edit_user_profile', methods=['GET', 'POST'])
@login_required
def edit_user_profile():
    print(current_user.name, 'current user')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        country = request.form['country']
        state = request.form['state']
        local_govt = request.form['local_govt'] 
        address = request.form['address']
        profile_pic = request.files['profile_pic']

        user_id = current_user.id

        try:
            if profile_pic:
                filename = secure_filename(profile_pic.filename)
                response = cloudinary.uploader.upload(profile_pic, public_id=f"users/{user_id}/{filename}")
                profile_pic_url = response['secure_url']

            if get_user(email):
                flash('Email already exists', 'danger')
                return redirect(url_for('edit_user_profile'))
            
            update_user_profile(user_id, name, email, phone_number, country, state, local_govt, address, profile_pic_url)
            flash('Profile updated successfully', 'success')
            print(name, email, phone_number, country, state, local_govt, address, profile_pic_url, '///////////////////////////////')
            return redirect(url_for('user_index', user_id=user_id))

        except Exception as e:
            print(f'Error: {e}')
            flash('Error updating profile', 'danger')
    return render_template("edit_user_profile.html", current_user=current_user)





@app.route('/edit_worker_profile', methods=['GET', 'POST'])
@login_required
def edit_worker_profile():
    print(current_user.name, 'current user')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        country = request.form['country']
        state = request.form['state']
        local_govt = request.form['local_govt'] 
        address = request.form['address']
        profile_pic = request.files['profile_pic']
        description = request.form['description']
        rate = request.form['rate']
        company = request.form['company']
        print(name, email, phone_number, country, state, local_govt, address, profile_pic, description, rate, company)

        user_id = current_user.id

        try:
            if profile_pic:
                filename = secure_filename(profile_pic.filename)
                response = cloudinary.uploader.upload(profile_pic, public_id=f"workers/{user_id}/{filename}")
                profile_pic_url = response['secure_url']
            else:
                profile_pic_url = current_user.profile_pic

            if get_user(email):
                flash('Email already exists', 'danger')
                return redirect(url_for('edit_worker_profile'))
            
            # update_worker_profile(user_id, name, email, phone_number, country, state, local_govt, address, profile_pic_url, description,  rate, company)
            update_worker_profile(user_id, name, email, phone_number, country, state, local_govt, address, profile_pic_url, description, rate, company)
            flash('Profile updated successfully', 'success')
            print(name, email, phone_number, country, state, local_govt, address, profile_pic_url, '///////////////////////////////')
            return redirect(url_for('worker_index', user_id=user_id))
        except Exception as e:
            print(f'Error: {e}')
            flash('Error updating profile', 'danger')
    
    return render_template("edit_worker_profile.html", current_user=current_user)













@app.route('/worker_profile', methods=['GET', 'POST'])
@login_required
def worker_profile():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM workers WHERE id = %s"
        cursor.execute(query, (current_user.id,))

        worker = cursor.fetchone()
        print(worker)

        cursor.close()
        connection.close()
    except Exception as e:
        print(f'Error: {e}')
        flash('Error fetching worker profile', 'danger')
    return render_template("worker_profile.html", current_user=current_user, worker=worker)










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
    







def worker_profile(user_id):
    # try:
    connection  = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM workers WHERE id = %s"
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
            'service': user['service'],
            'rate': user['rate'],
            'company': user['company'],
            'description': user['description'],
            'work_pic1': user['work_pic1'],
            'work_pic2': user['work_pic2'],
            'work_pic3': user['work_pic3']
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




@app.route('/user_index/<string:user_id>', methods=['GET', 'POST'])
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








@app.route('/worker_index/<string:user_id>', methods=['GET', 'POST'])
@login_required
def worker_index(user_id):
    user = worker_profile(user_id)
    print(user)
    user['service'] = user['service'].capitalize()
    return render_template("worker_index.html", current_user=current_user, user=user, user_id=user_id)








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
    

@app.route('/item_profile/<string:worker_id>')
@login_required
def item_profile(worker_id):
    worker = get_worker_id(worker_id)
    print(worker)
    return render_template('item_profile.html', worker_id=worker_id, worker=worker)












# Reviews 


from datetime import datetime  # Import datetime module
from datetime import datetime  # Import datetime module

@app.route('/reviews/<string:worker_id>', methods=['GET', 'POST'])
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
                sql = """INSERT INTO worker_reviews (id, user_id, worker_id, name, email, phone_number, enjoy_service, suggestions, created_at)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                cursor.execute(sql, (gen_ran_string(), user_id, worker_id, name, email, phone_number, enjoy_service, suggestions, datetime.now()))
                connection.commit()

                flash('Review submitted successfully', 'success')
                return redirect(url_for('view_reviews', worker_id=worker_id)) 

        except Exception as e:
            print(f"Error: {e}")
            flash('An error occurred while submitting the review', 'danger')

        finally:
            connection.close()
        return redirect(url_for('reviews', worker_id=worker_id))

    return render_template('reviews.html', current_user=current_user, worker_id=worker_id)








from datetime import datetime


# View Reviews
@app.route('/view_reviews/<string:worker_id>', methods=['GET', 'POST'])
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











from flask_wtf.csrf import generate_csrf


# CONTACT ADMIN

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']

            if not name:
                flash('Your name is required', 'danger')
            if not email:
                flash('Your email is required', 'danger')
            if not subject:
                flash('This message needs a subject', 'danger')
            if not message:
                flash('Please include a message', 'danger')
            print(name, email, subject, message)
            contact_me(name, email, subject, message)
            flash('Message Sent ', 'success')
            # return redirect('user_index')  # Redirect to 'index_services' route
        return render_template('contact.html')
    except Exception as e:
        print(e)
        csrf_token = generate_csrf()
        return render_template('contact.html', csrf_token=csrf_token, current_user=current_user)
    




# Worker Contact Admin

@app.route('/worker_contact', methods=['GET', 'POST'])
@login_required
def worker_contact():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']

            if not name:
                flash('Your name is required', 'danger')
            if not email:
                flash('Your email is required', 'danger')
            if not subject:
                flash('This message needs a subject', 'danger')
            if not message:
                flash('Please include a message', 'danger')
            print(name, email, subject, message)
            contact_me(name, email, subject, message)
            flash('Message Sent ', 'success')
            # return redirect('user_index')  # Redirect to 'index_services' route
        return render_template('worker_contact.html')
    except Exception as e:
        print(e)
        csrf_token = generate_csrf()
        return render_template('worker_contact.html', csrf_token=csrf_token, current_user=current_user)
    





#


@app.route('/payment/<worker_id>', methods=['GET', 'POST'])
def payment(worker_id):
    pass
    return render_template('payment.html', current_user=current_user, worker_id=worker_id)




# def add_payment(worker_id, amount_paid, category, method, receipt):
#     try:
#         connection = mysql.connector.connect(**config)
#         cursor = connection.cursor()
#         query = "UPDATE workers SET amount_paid = %s, category = %s, method = %s, receipt = %s WHERE id = %s"
#         values = (amount_paid, category, method, receipt, worker_id)
#         cursor.execute(query, values)
#         connection.commit()
#     except mysql.connector.Error as err:
#         print("Error:", err)
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()




@app.route('/payment_bank/<worker_id>', methods=['GET', 'POST'])
def payment_bank(worker_id):
    print(request.method, 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    if request.method == 'POST':
        print('form submitted')
        amount_paid = float(request.form.get('amount'))  # Convert to float
        category = request.form.get('category')
        method = request.form.get('method')
        receipt = request.files.get('receipt')
        print(amount_paid, category, receipt, 'xxxxxxxxxxxxxxxxxxx')
        try:
            if receipt:
                filename = secure_filename(receipt.filename)
                response = cloudinary.uploader.upload(receipt, public_id=f"bank_transfer/{filename}")
                receipt_url = response['secure_url']
                print(amount_paid, category, receipt_url, 'cccccccccccccccccccc ')
                add_payment( amount_paid=amount_paid, category=category, method=method, receipt=receipt_url, worker_id=worker_id)
                print(amount_paid, category, method, receipt_url, 'qqqqqqqqqqqqqqq ')
                print("Payment added successfully", amount_paid, category, receipt_url)
                flash('Payment added successfully. Please wait for confirmation', 'success')
                return redirect(url_for('login_for_worker'))
        except Exception as e:
            print(f"Error: {e}")
            flash('An error occurred while submitting the payment', 'error')

    return render_template('payment_bank.html', worker_id=worker_id)






def add_payment(id_, email, amount, plan):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO payments (worker_id, email, amount, plan) VALUES (%s, %s, %s, %s)', (id_, email, amount, plan))
        connection.commit()
        print('Payment added')
    except mysql.connector.Error as err:
        print(err)
        print('Payment not added')
    finally:
        cursor.close()
        connection.close()

@app.route('/payment_card/<worker_id>', methods=['GET', 'POST'])
def payment_card(worker_id):
    if request.method == 'POST':
        email = request.form.get('email')
        amount = request.form.get('amount')
        plan = request.form.get('plan')

        if not email or not amount or not plan:
            flash('Please fill in all fields', 'danger')
            return render_template('payment_card.html', worker_id=worker_id)

        add_payment(id_=worker_id, email=email, amount=amount, plan=plan)
        flash('Payment successful!', 'success')
        return redirect(url_for('payment_card', worker_id=worker_id))

    return render_template('payment_card.html', worker_id=worker_id)


# Endpoint to handle Paystack webhook notifications
@app.route('/paystack/webhook', methods=['POST'])
def paystack_webhook():
    # Parse the JSON data from Paystack
    data = request.json
    
    # Extract relevant information
    reference_id = data['data']['reference']
    amount = data['data']['amount']
    status = data['data']['status']
    email = data['data']['customer']['email']
    payment_plan = data['data']['metadata']['payment_plan']

    # Save the payment information to MySQL
    save_payment(reference_id, amount, status, email, payment_plan)

    return 'Webhook received successfully', 200



from flask import jsonify, request
import mysql.connector
# @app.route('/save_payment', methods=['POST'])
@app.route('/save_payment', methods=['POST'])
def save_payment():
    # Get data from the request
    data = request.json
    email = data['email']
    amount = data['amount']
    plan = data['plan']
    reference = data['reference']
    status = data['status']

    # Save payment information to MySQL
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = "INSERT INTO payments (email, amount, payment_plan, reference_id, status) VALUES (%s, %s, %s, %s, %s)"
    values = (email, amount, plan, reference, status)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Payment data saved successfully'}), 200










@app.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/meeting?roomID={room_id}")
    return render_template('join.html', current_user=current_user)




@app.route('/meeting', methods=['GET', 'POST'])
@login_required
def meeting():
    pass
    return render_template('meeting.html', current_user=current_user)




@app.route('/video_dashboard.html', methods=['GET', 'POST'])
@login_required
def video_dashboard():
    pass
    return render_template('video_dashboard.html', current_user=current_user)




# Getting daily sales

from datetime import date, datetime
def get_daily_sales():
    try:
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute("SELECT SUM(amount) FROM payments WHERE date >= %s AND date <= %s", (start_of_day, end_of_day))
        total_sales = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return total_sales if total_sales else 0
    except mysql.connector.Error as err:
        print(err)



def get_total_sales_total():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute("SELECT SUM(amount) FROM payments")
        total_amount = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return total_amount if total_amount else 0
    except mysql.connector.Error as error:
        print("Error fetching total sales total:", error)
        return 0

























# ADMIN PAGE

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # if not current_user.is_admin:
    #     flash('You are not authorized to access this page!', 'danger')
    #     return redirect(url_for('login'))

    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Execute MySQL query to count messages
        cursor.execute("SELECT COUNT(*) AS message_count FROM contacts")
        result = cursor.fetchone()
        message_count = result[0]


        # Fetch the count of notifications
        # cursor.execute("SELECT COUNT(*) AS notification_count FROM notifications")
        # result = cursor.fetchone()
        # notification_count = result['notification_count']

        
        today_sales_total = get_daily_sales()
        total_sales_total = get_total_sales_total()

        cursor.execute("SELECT * FROM payments WHERE status = 'success'")
        my_payments = cursor.fetchall()
        print(my_payments,'888888888888888888888888888')

        # Close cursor and connection
        cursor.close()
        connection.close()

        from datetime import datetime

# Your existing code ...

        for payment_data in my_payments:
            if isinstance(payment_data, dict):  # Check if it's a dictionary
                payment = payment_data
            elif isinstance(payment_data, tuple):  # Check if it's a tuple
                payment = {
                    'id': payment_data[0],
                    'email': payment_data[1],
                    'amount': payment_data[2],
                    'payment_plan': payment_data[3],
                    'created_at': payment_data[4],
                    'reference_id': payment_data[5],
                    'status': payment_data[6]
                }
            else:
                print("Error: Expected a dictionary or a tuple but received something else:", payment_data)
                continue

            # Proceed with processing for valid data
            if 'created_at' in payment:
                if isinstance(payment['created_at'], datetime):  # Corrected import
                    # Format the 'created_at' datetime object
                    payment['created_at'] = payment['created_at'].strftime('%b %d %Y')
                else:
                    print("Error: Unexpected type for 'created_at'", type(payment['created_at']))
                    continue
            else:
                print("Error: 'created_at' key not found")
                continue

    # Proceed with your logic here using the 'payment' dictionary



    




        
                
        return render_template('admin.html', current_user=current_user, my_payments=my_payments, datetime=datetime, today_sales_total=today_sales_total, total_sales_total=total_sales_total, message_count=message_count)

    except mysql.connector.Error as error:
        # Handle error gracefully
        print("Error while connecting to MySQL", error)
        flash("Error occurred while retrieving message count from MySQL", "danger")
        return render_template('admin.html')
    





@app.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    try:
        if not current_user.is_admin:
            flash('You are not authorized to access this page!', 'danger')
            return redirect(url_for('login'))
        
        # Establish connection to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='language007',
            database='all_services'
        )
        cursor = connection.cursor(dictionary=True)

        # Execute MySQL query to fetch messages
        cursor.execute("SELECT id, name, email, subject, message, sent_at FROM contacts")
        messages = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # reset_message_count()
        for message in messages:
            if isinstance(message['sent_at'], str):  # Check if it's a string
                # Convert string to datetime object and then format it
                message['sent_at'] = datetime.strptime(message['sent_at'], '%Y-%m-%d %H:%M:%S').strftime('%b %d %Y')
            # If it's already a datetime object, directly format it
            else:
                message['sent_at'] = message['sent_at'].strftime('%b %d %Y')

        # Render template with messages and current user
        return render_template('message.html', messages=messages, current_user=current_user, datetime=datetime)

    except mysql.connector.Error as error:
        # Handle error gracefully
        print("Error while connecting to MySQL", error)
        return "Error occurred while connecting to MySQL"
    return render_template('message.html', current_user=current_user)




@app.template_filter('length')
def length(s):
    return len(s)








@app.route('/message_count')
def message_count():
    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect()
        cursor = connection.cursor(dictionary=True)

        # Execute MySQL query to count messages
        cursor.execute("SELECT COUNT(*) AS message_count FROM contacts")
        result = cursor.fetchall()
        print(result, '******************')
        
        # Fetch the count of messages
        message_count = result['message_count']

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Render template with message count
        return render_template('message.html', message_count=message_count)

    except mysql.connector.Error as error:
        # Handle error gracefully
        print("Error while connecting to MySQL", error)
        return "Error occurred while connecting to MySQL"







def get_message(message_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        query = "SELECT id, name, email, subject, message, sent_at FROM contacts WHERE id = %s"
        cursor.execute(query, (message_id,))
        
        contact_message = cursor.fetchone()
        cursor.close()
        connection.close()

        if contact_message:
            print(contact_message, '*************************************')
            return {
                'id': contact_message[0],
                'name': contact_message[1],
                'email': contact_message[2],
                'subject': contact_message[3],
                'message': contact_message[4],
                'sent_at': contact_message[5]
            }
        else:
            return None  # Return None if no message found
    except mysql.connector.Error as err:
        print("Error: ", err)
        return None  # Return None in case of an error





@app.route('/read_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def read_message(message_id):
    if not current_user.is_admin:
        flash('You are not authorized to access this page!', 'danger')
        return redirect(url_for('login'))
    message_admin = get_message(message_id)
    # print(message)
    return render_template('read_message.html', current_user=current_user, message=message_admin, message_id=message_id, datetime=datetime)





@app.route('/notification', methods=['GET', 'POST'])
def notification():
    return render_template('notification.html', current_user=current_user)



@app.route('/all_users', methods=['GET', 'POST'])
def all_users():
    return render_template('all_users.html', current_user=current_user)
    




if __name__ == "__main__":
    app.run(debug=True)