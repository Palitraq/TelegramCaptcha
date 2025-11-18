# Telegram Captcha Bot

Bot for automatic user verification when joining private Telegram channels using math captchas.

## Features

- Automatic sending of math captchas to private messages upon join request
- Polls with simple math examples (addition of numbers from 1 to 20)
- 10-minute timer for response
- Automatic approval on correct answer
- Automatic rejection on incorrect answer or timeout

## Installation

```bash
1. Install python 3.11.0
2. pip install -r requirements.txt
3. edit config.py
4. python bot.py
```

## How it works

1. User sends join request to channel
2. Bot automatically sends math captcha to user's private messages
3. User has 10 minutes to respond
4. On correct answer - request is approved
5. On incorrect answer or timeout - request is rejected
