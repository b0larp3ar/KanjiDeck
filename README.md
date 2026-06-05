# KanjiDeck v1.0.0

KanjiDeck is a web-based Japanese vocabulary trainer built with Flask and SQLite. Users can select a JLPT level (N5–N1) and practice vocabulary using flashcards with a clean modern UI.

Live on: 
https://kanjideck.onrender.com/

## Features

* JLPT level selection (N5, N4, N3, N2, N1)
* Random vocabulary cards from an SQLite database
* Show/Hide answer functionality
* Next card generation
* Modern dark-themed UI
* Dynamic routing with Flask

## Technologies Used

### Backend

* Python
* Flask
* SQLite

### Frontend

* HTML
* CSS
* JavaScript

## Screenshots

### Home Page

![Home Page](images/homepage.png)

### Review Page

![Home Page](images/review_3.png)
![Home Page](images/review_4.png)

## Project Structure

```text
KanjiDeck/
│
├── app.py
├── database.py
├── vocabulary.db
├── jlpt_vocab.csv
│
├── templates/
│   ├── home.html
│   └── review.html
│
├── static/
│   ├── home_style.css
│   └── review_style.css
│
├── images/
│   ├── homepage.png
│   ├── review_1.png
│   └── review_2.png
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Future Improvements

* Larger JLPT vocabulary dataset
* Import vocabulary from external datasets
* User progress tracking
* Correct/Incorrect answer statistics
* Spaced repetition system
* Search functionality
* User accounts

## How to Run locally

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

## License

This project was created for learning and educational purposes.
