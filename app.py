from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://iotStudent:zxcv2010@localhost/python-test-db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class GardenTool(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight = db.Column(db.Float)
    price = db.Column(db.Float)
    country_of_origin = db.Column(db.String(length=50))
    manufacturer = db.Column(db.String(length=100))

    def __init__(self,
                 weight,
                 price,
                 country_of_origin,
                 manufacturer):
        self.weight = weight
        self.price = price
        self.country_of_origin = country_of_origin
        self.manufacturer = manufacturer


class GardenToolSchema(ma.Schema):
    class Meta:
        fields = ('weight', 'price',
                  'country_of_origin', 'manufacturer')


garden_tool_schema = GardenToolSchema()
garden_tools_schema = GardenToolSchema(many=True)
db.create_all()


@app.route("/garden_tool", methods=["POST"])
def add_garden_tool():
    weight = request.get_json()["weight"]
    price = request.get_json()["price"]
    country_of_origin = request.get_json()["country_of_origin"]
    manufacturer = request.get_json()["manufacturer"]

    new_garden_tool = GardenTool(weight, price, country_of_origin, manufacturer)

    db.session.add(new_garden_tool)
    db.session.commit()

    return garden_tool_schema.jsonify(new_garden_tool)


@app.route("/garden_tool", methods=["GET"])
def get_garden_tool():
    all_garden_tools = GardenTool.query.all()
    result = garden_tools_schema.dump(all_garden_tools)
    return jsonify(result.data)


@app.route("/garden_tool/<id>", methods=["GET"])
def garden_tool_detail(id):
    garden_tool = GardenTool.query.get(id)
    return garden_tool_schema.jsonify(garden_tool)


@app.route("/garden_tool/<id>", methods=["PUT"])
def garden_tool_update(id):
    garden_tool = GardenTool.query.get(id)
    weight = request.get_json()["weight"]
    price = request.get_json()["price"]
    country_of_origin = request.get_json()["country_of_origin"]
    manufacturer = request.get_json()["manufacturer"]

    garden_tool.weight = weight
    garden_tool.price = price
    garden_tool.country_of_origin = country_of_origin
    garden_tool.manufacturer = manufacturer

    db.session.commit()
    return garden_tool_schema.jsonify(garden_tool)


@app.route("/garden_tool/<id>", methods=["DELETE"])
def garden_tool_delete(id):
    garden_tool = GardenTool.query.get(id)
    db.session.delete(garden_tool)
    db.session.commit()

    return garden_tool_schema.jsonify(garden_tool)


if __name__ == '__main__':
    app.run(debug=True)
