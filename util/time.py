def format_second_to_str(second):
    mins = second // 60
    secs = second % 60 if mins else second
    secs = f"0{secs}" if secs < 10 else secs
    mins = f"0{mins}" if mins < 10 else mins
    return f"{mins}:{secs}"
