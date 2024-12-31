import math


def format_time(time: int) -> str:
    minutes = math.floor(time / 60)
    seconds = round(time % 60)
    seconds = seconds if seconds > 9 else f"0{seconds}"
    return f"{minutes}:{seconds}"
