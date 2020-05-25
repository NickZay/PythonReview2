from flask import Flask, render_template, request, redirect, url_for
from functions import calculate, generate
import os
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'C::\\PythonProjects\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#def calculate(input_file='Alice.txt', probabilities_file='probabilities.txt', depth=3):
#def generate(probabilities_file='probabilities.txt', output_file=None, depth=3, count=50, verbosity=0):


@app.route("/", methods=["GET", "POST"])
def get_home():
    if request.method == "POST":
        if not os.path.exists('uploads'):
            os.mkdir("uploads")
        input_file = request.files['input_file']
        filename = secure_filename(input_file.filename)
        path = os.path.join('uploads', filename)
        input_file.save(path)
        input_depth = request.form["depth"]
        input_count = request.form["count"]
        input_verbosity = request.form["verbosity"]
        message_small = '''
            <html>
            <body>
            <p>{result[0]}</p>
            <p><a href="/">Back</a>
            </body>
            </html>
               '''
        message_big = '''
                    <html>
                    <body>
                    <p>{result[0]}</p>
                    <p>{result[1]}</p>
                    <p>{result[2]}</p>
                    <p>{result[3]}</p>
                    <p><a href="/">Back</a>
                    </body>
                    </html>
                       '''
        calculate(path, int(input_depth))
        result = generate(int(input_depth), int(input_count), int(input_verbosity))
        if len(result) > 1:
            return message_big.format(result=result)
        return message_small.format(result=result)
    return render_template("home.html")


@app.route("/about")
def get_about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

