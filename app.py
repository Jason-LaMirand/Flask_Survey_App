from pdb import post_mortem
from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from random import randint,  choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "cheese"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    """Shows home page of application."""

    title = survey.title
    instructions = survey.instructions

    return render_template('start_survey.html', title=title, instructions=instructions)


@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    return redirect("/questions/0")


@app.route('/questions/<int:question_id>')
def show_questions(question_id):
    """Shows question of the survey"""
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != question_id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_id]

    return render_template('questions.html', question_number=question_id, question=question)


@app.route('/answer', methods=["POST"])
def handling_answers():
    answers = request.form['answer']

    responses.append(answers)

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def finished_survey():

    return render_template('complete.html')
