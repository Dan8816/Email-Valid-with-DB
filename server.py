from flask import Flask, render_template, request, redirect, session, flash, url_for
import re
from datetime import datetime, date, time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

mysql = connectToMySQL('emailsdb')

@app.route('/')
def index():
    all_emails = mysql.query_db("select * from emails")
    print("fetched all emails", all_emails)
    print('#'*50)
    return render_template("index.html", emails = all_emails)

@app.route('/success')
def success():
    all_emails = mysql.query_db("select * from emails")
    print("fetched all emails", all_emails)
    print('#'*50)
    return render_template('success.html', emails = all_emails)

#@app.route('/remove')
#def remove():
    #all_emails = mysql.query_db("select * from emails")
    #query = "DELETE FROM emails WHERE id = (%(id)s);"
    #id = {
        #'id': each['id']
    #}
    #mysql.querry_db(query2, id)
    #return redirect('/success')

@app.route('/process', methods=['POST'])
def validaShun():
    print("entering validation testing")
    errors = 0
    if 'email' not in session:
        session['email'] = ''
    if request.form['email'] == '':
        flash('Gimme an email', 'emailError')
        return redirect('/')
    if not EMAIL_REGEX.match(request.form['email']):
        flash('You born under a rock, 1980 called!', 'emailError')
        return redirect('/')
    else:
        print('user submit was successfull')
        session['email'] = request.form['email']
        query = "INSERT INTO emails (email) VALUES (%(email)    s);"
        email = {
                'email': session['email']
               }
        print(email)
        mysql.query_db(query, email)
        return redirect('/success')

if __name__ == "__main__":
    
    app.run(debug=True)


