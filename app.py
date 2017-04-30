from functools import wraps

from flask import render_template, flash, request, redirect, url_for, session
from passlib.hash import sha256_crypt

from config import app, db
from forms import RegisterForm, VideoForm
from models import Users, Videos

from werkzeug.contrib.fixers import ProxyFix

app = app
db.init_app(app)
db.create_all()


# TODO: Decorator login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['logged_in'] == False:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# TODO: HomePage
@app.route('/')
def index():
    data = Videos.query.all()
    if len(data) > 0:
        return render_template('home.html', videos=data)
    else:
        msg = 'No Videos Found'
        return render_template('home.html', msg=msg)


# TODO: About
@app.route('/about')
def about():
    return render_template('about.html')


# TODO: Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        user = Users(name=name, username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash("Something went wrong with DB")
        flash('You are now registered and can login!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# TODO: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        result = Users.query.filter_by(username=username).first()
        if result is not None:
            password = result.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login_html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


# TODO: Logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# TODO: Videos
@app.route('/videos')
def videos():
    data = Videos.query.all()
    if len(data) > 0:
        return render_template('videos.html', videos=data)
    else:
        msg = 'No Videos Found'
        return render_template('videos.html', msg=msg)


# TODO: Video Details
@app.route('/video/<int:id>/')
def video(id):
    data = Videos.query.get(id)
    app.logger.info(data)
    if data:
        return render_template('video.html', video=data)
    else:
        msg = "No video found!"
        return render_template('video.html', msg=msg)


# TODO: Add Video
@app.route('/add_video', methods=["GET", "POST"])
@login_required
def add_video():
    form = VideoForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        link = form.link.data
        author = session['username']
        video = Videos(title, link, author)
        db.session.add(video)
        db.session.commit()
        flash("Video created", "success")
        return redirect(url_for('dashboard'))
    else:
        error = form.errors
        return render_template('add_video.html', form=form, error=error)
    return render_template('add_video.html', form=form)


# TODO: Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    data = Videos.query.all()
    if len(data) > 0:
        return render_template('dashboard.html', videos=data)
    else:
        msg = 'No Videos Found'
        return render_template('dashboard.html', msg=msg)


# TODO: Edit Video
@app.route('/edit_video/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_video(id):
    data = Videos.query.get(id)
    form = VideoForm(request.form)

    form.title.data = data.title
    form.title.link = data.link
    if request.method == 'POST' and form.validate():
        data.title = request.form["title"]
        data.link = request.form["link"]
        db.session.commit()
        flash("Video updated!", "success")
        return redirect(url_for('dashboard'))
    return render_template('edit_video.html', form=form)


# TODO: Delete Video
@app.route('/delete_video/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_video(id):
    data = Videos.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
        msg = "Video deleted!"
        return render_template('dashboard.html', msg=msg)
    else:
        error = "Video was not deleted!"
        return render_template('dashboard.html', error=error)

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
