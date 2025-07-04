// 配置API基础URL
const API_BASE_URL = 'http://127.0.0.1:5000'; // 改用IP地址避免可能的localhost解析问题

// 全局函数声明
window.showLogin = function() {
    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('registerSection').style.display = 'none';
    document.getElementById('loginContainer').style.display = 'block';
    document.getElementById('mainContainer').style.display = 'none';
};

window.showRegister = function() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('registerSection').style.display = 'block';
    document.getElementById('loginContainer').style.display = 'block';
    document.getElementById('mainContainer').style.display = 'none';
};

let currentUser = JSON.parse(localStorage.getItem('currentUser')) || null;

// 初始化事件监听
document.addEventListener('DOMContentLoaded', function() {
    // 恢复登录状态
    if (currentUser) {
        document.getElementById('loginContainer').style.display = 'none';
        document.getElementById('loginSection').style.display = 'none';
        document.getElementById('registerSection').style.display = 'none';
        document.getElementById('userCenter').style.display = 'block';
        document.getElementById('mainContainer').style.display = 'block';
        document.getElementById('displayUsername').textContent = currentUser.username;
        document.getElementById('successMessage').style.display = 'block';
        loadFacilities();
        loadUserBookings();
        loadTimeSlots();
    }
    
    // 登录表单提交
    document.getElementById('loginForm')?.addEventListener('submit', function(e) {
        e.preventDefault();
        login();
    });

    // 注册表单提交
    document.getElementById('registerForm')?.addEventListener('submit', function(e) {
        e.preventDefault();
        register();
    });

    // 导航链接点击事件
    document.querySelector('.nav-links a[onclick="showLogin()"]')?.addEventListener('click', function(e) {
        e.preventDefault();
        showLogin();
    });

    document.querySelector('.nav-links a[onclick="showRegister()"]')?.addEventListener('click', function(e) {
        e.preventDefault();
        showRegister();
    });
});

// 用户注册
window.register = async function() {
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;

    if (password !== confirmPassword) {
        alert('密码不一致，请重新输入');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/users/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: username,  // 使用用户名作为email
                password: password
            })
        });

        const data = await response.json();
        if (response.ok) {
            alert('注册成功！请登录');
            document.getElementById('registerForm').reset();
            showLogin();
        } else {
            alert(data.error || '注册失败');
        }
    } catch (error) {
        alert('无法连接后端服务，请确保：\n1. 后端服务已启动\n2. 网络连接正常\n3. 端口未被占用');
        console.error('API请求失败:', error);
    }
};

// 用户登录
window.login = async function() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
        alert('请输入用户名和密码');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: username,
                password: password
            })
        });

        const data = await response.json();
        if (response.ok) {
            // 确保存储完整的用户信息
            const userData = {
                id: data.user_id || data.id,
                username: data.username,
                email: data.email,
                is_admin: data.is_admin
            };
            currentUser = userData;
            localStorage.setItem('currentUser', JSON.stringify(userData));
            console.log('用户登录成功:', userData);
            
            if (data.is_admin) {
                window.location.href = '/admin';
            } else {
                document.getElementById('loginContainer').style.display = 'none';
                document.getElementById('loginSection').style.display = 'none';
                document.getElementById('registerSection').style.display = 'none';
                document.getElementById('userCenter').style.display = 'block';
                document.getElementById('mainContainer').style.display = 'block';
                document.getElementById('displayUsername').textContent = data.username;
                document.getElementById('successMessage').style.display = 'block';
                loadFacilities();
                loadUserBookings();
                loadTimeSlots();
            }
        } else {
            alert(data.error || '登录失败');
        }
    } catch (error) {
        alert('无法连接后端服务，请确保：\n1. 后端服务已启动\n2. 网络连接正常\n3. 端口未被占用');
        console.error('API请求失败:', error);
    }
};

