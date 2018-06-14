import os, sys
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from init import app
from flask_login import LoginManager
from user.models import User, AnonymousUser

###### Very important!!!!!!!! Otherwise all 404!!!!!!!
from main import views
from user import views
from article import views

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.anonymous_user = AnonymousUser
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000)))
)


if __name__ == '__main__':
    manager.run()
