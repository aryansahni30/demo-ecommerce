from flask import Flask
from api.users import users_bp
from api.orders import orders_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(orders_bp)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
