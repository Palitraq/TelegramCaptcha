BOT_TOKEN = "token"
MATH_RANGE = (1, 20) # range of numbers for math captcha
CAPTCHA_MODE = "math" # math or custom (default: math)
open_period = 100 # open period for captcha in seconds

CUSTOM_CAPTCHA = {
    "question": "2+2",
    "options": ["3", "4", "5", "6"],
    "correct_index": 1 # correct INDEX (0-based)
}