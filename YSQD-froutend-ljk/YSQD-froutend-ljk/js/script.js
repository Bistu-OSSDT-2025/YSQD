// 这是 script.js 文件
console.log("脚本已加载");

// 表单验证
document.addEventListener('DOMContentLoaded', function () {
// 登录表单验证
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        if (!username || !password) {
            e.preventDefault();
            alert('请输入用户名和密码');
        } else {
            // 模拟登录成功
            e.preventDefault();
            // 存储用户名
            sessionStorage.setItem('username', username);
            
            // 显示原生提示
            alert('登录成功，3秒后跳转到场馆选择界面');
            
            // 3秒后自动跳转到场馆列表
            setTimeout(() => {
                window.location.href = '/venues/list.html';
            }, 3000);
        }
    });
}

// 注册表单验证
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', function (e) {
        const username = document.getElementById('regUsername').value.trim();
        const password = document.getElementById('regPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const phone = document.getElementById('phone').value;

        if (!username || !password || !confirmPassword || !phone) {
            e.preventDefault();
            alert('请填写所有必填字段');
            return;
        }

        if (password.length < 6) {
            e.preventDefault();
            alert('密码长度至少为6位');
            return;
        }

        if (password !== confirmPassword) {
            e.preventDefault();
            alert('两次输入的密码不一致');
            return;
        }

        const phonePattern = /^\d{11}$/;
        if (!phonePattern.test(phone)) {
            e.preventDefault();
            alert('请输入有效的11位手机号码');
            return;
        }

        // 模拟注册成功
        e.preventDefault();
        alert('注册成功！');
        // 在实际应用中这里会有跳转逻辑
        window.location.href = 'index.html';
    });
}
});
