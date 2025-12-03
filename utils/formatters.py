def format_bytes(bytes_num):
    if bytes_num == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while bytes_num >= 1024 and i < len(units) - 1:
        bytes_num /= 1024.0
        i += 1
    
    return f"{bytes_num:.2f} {units[i]}"

def format_percent(value):
    return f"{value:.1f}%"

def format_frequency(hz):
    if hz >= 1_000_000_000:  # GHz
        return f"{hz / 1_000_000_000:.2f} GHz"
    elif hz >= 1_000_000:  # MHz
        return f"{hz / 1_000_000:.2f} MHz"
    else:  # Hz
        return f"{hz:.0f} Hz"

def format_time_seconds(seconds):
    if seconds < 60:
        return f"{seconds:.0f} сек"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} мин"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} ч"
    else:
        days = seconds / 86400
        return f"{days:.1f} дн"