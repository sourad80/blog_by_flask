from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Post,Announcments
from app.posts.forms import create_post

posts = Blueprint('posts',__name__)

@posts.route('/post_new',methods=['POST','GET'])
@login_required
def post_new():
    form = create_post()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Post created','success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html",title = "Create Post", legend = "Create Post" ,form = form, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html",title = post.title, post = post, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@posts.route('/post/<int:post_id>/update',methods=['POST','GET'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    form = create_post()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Post Updated','success')
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content 
    return render_template("create_post.html",title = "Update Post",legend = "Update Post", form = form, announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10))

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post Deleted','warning')
    return redirect(url_for('main.home'))