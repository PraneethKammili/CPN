from flask import Flask, session, url_for, render_template, redirect, request,flash
from otp import genotp
from cmail import send_mail
from stoken import entoken,dctoken
import bcrypt
import mysql.connector
app = Flask(__name__)
app.secret_key = 'demnii123'
from mysql.connector import (connection)
mydb=connection.MySQLConnection(user='root',host='localhost',password='_Praneeth_07_',db='cpn')

@app.route('/')
def welcome():
    return render_template('welcome.html')  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        qualification = request.form['qualification']
        otp=genotp()
        userdata={'name':name,'email':email,'password':password,'phone':phone,'qualification':qualification,'otp':otp}
        subject=f'OTP for CPN Registration'
        body=f'use the otp {otp}'
        send_mail(to=email,body=body,subject=subject)
        flash(f'OTP has sent to given mail {email}')
        return redirect(url_for('otpverify',endata=entoken(data=userdata)))
    return render_template('register.html')

@app.route('/otpverify/<endata>',methods=['GET','POST'])
def otpverify(endata):
    try:
        ddata=dctoken(data=endata)
    except Exception as e:
        print(f'Error in dcode admindata {e}')
        flash('could not verify otp')
        return redirect(url_for('register'))
    else:
        if request.method=='POST':
            uotp=request.form['otp']
            if uotp==ddata['otp']:
                salt=bcrypt.gensalt()
                hash=bcrypt.hashpw(ddata['password'].encode('utf-8'),salt)
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into userdata(name,email,password,phonenumber,qualification) values(%s,%s,%s,%s,%s)',[ddata['name'],ddata['email'],hash,ddata['phone'],ddata['qualification']])
                    mydb.commit()
                    
                except Exception as e:
                    print(f'Error is {e}')
                    flash('could not store data')
                    return redirect(url_for('register'))
                else:
                    flash(f'{ddata["email"]} successfully registered')
                    return redirect(url_for('login'))
            else:
                flash('otp wrong')
                return redirect(url_for('otpverify',endata=endata))
        return render_template('otpverify.html') 

@app.route('/login',methods=['GET','POST'])
def login():
    if not session.get('user'):
        if request.method=='POST':
            email=request.form['email']
            password=request.form['password'].encode('utf-8')
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select count(*) from userdata where email=%s',[email])
                email_count=cursor.fetchone()
                if email_count[0]==1:
                    cursor.execute('select password from userdata where email=%s',[email])
                    stored_password=cursor.fetchone()
                    if bcrypt.checkpw(password,stored_password[0]):
                        session['user']=email
                        return redirect(url_for('dashboard'))
                    else:
                        flash('password wrong')
                        return redirect(url_for('login'))
                else:
                    flash('Email not found')
                    return redirect(url_for('login'))
            except Exception as e:
                print(f'ERROR in login validation {e}')
        return render_template('login.html')
    else:
        return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    return "<h1>Welcome to the Dashboard!</h1>"
app.run(debug=True, use_reloader=True) 