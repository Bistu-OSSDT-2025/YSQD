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
            // 调用真实登录API
            e.preventDefault();
            fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                // 存储token和用户名
                sessionStorage.setItem('access_token', data.access_token);
                sessionStorage.setItem('username', data.username);
                
                alert('登录成功，正在跳转...');
                window.location.href = '/venues/list.html';
            })
            .catch(error => {
                alert(error.error || '登录失败');
            });
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

        // 调用真实注册API
        e.preventDefault();
            fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    phone: phone
                })
            })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message || '注册成功！');
            window.location.href = 'index.html';
        })
        .catch(error => {
            alert(error.error || '注册失败');
        });
    });
}
});
