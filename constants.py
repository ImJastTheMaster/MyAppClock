import ctypes

QSS = """
#my_timer {
    border-image: url(Egypt.jpg) 0 0 0 0 stretch stretch;
}
#my_time {
    border-image: url(art-london.jpg) 0 0 0 0 stretch stretch;
}
#reg_widget {
    border-image: url(new_york.jpg) 0 0 0 0 stretch stretch;
}
#widget {
    border-image: url(moon-sky.jpg) 0 0 0 0 stretch stretch;
}
#my_stopwatch {
    border-image: url(Paris.jpg) 0 0 0 0 stretch stretch;
}
"""
user32 = ctypes.windll.user32
SCREENSIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SECONDS = 60
FULL_PROGRESS = 100
MAX_LEN = 1000
TIME_SET = 1000
MIN_LEN = 100
MINI_LEN = 10
DAY_ON_MOUNTH = 30