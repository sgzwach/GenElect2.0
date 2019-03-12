from flask import Flask, render_template, url_for

#set app to flask instance
app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/login")
def login():
    return render_template('index.html')

@app.route("/register")
def register():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True) #start app in debug mode