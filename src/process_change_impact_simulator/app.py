from flask import Flask, jsonify
from process_simulator.database import initialize_database
from process_simulator.routes import register_routes

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("config.Config")
    if test_config: app.config.update(test_config)
    initialize_database(app.config["DATABASE_PATH"])
    register_routes(app)
    @app.get("/")
    def home():
        return jsonify({"application":"Process Change Impact Simulator","status":"running"})
    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(409)
    def handle_error(error):
        return jsonify({"error": str(error.description)}), error.code
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
