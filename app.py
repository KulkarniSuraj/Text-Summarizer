from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
import text_summarizer
import os
import codecs

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(file_name):
	with codecs.open(file_name, 'r', 'utf-8') as f:
		file_data = f.read()
		return file_data     

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



@app.route('/upload_text_file', methods=['POST', 'GET'])
def file_upload():
	if request.method == "POST":
		if request.files:
			txtf = request.files['txtfile']
			txtf.save(os.path.join(app.config["UPLOAD_FOLDER"], "mytext.txt"))
			print("file saved successfully")
			return text_summarizer.summarize_text(read_file('./uploads/mytext.txt'))

	return render_template("upload_file.html")


if __name__ == "__main__":
	app.run(debug=True)
