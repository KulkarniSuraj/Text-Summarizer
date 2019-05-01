from flask import Flask, render_template, request, url_for
import text_summarizer
import os

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")
	
@app.route("/services")
def services():
	return render_template("services.html")

@app.route("/webSummary")
def web_summary():
	return render_template("WebSum.html")

@app.route("/docSummary")
def doc_summary():
	return render_template("DocSum.html")

@app.route("/webSummary", methods=['POST', 'GET'])
def my_url():
	url = request.form['urltext']
	return text_summarizer.get_summary(url.strip())
	

@app.route('/docSummary', methods=['POST'])
def submit_text():
	user_text = request.form['userText']
	return render_template("DocSum.html", p=text_summarizer.summarize_text(user_text))

@app.route('/docSummary', methods=['POST', 'GET'])
def upload_file():
	pass


if __name__ == "__main__":
	app.run(debug=True)
