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


# ========== super admin routes -============
@app.route("/superadmindashboard")
def dashboard():    
    return render_template("superadmin/subase.html")

@app.route("/superadmin/profile")
def profile():    
    return render_template("superadmin/profile.html")


# ========== college routes -============
@app.route("/collegedashboard")
def cdashboard():    
    return render_template("college/cbase.html")

@app.route("/college/profile")
def cregister():    
    return render_template("college/profile.html")


# ========== hod routes -============
@app.route("/hoddashboard")
def hdashboard():    
    return render_template("hod/hbase.html") 

@app.route("/hod/profile")
def hregister():    
    return render_template("hod/profile.html")


# ========== faculty routes -============
@app.route("/facultydashboard")
def fdashboard():    
    return render_template("faculty/fbase.html")

@app.route("/faculty/profile")
def fregister():    
    return render_template("faculty/profile.html")


# ========== student routes -============
@app.route("/studentdashboard")
def sdashboard():    
    return render_template("student/sbase.html")

@app.route("/student/profile")
def sregister():
    return render_template("student/profile.html")



# ========== parent routes -============
@app.route("/parentdashboard")
def pdashboard():    
    return render_template("parent/pbase.html")

@app.route("/parent/profile")
def pregister():
    return render_template("parent/profile.html")


if __name__ == "__main__":
    app.run(debug=True)