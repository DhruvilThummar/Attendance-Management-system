from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login")
def login():    
    return render_template("login.html")

@app.route("/register")
def register():    
    return render_template("register.html")

@app.route("/superadmindashboard")
def dashboard():    
    return render_template("superadmin/sudashbord.html")

@app.route("/collegedashboard")
def cdashboard():    
    return render_template("college/cdashbord.html")

@app.route("/hoddashboard")
def hdashboard():    
    return render_template("hod/hdashbord.html")

@app.route("/studentdashboard")
def sdashboard():    
    return render_template("student/sdashbord.html")

@app.route("/parentdashboard")
def pdashboard():    
    return render_template("parent/pdashbord.html")

if __name__ == "__main__":
    app.run(debug=True)