// 加载设施
function loadFacilities() {
    fetch(`${API_BASE_URL}/api/venues`)
        .then(response => response.json())
        .then(data => {
            const facilitiesList = document.getElementById('facilitiesList');
            const facilitySelect = document.getElementById('facility');
            const courtSelect = document.getElementById('court');
            
            facilitiesList.innerHTML = '';
            facilitySelect.innerHTML = '<option value="">请选择</option>';
            courtSelect.innerHTML = '<option value="">请先选择设施</option>';
            
            data.forEach(venue => {
                // 添加设施到列表
                const venueElement = document.createElement('div');
                venueElement.className = 'facility-card';
                venueElement.innerHTML = `
                    <h3>${venue.name}</h3>
                    <p>类型: ${venue.type}</p>
                    <p>位置: ${venue.location}</p>
                    <p>价格: ¥${venue.price_per_hour}/小时</p>
                `;
                facilitiesList.appendChild(venueElement);

                // 添加到选择框
                const option = document.createElement('option');
                option.value = venue.id;
                option.textContent = venue.name;
                option.setAttribute('data-type', venue.type);
                facilitySelect.appendChild(option);
            });

            // 设施选择变化时更新场地编号
            facilitySelect.addEventListener('change', function() {
                const selectedOption = this.options[this.selectedIndex];
                const venueType = selectedOption.getAttribute('data-type');
                courtSelect.innerHTML = '<option value="">请选择</option>';
                
                if (venueType === 'badminton') {
                    // 羽毛球场生成10个场地编号
                    for (let i = 1; i <= 10; i++) {
                        const courtOption = document.createElement('option');
                        courtOption.value = i;
                        courtOption.textContent = `${i}号场地`;
                        courtSelect.appendChild(courtOption);
                    }
                } else if (venueType === 'gym') {
                    // 健身房只有1个场地
                    const courtOption = document.createElement('option');
                    courtOption.value = 1;
                    courtOption.textContent = '健身房';
                    courtSelect.appendChild(courtOption);
                }
            });
        })
        .catch(error => console.error('加载设施失败:', error));
}

// 加载用户预约
function loadUserBookings() {
    if (!currentUser) return;

    fetch(`${API_BASE_URL}/api/bookings?user_id=${currentUser.id}`)
        .then(response => response.json())
        .then(data => {
            const bookingsList = document.getElementById('bookingsList');
            bookingsList.innerHTML = '';
            
            data.forEach(booking => {
                const bookingElement = document.createElement('div');
                bookingElement.className = 'booking-card';
                let venueText = booking.venue.name;
                if (booking.venue.type === 'badminton') {
                    venueText += ` (${booking.court_id}号场地)`;
                }

                bookingElement.innerHTML = `
                    <h3>预约编号: ${booking.booking_number}</h3>
                    <p>设施: ${venueText}</p>
                    <p>日期: ${booking.date}</p>
                    <p>时间: ${booking.start_time} - ${booking.end_time}</p>
                    <p>状态: ${booking.status}</p>
                    <button onclick="cancelBooking('${booking.id}')">取消预约</button>
                `;
                bookingsList.appendChild(bookingElement);
            });
        })
        .catch(error => console.error('加载预约失败:', error));
}

