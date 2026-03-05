from flask import Flask, send_from_directory
from flask_cors import CORS
from app.routes.interview import interview_bp
from app.routes.teaching import teaching_bp
from app.services.interview_db_service import init_db, clear_db
import os

def create_app():
    app = Flask(__name__, static_folder="ui", static_url_path="/ui")
    CORS(app)
    init_db()
    clear_db()
    app.register_blueprint(interview_bp, url_prefix="/interview")
    app.register_blueprint(teaching_bp, url_prefix="/teaching")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Serve the UI
    @app.route("/")
    def index():
        return send_from_directory("ui", "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        if path and os.path.exists(os.path.join("ui", path)):
            return send_from_directory("ui", path)
        return send_from_directory("ui", "index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)