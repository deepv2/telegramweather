# Telegram Weather Bot

#### Introduction
This is my first Python application, so I apologize in advance if it is not organized. Using the python-telegram-bot open source API and the
Python weather-api wrapper for Yahoo! weather, I created a script for a Telegram bot that allows the bot to text weather data back to you.

#### Usage
* ```/location``` sets the location via latitude and longitude coordinates.
* ```/weather``` gets the date, conditions, high, and low for the current day.
* ```/forecast``` gets the date, conditions, high, and low for the next 5 days.
* ```/time``` sets a daily timer at a specified hour and minute to text you the weather.
* ```/reset``` removes all daily timers set with /time.
* ```/help``` prints out this help information.

Notice: After typing ```/time``` once and setting a daily timer, typing ```/time``` again will not prompt you for a time, but inputting a time
anyways will still function normally and set a daily weather reminder.

#### Installation
**Before you use this script, you have to make a new bot with Telegram and copy the API token key!**
Instructions to make a bot can be found by messaging @BotFather in Telegram. Copy the API token key and paste
it in the section in main() with the variable token:
```Python
token = "INSERT API KEY HERE!"
```

It is highly recommended that you use virtualenv to make a virtual environment for this program, so that you do not contaminate your global
Python installation. Instructions for virtual environments can be found by searching online. This specific bot script was built and tested with Python 3.6.6 on Ubuntu 18.04.

To install dependencies and run the program:
```Python
pip install -r requirements.txt
python app.py
```

On specific systems with Python 2 and 3 installed globally, you may need to use ```pip3``` and ```python3```.

This only provides basic weather functionality, so feel free to modify this app to your liking! 
