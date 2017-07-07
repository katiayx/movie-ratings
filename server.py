"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, g, url_for, abort

from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

from model import connect_to_db, db, User, Rating


app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

class MyForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email("This field requires a valid email address")])
    password = PasswordField('password', validators=[DataRequired()])



@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')

@app.route('/register')
def register():
    """Show form for user signup."""

    form = MyForm()

    return render_template("register.html", form=form)


@app.route('/register', methods=['POST'])
def register_process():
    """validating registration info"""

    form = MyForm()
    if form.validate_on_submit():
        add_user_db()
        return redirect('/member')

    # return redirect('/register')


def add_user_db():
    """capture registration info and saving to db"""

    email = request.form.get('email')
    password = request.form.get('password')
    pw_hash = bcrypt.generate_password_hash(password)

    user = User(email=email,password=pw_hash)
    db.session.add(user)
    db.session.commit()

    # print email, password, pw_hash
    return

@app.route('/member')
@login_required
def logged_in():
    """Member dashboard."""

    # display member name
    # fillout rest of profile
    # list of movies rated
    # list of recommendations
    # link to search

    return render_template('member.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User log in page."""

    form = MyForm()

    if form.validate_on_submit():

        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Get outta here. Register!')
            return redirect('/register')

        # print "user_id: ", user.user_id
        # print "password: ", user.password
        # print "password from form: ", password

        # comparsion need to be db password vs. user form submission
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/member')
        else:
            flash('NOPE!')

        # print user.user_id, pw_hash, user.password

    return render_template('login.html', form=form)

    # next is equal to the originally request url
    # return redirect(request.args.get('next') or url_for('index'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    """ Logs users out and clean out any cookies associated with session."""

    logout_user()
    return redirect(url_for('index')) 

@app.before_request
def before_request():
    g.user = current_user

if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    app.run(host="0.0.0.0")
