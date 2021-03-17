from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from marshmallow import Schema, fields, ValidationError, pre_load


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
# initialize the database with the settings from app
db = SQLAlchemy(app)

# MODEL#
class BudgetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    recurring = db.Column(db.Boolean, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)

# SCHEMA #
class BudgetItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    cost = fields.Float()
    date_created = fields.DateTime()
    recurring = fields.Boolean()
    due_date = fields.DateTime()



# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/budgets', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return "hello"


if __name__ == "__main__":
    app.run(debug=True)
