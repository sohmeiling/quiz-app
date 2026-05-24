import sqlite3
from random import choice


db_name = 'quiz.sqlite'
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    '''Delete all quiz tables.'''
    open()
    do('''DROP TABLE IF EXISTS quiz_content''')
    do('''DROP TABLE IF EXISTS question''')
    do('''DROP TABLE IF EXISTS quiz''')
    close()


def create():
    '''Create the database tables for quizzes, questions, and their links.'''
    open()
    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY,
            name VARCHAR
        )''')
    do('''CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY,
            question VARCHAR,
            answer VARCHAR,
            wrong1 VARCHAR,
            wrong2 VARCHAR,
            wrong3 VARCHAR
        )''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
            id INTEGER PRIMARY KEY,
            quiz_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY (quiz_id) REFERENCES quiz (id),
            FOREIGN KEY (question_id) REFERENCES question (id)
        )''')
    close()


def add_questions():
    '''Add sample questions. Students can replace these with their own.'''
    questions = [
        ('How many bytes are in one kilobyte?', '1024', '1000', '8', '64'),
        ('What is Python?', 'A programming language', 'A snake only', 'A database', 'A browser'),
        ('Which command creates a table in SQL?', 'CREATE TABLE', 'INSERT', 'SELECT', 'DROP'),
        ('Which Flask object stores data for each user?', 'session', 'request', 'cursor', 'table'),
        ('Which method sends form data hidden in the request body?', 'POST', 'GET', 'SELECT', 'PRINT'),
        ('Which HTML input lets users choose one answer from a group?', 'radio', 'text', 'hidden', 'submit'),
        ('Which template command prints a value?', '{{ value }}', '{% if %}', '{% for %}', '<form>'),
        ('Which SQL command gets records from a table?', 'SELECT', 'CREATE', 'INSERT', 'FOREIGN'),
        ('Which Flask function opens an HTML template?', 'render_template', 'redirect', 'url_for', 'shuffle'),
        ('Which function can mix the answer options?', 'shuffle', 'choice', 'print', 'connect'),
    ]

    open()
    cursor.executemany(
        '''INSERT INTO question (question, answer, wrong1, wrong2, wrong3)
           VALUES (?, ?, ?, ?, ?)''',
        questions
    )
    conn.commit()
    close()


def add_quiz():
    '''Add sample quiz categories.'''
    quizes = [
        ('Computer basics',),
        ('Python and Flask',),
        ('SQL and databases',),
    ]

    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()


def add_links():
    '''Connect questions to quizzes.'''
    links = [
        (1, 1), (1, 2), (1, 5),
        (2, 4), (2, 6), (2, 7), (2, 9), (2, 10),
        (3, 3), (3, 8),
    ]

    open()
    cursor.executemany(
        '''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)''',
        links
    )
    conn.commit()
    close()


def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()


def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')


def get_question_after(last_id=0, quiz_id=1):
    '''Return the next question after last_id for the selected quiz.'''
    query = '''SELECT quiz_content.id, question.question, question.answer,
                      question.wrong1, question.wrong2, question.wrong3
               FROM question, quiz_content
               WHERE quiz_content.question_id == question.id
               AND quiz_content.id > ? AND quiz_content.quiz_id == ?
               ORDER BY quiz_content.id'''
    open()
    cursor.execute(query, [last_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result


def get_quizes():
    '''Return a list of quizzes as (id, name).'''
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result


def get_quiz_count():
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open()
    cursor.execute(query)
    result = cursor.fetchone()
    close()
    return result


def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return choice(result)[0]


def check_answer(q_id, answer):
    '''Check whether the submitted answer is correct for this quiz question.'''
    query = '''SELECT question.answer
               FROM quiz_content, question
               WHERE quiz_content.id = ?
               AND quiz_content.question_id = question.id'''
    open()
    cursor.execute(query, [q_id])
    result = cursor.fetchone()
    close()

    if result is None:
        return False

    return result[0] == answer


def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_tables()


if __name__ == '__main__':
    main()
