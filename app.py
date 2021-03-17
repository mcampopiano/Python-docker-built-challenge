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

budgets_schema = BudgetItemSchema(many=True)


###### API #######

# @app.route('/budgets', methods=['POST', 'GET'])
# def get_budget_items():
#     budget_itmes = BudgetItem.query.all()
#     result = budgets_schema.dump(budget_itmes)
#     return {"budget items": result}

@app.route('/budgets', methods=['POST', 'GET'])
def handle_requests():
    if request.method == 'GET':
        budget_itmes = BudgetItem.query.all()
        result = budgets_schema.dump(budget_itmes)
        return {"budget items": result}
    elif request.method == 'POST':
        json_data = request.get_json()
        print(type(json_data))
        try:
            data = budgets_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        name = data['name']
        cost = data['cost']
        recurring = data['recurring']
        date_created = datetime.datetime.utcnow()
        # due_date = data['dueDate']
        budget_item = BudgetItem(name=name, cost=cost,recurring=recurring,
        date_created=date_created)
        db.session.add(budget_item)
        db.session.commit()
        result = budgets_schema.dump(budget_item.query.get(budget_item.id))
        return {"message": "Created a new budget item", "budget Item": result}




if __name__ == "__main__":
    app.run(debug=True)
