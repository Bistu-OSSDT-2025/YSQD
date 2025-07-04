from script import app, db, User
import bcrypt

with app.app_context():
    # Check if test user already exists
    # 创建普通测试用户
    if not User.query.filter_by(email="test@example.com").first():
        test_user = User(
            username="testuser",
            email="test@example.com"
        )
        test_user.set_password("testpass")
        db.session.add(test_user)
        print("普通测试用户创建成功")
    else:
        print("普通测试用户已存在")

    # 创建管理员测试用户
    if not User.query.filter_by(email="admin@example.com").first():
        admin_user = User(
            username="admin",
            email="admin@example.com",
            is_admin=True
        )
        admin_user.set_password("adminpass")
        db.session.add(admin_user)
        print("管理员测试用户创建成功")
    else:
        print("管理员测试用户已存在")

    db.session.commit()
