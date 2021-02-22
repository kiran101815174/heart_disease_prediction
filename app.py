#Set-ExecutionPolicy Unrestricted -Scope Process
#set FLASK_APP=app.py
import flask
from flask import Flask
from flask import render_template,request
app=Flask(__name__)
import pickle
import os

IMAGE_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
@app.route('/')
def main():
    show=['' for i in range(13)]
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'doctor.jpg')

    return render_template('basic.html',message="Submit",user_image=full_filename)
@app.route('/results',methods=['POST'])
def display():
    cells=[]
    for i in range(1,14):
        if i!=10:
            cells.append(int(request.form.get(f"cells{i}")))
        else:
            cells.append(float(request.form.get(f"cells{i}")))
    with open("heart_predict_model_final","rb") as f:
        with open("scaling_factors_final","rb") as f2:
            scaler_model=pickle.load(f2)
            predict_model=pickle.load(f)
    a,b,c,d,e=cells[0],cells[3],cells[4],cells[7],cells[9]
    x=scaler_model.transform([[cells[0],cells[3],cells[4],cells[7],cells[9]]])
    cells[0],cells[3],cells[4],cells[7],cells[9]=x[0]
    y_predict=predict_model.predict([cells])
    if y_predict== 1:
        message="sir/madam,you have a high chance of having a hear disease---Dr.AI"
    else:
        message="sir/madam, you are less likely to have a heart disease----Dr.AI"
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'doctor.jpg')

    return render_template("basic.html",message=message,a=a,b=b,c=c,d=d,e=e,user_image=full_filename)