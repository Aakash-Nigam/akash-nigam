from flask import Flask,render_template,redirect,request
import json

app = Flask(__name__)

with open('config.json','r') as c:
    params=json.load(c)['params']

@app.route('/')
def home():
 return render_template('index.html')

@app.route('/java')
def java():
 return render_template('java.html')

@app.route('/python')
def python():
 return render_template('python.html')

@app.route('/mysql')
def mysql():
 return render_template('mysql.html')

@app.route('/cards')
def cards():
 return render_template('cards.html')

@app.route('/video')
def video():
 return render_template('video.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='GET'):
      return render_template('login.html')
    else:
        return redirect('/')
@app.route('/signin',methods=['GET','POST'])
def signup():
    if(request.method=='GET'):
      return render_template('signin.html')
    else:
        return redirect('/')



app.run(debug="TRUE")
