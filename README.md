Instagram Reel/Video Downloader Telegram Bot
A simple, free Telegram bot to download Instagram videos and reels.
Powered by Python, yt-dlp, and the python-telegram-bot library.

Features
Download any public Instagram reel or post as a video file

Fast and reliable

Sends files directly in Telegram chat (no third-party links)

Checks for file size limits and handles timeouts gracefully

How to Use
Start the bot on Telegram

Send it any public Instagram reel or post link

Receive the video file directly in your chat!

Tech Stack
Python 3

yt-dlp

python-telegram-bot

requests

Getting Started
Clone this repo:

text
git clone https://github.com/yourusername/telegram-instagram-downloader-bot.git
Install dependencies:

text
pip install -r requirements.txt
Set the BOT_TOKEN in your environment variables or directly in bot.py

Run the bot:

text
python bot.py
Deployment
You can deploy this bot for free on platforms like Railway, Render, Replit, or PythonAnywhere.

Notes & Limitations
Only works with public Instagram content

Cannot download private/restricted videos

Videos larger than 50 MB will not be sent (Telegram bot API limit)

License
This project is released under the MIT License.

Credits
yt-dlp project

python-telegram-bot

Developed by Royal Dudy