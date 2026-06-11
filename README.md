# KanjiDeck v1.2.0

KanjiDeck is a web-based Japanese vocabulary flashcard application built with Flask and SQLite. It uses a custom spaced repetition system (SRS) to help users review JLPT vocabulary efficiently. Users can create accounts, track their own learning progress, review cards by JLPT level, and view detailed statistics about their performance.

Created to help learners efficiently review JLPT vocabulary through a custom SRS-based flashcard system

Live on: https://kanjideck.onrender.com/

Desktop App (Windows): [KanjiDeck-DA](https://github.com/nthnerr/KanjiDeck-DA)

## Features

* JLPT level selection (N5, N4, N3, N2, N1)
* 8000+ vocabulary flashcards from an SQLite database
* Show/Hide answer functionality
* Next card generation
* Modern dark-themed UI
* Dynamic routing with Flask
* Spaced Repetition System (SRS)
* Review statistics dashboard
* Review history tracking
* User registration and login
* Secure password hashing
* Session based authentication

## Screenshots

<table>
  <tr>
    <td align="center">
      <img src="images/v1.2 home.png" width="450"><br>
      Home Page
    </td>
    <td align="center">
      <img src="images/v1.2 review.png" width="450"><br>
      Review Screen
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="images/v1.2 login.png" width="450"><br>
      Statistics
    </td>
    <td align="center">
      <img src="images/v1.2 stats.png" width="450"><br>
      Login Page
    </td>
  </tr>
</table>

## Project Structure

```text
KanjiDeck/
│
├── app.py
├── database.py
├── vocabulary.db               -> JLPT vocabulary cards
├── userDatabase.py
├── users.db                    -> User accounts and authentication
├── userProgressDatabase.py
├── userProgress.db             -> User progress and queue positions
├── jlpt_vocab.csv
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── statistics.html
│   └── review.html
│
├── static/
│   ├── home_style.css
│   ├── login_style.css
│   ├── register_style.css
│   ├── statistics_style.css
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
---
## Database Structure

### User

Stores user account information.

| Column        | Description     |
| ------------- | --------------- |
| id            | User ID         |
| username      | Unique username |
| password_hash | Hashed password |

### UserProgress

Stores review progress for each card.

| Column    | Description                 |
| --------- | --------------------------- |
| id        | Row ID                      |
| user_id   | User ID                     |
| card_id   | Vocabulary card ID          |
| level     | JLPT level                  |
| correct   | Number of correct reviews   |
| incorrect | Number of incorrect reviews |
| position  | Next review position        |

### UserQueue

Stores the current review queue position for each JLPT level.

| Column           | Description            |
| ---------------- | ---------------------- |
| user_id          | User ID                |
| level            | JLPT level             |
| current_position | Current queue position |

### Vocabulary

Stores all vocabulary cards.

| Column   | Description     |
| -------- | --------------- |
| id       | Card ID         |
| original | Japanese word   |
| furigana | Reading         |
| english  | English meaning |
| level    | JLPT level      |

---

## How the SRS Works

KanjiDeck uses a custom spaced repetition system.

* Cards answered correctly move further into the review queue.
* Cards answered incorrectly reappear sooner.
* Review scheduling is tracked independently for each user.
* Each JLPT level maintains its own review queue.

## Future improvements

* Search functionality
* Improved SRS algorithm
* Progress graphs
* Mobile friendly UI improvements

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

## Tech stack

* Python
* Flask
* SQLite
* HTML
* CSS
* Javascript

## License

This project was created for learning and educational purposes.
