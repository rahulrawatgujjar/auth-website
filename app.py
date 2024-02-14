from flask import Flask, render_template, request, jsonify,redirect,url_for,flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
db_string=os.environ.get("DB_STRING")
secret_key=os.environ.get("SECRET_KEY")

app=Flask(__name__)
app.config['SECRET_KEY'] = secret_key
# app.config['SQLALCHEMY_DATABASE_URI'] = "ente db_url"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine=create_engine(db_string)

# db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
  return User.get(user_id)

class User(UserMixin):
  def __init__(self,user_id,name,email):
    self.id=user_id
    self.name=name
    self.email=email

  @staticmethod
  def get(user_id):
    with engine.connect() as conn:
      query=text("SELECT name,email FROM users where id=:user_id")
      parameters={"user_id":user_id}
      result=conn.execute(query,parameters)
      conn.commit()
      result=result.all()
      result=result[0]._asdict()
      return User(user_id,result["name"],result["email"])


@app.route("/")
def home():
  return render_template("home.html")

@app.route("/login",methods=["GET","POST"])
def login():
  if request.method=="POST":
    data=request.form
    email,password=data["email"],data["password"]
    with engine.connect() as conn:
      query=text("SELECT id,name,email,password FROM users WHERE email=:email")
      parameters={
        "email":email
      }
      result=conn.execute(query,parameters).first()
      conn.commit()
      if result:
        result=result._asdict()
        if check_password_hash(result["password"],password):
          user=User(user_id=result["id"],name=result["name"],email=result["email"])
          login_user(user)
          return redirect(url_for("dashboard"))
        else:
          flash("Invalid Password","error")
      else:
        flash("Invalid Username","error")
      return render_template("login.html")
  return render_template("login.html")



@app.route("/register",methods=["GET","POST"])
def register():
  if request.method=="POST":
    data=request.form
    name,email,password=data["name"],data["email"],data["password"]
    hashed_password=generate_password_hash(password)
    with engine.connect() as conn:
      # checking that user already exist or not
      query=text("SELECT id,name,email,password FROM users WHERE email=:email")
      parameters={
        "email":email
      }
      result=conn.execute(query,parameters).first()
      conn.commit()
      if result:
        flash("Email alrgeady exists","error")
        return render_template("register.html")
      else:
        query=text("INSERT INTO users(name,email,password) VALUES(:name,:email,:password)")
        parameters={
          "name":name,
          "email":email,
          "password":hashed_password
        }
        conn.execute(query,parameters)
        conn.commit()
        flash("Registration successfull. Please login.","success")
        return redirect(url_for("login"))
  return render_template("register.html")


@app.route("/dashboard")
@login_required
def dashboard():
  return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("login"))



if __name__=="__main__":
  app.run(host="0.0.0.0",debug=True)