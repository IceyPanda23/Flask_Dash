from flask import Flask,request,render_template,redirect,url_for,jsonify,flash,send_file,make_response,session
from sqlalchemy import create_engine,text as sql_text,Column,Integer,String,Text,select
from sqlalchemy.orm import sessionmaker,declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
import os
from pathlib import Path
import json
import uuid
from datetime import datetime,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from redis import Redis



app = Flask(__name__)
app.secret_key = "15561db9a8468cc46c9828aa29f1fa0591084aa2fd839ab3c6a68a49cf26f89ef6fe1d6faecf2647606e001b8a557301b118d665288244b1cb93b5e4c046696c"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
DB_PASS = '*Grundig3603644998745'
DB_USERNAME = 'adminsuperadmin2026'
DB_HOST = 'image_dashboard_ipo_pg'
DB_PORT = '5432'
DB_NAME = 'IMAGE_IPO_DASHBOARD'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='flask_redis',port=6379,db=0)
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_SECURE'] = False      # must be True for HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # prevents CSRF issues
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'ipo_users'
    id = db.Column(Integer,primary_key=True)
    username = db.Column(String,nullable=False)
    password = db.Column(Text,nullable=False)
    role = db.Column(String,nullable=False,server_default="2")
    email = db.Column(String(60),nullable=False,unique=True)
    code = db.Column(String(60),nullable=False,unique=True)



@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('Both email and password are required for login','error')
            return redirect(url_for('login'))
        select_query = select(User).where(User.email == email)
        user = db.session.execute(select_query).scalar_one_or_none()
        if user and check_password_hash(user.password,password):
            session['role'] = user.role
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect Username / Password. Kindly try again .','error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/settings',methods=['GET','POST'])
def settings():
    return render_template('settings.html',username=session['username'],role=session['role'])

@app.route('/',methods=['POST','GET'])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html',username = session['username'],role = session['role'])
    else:
        return redirect(url_for('login'))




