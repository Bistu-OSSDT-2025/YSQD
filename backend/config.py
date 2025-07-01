class Config:
    # 基础配置
    SECRET_KEY = 'your_secret_key_here'  # 生产环境需替换为强密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 数据库配置（使用SQLite）
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

    # JWT配置
    JWT_SECRET_KEY = 'jwt_secret_key_here'  # 独立于主密钥
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时有效期
