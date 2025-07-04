<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>旅游景点推荐</title>
    <style>
        /* 基础样式 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }
        
        body {
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* 头部样式 */
        header {
            background-color: #3a7bd5;
            color: white;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
        }
        
        .nav-menu {
            display: flex;
            list-style: none;
        }
        
        .nav-menu li {
            margin-left: 30px;
        }
        
        .nav-menu a {
            color: white;
            text-decoration: none;
            transition: color 0.3s;
            padding: 5px 10px;
            border-radius: 4px;
        }
        
        .nav-menu a:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        /* 轮播图样式 */
        .banner {
            margin: 30px 0;
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .banner img {
            width: 100%;
            height: 400px;
            object-fit: cover;
        }
        
        .banner-controls {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 20px;
        }
        
        .banner-control {
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .banner-control:hover {
            background-color: rgba(0, 0, 0, 0.8);
        }
        
        .banner-dots {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
        }
        
        .banner-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, 0.5);
            margin: 0 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .banner-dot.active {
            background-color: white;
        }
        
        /* 景点分类样式 */
        .category {
            margin: 40px 0;
        }
        
        .section-title {
            font-size: 24px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3a7bd5;
            display: inline-block;
        }
        
        .category-list {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .category-item {
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            width: calc(25% - 20px);
        }
        
        .category-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
        }
        
        .category-img {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        
        .category-info {
            padding: 15px;
        }
        
        .category-name {
            font-size: 18px;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        .category-desc {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 10px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .category-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .category-tag {
            background-color: #3a7bd5;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        
        .favorite-btn {
            background-color: transparent;
            border: none;
            cursor: pointer;
            color: #999;
            font-size: 18px;
        }
        
        .favorite-btn.active {
            color: #ff4500;
        }
        
        /* 搜索样式 */
        .search {
            margin: 40px 0;
            text-align: center;
        }
        
        .search-input {
            width: 500px;
            padding: 12px 15px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 4px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .search-input:focus {
            border-color: #3a7bd5;
        }
        
        .search-btn {
            padding: 12px 25px;
            background-color: #3a7bd5;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            margin-left: 10px;
            transition: background-color 0.3s;
        }
        
        .search-btn:hover {
            background-color: #2a65b5;
        }
        
        /* 页脚样式 */
        footer {
            background-color: #333;
            color: white;
            padding: 30px 0;
            margin-top: 50px;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        
        .footer-column {
            width: 30%;
            margin-bottom: 20px;
        }
        
        .footer-title {
            font-size: 18px;
            margin-bottom: 15px;
            position: relative;
            padding-bottom: 10px;
        }
        
        .footer-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 40px;
            height: 2px;
            background-color: #3a7bd5;
        }
        
        .footer-links {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 10px;
        }
        
        .footer-links a {
            color: #aaa;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .footer-links a:hover {
            color: white;
        }
        
        .footer-contact p {
            margin-bottom: 10px;
        }
        
        .copyright {
            text-align: center;
            padding-top: 20px;
            margin-top: 20px;
            border-top: 1px solid #444;
            color: #888;
            font-size: 14px;
        }
        
        /* 响应式设计 */
        @media (max-width: 1200px) {
            .container {
                width: 100%;
            }
            
            .category-item {
                width: calc(33.33% - 20px);
            }
        }
        
        @media (max-width: 992px) {
            .category-item {
                width: calc(50% - 20px);
            }
            
            .footer-column {
                width: 50%;
            }
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .nav-menu {
                margin-top: 15px;
                flex-wrap: wrap;
            }
            
            .nav-menu li {
                margin: 5px 15px 5px 0;
            }
            
            .banner img {
                height: 300px;
            }
            
            .search-input {
                width: 100%;
            }
            
            .search-btn {
                width: 100%;
                margin-left: 0;
                margin-top: 10px;
            }
            
            .category-item {
                width: 100%;
            }
            
            .footer-column {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <!-- 头部导航 -->
    <header>
        <div class="container header-content">
            <div class="logo">旅游景点推荐</div>
            <ul class="nav-menu">
                <li><a href="#home">首页</a></li>
                <li><a href="#categories">景点分类</a></li>
                <li><a href="#search">搜索景点</a></li>
                <li><a href="#favorites">我的收藏</a></li>
            </ul>
        </div>
    </header>

    <div class="container">
        <!-- 轮播图 -->
        <div class="banner" id="banner">
            <img src="https://picsum.photos/1200/400?random=1" alt="热门景点" class="banner-image">
            <div class="banner-controls">
                <div class="banner-control" id="prev-btn">
                    <i class="fas fa-chevron-left"></i>
                </div>
                <div class="banner-control" id="next-btn">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
            <div class="banner-dots" id="banner-dots"></div>
        </div>

        <!-- 景点分类 -->
        <section class="category" id="categories">
            <h2 class="section-title">景点分类</h2>
            <div class="category-list" id="category-list">
                <!-- 景点卡片将通过JavaScript动态生成 -->
            </div>
        </section>

        <!-- 搜索区域 -->
        <section class="search" id="search">
            <h2 class="section-title">搜索景点</h2>
            <input type="text" class="search-input" id="search-input" placeholder="输入景点名称或关键词...">
            <button class="search-btn" id="search-btn">搜索</button>
            <div class="search-results" id="search-results">
                <!-- 搜索结果将通过JavaScript动态生成 -->
            </div>
        </section>
    </div>

    <!-- 页脚 -->
    <footer>
        <div class="container footer-content">
            <div class="footer-column">
                <h3 class="footer-title">关于我们</h3>
                <p>旅游景点推荐网站致力于为游客提供最全面、最准确的景点信息，帮助您规划完美的旅行。</p>
            </div>
            <div class="footer-column">
                <h3 class="footer-title">快速链接</h3>
                <ul class="footer-links">
                    <li><a href="#home">首页</a></li>
                    <li><a href="#categories">景点分类</a></li>
                    <li><a href="#search">搜索景点</a></li>
                    <li><a href="#favorites">我的收藏</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h3 class="footer-title">联系我们</h3>
                <div class="footer-contact">
                    <p><i class="fas fa-envelope"></i> contact@travelsite.com</p>
                    <p><i class="fas fa-phone"></i> 400-123-4567</p>
                    <p><i class="fas fa-map-marker-alt"></i> 北京市朝阳区旅游大厦</p>
                </div>
            </div>
        </div>
        <div class="copyright">
            &copy; 2025 旅游景点推荐网站. 保留所有权利.
        </div>
    </footer>

    <script>
        // 景点数据
        const attractions = [
            {
                id: 1,
                name: "故宫博物院",
                description: "北京故宫是中国明清两代的皇家宫殿，旧称紫禁城，位于北京中轴线的中心，是中国古代宫廷建筑之精华。",
                image: "https://picsum.photos/600/400?random=101",
                category: "历史古迹",
                location: "北京市东城区",
                favorite: false
            },
            {
                id: 2,
                name: "西湖",
                description: "西湖有100多处公园景点，有“西湖十景”“新西湖十景”“三评西湖十景