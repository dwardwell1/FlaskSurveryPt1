from flask import Flask, request, render_template, redirect, flash, jsonify, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from surveys import Question, Survey, satisfaction_survey


app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

RESPONSES_KEY = 'responses'

@app.route('/' )
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions = instructions)

@app.route('/start', methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/questions/<int:num>')
def question_page(num):
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
         return render_template("thanks.html")

    if (len(responses) != num):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {num}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[num]
    return render_template(
        "question.html", question_num=num, question=question.question, choices=question.choices)
    


   

   
@app.route('/answer', methods=["POST"])
def answers():
    responses = session[RESPONSES_KEY]
    choice = request.form["choice_selection"]
    responses.append(choice)
    session[RESPONSES_KEY] = responses 
    if (len(responses) == len(satisfaction_survey.questions)):
        
        return render_template("thanks.html")

    else:
        return redirect(f"/questions/{len(responses)}")
  
 
