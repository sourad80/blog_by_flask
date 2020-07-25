from flask import Blueprint,render_template
from app.models import Announcments

errors = Blueprint('errors',__name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10)) , 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10)) , 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', announcements = Announcments.query.order_by(Announcments.date_posted.desc()).paginate(page=1, per_page=10)) , 500