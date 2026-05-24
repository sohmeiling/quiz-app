# code for the web application
import os
from random import shuffle

from flask import Flask, redirect, render_template, request, session, url_for

from db_scripts import check_answer, get_question_after, get_quizes


folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'


def start_quiz(quiz_id):
    '''Create the values we need to remember during one quiz.'''
    session['quiz'] = int(quiz_id)
    session['last_question'] = 0
    session['total'] = 0
    session['answers'] = 0


def end_quiz():
    '''Clear the quiz data for this user.'''
    session.clear()


def index():
    '''First page: choose a quiz, then start the selected quiz.'''
    if request.method == 'GET':
        return render_template('start.html', q_list=get_quizes())

    quiz_id = request.form.get('quiz')
    start_quiz(quiz_id)
    return redirect(url_for('test'))


def question_form(question):
    '''Create the question page from a database record.'''
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template(
        'test.html',
        question=question[1],
        quest_id=question[0],
        answers_list=answers_list
    )


def save_answers():
    '''Save progress and update the score after the user answers.'''
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')

    session['last_question'] = int(quest_id)
    session['total'] += 1

    if check_answer(quest_id, answer):
        session['answers'] += 1


def test():
    '''Question page: save POSTed answers and show the next question.'''
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))

    if request.method == 'POST':
        save_answers()

    next_question = get_question_after(
        session['last_question'],
        session['quiz']
    )

    if next_question is None or len(next_question) == 0:
        return redirect(url_for('result'))

    return question_form(next_question)


def result():
    '''Show the final score and then reset the quiz session.'''
    correct = session.get('answers', 0)
    total = session.get('total', 0)
    end_quiz()
    return render_template('result.html', answers=correct, total=total)


app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
app.add_url_rule('/result', 'result', result)


if __name__ == '__main__':
    app.run()