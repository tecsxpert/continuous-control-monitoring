from flask import Flask
from flask_cors import CORS
from routes.report import report_bp

from routes.describe import describe_bp
from routes.recommend import recommend_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(describe_bp, url_prefix="/describe")
    app.register_blueprint(recommend_bp, url_prefix="/recommend")
    app.register_blueprint(report_bp, url_prefix="/generate-report")
    
    @app.route('/health')
    def health():
        return {"status": "AI service running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)