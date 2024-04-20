from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app
)

from app.db import getDB
import requests

bp = Blueprint('mail', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search', '') 
    db, c = getDB()

    if search.strip():
        c.execute('SELECT * FROM email WHERE content LIKE %s', ('%' + search + '%',))
    else:
        c.execute('SELECT * FROM email')
        
    mails = c.fetchall()
    return render_template('mails/index.html', mails=mails)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []
        
        if not email:
            errors.append('Email es obligatorio')
        if not subject:
            errors.append('El asunto es obligatorio')
        if not content:
            errors.append('El contenido es obligatorio')

        if len(errors) == 0:
            db, c = getDB()
            c.execute('INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)', (email, subject, content))
            db.commit()
            send(email, subject, content)
            return redirect(url_for('mail.index'))
            
        else:
            for error in errors:
                flash(error)
        
        print(errors)
    return render_template('mails/create.html')

def send(to, subject, content):
    try:
        print(to + ' ' + subject + ' ' + content)
        response = requests.post(
            f"https://api.mailgun.net/v3/{current_app.config['MAILGUN_DOMAIN']}/messages",
            auth=("api", current_app.config['MAILGUN_KEY']),
            data={"from": f"no-reply@{current_app.config['MAILGUN_DOMAIN']}",
                  "to": [to],
                  "subject": subject,
                  "text": content})
        if response.status_code != 200:
            print(f"Failed to send email: {response.text}")
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
