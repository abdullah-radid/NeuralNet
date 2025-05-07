from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy 
from flask import flash
from datetime import datetime

# Here we will crete the Flask and connect it to the database

app = Flask(__name__)
app.secret_key = 'dev_key_for_neuralnet_project' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
db = SQLAlchemy(app)

# This class is for storing user info

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)  
    username = db.Column(db.String(60), unique=True, nullable=False) 
    password = db.Column(db.String(60), nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return '<Task %r>' % self.id 
        
# This class will hold forum/discussion posts

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
# This class will keep a track of boookmarks for users

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200))
    url = db.Column(db.String(300))
    
# page route
@app.route('/', methods = ['POST', 'GET']) 
def index(): 
    return render_template("index.html") 

#Route for the user dashboard (only if logged in)

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    bookmarks = Bookmark.query.filter_by(user_id=session['user_id']).all()
    my_posts = Discussion.query.filter_by(username=session['username']).order_by(Discussion.timestamp.desc()).all()

    return render_template("home.html", bookmarks=bookmarks, my_posts=my_posts)
    
# Route for the about us page

@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("about.html")

# Route for the news page

@app.route('/news')
def news():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("news.html")

# Route for the profile editing page
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template("profile.html", current_user=user)

# Route for the login page and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))

        flash("InvALid username or password.", "error")
        return redirect(url_for('login'))
    
    return render_template("login.html")
    
# Route for the signup page after validation
@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        print(f"New registration: {username}")
        email = request.form['email']
        password = request.form['password']

        does_user_exist = User.query.filter_by(username=username).first()
        does_email_exist = User.query.filter_by(email=email).first()

        if does_user_exist:
            flash("This username is already registered. Try again.", "INVALID")
            return redirect(url_for('signup'))

        if does_email_exist:
            flash("This email is already in use. Try again.", "INVALID")
            return redirect(url_for('login'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account creation was sucessful, welcome to NeuralNet!", "Success")
        return redirect(url_for("login"))
    return render_template("signup.html")

# To log out the user by clearing their session data and redirect to login
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/forum')
def forum():
    # To list discussions, with optional filter for user’s own posts
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.args.get('mine') == 'true':
        discussions = Discussion.query.filter_by(username=session['username']).order_by(Discussion.timestamp.desc()).all()
    else:
        discussions = Discussion.query.all()

# Insertion sort by title (DSA touch)
        for i in range(1, len(discussions)):
            key = discussions[i]
            j = i - 1
        while j >= 0 and discussions[j].title.lower() > key.title.lower():
            discussions[j + 1] = discussions[j]
            j -= 1
        discussions[j + 1] = key

    return render_template("forum.html", discussions=discussions)
    
# Create a discussion post from data

@app.route('/create_discussion', methods=['POST'])
def create_discussion():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    content = request.form['content']
    user = User.query.get(session['user_id'])

    new_post = Discussion(title=title, content=content, username=user.username)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('forum'))
    
# Delete a discussion if owned by logged in user

@app.route('/delete_discussion', methods=['POST'])
def delete_discussion():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    discussion_id = request.form['discussion_id']
    post = Discussion.query.get_or_404(discussion_id)
    user = User.query.get(session['user_id'])

    if post.username != user.username:
        flash("You can't delete someone else's post.")
        return redirect(url_for('forum'))

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.")
    return redirect(url_for('forum'))
    
# To allow logged‑in user to change their username, email, or password

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    new_username = request.form.get('new_username').strip()
    new_email = request.form.get('new_email').strip()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password').strip()

    # Validate current password
    if user.password != current_password:
        flash("Current password is incorrect.", "error")
        return redirect(url_for('profile'))

    # Update username/email if changed
    if new_username:
        user.username = new_username
    if new_email:
        user.email = new_email
    if new_password:
        user.password = new_password

    db.session.commit()
    return redirect(url_for('profile'))

# To add a bookmark if it doesn’t exist

@app.route('/bookmark', methods=['POST'])
def bookmark():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    url = request.form['url']
    user_id = session['user_id']

    # Avoid duplicates
    existing = Bookmark.query.filter_by(user_id=user_id, url=url).first()
    if not existing:
        new_bookmark = Bookmark(user_id=user_id, title=title, url=url)
        db.session.add(new_bookmark)
        db.session.commit()

    return redirect(request.referrer or url_for('news'))
    
#  To remove all bookmarks for the user

@app.route('/clear_bookmarks')
def clear_bookmarks():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Bookmark.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
