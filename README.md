# KanjiDeck

KanjiDeck is a web-based Japanese vocabulary trainer built with Flask and SQLite. Users can select a JLPT level (N5–N1) and practice vocabulary using flashcards with a clean modern interface.

## Features

* JLPT level selection (N5, N4, N3, N2, N1)
* Random vocabulary cards from a SQLite database
* Show/Hide answer functionality
* Next card generation
* Modern dark-themed user interface
* Dynamic routing with Flask
* SQLite database integration

## Technologies Used

### Backend

* Python
* Flask
* SQLite

### Frontend

* HTML
* CSS
* JavaScript

### Version Control

* Git
* GitHub

## Screenshots

### Home Page

![Home Page](images/home.png)

### Review Page

![Home Page](images/review_1.png)
![Home Page](images/review_2.png)

## Project Structure

```text
KanjiDeck/
│
├── app.py
├── vocabulary.db
│
├── templates/
│   ├── home.html
│   └── review.html
│
├── static/
│   ├── home_style.css
│   └── review_style.css
│
└── README.md
```

## How to Run

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/KanjiDeck.git
```

2. Navigate to the project directory

```bash
cd KanjiDeck
```

3. Install Flask

```bash
pip install flask
```

4. Run the application

```bash
python app.py
```

5. Open your browser and visit

```text
http://127.0.0.1:5000
```

## What I Learned

This project helped me learn:

* Flask routing
* Dynamic URLs
* HTML templates with Jinja
* SQLite database integration
* SQL queries
* CSS layout and styling
* Git and GitHub workflows

## Future Improvements

* Larger JLPT vocabulary dataset
* Import vocabulary from external datasets
* User progress tracking
* Correct/Incorrect answer statistics
* Spaced repetition system
* Search functionality
* User accounts
* Deployment to a public server

## License

This project was created for learning and educational purposes.
