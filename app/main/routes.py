from flask import render_template, request, Blueprint,redirect,url_for,flash
from app import db
from app.models import Post,Announcments
from flask_login import current_user,login_required
from app.main.forms import Announcment

main = Blueprint('main',__name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page',1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)   
    return render_template("home.html", post = posts , title = "Home", announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@main.route('/about')
def about():
    return render_template("about.html", announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@main.route('/announcment',methods=['POST','GET'])
@login_required
def announcment():
    if current_user.username == "Sourad80":
        form = Announcment()
        if form.validate_on_submit():
            announcment = Announcments(title = form.title.data)
            db.session.add(announcment)
            db.session.commit()
            flash(f'Announced', 'success')
            return redirect(url_for('main.home'))
        return render_template("announcment.html",title = "Announce", form = form, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))
    flash(f'You are not a site admin!', 'danger')
    return redirect(url_for('main.home'))