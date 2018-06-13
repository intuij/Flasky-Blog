import os


SECRET_KEY = 'spzllm'
DEBUG = True
DB_USERNAME = 'root'
DB_PASSWORD = '123456'
BLOG_DB_NAME = 'flasky'
DB_HOST = os.getenv('IP', '127.0.0.1')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
ADMIN_EMAIL = 'admin@gmail.com'