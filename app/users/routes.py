from flask import render_template,url_for,redirect,flash,request,Blueprint
from app.users.forms import Registration, Login, Update, request_reset_password,reset_password
from app import db,bcrypt
from app.models import User,Post,Announcments
from PIL import Image
from flask_login import login_user,current_user,logout_user,login_required
from app.users.utils import save_image, send_reset_email

users = Blueprint('users',__name__)

@users.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        flash(f'Logged in as {user.username}!', 'success')
        return redirect(url_for('main.home'))

    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('Utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password )
        db.session.add(user)
        db.session.commit()
        flash(f'Created New Account.You can Login now', 'success')
        return redirect(url_for('main.home'))
    return render_template("register.html", title = "Sign Up", form = form, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@users.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        flash(f'Already loged in', 'success')
        return redirect(url_for('main.home'))
    
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember= form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in as {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Failed login!!!!! Check email and password!!', 'danger')
    return render_template("login.html", title = "Login", form = form, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account',methods=['POST','GET'])
@login_required
def account():
    form = Update()
    if form.validate_on_submit():
        if form.image.data:
            image_filename = save_image(form.image.data)
            temp = current_user.image_file
            current_user.image_file = image_filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account Upated','success')
        redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template("account.html", title = "Account",form = form,image = image, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@users.route('/user/<string:username>')
def user_post(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=1) 
    title = username + ' Activity'
    image = url_for('static', filename = 'profile_pics/' + user.image_file)
    return render_template("user_posts.html", post = posts ,image = image, user = user, title = title, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10) )

@users.route('/request_password',methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = request_reset_password()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f'An reset password link have been sent to the registered mail','info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html',title="Reset Password",form=form, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@users.route('/reset_password/<token>',methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash(f'The token is invalid or expired','warning')
        return redirect(url_for('users.reset_request'))
    form = reset_password()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html',title="Reset Password",form=form, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))