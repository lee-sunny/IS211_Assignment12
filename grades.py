import sqlite3 as lite
from flask import Flask, request, session, g, redirect, url_for, render_template, flash

DATABASE = "hw12.db"
USERNAME = "admin"
PASSWORD = "password"
SECRET_KEY = "secretkey"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return lite.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

con = lite.connect(DATABASE)
with con:
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS students")
    c.execute("DROP TABLE IF EXISTS quiz")
    c.execute("DROP TABLE IF EXISTS results")
    
    c.execute("""CREATE TABLE students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT,
                    lastname TEXT)""")
    c.execute("""CREATE TABLE QUIZ (
                    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    questions INTEGER,
                    qz_subject TEXT,
                    quiz_date DATE)""")
    c.execute("""CREATE TABLE results (
                    results_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    quiz_id INTEGER,
                    score INTEGER)""")

    c.execute("INSERT INTO students (student_id, firstname, lastname) VALUES (1, 'John', 'Smith')")
    c.execute("INSERT INTO quiz (quiz_id, qz_subject, questions, quiz_date) VALUES (1, 'Python Basics', 5, '2015-05-05')")
    c.execute("INSERT INTO results (results_id, student_id, quiz_id, score) VALUES (1, 1, 1, 85)")

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Username is Invalid.'
            return render_template('login.html', error=error)
        elif request.form['password'] != 'password':
            error = 'Password is Invalid.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    else:
        return render_template('login.html', error=error)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['logged_in'] is not True:
        return redirect('/login')
    else:
        cur = g.db.execute('SELECT student_id, firstname, lastname from students')
        students = [dict(student_id=row[0], firstname=row[1], lastname=row[2])
                    for row in cur.fetchall()]

        cur = g.db.execute('SELECT quiz_id, qz_subject, questions, quiz_date from quiz')
        quizzes = [dict(quiz_id=row[0], qz_subject=row[1], questions=row[2], quiz_date=row[3])
                   for row in cur.fetchall()]

        return render_template("dashboard.html", students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template("add_student.html")
    elif request.method == 'POST':
        g.db.execute('INSERT into Students (firstname, lastname) values (?, ?)',
                     [request.form['StudentFirstName'], request.form['StudentLastName']])
        g.db.commit()
    return redirect(url_for('dashboard'))


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('add_quiz.html')
    elif request.method == 'POST':
        g.db.execute('INSERT into Quiz (qz_subject, questions, quiz_date) '
                     'values (?, ?, ?)', [request.form['QuizSubject'], request.form['QuizQuestions'],request.form['QuizDate']])
        g.db.commit()
    return redirect(url_for('dashboard'))


@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('add_score.html')
    elif request.method == 'POST':
        g.db.execute('INSERT into Results (student_id, quiz_id, score) values (?, ?, ?)',
                     [request.form['StudentID'], request.form['QuizID'], request.form['Score']])
        g.db.commit()
    return redirect(url_for('dashboard'))


@app.route('/results', methods=['GET'])
def view_results():
    if session['logged_in'] is not True:
        return redirect('/login')
    else:
        cur = g.db.execute("""SELECT students.firstname, students.lastname, quiz.qz_subject, results.score
                            FROM students
                            JOIN Results ON students.student_id = results.student_id
                            JOIN Quiz ON results.quiz_id = quiz.quiz_id;"""
                           )
        students = [dict(firstname=row[0], lastname=row[1], qz_subject=row[2], score=row[3])
                    for row in cur.fetchall()]
        return render_template("results.html", students=students)


if __name__ == '__main__':
    app.run(debug=True)
