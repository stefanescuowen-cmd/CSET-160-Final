from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
app = Flask(__name__)



conn_str = "mysql://root:Yohan969$$@localhost/exam_platform"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/base')
def base():
    return render_template('base.html')