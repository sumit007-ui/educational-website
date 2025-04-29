# Professional Educational Website with Career Guidance

A modern, responsive educational website built with HTML5, CSS3, JavaScript, and Flask, featuring career guidance resources and interactive learning tools.

## Features

### Frontend
- Responsive Navigation Bar
- Interactive Hero Slider
- Course Catalog with detailed descriptions
- Career Roadmaps for various fields
- Downloadable Resume Templates
- Company-Specific Interview Questions and tips
- Dark Mode Support for better accessibility
- Mobile-First Design for seamless experience on all devices

### Backend
- Flask-powered dynamic content rendering
- User authentication with Flask-Login
- Database integration using Flask-SQLAlchemy
- Secure form handling with Flask-WTF
- Environment variable management with python-dotenv

## Project Structure

```
educational-website/
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── logo.png
│   ├── hero-1.jpg
│   ├── hero-2.jpg
│   └── hero-3.jpg
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── courses.html
│   └── roadmap.html
├── app.py
├── requirements.txt
└── .env
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/educational-website.git
cd educational-website
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
```

### 5. Add Your Images
- Place your logo in the `images` directory as `logo.png`.
- Add hero section background images as `hero-1.jpg`, `hero-2.jpg`, and `hero-3.jpg`.

### 6. Run the Flask Application
```bash
flask run
```
The application will be available at `http://127.0.0.1:5000`.

### 7. Open the Website
Open `http://127.0.0.1:5000` in your web browser to view the website.

## Dependencies

The project uses the following Python packages (defined in `requirements.txt`):
- Flask==2.0.1
- Flask-SQLAlchemy==2.5.1
- Flask-Login==0.5.0
- Flask-WTF==1.0.0
- Werkzeug==2.0.1
- python-dotenv==1.0.0
- email-validator==2.1.0.post1

Additionally, the frontend uses:
- **Bootstrap 5.3.0**: For responsive layout and components.
- **Font Awesome 6.0.0**: For icons used across the website.
- **Swiper 8.0.0**: For the interactive hero slider.

## Browser Support

This website is compatible with the latest versions of the following browsers:
- Google Chrome
- Mozilla Firefox
- Apple Safari
- Microsoft Edge

## Contributing

We welcome contributions! If you have ideas for new features or improvements, feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
