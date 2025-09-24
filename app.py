from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from random import randint

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'quizzer1pro@gmail.com'
app.config['MAIL_PASSWORD'] = 'qkdk onns awhj fnuz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        otp = randint(100000, 999999)
        session['otp'] = otp
        session['email'] = email

        # Send email
        msg = Message('Your OTP Code', sender='your_email@gmail.com', recipients=[email])
        msg.body = f'Your OTP code is {otp}'
        mail.send(msg)
        flash('OTP has been sent to your email!', 'info')
        return redirect(url_for('verify_otp'))
    return render_template('index.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form['otp']
        if 'otp' in session and str(session['otp']) == user_otp:
            flash('Email verified successfully!', 'success')
            return redirect(url_for('success'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect(url_for('verify_otp'))
    return render_template('otp.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
