# Import necessary modules and classes
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app,db)
db.init_app(app)

# Route to get a list of bakeries
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = []
    
    for bakery in bakeries:
        bakery_list.append({
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    response = make_response(
        jsonify(bakery_list),200
    )
    return response 

# Route to get details of a specific bakery by ID
@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if bakery:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        response = make_response(
        jsonify(bakery_data),200
        )
        return response 
    else:
        return jsonify({'error': 'Bakery not found'}), 404

# Route to get a list of baked goods sorted by price
@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_list = []

    for baked_good in baked_goods:
        baked_goods_list.append({
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

        response = make_response(
        jsonify(baked_goods_list),200
        )
    return response 

# Route to get the most expensive baked good
@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if baked_good:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        response = make_response(
        jsonify(baked_good_data),200
        )
        return response 
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
