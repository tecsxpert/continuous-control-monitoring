from flask import Flask
from flask_cors import CORS
from routes.report import report_bp
from flask_executor import Executor
from routes.issue import issue_bp
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.analyse import analyse_bp
from routes.batch import batch_bp
def create_app():
    app = Flask(__name__)
    CORS(app)

    executor = Executor()
    executor.init_app(app)
    app.executor = executor
    app.register_blueprint(describe_bp, url_prefix="/describe")
    app.register_blueprint(recommend_bp, url_prefix="/recommend")
    app.register_blueprint(report_bp, url_prefix="/generate-report")
    app.register_blueprint(issue_bp, url_prefix="/issue")
    app.register_blueprint(analyse_bp, url_prefix="/analyse-document")
    app.register_blueprint(batch_bp, url_prefix="/batch-process")
    
    @app.route('/health')
    def health():
        return {"status": "AI service running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)