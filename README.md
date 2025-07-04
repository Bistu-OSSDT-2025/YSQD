# 体育馆场地预约管理系统

![系统截图](static/images/logo.png)

一个基于Flask的体育馆场地预约管理系统，提供用户注册、场地预约、预约管理等功能。

## 功能特点

- 用户注册与登录系统
- 场地信息浏览与查询
- 可视化时间段选择预约
- 个人预约记录管理
- 管理员后台管理界面
- 响应式网页设计

## 技术栈

### 前端
- HTML5
- CSS3
- JavaScript (ES6)

### 后端
- Python 3
- Flask框架
- SQLAlchemy ORM
- bcrypt密码加密

### 数据库
- SQLite (开发环境)
- 可扩展至MySQL/PostgreSQL

## 安装与运行

### 环境要求
- Python 3.7+
- pip包管理工具

### 安装步骤
1. 克隆仓库：
```bash
git clone https://github.com/your-repo/gym-booking-system.git
cd gym-booking-system
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库：
```bash
python script.py
```

4. 启动服务：
```bash
python script.py
```

5. 访问系统：
打开浏览器访问 [http://localhost:5000](http://localhost:5000)

## 项目结构

```
gym-booking-system/
├── instance/                # 数据库文件
├── static/                 # 静态资源
│   ├── css/                # 样式表
│   ├── js/                 # JavaScript文件
│   └── images/             # 图片资源
├── templates/              # HTML模板
│   ├── admin.html          # 管理员页面
│   ├── admin_register.html # 管理员注册
│   └── index.html          # 用户主界面
├── script.py               # 主程序入口
├── requirements.txt        # 依赖列表
└── README.md               # 项目文档
```

## 使用说明

1. **用户注册**：
   - 点击导航栏"注册"按钮
   - 填写用户名和密码
   - 完成注册后自动跳转至登录页

2. **场地预约**：
   - 登录后进入主界面
   - 选择设施类型(如羽毛球场)
   - 选择具体场地编号
   - 选择日期和可用时间段
   - 提交预约

3. **查看预约**：
   - 在"我的预约记录"区域查看所有预约
   - 可取消未完成的预约

## 开发说明

- 调试模式运行：
```bash
python script.py
```

- 生产环境部署建议：
  - 使用Gunicorn或uWSGI作为WSGI服务器
  - 配置Nginx作为反向代理
  - 使用MySQL/PostgreSQL替代SQLite

## 常见问题

**Q: 为什么时间段不显示？**
A: 请确保：
1. 已选择设施、场地和日期
2. 后端服务正常运行
3. 检查浏览器控制台是否有错误

**Q: 如何添加新的场地类型？**
A: 修改`script.py`中的初始化代码，添加新的Venue记录

## 贡献指南

欢迎提交Pull Request。对于重大更改，请先创建Issue讨论。

## 许可证

MIT License
