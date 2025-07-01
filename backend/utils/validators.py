import re

def validate_username(username):
    """验证用户名格式（3-20个字符，仅允许字母数字和下划线）"""
    if not username:
        return False
    return 3 <= len(username) <= 20 and re.match(r'^\w+$', username) is not None

def validate_password(password):
    """验证密码格式（至少6个字符）"""
    return password and len(password) >= 6

def validate_venue_data(data):
    """验证场馆数据"""
    errors = {}
    if not data.get('name'):
        errors['name'] = '场馆名称不能为空'
    if not data.get('capacity'):
        errors['capacity'] = '容纳人数不能为空'
    elif not isinstance(data['capacity'], int) or data['capacity'] <= 0:
        errors['capacity'] = '容纳人数必须是正整数'
    return errors

def validate_booking_data(data):
    """验证预约数据"""
    errors = {}
    if not data.get('venue_id'):
        errors['venue_id'] = '必须选择场馆'
    if not data.get('start_time'):
        errors['start_time'] = '必须选择开始时间'
    if not data.get('end_time'):
        errors['end_time'] = '必须选择结束时间'
    elif data.get('start_time') and data.get('end_time') and data['start_time'] >= data['end_time']:
        errors['end_time'] = '结束时间必须晚于开始时间'
    return errors
