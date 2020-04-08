from flask import Flask,render_template,request,redirect,session,url_for
import json
import subprocess
from flask_wtf import FlaskForm
from wtforms import RadioField

SECRET_KEY = 'development'

app=Flask(__name__)
app.secret_key = "the phenominals"

app.config.from_object(__name__)

class SimpleForm(FlaskForm):
    example = RadioField('Time', choices=[
        (1,'30 min'), (2,'1 hour'),(3,'1 hour & 30 min'),(4,'2 hour'),],
        default=1, coerce=int)


with open('config.json','r') as c:
    params=json.load(c)['params']

@app.route('/')
def index():
    return 'bhai apka swagat hai apni website mein'

@app.route('/vidyoconnector')
def videoconnector():
    if 'user' in session:
        return render_template('VidyoConnector.html',host=params['app_id'])

@app.route('/vidyoconnectorcustom')
def vconnectcustom():
    if 'user' in session:
        return render_template('VidyoConnectorCustomLayout.html',host=params['app_id'])

@app.route('/launcher')
def vlauncher():
    if 'user' in session:
        return render_template('VidyoConnectorLauncher.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    if(request.method=='POST'):
        username=request.form['username']
        password=request.form['password']
        cuser=params['teacher']
        cpass=params['password']
        if( username == cuser and password == cpass ):
            session['user']=username
            return redirect(url_for('teacher_token'))
        else:
            return redirect(url_for('admin'))
    return render_template('admin.html')


@app.route('/teacher_token',methods=['GET','POST'])
def teacher_token():
    # Generating token ....
    if 'user' in session:
         if(request.method=='POST'):
                forms = SimpleForm()
                time=forms.example.data
                timeinsec=0
                if time==1:
                    timeinsec=1800
                elif time==2:
                    timeinsec=3600
                elif time==3:
                    timeinsec=5400
                else:
                    timeinsec=7200
                Token = generateToken(timeinsec)
                return render_template('teacher.html', token=Token, form=forms)
    elif 'user' not in session:
        return render_template('admin.html')
    if(request.method=='GET'):
        forms = SimpleForm()
        return render_template('teacher.html',form=forms)

def generateToken(timeinsec):
     key = params['dkey']
     appID = params['rapp_id']
     user = params['userName']
     expires = str(timeinsec)
     token_result = str(subprocess.getoutput("python generateToken.py --key=" + key + " --appID=" + appID + " --userName=" + user + " --expiresInSecs=" + expires)).split('\n')
     generated_token = token_result[-1]
     return generated_token


@app.route('/student')
def student():
    return render_template('student.html')


@app.route('/logout')
def logout():
        if 'user' in session:
            session.pop('user', None)
            return render_template('logout.html')
        return render_template('admin.html')

@app.route('/gettoken')
def gettoken():
        if 'user' in session:
            return render_template('publish_token.html')
        return render_template('admin.html')

app.run(debug=True)