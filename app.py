from flask import Flask, render_template, request, url_for

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

if __name__ == "__main__":
	app.run(debug=True)
