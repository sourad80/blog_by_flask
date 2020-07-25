import os
import secrets
from flask import url_for,current_app
from app import mail
from flask_mail import Message
from PIL import Image


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_image.filename)
    filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path , 'static/profile_pics' , filename)

    size = (125,125)
    i = Image.open(form_image)
    i.thumbnail(size)

    i.save(picture_path)
    return filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@gmail.com',recipients=[user.email])
    msg.body = f'''To reset the password, click the link below
{url_for('users.reset_token',token=token,_external=True)}

If you haven't requested a password change please ignore it.Nothing will be changed.
'''
    mail.send(msg)