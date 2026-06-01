import os
import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Add the parent directory to sys.path to allow absolute imports from other folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration
from backend.config import Config

# Initialize the database instance
db = SQLAlchemy()

def create_app():
    """
    Application Factory Pattern.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object(Config)

    # Initialize database with the app config
    db.init_app(app)

    # Enable CORS for all routes, allowing the frontend to communicate with this backend
    CORS(app)

    # Import and register Blueprints (Routes)
    # We use a try-except block to prevent errors if routes.py isn't generated yet,
    # though logically we assume the project is being built in order.
    try:
        from backend.routes import main_bp
        app.register_blueprint(main_bp)
    except ImportError:
        print("Warning: routes.py not found or error importing routes.")

    # Shell context processor for easy database debugging in flask shell
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}

    # Basic Error Handlers
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error="Internal Server Error"), 500

    # Database Initialization
    with app.app_context():
        try:
            # Import models here so they are registered with SQLAlchemy before creation
            from models.product import Product
            from models.employee import Employee
            
            # Create tables
            db.create_all()
            print("Database initialized successfully.")
        except ImportError:
            print("Warning: Models not found yet. Skipping database table creation.")
        except Exception as e:
            print(f"Error initializing database: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    # Run the application
    app.run(debug=True, port=5000)
