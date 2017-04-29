from functools import wraps

from flask import render_template, flash, request, redirect, url_for, session
from passlib.hash import sha256_crypt

from config import app, db
from forms import RegisterForm, ArticleForm
from models import Users, Articles

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
    return render_template('home.html')


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


# TODO: Articles
@app.route('/articles')
def articles():
    data = Articles.query.all()
    if len(data) > 0:
        return render_template('articles.html', articles=data)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)


# TODO: Article Details
@app.route('/article/<int:id>/')
def article(id):
    data = Articles.query.get(id)
    app.logger.info(data)
    if data:
        return render_template('article.html', article=data)
    else:
        msg = "No article found!"
        return render_template('article.html', msg=msg)


# TODO: Add Article
@app.route('/add_article', methods=["GET", "POST"])
@login_required
def add_article():
    form = ArticleForm(request.form)
    app.logger.info(request.method)
    app.logger.info(form.errors)
    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data
        author = session['username']
        article = Articles(title, body, author)
        db.session.add(article)
        db.session.commit()
        flash("Article Created", "success")
        return redirect(url_for('dashboard'))
    else:
        error = form.errors
        return render_template('add_article.html', form=form, error=error)
    return render_template('add_article.html', form=form)


# TODO: Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    data = Articles.query.all()
    if len(data) > 0:
        return render_template('dashboard.html', articles=data)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)


# TODO: Edit Article
@app.route('/edit_article/<string:id>/', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    data = Articles.query.get(id)
    form = ArticleForm(request.form)

    form.title.data = data.title
    form.title.body = data.body
    if request.method == 'POST' and form.validate():
        data.title = request.form["title"]
        data.body = request.form["body"]
        db.session.commit()
        flash("Article updated!", "success")
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)


# TODO: Delete Article
@app.route('/delete_article/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_article(id):
    data = Articles.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
        msg = "Article deleted!"
        return render_template('dashboard.html', msg=msg)
    else:
        error = "Article was not deleted!"
        return render_template('dashboard.html', error=error)

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
