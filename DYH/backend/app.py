from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate, jwt
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key-here')

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # 导入路由
    from .routes.auth import auth_bp
    from .routes.venues import venues_bp
    from .routes.reservations import reservations_bp

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(venues_bp, url_prefix='/venues')
    app.register_blueprint(reservations_bp, url_prefix='/reservations')

    @app.route('/')
    def hello():
        return "场馆预约平台后端服务已启动"

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
