from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from pymongo import MongoClient
from flask import jsonify
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
myclient = MongoClient("mongodb://10.0.0.13:27017/")
mydb = myclient["cloudapp"]
mycol = mydb["messages"]
# Issue the serverStatus command and print the results

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Message:', validators=[validators.required()])


@app.route("/send", methods=['GET', 'POST'])
def send():
    data = request.get_data()
    print(data)
    message = data.decode("utf-8").split("=")[1]
    result = mycol.insert_one({'message': message})
    form = ReusableForm(request.form)
    return render_template('hello.html', form=form)

@app.route("/retreive", methods=['GET', 'POST'])
def retreive():
    messages = {}
    count = 0
    for x in mycol.find():
        count += 1
        messages[str(count)] = x['message']
    return jsonify(messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='50001')
