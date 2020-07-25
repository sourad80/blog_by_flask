import secrets

class config:
    SECRET_KEY = str(secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '#replace this with a gmail'
    MAIL_PASSWORD = '#replace this with a password'
