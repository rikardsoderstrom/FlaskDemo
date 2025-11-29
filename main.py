from flask import Flask, jsonify, request
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="postgresql+psycopg2",
    host="localhost",
    port="5432",
    username="postgres",
    password="Rikard99",
    database="flask_demo"
)

engine = create_engine(url)

app = Flask(__name__)
Session = sessionmaker(bind=engine)

@app.get('/users')
def get_users():
    with Session() as session:
        result = session.execute(text("SELECT * FROM users")).fetchall()
        users_list = [{"id": row.id, "name": row.name, "email": row.email} for row in result]

    return jsonify(users_list), 200


@app.get('/product')
def get_product():
    with Session() as session:
        result = session.execute(text("SELECT * FROM product")).fetchall()
        product_list = [{"id": row.id, "name": row.name, "price": row.price, "stock": row.stock} for row in result]

    return jsonify(product_list), 200


@app.get('/products/<int:product_id>')
def det_product(product_id):
    with Session() as session:
        result = session.execute(
            text("SELECT * FROM product WHERE id = :id"),
            {"id": product_id}
        ).fetchone()

        if not result:
            return jsonify({"message": f"No product found with id {product_id}."}), 404

        product = {
            "id": result.id,
            "name": result.name,
            "price": result.price,
            "stock": result.stock
        }

    return jsonify(product), 200


@app.get('/users/<int:users_id>')
def det_users(users_id):
    with Session() as session:
        result = session.execute(
            text("SELECT * FROM users WHERE id = :id"),
        {"id": users_id}
        ) .fetchone()

        if not result:
            return jsonify({"message": f"No user found with id {users_id}."}), 404

        users = {
            "id": result.id,
            "name": result.name,
            "email": result.email
        }

    return jsonify(users), 200

@app.post('/products')
def create_product():
    with Session() as session:
        data = request.get_json()
        name = data.get("name")
        price = data.get("price")
        stock = data.get("stock")

        if not name or not price or not stock:
            return jsonify({"message": "Please provide all required fields."}), 400

        session.execute(text("""INSERT INTO product (name, price, stock) 
                                          VALUES (:name, :price, :stock)
                                       """),
                                  {"name": name, "price": price, "stock": stock})

        session.commit()

    return jsonify({"message": f"Product '{name}' was created successfully."}), 201

@app.post('/users')
def create_users():
    with Session() as session:
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")

        if not name or not password or not email:
            return jsonify({"message": "Please provide all required fields."}), 400

        session.execute(text("""INSERT INTO users (name, password, email)
                                            VALUES (:name, :password, :email)
                                        """),
                                            {"name": name, "password": password, "email": email})
        session.commit()

    return jsonify({"message": f"User created successfully."}), 201



@app.delete('/products/<int:product_id>')
def delete_product(product_id):
    with Session() as session:
        session.execute(text("DELETE FROM product WHERE id = :id"),
                        {"id": product_id})
        session.commit()

    return jsonify({"message": f"Product with id {product_id} was deleted."}), 201

@app.delete('/users/<int:users_id>')
def delete_users(users_id):
    with Session() as session:
        session.execute(text("DELETE FROM users WHERE id = :id"),
                        {"id": users_id})
        session.commit()

    return jsonify({"message": f"User with id {users_id} was deleted."}), 200


