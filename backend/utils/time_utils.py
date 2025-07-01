from datetime import datetime

def parse_datetime(dt_str):
    """解析ISO格式时间字符串为datetime对象"""
    try:
        # 支持两种常见格式：YYYY-MM-DDTHH:MM:SS 和 YYYY-MM-DD HH:MM:SS
        if 'T' in dt_str:
            return datetime.fromisoformat(dt_str)
        else:
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError) as e:
        raise ValueError(f"时间格式无效: {dt_str}。请使用 'YYYY-MM-DDTHH:MM:SS' 或 'YYYY-MM-DD HH:MM:SS' 格式") from e
