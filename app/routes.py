from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from your_models_module import db, Restaurant, Pizza, RestaurantPizza
from your_validations_module import RestaurantForm, RestaurantPizzaForm

app = Flask(__name__)
api = Api(app)

# Route for getting all restaurants
class RestaurantsResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurant_list = []
        for restaurant in restaurants:
            restaurant_data = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            restaurant_list.append(restaurant_data)
        return jsonify(restaurant_list)

api.add_resource(RestaurantsResource, '/restaurants')

# Route for getting a specific restaurant by ID
class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            pizzas = [{"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients} for pizza in restaurant.pizzas]
            restaurant_data = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": pizzas
            }
            return jsonify(restaurant_data)
        else:
            return jsonify({"error": "Restaurant not found"}), 404

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            # Delete associated RestaurantPizza entries
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({"error": "Restaurant not found"}), 404

api.add_resource(RestaurantResource, '/restaurants/<int:id>')

# Route for getting all pizzas
class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizza_list = [{"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients} for pizza in pizzas]
        return jsonify(pizza_list)

api.add_resource(PizzasResource, '/pizzas')

# Route for creating a new RestaurantPizza
class RestaurantPizzasResource(Resource):
    def post(self):
        form = RestaurantPizzaForm(request.json)
        if form.validate():
            pizza_id = form.pizza_id.data
            restaurant_id = form.restaurant_id.data
            price = form.price.data

            restaurant = Restaurant.query.get(restaurant_id)
            pizza = Pizza.query.get(pizza_id)

            if restaurant and pizza:
                restaurant_pizza = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
                db.session.add(restaurant_pizza)
                db.session.commit()
                return jsonify({"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients})
            else:
                return jsonify({"errors": ["Invalid restaurant or pizza ID"]}), 400
        else:
            return jsonify({"errors": form.errors}), 400

api.add_resource(RestaurantPizzasResource, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(debug=True)
