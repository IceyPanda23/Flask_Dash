from flask import Flask,request,render_template,redirect,url_for,jsonify,flash,send_file,make_response
from sqlalchemy import create_engine,text as sql_text,Column,Integer,String
import pandas as pd
import os
from pathlib import Path
import json
import uuid


app = Flask(__name__)
app.secret_key = ""