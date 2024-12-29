from flask import Flask, render_template, request
from analyze import get_answer
from waitress import serve

app = Flask(__name__)

@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/coding', methods=['GET'])
def get_coding_answer():
    try:
        question = request.args.get('input')
        if not question:
            return render_template('index.html')
        
        # Get the raw response from get_answer without any parsing
        response = get_answer(question)
        
        return render_template('answer.html', myquestion=question, response=response)
    except Exception as e:
        return render_template('answer.html', myquestion=question, error=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.debug = True
    serve(app, host='0.0.0.0', port=8000)