// 加载时间段
function loadTimeSlots() {
    console.log('正在加载时间段...');
    const timeSlots = document.getElementById('timeSlots');
    if (!timeSlots) {
        console.error('找不到timeSlots元素');
        return;
    }
    
    const date = document.getElementById('date').value;
    const facilityId = document.getElementById('facility').value;
    const courtId = document.getElementById('court').value;
    
    console.log('当前选择:', {date, facilityId, courtId});
    
    if (!date || !facilityId || !courtId) {
        return;
    }

    // 获取已预约时间段
    fetch(`${API_BASE_URL}/api/bookings?date=${date}&venue_id=${facilityId}&court_id=${courtId}`)
        .then(response => response.json())
        .then(bookings => {
            timeSlots.innerHTML = '';
            const bookedSlots = bookings.map(b => b.start_time.substring(0,5));
            
            for (let hour = 8; hour <= 20; hour++) {
                const timeStr = `${hour}:00`;
                const isBooked = bookedSlots.includes(timeStr);
                
                const timeSlot = document.createElement('div');
                timeSlot.className = `time-slot ${isBooked ? 'booked' : ''}`;
                timeSlot.textContent = `${hour}:00 - ${hour+1}:00`;
                timeSlot.style.cssText = `
                    padding: 10px 15px;
                    margin: 5px;
                    border: 2px solid ${isBooked ? '#cccccc' : '#e0e0e0'};
                    border-radius: 8px;
                    display: inline-block;
                    background: ${isBooked ? '#f0f0f0' : '#f8f9fa'};
                    color: ${isBooked ? '#999999' : '#333'};
                    font-weight: 500;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    cursor: ${isBooked ? 'not-allowed' : 'pointer'};
                `;
                
                if (!isBooked) {
                    timeSlot.addEventListener('mouseenter', function() {
                        if (!this.classList.contains('selected')) {
                            this.style.background = '#e9ecef';
                        }
                    });
                    
                    timeSlot.addEventListener('mouseleave', function() {
                        if (!this.classList.contains('selected')) {
                            this.style.background = '#f8f9fa';
                        }
                    });
                    
                    timeSlot.addEventListener('click', function() {
                        document.querySelectorAll('.time-slot').forEach(slot => {
                            slot.style.background = slot.classList.contains('booked') ? '#f0f0f0' : '#f8f9fa';
                            slot.style.color = slot.classList.contains('booked') ? '#999999' : '#333';
                            slot.style.borderColor = slot.classList.contains('booked') ? '#cccccc' : '#e0e0e0';
                            slot.classList.remove('selected');
                        });
                        this.style.background = '#007bff';
                        this.style.color = 'white';
                        this.style.borderColor = '#0056b3';
                        this.classList.add('selected');
                        document.getElementById('selectedTime').value = `${hour}:00-${hour+1}:00`;
                    });
                }
                timeSlots.appendChild(timeSlot);
            }
        })
        .catch(error => console.error('加载时间段失败:', error));
}

// 处理预约表单提交
document.getElementById('bookingForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!currentUser) {
        alert('请先登录');
        return;
    }

    const facilityId = document.getElementById('facility').value;
    const courtId = document.getElementById('court').value;
    const date = document.getElementById('date').value;
    const timeSlot = document.getElementById('selectedTime').value;

    if (!facilityId || !courtId || !date || !timeSlot) {
        alert('请填写完整的预约信息');
        return;
    }

    const [startTime, endTime] = timeSlot.split('-');
    
    if (!currentUser || !currentUser.id) {
        alert('用户会话已过期，请重新登录');
        window.location.reload();
        return;
    }

    const bookingData = {
        user_id: currentUser.id,
        venue_id: facilityId,
        court_id: parseInt(courtId),
        date: date,
        start_time: startTime,
        end_time: endTime
    };

    console.log('提交的预约数据:', bookingData); // 调试日志

    fetch(`${API_BASE_URL}/api/bookings`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingData)
    })
    .then(async response => {
        const data = await response.json();
        console.log('API响应:', { status: response.status, data }); // 详细日志
        
        if (!response.ok) {
            console.error('预约失败详情:', {
                request: bookingData,
                response: data
            });
        }
        
        if (response.ok) {
            alert(`预约成功！预约编号: ${data.booking_number}`);
            loadUserBookings();
        } else {
            alert(`预约失败: ${data.error || '未知错误'}\n状态码: ${response.status}`);
        }
        return data;
    })
    .catch(error => {
        console.error('预约请求失败:', {
            error: error,
            request: bookingData
        });
        alert(`预约失败: ${error.message || '网络错误，请检查连接后重试'}`);
    });
});

// 取消预约
window.cancelBooking = function(bookingId) {
    if (confirm('确定要取消此预约吗？')) {
        fetch(`${API_BASE_URL}/api/bookings/${bookingId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadUserBookings();
        })
        .catch(error => console.error('取消预约失败:', error));
    }
};

// 退出登录
window.logout = function() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    window.location.reload();
};
