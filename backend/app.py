from flask import Flask, redirect, url_for
from extensions import db, migrate, jwt
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # 导入路由
    from routes import auth, venue, booking, admin
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(venue.bp)
    app.register_blueprint(booking.bp)
    app.register_blueprint(admin.bp)
    
    # 添加根路由重定向到登录页
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
