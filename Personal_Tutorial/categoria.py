### pip install flask
### pip install flask-sqlalchemy
### pip install flask-marshmallow
### pip install marshmallow-sqlalchemy
### pip install pymysql

from flask import Flask,jsonify
from flask_sqlalchemy import sqlalchemy
from flask_marshmallow import Marshmallow

app = flask(__name__)
app.config['SQ']

### Mensaje de bienvenida 
@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenida'})

if __name__=="_main_":
    app.run(debug=True)