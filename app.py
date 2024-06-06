from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/start', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/')
def start():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def question(qid):
    responses = session.get('responses', [])
    if qid != len(responses):
        flash("Invalid question ID.")
        return redirect(f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question_num=qid, question=question)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['answer']
    responses = session.get('responses', [])
    responses.append(answer)
    session['responses'] = responses

    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
