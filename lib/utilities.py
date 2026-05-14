import time

def format_time(s):
    if s < 0:
        return "Invalid time"
        
    total_ms = round(s * 1000)
    
    if total_ms == 0:
        return "0 sec 0 ms"

    DAYS_MS, HOURS_MS, MINUTES_MS, SECONDS_MS, MS = 86400000, 3600000, 60000, 1000, 1
    units = [DAYS_MS, HOURS_MS, MINUTES_MS, SECONDS_MS, MS]
    names = ["day", "hour", "min", "sec", "ms"]
    parts = []
    
    for unit, name in zip(units, names):
        if name == "ms":
            value = total_ms 
        else:
            value = total_ms // unit

        if value > 0:
            parts.append(f"{value} {name}{'s' if name not in ('min', 'sec', 'ms') and value > 1 else ''}")
            total_ms %= unit
            if name == "sec": 
                break

    if total_ms > 0 and total_ms < 1000:
        parts.append(f"{total_ms} ms")
        
    if not parts and total_ms > 0:
        return f"{total_ms} ms"
    
    if s < 1 and s > 0 and "ms" not in " ".join(parts):
        return f"{int(round(s))} sec {total_ms % 1000} ms"
        
    return " ".join(parts)
