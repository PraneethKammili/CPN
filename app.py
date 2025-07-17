from flask import Flask, session, url_for, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['user'] = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'qualification': request.form.get('qualification')
        }
        return redirect(url_for('register'))  

    return render_template('register.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate user logic here (e.g., check with DB or dummy values)
        if email == "user@example.com" and password == "123456":
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return "<h1>Welcome to the Dashboard!</h1>"
app.run(debug=True, use_reloader=True)