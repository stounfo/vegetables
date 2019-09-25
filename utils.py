from datetime import datetime

def datetime_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
