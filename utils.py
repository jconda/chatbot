from datetime import datetime

def parse_date(text):
    try:
        date = datetime.strptime(text.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
        return date
    except:
        return None

def parse_time(text):
    try:
        time = datetime.strptime(text.strip(), "%H:%M").strftime("%H:%M")
        return time
    except:
        return None