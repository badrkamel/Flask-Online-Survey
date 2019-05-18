#coding: utf-8
from flask import Flask, render_template, redirect, url_for, request
from flask_mail import Mail,Message
from threading import Thread
from forms import EmailForm
import os

# Initialize app
app = Flask(__name__)

# Configuration

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "flask-task-secret"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME'),
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD'),

mail = Mail(app)

# Send asynchronous emails
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


# Name and email of user who will receive our survey.
name = 'your-name'
recipients = ['user@email.com']


# send an email to the user
@app.route('/', methods=['GET'])
def index():
    try:
    
        msg = Message(subject='Survey For You ' + name,
                        # Get user e-mail from the environment.
                        sender=os.environ.get('MAIL_USERNAME'),
                        recipients=recipients)

        msg.html = render_template('email_pages/message.html', name=name)

        thread = Thread(target=send_async_email, args=[app,msg])
        thread.start()

        mail.send(msg)
    except Exception as e:
        # Redirect to the error page if an error occurs.
        return redirect(url_for('error'))

    title = 'Email sent successfully'
    template_path = 'index.html'
    return render_template (template_path, title=title, name=name)


# contact page
@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = EmailForm()
    if request.method == 'POST':
        try:
            
            print(request.remote_addr) # Get IP address of visitors
            print(form.full_name.data) # Get full name
            print(form.choices.data) # Get vlaue of choice
            print(recipients) # Recipients

            # Fill in the database
			"""Here
			"""

            return redirect(url_for('thank_you'))

        except Exception as e:
            return redirect(url_for('error'))
            
    template_path = 'email_pages/contact_page.html'
    return render_template (template_path, title='Contact page', form=form)


# Error page
@app.route('/error')
def error():
    template_path = 'email_pages/error_page.html'
    return render_template(template_path, title="Error")

# Thank you page
@app.route('/thank-you')
def thank_you():
    template_path = 'email_pages/thankyou_page.html'
    return render_template(template_path, title="Thank you")


if __name__ == '__main__':
    app.run()