from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = SelectField('Subject', choices=[
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('business', 'Business Opportunity')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Message')

class CourseEnrollmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    course = SelectField('Course', choices=[
        ('web', 'Web Development'),
        ('data', 'Data Science'),
        ('cyber', 'Cyber Security'),
        ('ai', 'AI & Machine Learning')
    ], validators=[DataRequired()])
    submit = SubmitField('Begin Your Journey')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    form = CourseEnrollmentForm()
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

import requests  # Ensure this is installed and added to requirements.txt

@app.route('/free_books', methods=['GET'])
def free_books():
    """Render the main Free Books page."""
    return render_template('free_books.html', title='Free Books')
@app.route('/free_books_search', methods=['GET'])
def free_books_search():
    """Search for free books using an external API."""
    query = request.args.get('query', '').strip()
    page = int(request.args.get('page', 1))
    books = []

    if query:
        try:
            # Example API call to Open Library
            response = requests.get(
                'https://openlibrary.org/search.json',
                params={'q': query, 'page': page}
            )
            if response.status_code == 200:
                data = response.json()
                print(data)  # Debug: Print the API response to the console
                books = [
                    {
                        'title': book.get('title'),
                        'authors': book.get('author_name', []),
                        'cover_image': f"http://covers.openlibrary.org/b/id/{book.get('cover_i')}-L.jpg" if book.get('cover_i') else None,
                        'year': book.get('first_publish_year'),
                        'source': 'openlibrary',
                        'download_links': {
                            'read': f"https://openlibrary.org{book.get('key')}",
                            'detail': f"https://openlibrary.org{book.get('key')}"
                        }
                    }
                    for book in data.get('docs', [])
                ]
            else:
                flash('Failed to fetch books from the API. Please try again later.', 'danger')
    
            if not books:
                flash(f'No books found matching "{query}". Please try a different search term.', 'warning')
        except Exception as e:
            print(f"Error: {e}")  # Debug: Print the exception to the console
            flash('An error occurred while fetching books. Please try again later.', 'danger')

    return render_template(
        'free_book_search.html',
        query=query,
        books={'books': books, 'count': len(books)}
    )


response = requests.get("https://openlibrary.org/search.json?q=harry+potter&page=1")
if response.status_code == 200:
    print(response.json())  # Debug: Print the API response to the console
else:
    print("Failed to fetch data from the API.")


@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            # Here you would typically save the message to the database
            # For now, we'll just show a success message
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('An error occurred while sending your message. Please try again.', 'danger')
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create new tables
        db.create_all()
    app.run(debug=True)
