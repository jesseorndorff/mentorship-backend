from flask import render_template, request, redirect, url_for, flash,session
from app.api.dao.user import UserDAO
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from werkzeug import secure_filename
import os 
 
obj = UserDAO()

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/static/uploads/'.format(PROJECT_HOME)
UPLOADED_IMAGES_URL = 'http://209.97.155.113:5000/static/uploads/'

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath   


def dboard(app):
    @app.route('/admin') 
    def admin():
        obj = UserModel.query.order_by(UserModel.id).all()
        return render_template('admin/dashboard.html',title='Home',obj=obj)

    @app.route('/admin/login', methods=['GET', 'POST'])
    def login_page():
        session['username'] = 'Admin'
        error = None
        if request.method == 'POST':
            print(db)
            authenticate = obj.authenticate(
                request.form['username'], request.form['password'])
            try:
                username = UserModel.query.filter_by(
                    username=request.form['username']).first()
                if username.is_admin and username.password_hash:
                    if session['username'] == username.name:
                        flash('You were successfully logged in....')
                        return redirect(url_for('admin'))
                elif authenticate:
                    flash('Only admin can login....')
                    return render_template('admin/login.html', title='Login')
                else:
                    error = 'Please check your login details and try again.'
                    return render_template('admin/login.html', title='Login', error=error)
            except Exception as e:
                print(e)
        return render_template('admin/login.html', title='Login',error = error)
    @app.route("/logout/")
    # @login_required
    def logout():
        session.clear()
        flash("You have been logged out!")
        return redirect(url_for('login_page'))
        
    @app.route('/userdata/<id>')
    def user(id):
        try:
            '''
                Detail View
            '''
            obj = UserModel.query.filter_by(id=id).first()
            return render_template('admin/userview.html', title=obj.name, obj=obj)
        except Exception as e:
            return render_template('admin/userview.html', title='No Name', obj=obj)
        

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'POST':
            data = request.form
            f = request.files['file']
            username = data.get("username", None)
            if username:
                user_with_same_username = UserModel.find_by_username(username)
                # username should be unique
                if user_with_same_username:
                    flash("Username already exists!!")
                user.username = username
            if request.form['name']:
                name = request.form['name']
            if "username" in data:
                if request.form["username"]:
                    username = request.form['username']
                else:
                    username = None
            if "bio" in data:
                if request.form["bio"]:
                    bio = request.form["bio"]
                else:
                    bio = None
            if "email" in data:
                if request.form["email"]:
                    email = request.form["email"]
                else:
                    email = None
            if "password" in data and "password1" in data:
                if request.form['password'] == request.form['password1']:
                    if request.form["password"]:
                        password = request.form["password"]
                    else:
                        password = None
                    flash("Password didn;t Matched!!")
            if "skill" in data:
                if request.form["skill"]:
                    skill = request.form["skill"]
                else:
                    skill = None
            if "location" in data:
                if request.form["location"]:
                    location = request.form["location"]
                else:
                    location = None
            if "occupation" in data:
                if request.form["occupation"]:
                    occupation = request.form["occupation"]
                else:
                    occupation = None
            if "organization" in data:
                if request.form["organization"]:
                    organization = request.form["organization"]
                else:
                    organization = None              
            if "interests" in data:
                if request.form["interests"]:
                    interests = request.form["interests"]
                else:
                    interests = None 
            if "is_admin" in data:
                if request.form["is_admin"]:
                    is_admin = request.form["is_admin"]
                else:
                    is_admin = None   
            if "need_mentoring" in data:
                if request.form["need_mentoring"]:
                    need_mentoring = request.form["need_mentoring"]
                else:
                    need_mentoring = None   
            if "available_to_mentor" in data:
                if request.form["available_to_mentor"]:
                    available_to_mentor = request.form["available_to_mentor"]
                else:
                    available_to_mentor = None  
            if "email_verified" in data:
                if request.form["email_verified"]:
                    email_verified = request.form["email_verified"]
                else:
                    email_verified = None  
            if "terms_and_conditions" in data:
                if request.form["terms_and_conditions"]:
                    email_verified = request.form["terms_and_conditions"]
                else:
                    email_verified = None
            if f:
                img_name = secure_filename(f.filename)
                create_new_folder(UPLOAD_FOLDER)
                saved_path = os.path.join('static/uploads/', img_name)
                f.save(saved_path)
                path = UPLOADED_IMAGES_URL+img_name
                data.profile_photo = path
                db.session.commit()
            else:
                pass  
            my_data = UserModel(name, username, email, password,terms_and_conditions,
                                is_admin,email_verified,available_to_mentor,
                                need_mentoring,interests,organization,
                                occupation,location,skill )
            db.session.add(my_data)
            db.session.commit()
            flash("User Inserted Successfully")
            return redirect(url_for('admin'))
        return render_template('admin/create.html', title='Create User')
    @app.route('/update/<id>', methods=['GET', 'POST'])
    def update(id):
        obj = UserModel.query.filter_by(id=id).first()
        if request.method == 'POST':
            print(obj.id)
            f = request.files['file']
            print(request.form)
            data = UserModel.query.get(obj.id)
            if request.form["name"]:
                data.name = request.form["name"]
                db.session.commit()
            if request.form["bio"]:
                data.bio = request.form["bio"]
                db.session.commit()
            if request.form["location"]:
                data.location = request.form["location"]
                db.session.commit()
            if request.form["occupation"]:
                data.occupation = request.form["occupation"]
                db.session.commit()
            if request.form["organization"]:
                data.organization = request.form["organization"]
                db.session.commit()
            if request.form["slack_username"]:
                data.slack_username = request.form["slack_username"]
                db.session.commit()  
            if request.form["social_media_links"]:
                data.social_media_links = request.form["social_media_links"]
                db.session.commit()  
            if request.form["skills"]:
                data.skills = request.form["skills"]
                db.session.commit()     
            if request.form["interests"]:
                data.interests = request.form["interests"]
                db.session.commit()
            if request.form["resume_url"]:
                data.resume_url = request.form["resume_url"]
                db.session.commit()
            if f:
                img_name = secure_filename(f.filename)
                create_new_folder(UPLOAD_FOLDER)
                saved_path = os.path.join('static/uploads/', img_name)
                f.save(saved_path)
                path = UPLOADED_IMAGES_URL+img_name
                data.profile_photo = path
                db.session.commit()
            else:
                pass
            if request.form["need_mentoring"]:
                data.need_mentoring = request.form["need_mentoring"]
            if request.form["available_to_mentor"]:
                data.available_to_mentor = request.form["available_to_mentor"]
            flash("User Updated Successfully")
            return redirect(url_for('admin'))
        return render_template('admin/update.html',title='Update User', obj=obj)
    
    @app.route('/delete/<id>/', methods=['GET', 'POST'])
    def delete(id):
        my_data = UserModel.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("User Deleted Successfully")

        return redirect(url_for('admin'))
