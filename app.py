from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
# initialize the database with the settings from app
db = SQLAlchemy(app)

class BudgetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    recurring = db.Column(db.Boolean, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Budget_Item %r>' % self.id



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
