from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from surveys import Question, Survey, satisfaction_survey


app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

responses = []

@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions = instructions)

@app.route('/questions/<num>')
def question_page(num):
    num = int(num)
    responses_num = len(responses)
    if num == responses_num:
        question = satisfaction_survey.questions[num].question
        choices = satisfaction_survey.questions[num].choices
        return render_template('question.html', question = question, num = num, choices = choices )
    if responses_num >= len(satisfaction_survey.questions):
         return f"thank you for completing survey"
    if num > responses_num or num < responses_num:
        flash("Redirected to current survery question")
        return redirect(f'/questions/{responses_num}') 


   

   
@app.route('/answer', methods=["POST"])
def answers():
    answer = request.form['choice_selection']
    num = int(request.form["q_id"]) 
    last_q = len(satisfaction_survey.questions)
    if num >= last_q - 1:
        responses.append(answer)
        return render_template("/thanks.html")
    else:    
        responses.append(answer)
        num += 1
        return redirect(f'/questions/{num}')
    
 
