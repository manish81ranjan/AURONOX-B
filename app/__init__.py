from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.db.mongo import init_mongo

from app.routes.health import health_bp
from app.routes.products import products_bp
from app.routes.orders import orders_bp
from app.routes.contact import contact_bp
from app.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/api/*": {"origins": [app.config["FRONTEND_ORIGIN"]]}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    init_mongo(app)

    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")
    app.register_blueprint(contact_bp, url_prefix="/api/contact")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.route("/", methods=["GET"])
    def home():
        return {"message": "AURONOX backend running"}, 200

    return app