from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import json
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# Issue the serverStatus command and print the results

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Message:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)


    print(form.errors)
    if request.method == 'POST':
        if request.form['submit_button'] == 'Retreive':
            messages = requests.get('http://10.0.0.10:50001/retreive')
            messages = json.loads(messages.text)
            for key, value in messages.items():
                flash('Message ' + str(key) + " : " + str(value))
        elif request.form['submit_button'] == 'Submit':
            name = request.form['name']
            print(name)

            if form.validate():
                # Save the comment here.
                data = {'message': name }

                # sending post request and saving response as response object
                r = requests.post(url='http://10.0.0.10:50001/send', data=data)

            else:
                flash('All the form fields are required. ')
            pass  # do something else
        else:
            pass

        name = request.form['name']
        print(name)

    return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0')