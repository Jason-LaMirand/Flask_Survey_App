from pdb import post_mortem
from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from random import randint,  choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "cheese"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSE = "responses"


@app.route('/')
def home_page():
    """Shows home page of application. Gets information like 'title' and 'instructions' from the survey document."""

    title = survey.title
    instructions = survey.instructions

    return render_template('start_survey.html', title=title, instructions=instructions)


@app.route("/start", methods=["POST"])
def start_survey():
    """Clear response data."""
    session[RESPONSE] = []

    return redirect("/questions/0")


@app.route('/questions/<int:question_id>')
def show_questions(question_id):
    """Shows question of the survey"""
    responses = session.get(RESPONSE)

    if (responses is None):
        """return user to Home if they have not started the survey yet."""
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        """Sends user to the completion page if they have already answered all the questions."""
        return redirect("/complete")

    if (len(responses) != question_id):
        """sends user an error message if they typed in a wrong question id."""
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_id]

    return render_template('questions.html', question_number=question_id, question=question)


@app.route('/answer', methods=["POST"])
def handling_answers():
    """Gets the resonses from the form."""
    answer = request.form['answer']
    """Sends answers to questins and put them in the session[RESPONSE]"""
    responses = session[RESPONSE]
    responses.append(answer)
    session[RESPONSE] = responses

    if (len(responses) == len(survey.questions)):
        """if the responses are all there an equal to the same amount from the survey it pushes you to the completion page."""
        return redirect("/complete")

    else:
        """If not completed it will return you to the questions that you need to do in order."""
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def finished_survey():
    """Opens up a you have completed page."""
    return render_template('complete.html')
