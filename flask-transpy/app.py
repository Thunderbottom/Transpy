import flask_transpy
from flask import Flask, render_template, json, request

app = Flask(__name__)


@app.route("/")
@app.route("/main")
def main():
    return render_template('get_translated.html')


@app.route('/translateText', methods=['POST', 'GET'])
def translateText():
    _input = request.form['inputString']
    _iter = int(request.form['inputIter'])
    translated_text = []
    og_lang_text = []
    languages = []
    text_color = 'text-success'

    if _input and _iter:
        translated_text, og_lang_text, languages, cosineVal = flask_transpy.get_items(
            input_string=_input, iterations=_iter)
        if cosineVal < 0.7:
            text_color = 'text-warning'
        elif cosineVal < 0.3:
            text_color = 'text-danger'
        return render_template('response.html', translation=translated_text, original_lang=og_lang_text, language=languages, cos_val=cosineVal, color=text_color)

if __name__ == "__main__":
    app.run(port=5000)
