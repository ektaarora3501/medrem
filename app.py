from flask import Flask,render_template,redirect,url_for,request,session
from form import Regis_form,login_form,veri_form
from twilio.rest import Client
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError,InvalidRequestError
from random import randint
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user

account_sid="AC8d9cd796662e71009515af66742adac0"
auth_token="959724443bbd2ab2ffaf4edcb774dcbf"

client = Client(account_sid,auth_token)

from_whatsapp_number='whatsapp:+14155238886'           #+14155238886

to_whatsapp_number='whatsapp:+918360581227'



app=Flask(__name__)

app.config['SECRET_KEY']="00b70837bacb0419eec283e85a1d4810"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data_new.db'
db=SQLAlchemy(app)
login=LoginManager(app)

class otpv(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     otp=db.Column(db.Integer,unique=True,nullable=False)

     def __repr__(self):
          return f"otpv('{self.otp}')"

class log2(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     ot=db.Column(db.String(10),unique=True,nullable=False)
     def __repr__(self):
          return f"log2('{self.ot}')"


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register",methods=['GET','POST'])
def register():
    form=Regis_form()
    if form.validate_on_submit():
           print("valid")
           phone=request.form.get('phone_no')

           return redirect(url_for('verification',phone=phone))
    return render_template("register.html",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form=login_form()
    if form.validate_on_submit():
        print("valid")
    return render_template("login.html",form=form)


@app.route("/verification/<phone>",methods=['GET','POST'])
def verification(phone):
        form=veri_form()
        count=0
        m=0
    #if form.validate_on_submit():

        #print(message.sid)
        if form.validate_on_submit():
            ot=request.form.get('otp')
            #n=otpv.query.filter_by(id=1).first()
            print(ot,n.otp)
            #m=n.otp
            if(ot==m):
                print("true")
                #db.session.remove(m)
                #db.session.commit()
                return redirect(url_for('index'))
            else:
                error='invalid otp'
                return render_template('verification.html',error=error,form=form,phone=phone)

        m=secrets.token_hex(2)
        print('m=',m)
        p=log2(ot=m)
        db.session.add(m)
        #db.session.commit()
        count=count+1
        client.messages.create(body='your otp is \n'+ str(m),
                            from_=from_whatsapp_number,
                             to=to_whatsapp_number)
        return render_template('verification.html',form=form,phone=phone)

@app.route("/dashboard/<username>")
def dashboard(username):
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True)
